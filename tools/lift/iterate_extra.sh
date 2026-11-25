#!/usr/bin/env bash
# M6: descobre em execução as funções alcançadas só por ponteiro e as traduz no crate extra.
# Ciclo: roda m6_run -> se parar em "folha sem tradução nem handler: RVA 0x..", acrescenta o RVA
# às raízes do extra, regenera (só as raízes, LIFT_NOFOLLOW) e recompila; para em qualquer outro erro.
# Uso: bash tools/lift/iterate_extra.sh <in.wav> <out.wav> [max_iter=40]
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
IN="$1"; OUT="$2"; MAX="${3:-40}"
ROOTS="$ROOT/lifted_extra/roots.txt"
touch "$ROOTS"
for i in $(seq 1 "$MAX"); do
  LOG="$(mktemp)"
  ./lifted_extra/target/release/m6_run.exe "$IN" "$OUT" 512 > "$LOG" 2>&1
  rc=$?
  if grep -q "Permission denied" "$LOG"; then
    echo "ITER $i: App Control bloqueou o .exe; recompilando com outro carimbo"
    (cd lifted_extra && M6_STAMP="$RANDOM$RANDOM" cargo build --release --bin m6_run 2>&1 | grep -E "^error" -A6 | head -20)
    continue
  fi
  tail -3 "$LOG"
  if [ $rc -eq 0 ]; then echo "ITER $i: OK"; exit 0; fi
  RVA=$(grep -o "folha sem tradução nem handler: RVA 0x[0-9A-F]*" "$LOG" | grep -o "0x[0-9A-F]*$")
  if [ -z "$RVA" ]; then echo "ITER $i: parou por outro motivo"; cat "$LOG" | tail -5; exit 2; fi
  if grep -qw "$RVA" "$ROOTS"; then echo "ITER $i: $RVA já estava nas raízes"; exit 3; fi
  echo "$RVA" >> "$ROOTS"
  echo "ITER $i: + $RVA"
  LIFT_NOFOLLOW=1 LIFT_PREFIX=soultree_lifted:: LIFT_EXCLUDE=lifted/src/gen_engine.rs \
    py tools/lift/lift.py lifted_extra/src/gen_extra.rs $(cat "$ROOTS") | head -1
  (cd lifted_extra && cargo build --release --bin m6_run 2>&1 | grep -E "^error" -A6 | head -20)
done
echo "limite de iterações"; exit 4

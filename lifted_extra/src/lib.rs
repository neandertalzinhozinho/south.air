//! Complemento do motor traduzido: funções alcançadas só em execução (ponteiros gravados
//! em tempo de inicialização). Gerado por `tools/lift/lift.py` com
//! `LIFT_PREFIX=soultree_lifted:: LIFT_EXCLUDE=../lifted/src/gen_engine.rs`.
pub mod gen_extra;

/// Registra as funções e imports deste crate no despacho do crate base.
pub fn register() {
    let _ = soultree_lifted::EXTRA.set(gen_extra::lifted);
    let _ = soultree_lifted::EXTRA_IMPORT.set(gen_extra::import_name);
}

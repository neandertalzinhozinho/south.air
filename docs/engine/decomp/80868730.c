// FUN_180868730 @ 0x180868730

int FUN_180868730(longlong *param_1)

{
  undefined8 *puVar1;
  int iVar2;
  int iVar3;
  undefined8 local_128 [16];
  int local_a8;
  int local_a4;
  undefined8 local_98 [16];
  int local_18;
  int local_14;
  
  puVar1 = local_128;
  if (*(char *)(*param_1 + 0x58) == '\0') {
    return (int)param_1[0x58f] + (int)param_1[6];
  }
  iVar2 = 0;
  local_a4 = (int)param_1[0x5e2];
  local_a8 = (int)param_1[0x5e1];
  iVar3 = 0;
  if (0 < (int)param_1[0x5e1]) {
    do {
      iVar3 = iVar3 + 1;
      *puVar1 = *(undefined8 *)
                 ((longlong)param_1 + (0x2e88 - (longlong)local_128) + (longlong)puVar1);
      puVar1 = puVar1 + 1;
    } while (iVar3 < local_a8);
  }
  local_14 = (int)param_1[0x59];
  local_18 = (int)param_1[0x58];
  if (0 < (int)param_1[0x58]) {
    puVar1 = local_98;
    do {
      iVar2 = iVar2 + 1;
      *puVar1 = *(undefined8 *)((longlong)param_1 + (0x240 - (longlong)local_98) + (longlong)puVar1)
      ;
      puVar1 = puVar1 + 1;
    } while (iVar2 < local_18);
  }
  return (local_14 + local_a4) / 2 + (int)param_1[0x58f] + (int)param_1[6];
}


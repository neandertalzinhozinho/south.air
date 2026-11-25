 (GhidraScript)  

undefined8 *
FUN_180878200(undefined8 *param_1,undefined8 param_2,int param_3,int param_4,undefined4 param_5)

{
  int iVar1;
  undefined8 *puVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x11] = 0;
  param_1[0x12] = 0;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x18] = 0;
  param_1[0x19] = 0;
  param_1[0x1a] = 0;
  param_1[0x1b] = 0;
  param_1[0x1c] = 0;
  param_1[0x1d] = 0;
  param_1[0x1e] = 0;
  param_1[0x1f] = 0;
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  param_1[0x23] = 0;
  param_1[0x24] = 0;
  param_1[0x25] = 0;
  param_1[0x26] = 0;
  param_1[0x27] = 0;
  param_1[0x28] = 0;
  param_1[0x29] = 0;
  param_1[0x2a] = 0;
  param_1[0x2b] = 0;
  param_1[0x2c] = 0;
  param_1[0x2d] = 0;
  param_1[0x2e] = 0;
  param_1[0x2f] = 0;
  param_1[0x30] = 0;
  param_1[0x31] = 0;
  param_1[0x32] = 0;
  param_1[0x33] = 0;
  param_1[0x34] = 0;
  param_1[0x35] = 0;
  FUN_1808688b0(0,param_2,param_5);
  FUN_1808688b0(param_1 + 0x12,param_3,param_5);
  if (param_4 < param_3) {
    param_4 = param_3;
  }
  FUN_1808688b0(param_1 + 0x24,param_4,param_5);
  iVar1 = 0;
  if (0 < *(int *)((longlong)param_1 + 0x8c)) {
    puVar2 = param_1;
    do {
      FUN_1800010d0(*puVar2,*(undefined4 *)(param_1 + 0x11));
      iVar1 = iVar1 + 1;
      puVar2 = puVar2 + 1;
    } while (iVar1 < *(int *)((longlong)param_1 + 0x8c));
  }
  param_1[0x10] = 0;
  iVar1 = 0;
  if (0 < *(int *)((longlong)param_1 + 0x11c)) {
    puVar2 = param_1 + 0x12;
    do {
      FUN_1800010d0(*puVar2,*(undefined4 *)(param_1 + 0x23));
      iVar1 = iVar1 + 1;
      puVar2 = puVar2 + 1;
    } while (iVar1 < *(int *)((longlong)param_1 + 0x11c));
  }
  param_1[0x22] = 0;
  iVar1 = 0;
  if (0 < *(int *)((longlong)param_1 + 0x1ac)) {
    puVar2 = param_1 + 0x24;
    do {
      FUN_1800010d0(*puVar2,*(undefined4 *)(param_1 + 0x35));
      iVar1 = iVar1 + 1;
      puVar2 = puVar2 + 1;
    } while (iVar1 < *(int *)((longlong)param_1 + 0x1ac));
  }
  param_1[0x34] = 0;
  return param_1;
}

 (GhidraScript)  

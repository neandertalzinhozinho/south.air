// FUN_1808ae650 @ 0x1808ae650

undefined8 * FUN_1808ae650(longlong param_1,undefined8 *param_2)

{
  undefined4 uVar1;
  undefined8 *puVar2;
  int iVar3;
  int iVar4;
  
  iVar3 = *(int *)(param_1 + 0x84);
  uVar1 = *(undefined4 *)(param_1 + 0x80);
  iVar4 = 0;
  *param_2 = 0;
  param_2[1] = 0;
  param_2[2] = 0;
  param_2[3] = 0;
  param_2[4] = 0;
  param_2[5] = 0;
  param_2[6] = 0;
  param_2[7] = 0;
  param_2[8] = 0;
  param_2[9] = 0;
  param_2[10] = 0;
  param_2[0xb] = 0;
  param_2[0xc] = 0;
  param_2[0xd] = 0;
  param_2[0xe] = 0;
  param_2[0xf] = 0;
  *(undefined4 *)(param_2 + 0x10) = uVar1;
  iVar3 = (int)(((longlong)iVar3 & 0x3fffffffffffffffU) >> 1);
  param_2[0x11] = (longlong)iVar3 << 3;
  *(int *)((longlong)param_2 + 0x84) = iVar3;
  if (0 < *(int *)(param_1 + 0x80)) {
    puVar2 = param_2;
    do {
      iVar4 = iVar4 + 1;
      *puVar2 = *(undefined8 *)((param_1 - (longlong)param_2) + (longlong)puVar2);
      puVar2 = puVar2 + 1;
    } while (iVar4 < *(int *)(param_1 + 0x80));
  }
  return param_2;
}


// FUN_18034c400 @ 0x18034c400

/* WARNING: Removing unreachable block (ram,0x00018034c697) */

void FUN_18034c400(undefined8 param_1)

{
  longlong lVar1;
  longlong *plVar2;
  uint uVar3;
  longlong lVar4;
  undefined1 local_res0;
  undefined1 auStack_1e8 [128];
  undefined1 auStack_158 [40];
  char *local_130;
  undefined8 local_120;
  undefined8 local_110;
  undefined *puStack_108;
  uint local_e8;
  uint local_e4;
  undefined *puStack_e0;
  undefined8 local_d0;
  ulonglong local_30;
  
  local_30 = DAT_1821c7640 ^ (ulonglong)auStack_158;
  uVar3 = (uint)&local_res0 & 0xaff;
  uVar3 = (uVar3 * uVar3 * 0x10 + 4) % 0x13;
  local_e8 = ((int)(-uVar3 | uVar3) >> 0x1f) * -0xdad8 ^ 0xd0d8;
  uVar3 = (uint)&local_res0 & 0xaff;
  uVar3 = ((uVar3 + 1) * uVar3 + 7) % 0x51;
  local_e4 = ((int)(-uVar3 | uVar3) >> 0x1f) * -0xff28 ^ 0xf8b8;
  lVar4 = 0x180000000;
  local_120 = 0x79914a0;
  lVar1 = 9;
  local_110 = 0x3ff8;
  puStack_108 = &UNK_181dac008;
  local_130 = "ation Required: ";
  puStack_e0 = &UNK_1879914a0;
  do {
    lVar4 = lVar4 + lVar1;
    lVar1 = ((~(lVar1 - lVar4) + 1U) - lVar4 ^ 0xffffffffffffffff) + 1;
    lVar4 = lVar4 - lVar1;
    uVar3 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar3 != 0);
  local_d0 = param_1;
                    /* WARNING: Call to offcut address within same function */
  func_0x00018034c6a9(0,lVar1);
  plVar2 = (longlong *)(ulonglong)((int)auStack_1e8 + 0x68);
  lVar1 = plVar2[3];
  plVar2[3] = lVar1 + 0x1e7;
  plVar2[2] = lVar1 + 0x102fb2;
  plVar2[1] = lVar1 + -0x6291;
  *plVar2 = lVar1 + 0x104c6b;
  plVar2[-1] = lVar1 + -0x6291;
  plVar2[-2] = lVar1 + 0x104c6b;
  plVar2[-3] = lVar1 + 0x102fb2;
  plVar2[-4] = lVar1 + 0x886aa;
  plVar2[-5] = lVar1 + 0x104c6b;
  plVar2[-6] = lVar1 + 0x102fb2;
                    /* WARNING: Could not recover jumptable at 0x00018034c868. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)(lVar1 + 0x104c6b))();
  return;
}


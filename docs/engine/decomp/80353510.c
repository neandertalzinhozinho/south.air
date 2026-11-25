// FUN_180353510 @ 0x180353510

/* WARNING: Removing unreachable block (ram,0x0001803535c2) */
/* WARNING: Removing unreachable block (ram,0x000180353635) */

undefined8 FUN_180353510(undefined8 param_1)

{
  undefined8 uVar1;
  uint uVar2;
  int iVar3;
  longlong *plVar4;
  longlong lVar5;
  undefined1 local_res0;
  undefined1 auStack_148 [32];
  undefined4 local_128;
  undefined4 local_d0;
  uint local_cc;
  undefined8 local_c0;
  ulonglong local_30;
  
  local_30 = DAT_1821c7640 ^ (ulonglong)auStack_148;
  uVar2 = (uint)&local_res0 & 0x71ff;
  iVar3 = uVar2 * uVar2 + 1;
  uVar2 = (iVar3 >> 4) + (iVar3 >> 1) + iVar3 * 0x24924924 >> 0x1d;
  uVar2 = (int)(uVar2 - 7) >> 0x1f & uVar2;
  local_cc = ((int)(uVar2 | -uVar2) >> 0x1f) * -0xfac8 ^ 0xffa8;
  uVar2 = 0xffffffff;
  local_128 = 0xb3;
  local_d0 = 0x360;
  lVar5 = 0x360;
  local_c0 = param_1;
                    /* WARNING: Call to offcut address within same function */
  func_0x0001803536c7();
  plVar4 = (longlong *)(ulonglong)uVar2;
  uVar1 = *plVar4;
  *plVar4 = lVar5 + 0x162;
  plVar4[-1] = lVar5 + -0x5305;
  plVar4[-2] = lVar5 + 0xdca;
  plVar4[-3] = lVar5 + -0x203e;
  plVar4[-4] = lVar5 + -0x5305;
  plVar4[-5] = lVar5 + -0x5306;
  plVar4[-6] = lVar5 + 0x7a37;
  plVar4[-7] = lVar5 + 0x1fe4;
  return uVar1;
}


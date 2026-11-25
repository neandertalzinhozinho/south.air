// FUN_18086f480 @ 0x18086f480

longlong * FUN_18086f480(uint *param_1,longlong *param_2,int param_3)

{
  uint uVar1;
  longlong *plVar2;
  int iVar3;
  longlong lVar4;
  int iVar5;
  ulonglong uVar6;
  longlong local_1b8 [16];
  uint local_138;
  int local_134;
  longlong local_130;
  longlong local_128 [16];
  uint local_a8;
  int iStack_a4;
  undefined8 uStack_a0;
  longlong local_98 [16];
  uint local_18;
  int iStack_14;
  undefined8 uStack_10;
  
  local_1b8[0] = 0;
  iVar3 = 0;
  local_134 = *(int *)(*(longlong *)(param_1 + 2) + 0x88);
  iVar5 = (param_1[0x24] - *(int *)(*(longlong *)(param_1 + 2) + 0x88)) + param_3;
  local_138 = *param_1;
  local_1b8[0xf] = 0;
  local_130 = (longlong)local_134 << 2;
  local_1b8[1] = 0;
  local_1b8[2] = 0;
  local_1b8[3] = 0;
  local_1b8[4] = 0;
  local_1b8[5] = 0;
  local_1b8[6] = 0;
  local_1b8[7] = 0;
  local_1b8[8] = 0;
  local_1b8[9] = 0;
  local_1b8[10] = 0;
  local_1b8[0xb] = 0;
  local_1b8[0xc] = 0;
  local_1b8[0xd] = 0;
  local_1b8[0xe] = 0;
  if (iVar5 < 1) {
    if (0 < (int)local_138) {
      plVar2 = local_1b8;
      do {
        iVar3 = iVar3 + 1;
        *plVar2 = *(longlong *)((longlong)param_1 + (0x10 - (longlong)local_1b8) + (longlong)plVar2)
        ;
        plVar2 = plVar2 + 1;
      } while (iVar3 < (int)local_138);
    }
    local_128[0] = 0;
    local_a8 = local_138;
    local_128[0xf] = 0;
    iStack_a4 = param_3;
    uStack_a0 = (longlong)param_3 << 2;
    local_128[1] = 0;
    local_128[2] = 0;
    local_128[3] = 0;
    local_128[4] = 0;
    local_128[5] = 0;
    local_128[6] = 0;
    local_128[7] = 0;
    local_128[8] = 0;
    local_128[9] = 0;
    local_128[10] = 0;
    local_128[0xb] = 0;
    local_128[0xc] = 0;
    local_128[0xd] = 0;
    local_128[0xe] = 0;
    if (0 < (int)local_138) {
      uVar1 = param_1[0x24];
      uVar6 = (ulonglong)local_138;
      lVar4 = 0;
      do {
        *(longlong *)((longlong)local_128 + lVar4) =
             *(longlong *)((longlong)local_1b8 + lVar4) + (longlong)(int)uVar1 * 4;
        uVar6 = uVar6 - 1;
        lVar4 = lVar4 + 8;
      } while (uVar6 != 0);
    }
    local_138 = *param_1;
    *param_2 = local_128[0];
    param_2[1] = local_128[1];
    param_2[2] = local_128[2];
    param_2[3] = local_128[3];
    param_2[4] = local_128[4];
    param_2[5] = local_128[5];
    param_2[6] = local_128[6];
    param_2[7] = local_128[7];
    param_2[8] = local_128[8];
    param_2[9] = local_128[9];
    param_2[10] = local_128[10];
    param_2[0xb] = local_128[0xb];
    param_2[0xc] = local_128[0xc];
    param_2[0xd] = local_128[0xd];
    param_2[0xe] = local_128[0xe];
    param_2[0xf] = local_128[0xf];
    param_2[0x10] = CONCAT44(iStack_a4,local_a8);
    param_2[0x11] = uStack_a0;
    param_2[0x12] = 0;
    param_2[0x13] = 0;
    param_2[0x14] = 0;
    param_2[0x15] = 0;
    param_2[0x16] = 0;
    param_2[0x17] = 0;
    param_2[0x18] = 0;
    param_2[0x19] = 0;
    param_2[0x1a] = 0;
    param_2[0x1b] = 0;
    param_2[0x1c] = 0;
    param_2[0x1d] = 0;
    param_2[0x1e] = 0;
    param_2[0x1f] = 0;
    iVar5 = 0;
    uStack_10._0_4_ = 0;
    uStack_10._4_4_ = 0;
    uStack_a0._0_4_ = (undefined4)uStack_10;
    uStack_a0._4_4_ = uStack_10._4_4_;
  }
  else {
    if (0 < (int)local_138) {
      plVar2 = local_1b8;
      do {
        iVar3 = iVar3 + 1;
        *plVar2 = *(longlong *)((longlong)param_1 + (0x10 - (longlong)local_1b8) + (longlong)plVar2)
        ;
        plVar2 = plVar2 + 1;
      } while (iVar3 < (int)local_138);
    }
    local_98[0] = 0;
    local_18 = local_138;
    local_98[0xf] = 0;
    iStack_14 = param_3 - iVar5;
    uStack_10 = (longlong)(param_3 - iVar5) << 2;
    local_98[1] = 0;
    local_98[2] = 0;
    local_98[3] = 0;
    local_98[4] = 0;
    local_98[5] = 0;
    local_98[6] = 0;
    local_98[7] = 0;
    local_98[8] = 0;
    local_98[9] = 0;
    local_98[10] = 0;
    local_98[0xb] = 0;
    local_98[0xc] = 0;
    local_98[0xd] = 0;
    local_98[0xe] = 0;
    if (0 < (int)local_138) {
      uVar1 = param_1[0x24];
      uVar6 = (ulonglong)local_138;
      lVar4 = 0;
      do {
        *(longlong *)((longlong)local_98 + lVar4) =
             *(longlong *)((longlong)local_1b8 + lVar4) + (longlong)(int)uVar1 * 4;
        uVar6 = uVar6 - 1;
        lVar4 = lVar4 + 8;
      } while (uVar6 != 0);
    }
    iVar3 = 0;
    local_1b8[0] = 0;
    local_1b8[0xf] = 0;
    local_138 = *param_1;
    local_134 = *(int *)(*(longlong *)(param_1 + 2) + 0x88);
    local_130 = (longlong)*(int *)(*(longlong *)(param_1 + 2) + 0x88) << 2;
    local_1b8[1] = 0;
    local_1b8[2] = 0;
    local_1b8[3] = 0;
    local_1b8[4] = 0;
    local_1b8[5] = 0;
    local_1b8[6] = 0;
    local_1b8[7] = 0;
    local_1b8[8] = 0;
    local_1b8[9] = 0;
    local_1b8[10] = 0;
    local_1b8[0xb] = 0;
    local_1b8[0xc] = 0;
    local_1b8[0xd] = 0;
    local_1b8[0xe] = 0;
    if (0 < (int)*param_1) {
      plVar2 = local_1b8;
      do {
        iVar3 = iVar3 + 1;
        *plVar2 = *(longlong *)((longlong)param_1 + (0x10 - (longlong)local_1b8) + (longlong)plVar2)
        ;
        plVar2 = plVar2 + 1;
      } while (iVar3 < (int)local_138);
    }
    local_128[0] = 0;
    local_128[0xf] = 0;
    uStack_a0 = (longlong)iVar5 << 2;
    local_128[1] = 0;
    local_128[2] = 0;
    local_128[3] = 0;
    local_128[4] = 0;
    local_128[5] = 0;
    local_128[6] = 0;
    local_128[7] = 0;
    local_128[8] = 0;
    local_128[9] = 0;
    local_128[10] = 0;
    local_128[0xb] = 0;
    local_128[0xc] = 0;
    local_128[0xd] = 0;
    local_128[0xe] = 0;
    if (0 < (int)local_138) {
      local_a8 = local_138;
      iStack_a4 = iVar5;
                    /* WARNING: Subroutine does not return */
      FUN_181798f36(local_128,local_1b8,(ulonglong)local_138 << 3);
    }
    *param_2 = local_98[0];
    param_2[1] = local_98[1];
    param_2[2] = local_98[2];
    param_2[3] = local_98[3];
    param_2[4] = local_98[4];
    param_2[5] = local_98[5];
    param_2[6] = local_98[6];
    param_2[7] = local_98[7];
    param_2[8] = local_98[8];
    param_2[9] = local_98[9];
    param_2[10] = local_98[10];
    param_2[0xb] = local_98[0xb];
    param_2[0xc] = local_98[0xc];
    param_2[0xd] = local_98[0xd];
    param_2[0xe] = local_98[0xe];
    param_2[0xf] = local_98[0xf];
    param_2[0x12] = 0;
    param_2[0x13] = 0;
    param_2[0x10] = CONCAT44(iStack_14,local_18);
    param_2[0x11] = uStack_10;
    param_2[0x14] = 0;
    param_2[0x15] = 0;
    param_2[0x16] = 0;
    param_2[0x17] = 0;
    param_2[0x18] = 0;
    param_2[0x19] = 0;
    param_2[0x1a] = 0;
    param_2[0x1b] = 0;
    param_2[0x1c] = 0;
    param_2[0x1d] = 0;
    param_2[0x1e] = 0;
    param_2[0x1f] = 0;
    uStack_a0._4_4_ = (undefined4)((ulonglong)uStack_a0 >> 0x20);
  }
  *(undefined4 *)(param_2 + 0x20) = 0;
  *(undefined4 *)((longlong)param_2 + 0x104) = 0;
  *(undefined4 *)(param_2 + 0x21) = 0;
  *(undefined4 *)((longlong)param_2 + 0x10c) = 0;
  *(uint *)(param_2 + 0x22) = local_138;
  *(int *)((longlong)param_2 + 0x114) = iVar5;
  *(undefined4 *)(param_2 + 0x23) = (undefined4)uStack_a0;
  *(undefined4 *)((longlong)param_2 + 0x11c) = uStack_a0._4_4_;
  return param_2;
}


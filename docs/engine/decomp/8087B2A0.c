// FUN_18087b2a0 @ 0x18087b2a0

void FUN_18087b2a0(longlong param_1)

{
  undefined8 uVar1;
  uint uVar2;
  undefined8 *puVar3;
  longlong lVar4;
  ulonglong uVar5;
  int iVar6;
  ulonglong uVar7;
  int iVar8;
  undefined4 uVar9;
  undefined8 local_208;
  uint uStack_200;
  int iStack_1fc;
  undefined8 local_1f8 [16];
  uint local_178;
  uint uStack_174;
  longlong lStack_170;
  undefined8 local_168 [16];
  int local_e8;
  uint local_e4;
  longlong local_e0;
  undefined8 local_d8 [4];
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  longlong lStack_50;
  
  iVar6 = 0;
  local_168[0xf] = 0;
  local_168[0] = 0;
  iVar8 = 0;
  local_e8 = *(int *)(param_1 + 0x4f8);
  local_e4 = *(uint *)(param_1 + 0x500);
  local_e0 = (longlong)(int)*(uint *)(param_1 + 0x500) << 2;
  local_168[1] = 0;
  local_168[2] = 0;
  local_168[3] = 0;
  local_168[4] = 0;
  local_168[5] = 0;
  local_168[6] = 0;
  local_168[7] = 0;
  local_168[8] = 0;
  local_168[9] = 0;
  local_168[10] = 0;
  local_168[0xb] = 0;
  local_168[0xc] = 0;
  local_168[0xd] = 0;
  local_168[0xe] = 0;
  if (0 < *(int *)(param_1 + 0x4f8)) {
    puVar3 = local_168;
    do {
      iVar8 = iVar8 + 1;
      *puVar3 = *(undefined8 *)(((param_1 + 0x478) - (longlong)local_168) + (longlong)puVar3);
      puVar3 = puVar3 + 1;
    } while (iVar8 < local_e8);
  }
  iStack_1fc = local_e4 * 4;
  uVar9 = *(undefined4 *)(*(longlong *)(param_1 + 0x2c38) + 4);
  local_208 = local_168[0];
  uStack_200 = local_e4;
  FUN_181c9a9fb();
  FUN_181c9aa01(uVar9);
  FUN_181c9a9fb();
  uVar9 = FUN_181c9a9d7();
  iVar8 = 0;
  uStack_174 = *(int *)(param_1 + 2000);
  local_1f8[0] = 0;
  local_1f8[0xf] = 0;
  local_178 = *(int *)(param_1 + 0x7c8);
  lStack_170 = (longlong)*(int *)(param_1 + 2000) << 2;
  local_1f8[1] = 0;
  local_1f8[2] = 0;
  local_1f8[3] = 0;
  local_1f8[4] = 0;
  local_1f8[5] = 0;
  local_1f8[6] = 0;
  local_1f8[7] = 0;
  local_1f8[8] = 0;
  local_1f8[9] = 0;
  local_1f8[10] = 0;
  local_1f8[0xb] = 0;
  local_1f8[0xc] = 0;
  local_1f8[0xd] = 0;
  local_1f8[0xe] = 0;
  if (0 < *(int *)(param_1 + 0x7c8)) {
    puVar3 = local_1f8;
    do {
      iVar8 = iVar8 + 1;
      *puVar3 = *(undefined8 *)(((param_1 + 0x748) - (longlong)local_1f8) + (longlong)puVar3);
      puVar3 = puVar3 + 1;
    } while (iVar8 < (int)local_178);
  }
  local_d8[0] = local_1f8[0];
  local_d8[1] = local_1f8[1];
  local_d8[2] = local_1f8[2];
  local_d8[3] = local_1f8[3];
  local_b8 = local_1f8[4];
  uStack_b0 = local_1f8[5];
  local_a8 = local_1f8[6];
  uStack_a0 = local_1f8[7];
  local_98 = local_1f8[8];
  uStack_90 = local_1f8[9];
  local_88 = local_1f8[10];
  uStack_80 = local_1f8[0xb];
  local_78 = local_1f8[0xc];
  uStack_70 = local_1f8[0xd];
  local_58 = CONCAT44(uStack_174,local_178);
  local_68 = local_1f8[0xe];
  uStack_60 = local_1f8[0xf];
  lStack_50 = lStack_170;
  FUN_180882c30(&local_208,local_d8,uVar9);
  uVar2 = local_e4;
  uVar5 = (ulonglong)(int)local_e4;
  if (*(char *)(param_1 + 0x58) == '\0') {
    FUN_180001220();
    FUN_1800012e0();
  }
  uVar1 = local_168[0];
  if (1 < *(ulonglong *)(param_1 + 0x48)) {
    local_1f8[0xf] = 0;
    local_178 = *(int *)(param_1 + 0x48) - 1;
    local_1f8[0] = 0;
    uStack_174 = uVar2;
    lStack_170 = uVar5 << 2;
    local_1f8[1] = 0;
    local_1f8[2] = 0;
    local_1f8[3] = 0;
    local_1f8[4] = 0;
    local_1f8[5] = 0;
    local_1f8[6] = 0;
    local_1f8[7] = 0;
    local_1f8[8] = 0;
    local_1f8[9] = 0;
    local_1f8[10] = 0;
    local_1f8[0xb] = 0;
    local_1f8[0xc] = 0;
    local_1f8[0xd] = 0;
    local_1f8[0xe] = 0;
    if (0 < (int)local_178) {
      lVar4 = 0;
      do {
        iVar6 = iVar6 + 1;
        *(undefined8 *)((longlong)local_1f8 + lVar4) =
             *(undefined8 *)((longlong)local_168 + lVar4 + 8);
        lVar4 = lVar4 + 8;
      } while (iVar6 < (int)local_178);
      uVar5 = (ulonglong)uStack_174;
    }
    local_d8[0] = local_1f8[0];
    local_d8[1] = local_1f8[1];
    local_d8[2] = local_1f8[2];
    local_d8[3] = local_1f8[3];
    local_b8 = local_1f8[4];
    uStack_b0 = local_1f8[5];
    local_a8 = local_1f8[6];
    uStack_a0 = local_1f8[7];
    local_98 = local_1f8[8];
    uStack_90 = local_1f8[9];
    local_88 = local_1f8[10];
    uStack_80 = local_1f8[0xb];
    local_78 = local_1f8[0xc];
    uStack_70 = local_1f8[0xd];
    local_68 = local_1f8[0xe];
    uStack_60 = local_1f8[0xf];
    local_58 = CONCAT44(uStack_174,local_178);
    lStack_50 = lStack_170;
    if (local_178 == 1) {
      FUN_1800010a0(uVar1,local_1f8[0],uVar5 & 0xffffffff);
    }
    else if (0 < (int)local_178) {
      puVar3 = local_d8;
      uVar7 = (ulonglong)local_178;
      do {
        FUN_1800010a0(uVar1,*puVar3,uVar5 & 0xffffffff);
        puVar3 = puVar3 + 1;
        uVar7 = uVar7 - 1;
      } while (uVar7 != 0);
    }
  }
  return;
}


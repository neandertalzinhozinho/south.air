// FUN_180880640 @ 0x180880640

void FUN_180880640(longlong *param_1,longlong param_2,undefined8 *param_3,undefined8 *param_4,
                  longlong *param_5)

{
  char cVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  undefined8 *puVar6;
  longlong lVar7;
  longlong lVar8;
  longlong lVar9;
  int local_res8 [2];
  int local_res10 [2];
  undefined8 *local_res18;
  undefined8 *local_res20;
  ulonglong in_stack_fffffffffffff508;
  int local_ad8 [4];
  uint local_ac8;
  longlong local_ac0;
  int local_ab8;
  int local_ab4;
  longlong local_ab0;
  int local_aa8;
  int local_aa4;
  longlong *local_a98;
  longlong *plStack_a90;
  longlong *local_a88;
  int *piStack_a80;
  undefined8 local_a78;
  undefined8 uStack_a70;
  undefined8 local_a68;
  undefined8 uStack_a60;
  longlong local_a58 [16];
  int local_9d8;
  int local_9d4;
  longlong local_9d0;
  longlong *local_9c8;
  longlong *plStack_9c0;
  longlong *local_9b8;
  int *piStack_9b0;
  undefined4 local_9a8;
  undefined4 uStack_9a4;
  undefined4 uStack_9a0;
  undefined4 uStack_99c;
  undefined4 local_998;
  undefined4 uStack_994;
  undefined4 uStack_990;
  undefined4 uStack_98c;
  undefined8 local_988;
  undefined8 uStack_980;
  undefined8 local_978;
  undefined8 uStack_970;
  undefined8 local_968;
  undefined8 uStack_960;
  undefined8 local_958;
  undefined8 uStack_950;
  undefined8 local_948;
  undefined8 uStack_940;
  undefined8 local_938;
  undefined8 uStack_930;
  undefined8 local_928;
  undefined8 uStack_920;
  undefined4 local_918;
  undefined4 uStack_914;
  undefined4 uStack_910;
  undefined4 uStack_90c;
  undefined8 local_908;
  undefined8 uStack_900;
  longlong local_868;
  undefined1 local_860 [1016];
  int local_468;
  int local_464;
  longlong local_460;
  longlong local_458;
  undefined1 local_450 [1016];
  int local_58;
  int local_54;
  longlong local_50;
  
  iVar2 = (int)param_1[10];
  lVar9 = (longlong)iVar2;
  lVar7 = 0;
  local_res10[0] = (int)param_1[9];
  local_ad8[0] = (int)param_1[0x592];
  lVar8 = 0;
  local_ac8 = *(uint *)(param_5 + 3);
  if (0 < iVar2) {
    uVar5 = local_ac8;
    do {
      uVar4 = uVar5 + local_res10[0];
      *(longlong *)(local_860 + lVar8 * 8 + -8) = *param_5 + (longlong)(int)uVar5 * 4;
      uVar5 = (uVar4 - (uVar4 & 0xf)) + 0x10;
      if ((uVar4 & 0xf) == 0) {
        uVar5 = uVar4;
      }
      lVar8 = lVar8 + 1;
      *(uint *)(param_5 + 3) = uVar5;
    } while (lVar8 < lVar9);
  }
  uVar5 = *(uint *)(param_5 + 3);
  lVar8 = 0;
  if (0 < iVar2) {
    do {
      uVar4 = uVar5 + local_ad8[0];
      *(longlong *)(local_860 + lVar8 * 8 + -8) = *param_5 + (longlong)(int)uVar5 * 4;
      uVar5 = (uVar4 - (uVar4 & 0xf)) + 0x10;
      if ((uVar4 & 0xf) == 0) {
        uVar5 = uVar4;
      }
      lVar8 = lVar8 + 1;
      *(uint *)(param_5 + 3) = uVar5;
    } while (lVar8 < lVar9);
  }
  local_ab8 = local_res10[0] * iVar2;
  local_458 = 0;
  local_ab4 = local_ab8 * 4;
  local_ac0 = *param_5 + (longlong)(int)param_5[3] * 4;
  uVar4 = (int)param_5[3] + local_ab8;
  uVar5 = (uVar4 - (uVar4 & 0xf)) + 0x10;
  if ((uVar4 & 0xf) == 0) {
    uVar5 = uVar4;
  }
  local_aa8 = local_ad8[0] * iVar2;
  *(uint *)(param_5 + 3) = uVar5;
  local_aa4 = local_aa8 * 4;
  local_ab0 = *param_5 + (longlong)(int)uVar5 * 4;
  uVar5 = uVar5 + local_aa8;
  uVar4 = (uVar5 - (uVar5 & 0xf)) + 0x10;
  if ((uVar5 & 0xf) == 0) {
    uVar4 = uVar5;
  }
  *(uint *)(param_5 + 3) = uVar4;
  lVar8 = param_1[9];
  local_res8[0] = iVar2;
  local_res18 = param_3;
  local_res20 = param_4;
  FUN_181798f42(local_450,0,0x3f8);
  local_54 = (int)lVar8;
  lVar8 = 0;
  local_50 = (longlong)local_54 << 3;
  local_58 = iVar2;
  if (0 < iVar2) {
    iVar3 = local_54 * 2;
    do {
      *(longlong *)(local_450 + lVar8 * 8 + -8) = *param_5 + (longlong)(int)uVar4 * 4;
      uVar5 = iVar3 + uVar4;
      uVar4 = (uVar5 - (uVar5 & 0xf)) + 0x10;
      if ((uVar5 & 0xf) == 0) {
        uVar4 = uVar5;
      }
      lVar8 = lVar8 + 1;
      *(uint *)(param_5 + 3) = uVar4;
    } while (lVar8 < lVar9);
  }
  uVar5 = *(uint *)(param_5 + 3);
  lVar8 = param_1[0x592];
  local_868 = 0;
  FUN_181798f42(local_860,0,0x3f8);
  local_464 = (int)lVar8;
  lVar8 = 0;
  local_460 = (longlong)local_464 << 3;
  local_468 = iVar2;
  if (0 < iVar2) {
    iVar2 = local_464 * 2;
    do {
      uVar4 = iVar2 + uVar5;
      *(longlong *)(local_860 + lVar8 * 8 + -8) = *param_5 + (longlong)(int)uVar5 * 4;
      uVar5 = (uVar4 - (uVar4 & 0xf)) + 0x10;
      if ((uVar4 & 0xf) == 0) {
        uVar5 = uVar4;
      }
      lVar8 = lVar8 + 1;
      *(uint *)(param_5 + 3) = uVar5;
    } while (lVar8 < lVar9);
  }
  plStack_a90 = &local_458;
  local_a88 = &local_868;
  piStack_a80 = local_res8;
  local_a78 = &local_ac0;
  uStack_a70 = local_res10;
  local_a68 = &local_ab0;
  uStack_a60 = local_ad8;
  cVar1 = *(char *)(*param_1 + 0x51);
  local_9d8 = SUB164(*(undefined1 (*) [16])(param_2 + 0x80),0);
  iVar2 = SUB164(*(undefined1 (*) [16])(param_2 + 0x80),4);
  uVar5 = *(uint *)(param_5 + 3);
  local_a58[0] = 0;
  puVar6 = local_res18;
  if (cVar1 != '\0') {
    puVar6 = local_res20;
  }
  local_988 = *puVar6;
  uStack_980 = puVar6[1];
  local_978 = puVar6[2];
  uStack_970 = puVar6[3];
  local_968 = puVar6[4];
  uStack_960 = puVar6[5];
  lVar8 = (longlong)local_9d8;
  local_958 = puVar6[6];
  uStack_950 = puVar6[7];
  local_948 = puVar6[8];
  uStack_940 = puVar6[9];
  local_938 = puVar6[10];
  uStack_930 = puVar6[0xb];
  local_928 = puVar6[0xc];
  uStack_920 = puVar6[0xd];
  local_918 = *(undefined4 *)(puVar6 + 0xe);
  uStack_914 = *(undefined4 *)((longlong)puVar6 + 0x74);
  uStack_910 = *(undefined4 *)(puVar6 + 0xf);
  uStack_90c = *(undefined4 *)((longlong)puVar6 + 0x7c);
  local_908 = puVar6[0x10];
  uStack_900 = puVar6[0x11];
  local_a58[0xf] = 0;
  local_9d0 = (longlong)iVar2 << 2;
  local_a58[1] = 0;
  local_a58[2] = 0;
  local_a58[3] = 0;
  local_a58[4] = 0;
  local_a58[5] = 0;
  local_a58[6] = 0;
  local_a58[7] = 0;
  local_a58[8] = 0;
  local_a58[9] = 0;
  local_a58[10] = 0;
  local_a58[0xb] = 0;
  local_a58[0xc] = 0;
  local_a58[0xd] = 0;
  local_a58[0xe] = 0;
  local_9d4 = iVar2;
  if (0 < local_9d8) {
    do {
      uVar4 = uVar5 + iVar2;
      local_a58[lVar7] = *param_5 + (longlong)(int)uVar5 * 4;
      uVar5 = (uVar4 - (uVar4 & 0xf)) + 0x10;
      if ((uVar4 & 0xf) == 0) {
        uVar5 = uVar4;
      }
      lVar7 = lVar7 + 1;
      *(uint *)(param_5 + 3) = uVar5;
    } while (lVar7 < lVar8);
  }
  local_a98 = param_1;
  FUN_180885040(param_1 + 0x58a,local_a58,local_res18,&local_988,
                in_stack_fffffffffffff508 & 0xffffffffffffff00,cVar1,param_5);
  local_9c8 = local_a98;
  plStack_9c0 = plStack_a90;
  local_9b8 = local_a88;
  piStack_9b0 = piStack_a80;
  local_9a8 = (undefined4)local_a78;
  uStack_9a4 = local_a78._4_4_;
  uStack_9a0 = (undefined4)uStack_a70;
  uStack_99c = uStack_a70._4_4_;
  local_998 = (undefined4)local_a68;
  uStack_994 = local_a68._4_4_;
  uStack_990 = (undefined4)uStack_a60;
  uStack_98c = uStack_a60._4_4_;
  FUN_1808875f0(param_1 + 1,param_2,local_a58,&local_988,&local_9c8,cVar1,param_5);
  *(uint *)(param_5 + 3) = local_ac8;
  return;
}


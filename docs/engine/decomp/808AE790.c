// FUN_1808ae790 @ 0x1808ae790

void FUN_1808ae790(undefined8 *param_1,longlong *param_2,int param_3)

{
  undefined4 uVar1;
  undefined8 uVar2;
  longlong lVar3;
  longlong lVar4;
  longlong *plVar5;
  longlong lVar6;
  undefined4 local_1d8;
  undefined4 uStack_1d4;
  undefined8 uStack_1d0;
  undefined8 local_1c8;
  uint uStack_1c0;
  undefined4 uStack_1bc;
  int local_1b8;
  int local_1b4;
  uint local_1a8;
  undefined4 uStack_1a4;
  undefined8 *puStack_1a0;
  undefined8 local_198 [16];
  int local_118;
  undefined4 uStack_114;
  undefined8 local_110;
  undefined8 *puStack_108;
  undefined8 local_100 [16];
  uint local_80;
  undefined4 uStack_7c;
  undefined4 local_68;
  undefined4 uStack_64;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  undefined4 local_58;
  undefined4 uStack_54;
  uint uStack_50;
  undefined4 uStack_4c;
  
  lVar6 = (longlong)(int)param_2[0x10];
  if (0 < lVar6) {
    uVar1 = *(undefined4 *)((longlong)param_2 + 0x84);
    plVar5 = param_2;
    do {
      local_1a8 = *(uint *)((longlong)param_1 + 0x8c);
      lVar3 = (longlong)(int)local_1a8;
      local_198[0xf] = 0;
      local_118 = *(int *)((longlong)param_1 + 0x84);
      local_198[0] = 0;
      local_198[1] = 0;
      local_198[2] = 0;
      local_198[3] = 0;
      local_198[4] = 0;
      local_198[5] = 0;
      local_198[6] = 0;
      local_198[7] = 0;
      local_198[8] = 0;
      local_198[9] = 0;
      local_198[10] = 0;
      local_198[0xb] = 0;
      local_198[0xc] = 0;
      local_198[0xd] = 0;
      local_198[0xe] = 0;
      puStack_1a0 = param_1;
      if (((0 < (int)local_1a8) && (1 < local_1a8)) &&
         ((param_1 + (int)(local_1a8 - 1) < local_198 ||
          (local_198 + (int)(local_1a8 - 1) < param_1)))) {
                    /* WARNING: Subroutine does not return */
        FUN_181798f36(local_198,param_1,lVar3 * 8);
      }
      if (0 < lVar3) {
                    /* WARNING: Subroutine does not return */
        FUN_181798f36(local_198,param_1,lVar3 << 3);
      }
      local_110 = CONCAT44(uStack_1a4,local_1a8);
      uStack_1c0 = local_118 - param_3 & *(int *)(param_1 + 0x11) - 1U;
      lVar3 = *plVar5;
      local_100[0] = 0;
      local_100[1] = 0;
      local_1d8 = 1;
      local_100[2] = 0;
      local_100[3] = 0;
      local_100[4] = 0;
      local_100[5] = 0;
      local_100[6] = 0;
      local_100[7] = 0;
      local_100[8] = 0;
      local_100[9] = 0;
      local_100[10] = 0;
      local_100[0xb] = 0;
      local_100[0xc] = 0;
      local_100[0xd] = 0;
      _local_80 = CONCAT44(uStack_114,uStack_1c0);
      local_100[0xe] = 0;
      local_100[0xf] = 0;
      uVar2 = *(undefined8 *)((longlong)plVar5 + ((longlong)local_100 - (longlong)param_2));
      local_1c8._0_4_ = (undefined4)uVar2;
      local_1c8._4_4_ = (undefined4)((ulonglong)uVar2 >> 0x20);
      uStack_1d0._0_4_ = (int)param_1;
      uStack_1d0._4_4_ = (int)((ulonglong)param_1 >> 0x20);
      local_58 = (undefined4)local_1c8;
      uStack_54 = local_1c8._4_4_;
      uStack_4c = uStack_1bc;
      local_68 = 1;
      uStack_64 = uStack_1d4;
      uStack_60 = (int)uStack_1d0;
      uStack_5c = uStack_1d0._4_4_;
      uStack_1d0 = param_1;
      local_1c8 = uVar2;
      puStack_108 = param_1;
      uStack_50 = uStack_1c0;
      FUN_18086f170(&local_68,&local_1d8,uVar1);
      lVar4 = (longlong)uStack_1d0._4_4_;
      if ((int)uStack_1d0 == 1) {
        FUN_1800010a0(CONCAT44(uStack_1d4,local_1d8),lVar3,uStack_1d0._4_4_);
      }
      if ((0 < local_1b4) && (local_1b8 == 1)) {
        FUN_1800010a0(CONCAT44(uStack_1bc,uStack_1c0),lVar3 + lVar4 * 4);
      }
      plVar5 = plVar5 + 1;
      lVar6 = lVar6 + -1;
    } while (lVar6 != 0);
  }
  if (0 < (longlong)*(int *)((longlong)param_1 + 0x8c)) {
    puStack_108 = param_1;
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(local_100,param_1,(longlong)*(int *)((longlong)param_1 + 0x8c) << 3);
  }
  *(uint *)((longlong)param_1 + 0x84) =
       *(int *)((longlong)param_1 + 0x84) + *(int *)((longlong)param_2 + 0x84) &
       *(int *)(param_1 + 0x11) - 1U;
  return;
}


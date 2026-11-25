// FUN_180881050 @ 0x180881050

void FUN_180881050(longlong *param_1,longlong param_2,undefined8 *param_3,undefined8 *param_4,
                  longlong *param_5)

{
  char cVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  undefined8 *puVar5;
  longlong lVar6;
  longlong lVar7;
  longlong lVar8;
  longlong lVar9;
  int local_res8 [2];
  int local_res10 [2];
  undefined8 *local_res18;
  undefined8 *local_res20;
  ulonglong in_stack_fffffffffffff9d8;
  int local_608 [3];
  uint local_5fc;
  longlong local_5f8;
  int local_5f0;
  int local_5ec;
  longlong local_5e8;
  int local_5e0;
  int local_5dc;
  longlong *local_5d8;
  int *piStack_5d0;
  undefined8 local_5c8;
  undefined8 uStack_5c0;
  undefined8 local_5b8;
  undefined8 uStack_5b0;
  longlong local_5a8 [16];
  int local_528;
  int local_524;
  longlong local_520;
  longlong *local_518;
  int *piStack_510;
  undefined4 local_508;
  undefined4 uStack_504;
  undefined4 uStack_500;
  undefined4 uStack_4fc;
  undefined4 local_4f8;
  undefined4 uStack_4f4;
  undefined4 uStack_4f0;
  undefined4 uStack_4ec;
  undefined8 local_4e8;
  undefined8 uStack_4e0;
  undefined8 local_4d8;
  undefined8 uStack_4d0;
  undefined8 local_4c8;
  undefined8 uStack_4c0;
  undefined8 local_4b8;
  undefined8 uStack_4b0;
  undefined8 local_4a8;
  undefined8 uStack_4a0;
  undefined8 local_498;
  undefined8 uStack_490;
  undefined8 local_488;
  undefined8 uStack_480;
  undefined4 local_478;
  undefined4 uStack_474;
  undefined4 uStack_470;
  undefined4 uStack_46c;
  undefined8 local_468;
  undefined8 uStack_460;
  
  local_res8[0] = (int)param_1[10];
  lVar9 = (longlong)local_res8[0];
  lVar8 = 0;
  local_res10[0] = (int)param_1[9];
  local_608[0] = (int)param_1[0x592];
  lVar6 = 0;
  local_5fc = *(uint *)(param_5 + 3);
  if (0 < local_res8[0]) {
    uVar4 = local_5fc;
    do {
      uVar3 = uVar4 + local_res10[0];
      uVar4 = (uVar3 - (uVar3 & 0xf)) + 0x10;
      if ((uVar3 & 0xf) == 0) {
        uVar4 = uVar3;
      }
      lVar6 = lVar6 + 1;
      *(uint *)(param_5 + 3) = uVar4;
    } while (lVar6 < lVar9);
  }
  uVar4 = *(uint *)(param_5 + 3);
  lVar6 = 0;
  if (0 < local_res8[0]) {
    do {
      uVar3 = uVar4 + local_608[0];
      uVar4 = (uVar3 - (uVar3 & 0xf)) + 0x10;
      if ((uVar3 & 0xf) == 0) {
        uVar4 = uVar3;
      }
      lVar6 = lVar6 + 1;
      *(uint *)(param_5 + 3) = uVar4;
    } while (lVar6 < lVar9);
  }
  lVar6 = 0;
  local_5f0 = local_res10[0] * local_res8[0];
  local_5ec = local_5f0 * 4;
  local_5f8 = *param_5 + (longlong)(int)param_5[3] * 4;
  uVar3 = (int)param_5[3] + local_5f0;
  uVar4 = (uVar3 - (uVar3 & 0xf)) + 0x10;
  if ((uVar3 & 0xf) == 0) {
    uVar4 = uVar3;
  }
  local_5e0 = local_608[0] * local_res8[0];
  *(uint *)(param_5 + 3) = uVar4;
  local_5dc = local_5e0 * 4;
  local_5e8 = *param_5 + (longlong)(int)uVar4 * 4;
  uVar4 = uVar4 + local_5e0;
  uVar3 = (uVar4 - (uVar4 & 0xf)) + 0x10;
  if ((uVar4 & 0xf) == 0) {
    uVar3 = uVar4;
  }
  *(uint *)(param_5 + 3) = uVar3;
  lVar7 = param_1[9];
  if (0 < local_res8[0]) {
    do {
      uVar4 = (int)lVar7 * 2 + uVar3;
      uVar3 = (uVar4 - (uVar4 & 0xf)) + 0x10;
      if ((uVar4 & 0xf) == 0) {
        uVar3 = uVar4;
      }
      lVar6 = lVar6 + 1;
      *(uint *)(param_5 + 3) = uVar3;
    } while (lVar6 < lVar9);
  }
  uVar4 = *(uint *)(param_5 + 3);
  lVar7 = 0;
  lVar6 = param_1[0x592];
  if (0 < local_res8[0]) {
    do {
      uVar3 = (int)lVar6 * 2 + uVar4;
      uVar4 = (uVar3 - (uVar3 & 0xf)) + 0x10;
      if ((uVar3 & 0xf) == 0) {
        uVar4 = uVar3;
      }
      lVar7 = lVar7 + 1;
      *(uint *)(param_5 + 3) = uVar4;
    } while (lVar7 < lVar9);
  }
  piStack_5d0 = local_res8;
  local_5c8 = &local_5f8;
  uStack_5c0 = local_res10;
  local_5b8 = &local_5e8;
  uStack_5b0 = local_608;
  cVar1 = *(char *)(*param_1 + 0x51);
  local_528 = SUB164(*(undefined1 (*) [16])(param_2 + 0x80),0);
  iVar2 = SUB164(*(undefined1 (*) [16])(param_2 + 0x80),4);
  uVar4 = *(uint *)(param_5 + 3);
  local_5a8[0] = 0;
  puVar5 = param_3;
  if (cVar1 != '\0') {
    puVar5 = param_4;
  }
  local_4e8 = *puVar5;
  uStack_4e0 = puVar5[1];
  local_4d8 = puVar5[2];
  uStack_4d0 = puVar5[3];
  local_4c8 = puVar5[4];
  uStack_4c0 = puVar5[5];
  lVar6 = (longlong)local_528;
  local_4b8 = puVar5[6];
  uStack_4b0 = puVar5[7];
  local_4a8 = puVar5[8];
  uStack_4a0 = puVar5[9];
  local_498 = puVar5[10];
  uStack_490 = puVar5[0xb];
  local_488 = puVar5[0xc];
  uStack_480 = puVar5[0xd];
  local_478 = *(undefined4 *)(puVar5 + 0xe);
  uStack_474 = *(undefined4 *)((longlong)puVar5 + 0x74);
  uStack_470 = *(undefined4 *)(puVar5 + 0xf);
  uStack_46c = *(undefined4 *)((longlong)puVar5 + 0x7c);
  local_468 = puVar5[0x10];
  uStack_460 = puVar5[0x11];
  local_5a8[0xf] = 0;
  local_520 = (longlong)iVar2 << 2;
  local_5a8[1] = 0;
  local_5a8[2] = 0;
  local_5a8[3] = 0;
  local_5a8[4] = 0;
  local_5a8[5] = 0;
  local_5a8[6] = 0;
  local_5a8[7] = 0;
  local_5a8[8] = 0;
  local_5a8[9] = 0;
  local_5a8[10] = 0;
  local_5a8[0xb] = 0;
  local_5a8[0xc] = 0;
  local_5a8[0xd] = 0;
  local_5a8[0xe] = 0;
  local_524 = iVar2;
  if (0 < local_528) {
    do {
      uVar3 = uVar4 + iVar2;
      local_5a8[lVar8] = *param_5 + (longlong)(int)uVar4 * 4;
      uVar4 = (uVar3 - (uVar3 & 0xf)) + 0x10;
      if ((uVar3 & 0xf) == 0) {
        uVar4 = uVar3;
      }
      lVar8 = lVar8 + 1;
      *(uint *)(param_5 + 3) = uVar4;
    } while (lVar8 < lVar6);
  }
  local_res18 = param_3;
  local_res20 = param_4;
  local_5d8 = param_1;
  FUN_180889bb0(param_1 + 0x58a,local_5a8,param_3,&local_4e8,
                in_stack_fffffffffffff9d8 & 0xffffffffffffff00,cVar1,param_5);
  local_518 = local_5d8;
  piStack_510 = piStack_5d0;
  local_508 = (undefined4)local_5c8;
  uStack_504 = local_5c8._4_4_;
  uStack_500 = (undefined4)uStack_5c0;
  uStack_4fc = uStack_5c0._4_4_;
  local_4f8 = (undefined4)local_5b8;
  uStack_4f4 = local_5b8._4_4_;
  uStack_4f0 = (undefined4)uStack_5b0;
  uStack_4ec = uStack_5b0._4_4_;
  FUN_18088ae20(param_1 + 1,param_2,local_5a8,&local_4e8,&local_518,cVar1,param_5);
  *(uint *)(param_5 + 3) = local_5fc;
  return;
}


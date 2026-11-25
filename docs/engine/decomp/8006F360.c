// FUN_18006f360 @ 0x18006f360

undefined8 FUN_18006f360(undefined8 param_1,undefined8 *param_2)

{
  uint uVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  int iVar4;
  undefined8 uVar5;
  longlong lVar6;
  undefined4 *puVar7;
  int local_38;
  int local_34;
  int local_30;
  undefined4 local_2c;
  
  if (*(int *)(param_2[4] + 0x18) != 1) {
    uVar1 = *(uint *)param_2[0xe];
    local_38 = 0;
    FUN_180071360(param_2);
    puVar2 = *(undefined8 **)param_2[4];
    puVar7 = (undefined4 *)*puVar2;
    *puVar2 = puVar7 + 0x20;
    puVar3 = (undefined8 *)param_2[4];
    if (puVar2[1] == 0) {
      puVar7 = (undefined4 *)0x0;
    }
    if ((uVar1 - 1 & uVar1) == 0) {
      iVar4 = 0x1f;
      if (uVar1 != 0) {
        for (; uVar1 >> iVar4 == 0; iVar4 = iVar4 + -1) {
        }
      }
      iVar4 = FUN_180072180(puVar7 + 2,iVar4,local_38,0,*(undefined8 *)*puVar3,
                            *(undefined8 *)puVar3[1]);
      *(code **)(puVar7 + 6) = FUN_180072480;
      *(code **)(puVar7 + 8) = FUN_1800726a0;
      *(code **)(puVar7 + 10) = FUN_180072a40;
      *(code **)(puVar7 + 0xc) = FUN_180072e20;
      *(code **)(puVar7 + 0xe) = FUN_180073440;
      *(code **)(puVar7 + 0x10) = FUN_1800735e0;
      *(undefined8 *)(puVar7 + 0x12) = 0;
      *(undefined8 *)(puVar7 + 0x14) = 0;
      *(undefined8 *)(puVar7 + 0x16) = 0;
      *(undefined8 *)(puVar7 + 0x18) = 0;
      *(undefined8 *)(puVar7 + 0x1a) = 0;
      *(undefined8 *)(puVar7 + 0x1c) = 0;
    }
    else {
      lVar6 = (-(*(ulonglong *)*puVar3 & 0x3f) & 0x3f) + *(ulonglong *)*puVar3;
      *(longlong *)(puVar7 + 4) = lVar6;
      iVar4 = FUN_1800737a0(uVar1,local_38,0,lVar6,**(undefined8 **)(param_2[4] + 8));
      *(undefined8 *)(puVar7 + 6) = 0;
      *(undefined8 *)(puVar7 + 8) = 0;
      *(undefined8 *)(puVar7 + 10) = 0;
      *(undefined8 *)(puVar7 + 0xc) = 0;
      *(undefined8 *)(puVar7 + 0xe) = 0;
      *(undefined8 *)(puVar7 + 0x10) = 0;
      *(code **)(puVar7 + 0x12) = FUN_180074180;
      *(code **)(puVar7 + 0x14) = FUN_180074520;
      *(code **)(puVar7 + 0x16) = FUN_180074ca0;
      *(code **)(puVar7 + 0x18) = FUN_1800750e0;
      *(code **)(puVar7 + 0x1a) = FUN_180075aa0;
      *(code **)(puVar7 + 0x1c) = FUN_180075ce0;
    }
    *puVar7 = 3;
    param_2[3] = puVar7;
    if (iVar4 != 0) {
      uVar5 = FUN_180075f60(iVar4);
      if ((int)uVar5 != 0) {
        return uVar5;
      }
    }
    *param_2 = FUN_18006f6a0;
    param_2[1] = FUN_18006f760;
    *(undefined4 *)((longlong)param_2 + 0x3c) = 0x1e;
    return 0;
  }
  uVar1 = *(uint *)param_2[0xe];
  local_2c = 0;
  FUN_180071360(param_2);
  **(longlong **)param_2[4] = **(longlong **)param_2[4] + 0x80;
  if ((uVar1 - 1 & uVar1) == 0) {
    iVar4 = 0x1f;
    if (uVar1 != 0) {
      for (; uVar1 >> iVar4 == 0; iVar4 = iVar4 + -1) {
      }
    }
    iVar4 = FUN_180071400(iVar4,local_2c,0,&local_38,&local_34,&local_30);
  }
  else {
    iVar4 = FUN_1800715c0(uVar1,local_2c,0,&local_38,&local_34,&local_30);
  }
  if (iVar4 == 0) {
    **(longlong **)param_2[4] =
         **(longlong **)param_2[4] + ((longlong)local_38 + 0x3fU & 0xffffffffffffffc0);
    **(longlong **)(param_2[4] + 8) =
         **(longlong **)(param_2[4] + 8) + ((longlong)local_34 + 0x3fU & 0xffffffffffffffc0);
    **(longlong **)(param_2[4] + 0x10) =
         **(longlong **)(param_2[4] + 0x10) + ((longlong)local_30 + 0x3fU & 0xffffffffffffffc0);
    return 0;
  }
  uVar5 = FUN_180075f60(iVar4);
  return uVar5;
}


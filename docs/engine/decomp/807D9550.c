// FUN_1807d9550 @ 0x1807d9550

/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void FUN_1807d9550(longlong *param_1,longlong param_2,longlong *param_3)

{
  longlong lVar1;
  longlong *plVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  longlong lVar5;
  undefined1 auStack_88 [32];
  longlong *local_68;
  longlong **local_60;
  undefined4 local_58;
  longlong *local_48;
  longlong local_40;
  int local_34;
  ulonglong local_20;
  
  local_20 = DAT_1821c7640 ^ (ulonglong)auStack_88;
  lVar1 = param_1[2];
  param_1[2] = param_1[2] + 4;
  if ((*(longlong *)(param_2 + 0x18) != 0) && (*param_1 != 0)) {
    (**(code **)(*(longlong *)*param_1 + 0x50))();
    plVar2 = *(longlong **)(param_2 + 0x18);
    if (local_34 == 2) {
      local_60 = &local_48;
      local_68 = (longlong *)((ulonglong)local_68 & 0xffffffff00000000);
      (**(code **)(*plVar2 + 0x70))(plVar2,*param_1,0,4);
      lVar5 = (longlong)(int)lVar1;
      lVar1 = param_3[1];
      local_48[lVar5 * 2] = *param_3;
      (local_48 + lVar5 * 2)[1] = lVar1;
      lVar1 = param_3[3];
      local_48[lVar5 * 2 + 2] = param_3[2];
      (local_48 + lVar5 * 2 + 2)[1] = lVar1;
      uVar3 = *(undefined4 *)((longlong)param_3 + 0x24);
      lVar1 = param_3[5];
      uVar4 = *(undefined4 *)((longlong)param_3 + 0x2c);
      plVar2 = local_48 + lVar5 * 2 + 4;
      *(int *)plVar2 = (int)param_3[4];
      *(undefined4 *)((longlong)plVar2 + 4) = uVar3;
      *(int *)(plVar2 + 1) = (int)lVar1;
      *(undefined4 *)((longlong)plVar2 + 0xc) = uVar4;
      uVar3 = *(undefined4 *)((longlong)param_3 + 0x34);
      lVar1 = param_3[7];
      uVar4 = *(undefined4 *)((longlong)param_3 + 0x3c);
      local_48 = local_48 + lVar5 * 2 + 6;
      *(int *)local_48 = (int)param_3[6];
      *(undefined4 *)((longlong)local_48 + 4) = uVar3;
      *(int *)(local_48 + 1) = (int)lVar1;
      *(undefined4 *)((longlong)local_48 + 0xc) = uVar4;
      (**(code **)(**(longlong **)(param_2 + 0x18) + 0x78))
                (*(longlong **)(param_2 + 0x18),*param_1,0);
    }
    else {
      local_58 = 0;
      local_60 = (longlong **)((ulonglong)local_60 & 0xffffffff00000000);
      local_68 = param_3;
      (**(code **)(*plVar2 + 0x180))(plVar2,*param_1,0,0);
    }
  }
  local_48 = (longlong *)*param_1;
  if (local_48 != (longlong *)0x0) {
    (**(code **)(*local_48 + 8))();
  }
  local_40 = param_1[1];
  FUN_180616080(param_2,&local_48);
}


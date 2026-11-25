// FUN_180324130 @ 0x180324130

undefined8 FUN_180324130(longlong param_1,int param_2,int param_3,uint param_4,undefined4 *param_5)

{
  undefined4 uVar1;
  longlong lVar2;
  longlong *plVar3;
  uint uVar4;
  char cVar5;
  undefined1 local_28 [16];
  
  uVar4 = 1;
  if (param_2 != 0) {
    if (param_2 == 1) {
      param_5[0x44] = 1;
    }
LAB_18032424e:
    FUN_181798f42(param_5,0,0x114);
    return 1;
  }
  if ((int)param_4 < 0) {
    return 1;
  }
  if (param_3 == 0) {
    lVar2 = *(longlong *)(param_1 + 0x38) + 0xd8;
  }
  else {
    lVar2 = *(longlong *)(param_1 + 0x38) + 0xe8;
  }
  if (*(int *)(lVar2 + 0xc) <= (int)param_4) {
    return 1;
  }
  if (param_3 == 0) {
    plVar3 = (longlong *)(*(longlong *)(param_1 + 0x38) + 0xd8);
  }
  else {
    plVar3 = (longlong *)(*(longlong *)(param_1 + 0x38) + 0xe8);
  }
  if (param_4 < *(uint *)((longlong)plVar3 + 0xc)) {
    lVar2 = *(longlong *)(*plVar3 + (longlong)(int)param_4 * 8);
  }
  else {
    lVar2 = 0;
  }
  if (lVar2 == 0) goto LAB_18032424e;
  *param_5 = 0;
  param_5[1] = param_3;
  uVar1 = FUN_18046e1a0(lVar2 + 0x60);
  param_5[2] = uVar1;
  FUN_18031a4c0(local_28,lVar2 + 0x60);
  FUN_180319500(param_5 + 3,lVar2 + 8);
  cVar5 = param_4 == 0;
  if (param_3 == 0) {
    if (!(bool)cVar5) goto LAB_180324225;
    plVar3 = (longlong *)
             (**(code **)(**(longlong **)(param_1 + 0x38) + 0x168))(*(longlong **)(param_1 + 0x38));
    if (plVar3 == (longlong *)0x0) {
      uVar4 = 0;
      goto LAB_180324225;
    }
    cVar5 = (**(code **)(*plVar3 + 0x28))(plVar3);
  }
  uVar4 = (uint)(cVar5 == '\0');
LAB_180324225:
  param_5[0x43] = uVar4;
  param_5[0x44] = (uint)(*(char *)(lVar2 + 0x88) != '\0');
  return 0;
}


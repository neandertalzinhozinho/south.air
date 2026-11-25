// FUN_1808774a0 @ 0x1808774a0

void FUN_1808774a0(undefined8 *param_1)

{
  longlong lVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined4 uVar5;
  
  if (*(char *)*param_1 == '\0') {
    uVar5 = FUN_180868730(param_1[2] + 0x5f8);
    uVar2 = param_1[5];
    uVar3 = param_1[4];
    uVar4 = param_1[3];
    *(undefined4 *)param_1[1] = uVar5;
    FUN_180881050(param_1[2] + 0x5f8,uVar4,uVar3,uVar2,param_1[6]);
    return;
  }
  lVar1 = param_1[2];
  uVar2 = param_1[5];
  uVar3 = param_1[4];
  uVar4 = param_1[3];
  *(undefined4 *)param_1[1] = 0;
  FUN_180880640(lVar1 + 0x5ed0,uVar4,uVar3,uVar2,param_1[6]);
  return;
}


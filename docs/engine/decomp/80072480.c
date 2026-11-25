// FUN_180072480 @ 0x180072480

undefined8 FUN_180072480(undefined8 param_1,float *param_2,longlong param_3,ulonglong param_4)

{
  float fVar1;
  longlong lVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  
  lVar2 = 0;
  if (param_4 == 0) {
    if (0 < *(int *)(param_3 + 0x18)) {
      return 0xfffffff8;
    }
    uVar5 = *(uint *)(param_3 + 4);
    if (4 < (int)uVar5) goto LAB_18007253d;
  }
  else {
    uVar5 = *(uint *)(param_3 + 4);
    if (4 < (int)uVar5) {
      if (0 < *(int *)(param_3 + 0x18)) {
        lVar2 = param_4 + (-(param_4 & 0x3f) & 0x3f);
      }
LAB_18007253d:
      iVar4 = 1 << (uVar5 - 1 & 0x1f);
      if ((int)uVar5 < 8) {
        if (*(int *)(param_3 + 8) == 0) {
          (**(code **)(&UNK_181dfa358 + (longlong)(int)uVar5 * 8))(param_1,param_2);
          iVar3 = 1 << (uVar5 & 0x1f);
        }
        else {
          (**(code **)(&UNK_181dfa320 + (longlong)(int)uVar5 * 8))
                    (param_1,param_2,*(undefined4 *)(param_3 + 0x10));
          iVar3 = 1 << (uVar5 & 0x1f);
        }
      }
      else if ((int)uVar5 < 0x14) {
        FUN_181d69e00(param_1,param_2,iVar4,*(undefined8 *)(param_3 + 0x38),
                      *(undefined8 *)(param_3 + 0x30),lVar2);
        iVar3 = 1 << (uVar5 & 0x1f);
        if (*(int *)(param_3 + 8) != 0) {
          FUN_180006160(*(undefined4 *)(param_3 + 0x10),param_2,iVar3);
        }
      }
      else {
        FUN_180088300(param_3,param_1,param_2,uVar5 - 1,lVar2);
        iVar3 = 1 << (uVar5 & 0x1f);
      }
      fVar1 = *param_2;
      *param_2 = param_2[1] + fVar1;
      param_2[1] = fVar1 - param_2[1];
      FUN_1800895c0(param_2,iVar4,1,*(undefined8 *)(param_3 + 0x50));
      lVar2 = (longlong)iVar3;
      if (lVar2 == 1) {
        param_2[1] = 0.0;
      }
      else {
        param_2[lVar2] = param_2[1];
        param_2[lVar2 + 1] = 0.0;
        param_2[1] = 0.0;
      }
      return 0;
    }
  }
  if (*(int *)(param_3 + 8) == 0) {
    (**(code **)(&UNK_181dfa2f8 + (longlong)(int)uVar5 * 8))(param_1,param_2);
  }
  else {
    (**(code **)(&UNK_181dfa2c8 + (longlong)(int)uVar5 * 8))
              (param_1,param_2,*(undefined4 *)(param_3 + 0x10));
  }
  lVar2 = (longlong)(1 << (uVar5 & 0x1f));
  if (lVar2 != 1) {
    param_2[lVar2] = param_2[1];
    param_2[lVar2 + 1] = 0.0;
  }
  param_2[1] = 0.0;
  return 0;
}


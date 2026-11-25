// FUN_1800020e0 @ 0x1800020e0

undefined8 FUN_1800020e0(longlong param_1,longlong param_2,int *param_3)

{
  int *piVar1;
  int iVar2;
  ulonglong uVar3;
  undefined8 uVar4;
  
  if (param_3 != (int *)0x0) {
    if (*param_3 != 7) {
      return 0xfffffff3;
    }
    if ((param_1 != 0) && (param_2 != 0)) {
      piVar1 = (int *)(*(undefined8 **)(param_3 + 2))[3];
      if ((piVar1 != (int *)0x0) && (*piVar1 == 3)) {
        uVar4 = (**(code **)(piVar1 + 6))(param_1,param_2,*(undefined8 *)(piVar1 + 2));
        return uVar4;
      }
      iVar2 = (*(code *)**(undefined8 **)(param_3 + 2))();
      uVar3 = (ulonglong)iVar2;
      if (uVar3 == 0) {
        return 0;
      }
      if (uVar3 != 7) {
        if (((uVar3 & 0xfffffffffffffffd) == 1) || (uVar3 == 5)) {
          return 0xfffffff8;
        }
        if (uVar3 == 2) {
          return 0xfffffff3;
        }
        if (uVar3 == 0) {
          return 0;
        }
        if (uVar3 - 100 < 3) {
          return 0;
        }
      }
      return 0xfffffffe;
    }
  }
  return 0xfffffff8;
}


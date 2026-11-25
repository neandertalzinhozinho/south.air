// FUN_18087a680 @ 0x18087a680

void FUN_18087a680(longlong *param_1)

{
  longlong lVar1;
  int iVar2;
  longlong lVar3;
  double dVar4;
  double dVar5;
  ulonglong uVar6;
  longlong lVar7;
  double dVar8;
  double dVar9;
  
  dVar4 = DAT_18207a138;
  lVar1 = *param_1;
  iVar2 = (int)param_1[1];
  lVar7 = 0;
  uVar6 = 0;
  dVar9 = DAT_18207a138 / (double)iVar2;
  if (iVar2 != 0) {
    do {
      *(float *)(lVar1 + uVar6 * 4) = (float)((double)uVar6 * dVar9);
      uVar6 = uVar6 + 1;
    } while (uVar6 < (ulonglong)(longlong)iVar2);
  }
  dVar5 = DAT_18207a1e0;
  dVar9 = DAT_18207a0b8;
  lVar3 = param_1[1];
  lVar1 = *param_1;
  if (0 < (longlong)(int)lVar3) {
    do {
      dVar8 = (double)FUN_181c9a9c5((double)*(float *)(lVar1 + lVar7 * 4) * dVar5);
      dVar8 = (dVar4 - dVar8) * dVar9;
      if (dVar8 <= 0.0) {
        dVar8 = 0.0;
      }
      *(float *)(lVar1 + lVar7 * 4) = (float)dVar8;
      lVar7 = lVar7 + 1;
    } while (lVar7 < (int)lVar3);
  }
  return;
}


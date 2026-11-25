// FUN_18087a370 @ 0x18087a370

void FUN_18087a370(longlong *param_1,undefined8 param_2,float param_3)

{
  int iVar1;
  longlong lVar2;
  double dVar3;
  double dVar4;
  ulonglong uVar5;
  longlong lVar6;
  longlong *plVar7;
  float fVar8;
  double dVar9;
  double dVar10;
  longlong alStack_e0 [4];
  longlong lStack_c0;
  longlong local_b8;
  longlong lStack_b0;
  longlong local_a8;
  longlong lStack_a0;
  longlong local_98;
  longlong lStack_90;
  longlong local_88;
  longlong lStack_80;
  longlong local_78;
  longlong lStack_70;
  int local_68;
  int iStack_64;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  
  dVar3 = DAT_18207a138;
  lVar6 = 0;
  lVar2 = *param_1;
  uVar5 = 0;
  alStack_e0[1] = param_1[2];
  alStack_e0[2] = param_1[3];
  local_b8 = param_1[6];
  lStack_b0 = param_1[7];
  local_98 = param_1[10];
  lStack_90 = param_1[0xb];
  alStack_e0[3] = param_1[4];
  lStack_c0 = param_1[5];
  local_a8 = param_1[8];
  lStack_a0 = param_1[9];
  local_68 = (int)param_1[0x10];
  iVar1 = *(int *)((longlong)param_1 + 0x84);
  alStack_e0[0] = param_1[1];
  local_78 = param_1[0xe];
  lStack_70 = param_1[0xf];
  fVar8 = DAT_182079f9c - param_3;
  local_88 = param_1[0xc];
  lStack_80 = param_1[0xd];
  iStack_64 = iVar1;
  uStack_60 = (int)param_1[0x11];
  uStack_5c = *(undefined4 *)((longlong)param_1 + 0x8c);
  dVar10 = DAT_18207a138 / (double)iVar1;
  if (iVar1 != 0) {
    do {
      *(float *)(lVar2 + uVar5 * 4) =
           (float)((double)uVar5 * dVar10 * (double)fVar8 + (double)param_3);
      uVar5 = uVar5 + 1;
    } while (uVar5 < (ulonglong)(longlong)iVar1);
  }
  if (1 < local_68) {
    plVar7 = alStack_e0;
    uVar5 = (ulonglong)(local_68 - 1);
    do {
      FUN_1800010a0(lVar2,*plVar7,iVar1);
      plVar7 = plVar7 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  dVar4 = DAT_18207a1e0;
  dVar10 = DAT_18207a0b8;
  iVar1 = *(int *)((longlong)param_1 + 0x84);
  lVar2 = *param_1;
  if (0 < (longlong)iVar1) {
    do {
      dVar9 = (double)FUN_181c9a9c5((double)*(float *)(lVar2 + lVar6 * 4) * dVar4);
      dVar9 = (dVar3 - dVar9) * dVar10;
      if (dVar9 <= 0.0) {
        dVar9 = 0.0;
      }
      *(float *)(lVar2 + lVar6 * 4) = (float)dVar9;
      lVar6 = lVar6 + 1;
    } while (lVar6 < iVar1);
  }
  return;
}


// FUN_180009ba0 @ 0x180009ba0

undefined8 FUN_180009ba0(longlong param_1,ulonglong param_2,uint param_3)

{
  float *pfVar1;
  longlong lVar2;
  float *pfVar3;
  float *pfVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  float fVar26;
  float fVar27;
  float fVar28;
  float fVar29;
  float fVar30;
  float fVar31;
  float fVar32;
  float fVar33;
  float fVar34;
  int iVar35;
  longlong lVar36;
  ulonglong uVar37;
  ulonglong uVar38;
  uint uVar39;
  ulonglong uVar40;
  
  if ((param_1 == 0) || (param_2 == 0)) {
    return 0xfffffff8;
  }
  if ((int)param_3 < 1) {
    return 0xfffffffa;
  }
  if (0xf < (int)param_3) {
    uVar39 = (uint)param_2 & 0x1f;
    if ((param_2 & 0x1f) != 0) {
      if ((param_2 & 3) != 0) goto LAB_180009d22;
      uVar39 = 0x20 - uVar39 >> 2;
    }
    if ((int)(uVar39 + 0x10) <= (int)param_3) {
      uVar37 = 0;
      iVar35 = param_3 - (param_3 - uVar39 & 0xf);
      uVar38 = (ulonglong)uVar39;
      if (uVar39 != 0) {
        do {
          *(float *)(param_2 + uVar37 * 4) =
               *(float *)(param_1 + uVar37 * 4) * *(float *)(param_2 + uVar37 * 4);
          uVar37 = uVar37 + 1;
        } while (uVar37 < uVar38);
      }
      do {
        pfVar1 = (float *)(param_1 + uVar38 * 4);
        fVar5 = pfVar1[1];
        fVar6 = pfVar1[2];
        fVar7 = pfVar1[3];
        fVar8 = pfVar1[4];
        fVar9 = pfVar1[5];
        fVar10 = pfVar1[6];
        fVar11 = pfVar1[7];
        pfVar3 = (float *)(param_1 + 0x20 + uVar38 * 4);
        fVar12 = *pfVar3;
        fVar13 = pfVar3[1];
        fVar14 = pfVar3[2];
        fVar15 = pfVar3[3];
        fVar16 = pfVar3[4];
        fVar17 = pfVar3[5];
        fVar18 = pfVar3[6];
        fVar19 = pfVar3[7];
        pfVar3 = (float *)(param_2 + uVar38 * 4);
        fVar20 = pfVar3[1];
        fVar21 = pfVar3[2];
        fVar22 = pfVar3[3];
        fVar23 = pfVar3[4];
        fVar24 = pfVar3[5];
        fVar25 = pfVar3[6];
        fVar26 = pfVar3[7];
        pfVar4 = (float *)(param_2 + 0x20 + uVar38 * 4);
        fVar27 = *pfVar4;
        fVar28 = pfVar4[1];
        fVar29 = pfVar4[2];
        fVar30 = pfVar4[3];
        fVar31 = pfVar4[4];
        fVar32 = pfVar4[5];
        fVar33 = pfVar4[6];
        fVar34 = pfVar4[7];
        pfVar4 = (float *)(param_2 + uVar38 * 4);
        *pfVar4 = *pfVar1 * *pfVar3;
        pfVar4[1] = fVar5 * fVar20;
        pfVar4[2] = fVar6 * fVar21;
        pfVar4[3] = fVar7 * fVar22;
        pfVar4[4] = fVar8 * fVar23;
        pfVar4[5] = fVar9 * fVar24;
        pfVar4[6] = fVar10 * fVar25;
        pfVar4[7] = fVar11 * fVar26;
        pfVar1 = (float *)(param_2 + 0x20 + uVar38 * 4);
        *pfVar1 = fVar12 * fVar27;
        pfVar1[1] = fVar13 * fVar28;
        pfVar1[2] = fVar14 * fVar29;
        pfVar1[3] = fVar15 * fVar30;
        pfVar1[4] = fVar16 * fVar31;
        pfVar1[5] = fVar17 * fVar32;
        pfVar1[6] = fVar18 * fVar33;
        pfVar1[7] = fVar19 * fVar34;
        uVar38 = uVar38 + 0x10;
      } while (uVar38 < (ulonglong)(longlong)iVar35);
      goto LAB_180009c70;
    }
  }
LAB_180009d22:
  iVar35 = 0;
LAB_180009c70:
  if (iVar35 + 1U <= param_3) {
    lVar36 = (longlong)iVar35;
    uVar37 = (int)param_3 - lVar36;
    if ((longlong)uVar37 < 4) {
      uVar38 = 0;
    }
    else {
      uVar40 = 0;
      lVar2 = param_2 + lVar36 * 4;
      uVar38 = (ulonglong)(int)((uint)uVar37 & 0xfffffffc);
      do {
        pfVar1 = (float *)(param_1 + lVar36 * 4 + uVar40 * 4);
        fVar5 = pfVar1[1];
        fVar6 = pfVar1[2];
        fVar7 = pfVar1[3];
        pfVar3 = (float *)(lVar2 + uVar40 * 4);
        fVar8 = pfVar3[1];
        fVar9 = pfVar3[2];
        fVar10 = pfVar3[3];
        pfVar4 = (float *)(lVar2 + uVar40 * 4);
        *pfVar4 = *pfVar1 * *pfVar3;
        pfVar4[1] = fVar5 * fVar8;
        pfVar4[2] = fVar6 * fVar9;
        pfVar4[3] = fVar7 * fVar10;
        uVar40 = uVar40 + 4;
      } while (uVar40 < uVar38);
    }
    if (uVar38 < uVar37) {
      lVar2 = param_2 + lVar36 * 4;
      do {
        *(float *)(lVar2 + uVar38 * 4) =
             *(float *)(param_1 + lVar36 * 4 + uVar38 * 4) * *(float *)(lVar2 + uVar38 * 4);
        uVar38 = uVar38 + 1;
      } while (uVar38 < uVar37);
    }
  }
  return 0;
}


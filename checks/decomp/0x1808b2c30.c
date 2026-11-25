 (GhidraScript)  

float FUN_1808b2c30(longlong param_1,float param_2,float *param_3)

{
  longlong lVar1;
  float *pfVar2;
  float *pfVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  ulonglong uVar14;
  float *pfVar15;
  longlong lVar16;
  ulonglong uVar17;
  longlong lVar18;
  ulonglong uVar19;
  longlong lVar20;
  ulonglong uVar21;
  
  uVar21 = 0;
  fVar4 = *param_3;
  uVar19 = 0;
  fVar5 = *(float *)(param_1 + *(longlong *)(param_1 + 0x80) * 4);
  *(undefined4 *)(param_1 + *(longlong *)(param_1 + 0x80) * 4) = 0;
  lVar20 = *(longlong *)(param_1 + 0x80);
  uVar17 = -lVar20 + 0x1f;
  lVar1 = param_1 + (*(longlong *)(param_1 + 0x80) + 1) * 4;
  if ((uVar17 & 0xfffffffffffffffc) != 0) {
    pfVar15 = (float *)(lVar1 + 4);
    lVar18 = (longlong)param_3 + (4 - lVar1);
2) + 1;
    uVar19 = lVar16 * 4;
    do {
      fVar6 = *(float *)(lVar18 + (longlong)pfVar15);
      pfVar15[-1] = param_2 * *(float *)(lVar18 + -4 + (longlong)pfVar15) + pfVar15[-1];
      fVar7 = *(float *)((longlong)param_3 + (8 - lVar1) + (longlong)pfVar15);
      *pfVar15 = param_2 * fVar6 + *pfVar15;
      fVar6 = *(float *)((longlong)pfVar15 + (longlong)param_3 + (0xc - lVar1));
      pfVar15[1] = param_2 * fVar7 + pfVar15[1];
      pfVar15[2] = param_2 * fVar6 + pfVar15[2];
      pfVar15 = pfVar15 + 4;
      lVar16 = lVar16 + -1;
    } while (lVar16 != 0);
  }
  uVar14 = uVar17 - uVar19;
  if (uVar19 < uVar17) {
    if (0xf < uVar14) {
      pfVar15 = (float *)(lVar1 + 0x10 + uVar19 * 4);
      lVar16 = (longlong)param_3 + (4 - lVar1);
      do {
        uVar19 = uVar19 + 0x10;
        pfVar3 = (float *)(lVar16 + -0x10 + (longlong)pfVar15);
        fVar6 = pfVar3[1];
        fVar7 = pfVar3[2];
        fVar8 = pfVar3[3];
        pfVar2 = (float *)((longlong)pfVar15 + lVar16);
        fVar9 = *pfVar2;
        fVar10 = pfVar2[1];
        fVar11 = pfVar2[2];
        fVar12 = pfVar2[3];
        pfVar15[-4] = *pfVar3 * param_2 + pfVar15[-4];
        pfVar15[-3] = fVar6 * param_2 + pfVar15[-3];
        pfVar15[-2] = fVar7 * param_2 + pfVar15[-2];
        pfVar15[-1] = fVar8 * param_2 + pfVar15[-1];
        pfVar2 = (float *)((longlong)param_3 + (0x14 - lVar1) + (longlong)pfVar15);
        fVar6 = *pfVar2;
        fVar7 = pfVar2[1];
        fVar8 = pfVar2[2];
        fVar13 = pfVar2[3];
        *pfVar15 = fVar9 * param_2 + *pfVar15;
        pfVar15[1] = fVar10 * param_2 + pfVar15[1];
        pfVar15[2] = fVar11 * param_2 + pfVar15[2];
        pfVar15[3] = fVar12 * param_2 + pfVar15[3];
        pfVar2 = (float *)((longlong)pfVar15 + (longlong)param_3 + (0x24 - lVar1));
        fVar9 = *pfVar2;
        fVar10 = pfVar2[1];
        fVar11 = pfVar2[2];
        fVar12 = pfVar2[3];
        pfVar15[4] = fVar6 * param_2 + pfVar15[4];
        pfVar15[5] = fVar7 * param_2 + pfVar15[5];
        pfVar15[6] = fVar8 * param_2 + pfVar15[6];
        pfVar15[7] = fVar13 * param_2 + pfVar15[7];
        pfVar15[8] = fVar9 * param_2 + pfVar15[8];
        pfVar15[9] = fVar10 * param_2 + pfVar15[9];
        pfVar15[10] = fVar11 * param_2 + pfVar15[10];
        pfVar15[0xb] = fVar12 * param_2 + pfVar15[0xb];
        pfVar15 = pfVar15 + 0x10;
      } while (uVar19 < uVar17 - ((uint)uVar14 & 0xf));
    }
    if (uVar19 < uVar17) {
      if (3 < uVar17 - uVar19) {
        pfVar15 = (float *)(lVar1 + 4 + uVar19 * 4);
        lVar18 = (longlong)param_3 + (4 - lVar1);
2) + 1;
        uVar19 = uVar19 + lVar16 * 4;
        do {
          fVar6 = *(float *)((longlong)pfVar15 + lVar18);
          pfVar15[-1] = param_2 * *(float *)((longlong)pfVar15 + lVar18 + -4) + pfVar15[-1];
          fVar7 = *(float *)((longlong)pfVar15 + (longlong)param_3 + (8 - lVar1));
          *pfVar15 = param_2 * fVar6 + *pfVar15;
          fVar6 = *(float *)((longlong)pfVar15 + (longlong)param_3 + (0xc - lVar1));
          pfVar15[1] = param_2 * fVar7 + pfVar15[1];
          pfVar15[2] = param_2 * fVar6 + pfVar15[2];
          pfVar15 = pfVar15 + 4;
          lVar16 = lVar16 + -1;
        } while (lVar16 != 0);
      }
      if (uVar19 < uVar17) {
        pfVar15 = (float *)(lVar1 + uVar19 * 4);
        lVar16 = uVar17 - uVar19;
        do {
          *pfVar15 = param_2 * *(float *)((longlong)pfVar15 + (longlong)param_3 + (4 - lVar1)) +
                     *pfVar15;
          pfVar15 = pfVar15 + 1;
          lVar16 = lVar16 + -1;
        } while (lVar16 != 0);
      }
    }
  }
  if (*(longlong *)(param_1 + 0x80) != 0) {
    uVar19 = *(ulonglong *)(param_1 + 0x80);
    lVar1 = -lVar20 + 0x20;
    if ((uVar19 & 0xfffffffffffffffc) != 0) {
      pfVar15 = (float *)(param_1 + 4);
      lVar16 = (longlong)param_3 + (lVar1 * 4 - param_1);
2) + 1;
      uVar21 = lVar20 * 4;
      do {
        pfVar15[-1] = param_2 * *(float *)(lVar16 + -4 + (longlong)pfVar15) + pfVar15[-1];
        *pfVar15 = param_2 * *(float *)(lVar16 + (longlong)pfVar15) + *pfVar15;
        pfVar15[1] = param_2 * *(float *)((longlong)param_3 + (lVar1 * 4 - param_1) + 4 +
                                         (longlong)pfVar15) + pfVar15[1];
        pfVar15[2] = param_2 * *(float *)((longlong)param_3 + (lVar1 * 4 - param_1) + 8 +
                                         (longlong)pfVar15) + pfVar15[2];
        pfVar15 = pfVar15 + 4;
        lVar20 = lVar20 + -1;
      } while (lVar20 != 0);
    }
    uVar17 = uVar19 - uVar21;
    if (uVar21 < uVar19) {
      if (0xf < uVar17) {
        pfVar15 = (float *)(param_1 + 0x10 + uVar21 * 4);
        lVar20 = (longlong)param_3 + (lVar1 * 4 - param_1);
        do {
          uVar21 = uVar21 + 0x10;
          pfVar2 = (float *)(lVar20 + -0x10 + (longlong)pfVar15);
          fVar6 = pfVar2[1];
          fVar7 = pfVar2[2];
          fVar8 = pfVar2[3];
          pfVar15[-4] = *pfVar2 * param_2 + pfVar15[-4];
          pfVar15[-3] = fVar6 * param_2 + pfVar15[-3];
          pfVar15[-2] = fVar7 * param_2 + pfVar15[-2];
          pfVar15[-1] = fVar8 * param_2 + pfVar15[-1];
          pfVar2 = (float *)((longlong)pfVar15 + lVar20);
          fVar6 = pfVar2[1];
          fVar7 = pfVar2[2];
          fVar8 = pfVar2[3];
          *pfVar15 = *pfVar2 * param_2 + *pfVar15;
          pfVar15[1] = fVar6 * param_2 + pfVar15[1];
          pfVar15[2] = fVar7 * param_2 + pfVar15[2];
          pfVar15[3] = fVar8 * param_2 + pfVar15[3];
          pfVar2 = (float *)((longlong)param_3 + (lVar1 * 4 - param_1) + 0x10 + (longlong)pfVar15);
          fVar6 = pfVar2[1];
          fVar7 = pfVar2[2];
          fVar8 = pfVar2[3];
          pfVar15[4] = *pfVar2 * param_2 + pfVar15[4];
          pfVar15[5] = fVar6 * param_2 + pfVar15[5];
          pfVar15[6] = fVar7 * param_2 + pfVar15[6];
          pfVar15[7] = fVar8 * param_2 + pfVar15[7];
          pfVar2 = (float *)((longlong)param_3 + (lVar1 * 4 - param_1) + 0x20 + (longlong)pfVar15);
          fVar6 = pfVar2[1];
          fVar7 = pfVar2[2];
          fVar8 = pfVar2[3];
          pfVar15[8] = *pfVar2 * param_2 + pfVar15[8];
          pfVar15[9] = fVar6 * param_2 + pfVar15[9];
          pfVar15[10] = fVar7 * param_2 + pfVar15[10];
          pfVar15[0xb] = fVar8 * param_2 + pfVar15[0xb];
          pfVar15 = pfVar15 + 0x10;
        } while (uVar21 < uVar19 - ((uint)uVar17 & 0xf));
      }
      if (uVar21 < uVar19) {
        if (3 < uVar19 - uVar21) {
          pfVar15 = (float *)(param_1 + 4 + uVar21 * 4);
          lVar16 = (longlong)param_3 + (lVar1 * 4 - param_1);
2) + 1;
          uVar21 = uVar21 + lVar20 * 4;
          do {
            pfVar15[-1] = param_2 * *(float *)(lVar16 + -4 + (longlong)pfVar15) + pfVar15[-1];
            *pfVar15 = param_2 * *(float *)(lVar16 + (longlong)pfVar15) + *pfVar15;
            pfVar15[1] = param_2 * *(float *)((longlong)param_3 + (lVar1 * 4 - param_1) + 4 +
                                             (longlong)pfVar15) + pfVar15[1];
            pfVar15[2] = param_2 * *(float *)((longlong)param_3 + (lVar1 * 4 - param_1) + 8 +
                                             (longlong)pfVar15) + pfVar15[2];
            pfVar15 = pfVar15 + 4;
            lVar20 = lVar20 + -1;
          } while (lVar20 != 0);
        }
        if (uVar21 < uVar19) {
          pfVar15 = (float *)(param_1 + uVar21 * 4);
          lVar20 = uVar19 - uVar21;
          do {
            *pfVar15 = param_2 * *(float *)((longlong)pfVar15 +
                                           (longlong)param_3 + (lVar1 * 4 - param_1)) + *pfVar15;
            pfVar15 = pfVar15 + 1;
            lVar20 = lVar20 + -1;
          } while (lVar20 != 0);
        }
      }
    }
  }
  *(ulonglong *)(param_1 + 0x80) = (ulonglong)((int)*(undefined8 *)(param_1 + 0x80) + 1U & 0x1f);
  return param_2 * fVar4 + fVar5;
}

 (GhidraScript)  

// FUN_1808615d0 @ 0x1808615d0

void FUN_1808615d0(int *param_1,float *param_2,float *param_3)

{
  float *pfVar1;
  float *pfVar2;
  float *pfVar3;
  float *pfVar4;
  float *pfVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  int iVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float *pfVar19;
  float *pfVar20;
  float *pfVar21;
  float fVar22;
  float fVar23;
  int iVar24;
  float *pfVar25;
  uint uVar26;
  float *pfVar27;
  int iVar28;
  int iVar29;
  float *pfVar30;
  float *pfVar31;
  float *pfVar32;
  ulonglong uVar33;
  float fVar34;
  float fVar35;
  float fVar36;
  float fVar37;
  float fVar38;
  float fVar39;
  float fVar40;
  
  fVar40 = *param_3;
  iVar29 = 0;
  iVar10 = *param_1;
  pfVar25 = *(float **)(param_1 + 4);
  iVar24 = (int)(iVar10 + (iVar10 >> 0x1f & 3U)) >> 2;
  iVar28 = 0;
  pfVar30 = param_3;
  pfVar31 = pfVar25;
  pfVar32 = param_2;
  if (3 < iVar24) {
    uVar26 = (iVar24 - 4U >> 2) + 1;
    uVar33 = (ulonglong)uVar26;
    iVar28 = uVar26 * 4;
    do {
      fVar6 = *pfVar30;
      fVar7 = pfVar30[1];
      fVar8 = pfVar30[3];
      fVar11 = pfVar31[1];
      fVar12 = pfVar31[2];
      fVar13 = pfVar31[0x11];
      fVar14 = pfVar31[0x12];
      fVar15 = pfVar31[5];
      fVar16 = pfVar31[6];
      fVar17 = pfVar31[9];
      fVar18 = pfVar31[10];
      fVar9 = pfVar30[2];
      fVar34 = pfVar31[0xd];
      fVar39 = pfVar31[0xe];
      fVar37 = fVar6 * pfVar31[7] + fVar40 * pfVar31[3] + fVar7 * pfVar31[0xb] +
               fVar8 * pfVar31[0x13] + fVar9 * pfVar31[0xf];
      *pfVar32 = fVar6 * pfVar31[4] + fVar40 * *pfVar31 + fVar7 * pfVar31[8] +
                 fVar8 * pfVar31[0x10] + fVar9 * pfVar31[0xc];
      pfVar32[1] = fVar6 * fVar15 + fVar40 * fVar11 + fVar7 * fVar17 +
                   fVar8 * fVar13 + fVar9 * fVar34;
      pfVar32[2] = fVar6 * fVar16 + fVar40 * fVar12 + fVar7 * fVar18 +
                   fVar8 * fVar14 + fVar9 * fVar39;
      pfVar32[3] = fVar37;
      fVar40 = pfVar30[4];
      fVar6 = pfVar30[5];
      fVar7 = pfVar30[7];
      fVar9 = pfVar31[0x19];
      fVar11 = pfVar31[0x1a];
      fVar12 = pfVar31[0x25];
      fVar13 = pfVar31[0x26];
      fVar14 = pfVar31[0x1d];
      fVar15 = pfVar31[0x1e];
      fVar16 = pfVar31[0x15];
      fVar17 = pfVar31[0x16];
      fVar8 = pfVar30[6];
      fVar18 = pfVar31[0x21];
      fVar34 = pfVar31[0x22];
      fVar39 = fVar40 * pfVar31[0x1b] + fVar37 * pfVar31[0x17] + fVar6 * pfVar31[0x1f] +
               fVar7 * pfVar31[0x27] + fVar8 * pfVar31[0x23];
      pfVar27 = (float *)((longlong)param_2 + (0x10 - (longlong)param_3) + (longlong)pfVar30);
      *pfVar27 = fVar40 * pfVar31[0x18] + fVar37 * pfVar31[0x14] + fVar6 * pfVar31[0x1c] +
                 fVar7 * pfVar31[0x24] + fVar8 * pfVar31[0x20];
      pfVar27[1] = fVar40 * fVar9 + fVar37 * fVar16 + fVar6 * fVar14 +
                   fVar7 * fVar12 + fVar8 * fVar18;
      pfVar27[2] = fVar40 * fVar11 + fVar37 * fVar17 + fVar6 * fVar15 +
                   fVar7 * fVar13 + fVar8 * fVar34;
      pfVar27[3] = fVar39;
      fVar40 = pfVar30[8];
      fVar6 = pfVar30[9];
      fVar7 = pfVar30[0xb];
      fVar9 = pfVar31[0x39];
      fVar11 = pfVar31[0x3a];
      fVar12 = pfVar31[0x29];
      fVar13 = pfVar31[0x2a];
      fVar14 = pfVar31[0x2d];
      fVar15 = pfVar31[0x2e];
      fVar16 = pfVar31[0x31];
      fVar17 = pfVar31[0x32];
      fVar8 = pfVar30[10];
      fVar18 = pfVar31[0x35];
      fVar34 = pfVar31[0x36];
      fVar37 = fVar40 * pfVar31[0x2f] + fVar39 * pfVar31[0x2b] + fVar6 * pfVar31[0x33] +
               fVar7 * pfVar31[0x3b] + fVar8 * pfVar31[0x37];
      pfVar27 = (float *)((longlong)param_2 + (0x20 - (longlong)param_3) + (longlong)pfVar30);
      *pfVar27 = fVar40 * pfVar31[0x2c] + fVar39 * pfVar31[0x28] + fVar6 * pfVar31[0x30] +
                 fVar7 * pfVar31[0x38] + fVar8 * pfVar31[0x34];
      pfVar27[1] = fVar40 * fVar14 + fVar39 * fVar12 + fVar6 * fVar16 +
                   fVar7 * fVar9 + fVar8 * fVar18;
      pfVar27[2] = fVar40 * fVar15 + fVar39 * fVar13 + fVar6 * fVar17 +
                   fVar7 * fVar11 + fVar8 * fVar34;
      pfVar27[3] = fVar37;
      fVar6 = pfVar30[0xc];
      fVar7 = pfVar30[0xd];
      fVar8 = pfVar30[0xf];
      pfVar27 = pfVar31 + 0x40;
      fVar11 = pfVar31[0x41];
      fVar12 = pfVar31[0x42];
      pfVar1 = pfVar31 + 0x4c;
      fVar13 = pfVar31[0x4d];
      fVar14 = pfVar31[0x4e];
      pfVar2 = pfVar31 + 0x44;
      fVar15 = pfVar31[0x45];
      fVar16 = pfVar31[0x46];
      pfVar3 = pfVar31 + 0x3c;
      fVar17 = pfVar31[0x3d];
      fVar18 = pfVar31[0x3e];
      fVar9 = pfVar30[0xe];
      pfVar4 = pfVar31 + 0x48;
      fVar34 = pfVar31[0x49];
      fVar39 = pfVar31[0x4a];
      fVar40 = fVar6 * pfVar31[0x43] + fVar37 * pfVar31[0x3f] + fVar7 * pfVar31[0x47] +
               fVar8 * pfVar31[0x4f] + fVar9 * pfVar31[0x4b];
      pfVar32 = pfVar32 + 0x10;
      pfVar31 = pfVar31 + 0x50;
      pfVar5 = (float *)((longlong)param_2 + (0x30 - (longlong)param_3) + (longlong)pfVar30);
      *pfVar5 = fVar6 * *pfVar27 + fVar37 * *pfVar3 + fVar7 * *pfVar2 +
                fVar8 * *pfVar1 + fVar9 * *pfVar4;
      pfVar5[1] = fVar6 * fVar11 + fVar37 * fVar17 + fVar7 * fVar15 +
                  fVar8 * fVar13 + fVar9 * fVar34;
      pfVar5[2] = fVar6 * fVar12 + fVar37 * fVar18 + fVar7 * fVar16 +
                  fVar8 * fVar14 + fVar9 * fVar39;
      pfVar5[3] = fVar40;
      pfVar30 = pfVar30 + 0x10;
      uVar33 = uVar33 - 1;
    } while (uVar33 != 0);
  }
  if (iVar28 < iVar24) {
    uVar33 = (ulonglong)(uint)(iVar24 - iVar28);
    do {
      fVar6 = *pfVar30;
      fVar7 = pfVar30[1];
      fVar8 = pfVar30[3];
      pfVar27 = pfVar31 + 4;
      fVar11 = pfVar31[5];
      fVar12 = pfVar31[6];
      pfVar4 = pfVar31 + 7;
      pfVar5 = pfVar31 + 3;
      fVar34 = fVar40 * *pfVar31;
      fVar39 = fVar40 * pfVar31[1];
      fVar37 = fVar40 * pfVar31[2];
      pfVar1 = pfVar31 + 0x10;
      fVar13 = pfVar31[0x11];
      fVar14 = pfVar31[0x12];
      pfVar19 = pfVar31 + 0x13;
      fVar9 = pfVar30[2];
      pfVar30 = pfVar30 + 4;
      pfVar2 = pfVar31 + 8;
      fVar15 = pfVar31[9];
      fVar16 = pfVar31[10];
      pfVar20 = pfVar31 + 0xb;
      pfVar3 = pfVar31 + 0xc;
      fVar17 = pfVar31[0xd];
      fVar18 = pfVar31[0xe];
      pfVar21 = pfVar31 + 0xf;
      pfVar31 = pfVar31 + 0x14;
      fVar40 = fVar6 * *pfVar4 + fVar40 * *pfVar5 + fVar7 * *pfVar20 +
               fVar8 * *pfVar19 + fVar9 * *pfVar21;
      *pfVar32 = fVar6 * *pfVar27 + fVar34 + fVar7 * *pfVar2 + fVar8 * *pfVar1 + fVar9 * *pfVar3;
      pfVar32[1] = fVar6 * fVar11 + fVar39 + fVar7 * fVar15 + fVar8 * fVar13 + fVar9 * fVar17;
      pfVar32[2] = fVar6 * fVar12 + fVar37 + fVar7 * fVar16 + fVar8 * fVar14 + fVar9 * fVar18;
      pfVar32[3] = fVar40;
      pfVar32 = pfVar32 + 4;
      uVar33 = uVar33 - 1;
    } while (uVar33 != 0);
  }
  pfVar27 = param_2 + (longlong)iVar10 + -5;
  pfVar25 = pfVar25 + ((longlong)iVar24 + 1) * 0x14;
  *pfVar32 = *pfVar30 * pfVar31[4] + fVar40 * *pfVar31;
  fVar40 = param_2[iVar10 + -1];
  if (3 < iVar24) {
    uVar26 = (iVar24 - 4U >> 2) + 1;
    uVar33 = (ulonglong)uVar26;
    iVar29 = uVar26 * 4;
    do {
      fVar6 = pfVar27[3];
      fVar7 = pfVar27[2];
      fVar8 = pfVar27[1];
      fVar11 = pfVar25[1];
      fVar12 = pfVar25[2];
      fVar13 = pfVar25[3];
      fVar14 = pfVar25[0xd];
      fVar15 = pfVar25[0xe];
      fVar16 = pfVar25[0xf];
      fVar17 = pfVar25[5];
      fVar18 = pfVar25[6];
      fVar34 = pfVar25[7];
      fVar39 = pfVar25[9];
      fVar37 = pfVar25[10];
      fVar22 = pfVar25[0xb];
      fVar9 = *pfVar27;
      fVar23 = pfVar25[0x11];
      fVar35 = pfVar25[0x12];
      fVar38 = pfVar25[0x13];
      fVar36 = fVar6 * pfVar25[4] + fVar40 * *pfVar25 + fVar7 * pfVar25[8] +
               fVar8 * pfVar25[0xc] + fVar9 * pfVar25[0x10];
      *pfVar27 = fVar36;
      pfVar27[1] = fVar6 * fVar17 + fVar40 * fVar11 + fVar7 * fVar39 +
                   fVar8 * fVar14 + fVar9 * fVar23;
      pfVar27[2] = fVar6 * fVar18 + fVar40 * fVar12 + fVar7 * fVar37 +
                   fVar8 * fVar15 + fVar9 * fVar35;
      pfVar27[3] = fVar6 * fVar34 + fVar40 * fVar13 + fVar7 * fVar22 +
                   fVar8 * fVar16 + fVar9 * fVar38;
      fVar40 = pfVar27[-1];
      fVar6 = pfVar27[-2];
      fVar7 = pfVar27[-4];
      fVar9 = pfVar25[0x19];
      fVar11 = pfVar25[0x1a];
      fVar12 = pfVar25[0x1b];
      fVar13 = pfVar25[0x25];
      fVar14 = pfVar25[0x26];
      fVar15 = pfVar25[0x27];
      fVar16 = pfVar25[0x1d];
      fVar17 = pfVar25[0x1e];
      fVar18 = pfVar25[0x1f];
      fVar34 = pfVar25[0x15];
      fVar39 = pfVar25[0x16];
      fVar37 = pfVar25[0x17];
      fVar8 = pfVar27[-3];
      fVar22 = pfVar25[0x21];
      fVar23 = pfVar25[0x22];
      fVar35 = pfVar25[0x23];
      fVar38 = fVar40 * pfVar25[0x18] + fVar36 * pfVar25[0x14] + fVar6 * pfVar25[0x1c] +
               fVar7 * pfVar25[0x24] + fVar8 * pfVar25[0x20];
      pfVar27[-4] = fVar38;
      pfVar27[-3] = fVar40 * fVar9 + fVar36 * fVar34 + fVar6 * fVar16 +
                    fVar7 * fVar13 + fVar8 * fVar22;
      pfVar27[-2] = fVar40 * fVar11 + fVar36 * fVar39 + fVar6 * fVar17 +
                    fVar7 * fVar14 + fVar8 * fVar23;
      pfVar27[-1] = fVar40 * fVar12 + fVar36 * fVar37 + fVar6 * fVar18 +
                    fVar7 * fVar15 + fVar8 * fVar35;
      fVar40 = pfVar27[-5];
      fVar6 = pfVar27[-6];
      fVar7 = pfVar27[-8];
      fVar9 = pfVar25[0x39];
      fVar11 = pfVar25[0x3a];
      fVar12 = pfVar25[0x3b];
      fVar13 = pfVar25[0x29];
      fVar14 = pfVar25[0x2a];
      fVar15 = pfVar25[0x2b];
      fVar16 = pfVar25[0x2d];
      fVar17 = pfVar25[0x2e];
      fVar18 = pfVar25[0x2f];
      fVar34 = pfVar25[0x31];
      fVar39 = pfVar25[0x32];
      fVar37 = pfVar25[0x33];
      fVar8 = pfVar27[-7];
      fVar22 = pfVar25[0x35];
      fVar23 = pfVar25[0x36];
      fVar35 = pfVar25[0x37];
      fVar36 = fVar40 * pfVar25[0x2c] + fVar38 * pfVar25[0x28] + fVar6 * pfVar25[0x30] +
               fVar7 * pfVar25[0x38] + fVar8 * pfVar25[0x34];
      pfVar27[-8] = fVar36;
      pfVar27[-7] = fVar40 * fVar16 + fVar38 * fVar13 + fVar6 * fVar34 +
                    fVar7 * fVar9 + fVar8 * fVar22;
      pfVar27[-6] = fVar40 * fVar17 + fVar38 * fVar14 + fVar6 * fVar39 +
                    fVar7 * fVar11 + fVar8 * fVar23;
      pfVar27[-5] = fVar40 * fVar18 + fVar38 * fVar15 + fVar6 * fVar37 +
                    fVar7 * fVar12 + fVar8 * fVar35;
      fVar6 = pfVar27[-9];
      fVar7 = pfVar27[-10];
      fVar8 = pfVar27[-0xc];
      fVar11 = pfVar25[0x41];
      fVar12 = pfVar25[0x42];
      fVar13 = pfVar25[0x43];
      fVar14 = pfVar25[0x4d];
      fVar15 = pfVar25[0x4e];
      fVar16 = pfVar25[0x4f];
      fVar17 = pfVar25[0x45];
      fVar18 = pfVar25[0x46];
      fVar34 = pfVar25[0x47];
      fVar39 = pfVar25[0x3d];
      fVar37 = pfVar25[0x3e];
      fVar22 = pfVar25[0x3f];
      fVar9 = pfVar27[-0xb];
      fVar23 = pfVar25[0x49];
      fVar35 = pfVar25[0x4a];
      fVar38 = pfVar25[0x4b];
      fVar40 = fVar6 * pfVar25[0x40] + fVar36 * pfVar25[0x3c] + fVar7 * pfVar25[0x44] +
               fVar8 * pfVar25[0x4c] + fVar9 * pfVar25[0x48];
      pfVar25 = pfVar25 + 0x50;
      pfVar27[-0xc] = fVar40;
      pfVar27[-0xb] =
           fVar6 * fVar11 + fVar36 * fVar39 + fVar7 * fVar17 + fVar8 * fVar14 + fVar9 * fVar23;
      pfVar27[-10] = fVar6 * fVar12 + fVar36 * fVar37 + fVar7 * fVar18 +
                     fVar8 * fVar15 + fVar9 * fVar35;
      pfVar27[-9] = fVar6 * fVar13 + fVar36 * fVar22 + fVar7 * fVar34 +
                    fVar8 * fVar16 + fVar9 * fVar38;
      pfVar27 = pfVar27 + -0x10;
      uVar33 = uVar33 - 1;
    } while (uVar33 != 0);
  }
  if (iVar29 < iVar24) {
    pfVar25 = pfVar25 + 8;
    uVar33 = (ulonglong)(uint)(iVar24 - iVar29);
    pfVar27 = pfVar27 + 2;
    do {
      fVar6 = pfVar27[1];
      fVar7 = *pfVar27;
      fVar8 = pfVar27[-2];
      pfVar30 = pfVar25 + -4;
      fVar11 = pfVar25[-3];
      fVar12 = pfVar25[-2];
      fVar13 = pfVar25[-1];
      pfVar31 = pfVar25 + -8;
      fVar35 = fVar40 * pfVar25[-7];
      fVar38 = fVar40 * pfVar25[-6];
      fVar36 = fVar40 * pfVar25[-5];
      pfVar32 = pfVar25 + 8;
      fVar14 = pfVar25[9];
      fVar15 = pfVar25[10];
      fVar16 = pfVar25[0xb];
      fVar9 = pfVar27[-1];
      fVar17 = *pfVar25;
      fVar18 = pfVar25[1];
      fVar34 = pfVar25[2];
      fVar39 = pfVar25[3];
      pfVar1 = pfVar25 + 4;
      fVar37 = pfVar25[5];
      fVar22 = pfVar25[6];
      fVar23 = pfVar25[7];
      pfVar25 = pfVar25 + 0x14;
      fVar40 = fVar6 * *pfVar30 + fVar40 * *pfVar31 + fVar7 * fVar17 +
               fVar8 * *pfVar32 + fVar9 * *pfVar1;
      pfVar27[-2] = fVar40;
      pfVar27[-1] = fVar6 * fVar11 + fVar35 + fVar7 * fVar18 + fVar8 * fVar14 + fVar9 * fVar37;
      *pfVar27 = fVar6 * fVar12 + fVar38 + fVar7 * fVar34 + fVar8 * fVar15 + fVar9 * fVar22;
      pfVar27[1] = fVar6 * fVar13 + fVar36 + fVar7 * fVar39 + fVar8 * fVar16 + fVar9 * fVar23;
      pfVar27 = pfVar27 + -4;
      uVar33 = uVar33 - 1;
    } while (uVar33 != 0);
  }
  return;
}


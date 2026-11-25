 (GhidraScript)  

void FUN_18087f0c0(longlong *param_1,longlong *param_2,undefined8 *param_3,longlong param_4,
                  float param_5,longlong *param_6)

{
  char cVar1;
  undefined4 uVar2;
  float fVar3;
  int iVar4;
  undefined8 uVar5;
  float fVar6;
  double dVar7;
  double dVar8;
  float fVar9;
  char *pcVar10;
  uint *puVar11;
  char cVar12;
  uint uVar13;
  uint **ppuVar14;
  uint **ppuVar15;
  uint *puVar16;
  uint uVar17;
  longlong lVar18;
  longlong lVar19;
  longlong *plVar20;
  int iVar21;
  float *pfVar22;
  uint *puVar23;
  ulonglong uVar24;
  bool bVar25;
  float fVar26;
  float fVar27;
  undefined4 local_res20 [2];
  float local_558 [4];
  uint *local_548;
  undefined8 uStack_540;
  int local_538;
  char *local_530;
  uint *local_528;
  int iStack_520;
  int iStack_51c;
  float local_518 [2];
  char *local_510;
  uint *local_508;
  int iStack_500;
  int iStack_4fc;
  longlong local_4f8 [4];
  longlong local_4d8;
  longlong lStack_4d0;
  longlong local_4c8;
  longlong lStack_4c0;
  longlong local_4b8;
  longlong lStack_4b0;
  longlong local_4a8;
  longlong lStack_4a0;
  longlong local_498;
  longlong lStack_490;
  undefined1 local_488 [16];
  undefined1 local_478 [16];
  undefined4 local_f8;
  int local_f4;
  longlong local_f0;
  
  local_4f8[0] = *param_1;
  local_4f8[1] = param_1[1];
  local_4f8[2] = param_1[2];
  local_4f8[3] = param_1[3];
  local_4d8 = param_1[4];
  lStack_4d0 = param_1[5];
  local_4b8 = param_1[8];
  lStack_4b0 = param_1[9];
  local_4c8 = param_1[6];
  lStack_4c0 = param_1[7];
  local_498 = param_1[0xc];
  lStack_490 = param_1[0xd];
  local_4a8 = param_1[10];
  lStack_4a0 = param_1[0xb];
  local_478 = *(undefined1 (*) [16])(param_1 + 0x10);
  local_488 = *(undefined1 (*) [16])(param_1 + 0xe);
  FUN_18087a7a0(local_4f8);
  cVar1 = *(char *)(param_4 + 0x52);
  local_530 = (char *)(param_4 + 0xb8);
  iStack_520 = *(int *)((longlong)param_1 + 0x84);
  iStack_51c = iStack_520 * 4;
  local_538 = (int)param_6[3];
  local_528 = (uint *)(*param_6 + (longlong)local_538 * 4);
  uVar17 = iStack_520 + local_538;
  local_510 = (char *)(param_4 + 0x1b8);
  uVar13 = (uVar17 - (uVar17 & 0xf)) + 0x10;
  if ((uVar17 & 0xf) == 0) {
    uVar13 = uVar17;
  }
  *(uint *)(param_6 + 3) = uVar13;
  fVar9 = DAT_18207a188;
  dVar8 = DAT_18207a118;
  dVar7 = DAT_182079fa0;
  fVar6 = DAT_182079f9c;
  if (local_530 == local_510) {
    *(int *)(param_6 + 3) = local_538;
    return;
  }
  do {
    pcVar10 = local_530;
    fVar27 = *(float *)(local_530 + 8);
    local_530 = pcVar10;
    if ((((*local_530 != '\0') && (local_530[1] != '\0')) && (*(int *)(local_530 + 0x1c) - 2U < 2))
       && (0.0 < fVar27)) {
      uVar2 = *(undefined4 *)(local_530 + 4);
      fVar3 = *(float *)(local_530 + 0xc);
      fVar26 = (float)FUN_181c9aa01(fVar3);
      iVar21 = iStack_520;
      puVar23 = local_528;
      local_4f8[0] = *param_2;
      local_4f8[1] = param_2[1];
      local_4f8[2] = param_2[2];
      local_4f8[3] = param_2[3];
      uVar5 = CONCAT44(iStack_51c,iStack_520);
      local_4c8 = param_2[6];
      lStack_4c0 = param_2[7];
      fVar26 = fVar26 - fVar6;
      local_4d8 = param_2[4];
      lStack_4d0 = param_2[5];
      local_4b8 = param_2[8];
      lStack_4b0 = param_2[9];
      if (fVar26 <= 0.0) {
        fVar26 = 0.0;
      }
      local_4a8 = param_2[10];
      lStack_4a0 = param_2[0xb];
      local_498 = param_2[0xc];
      lStack_490 = param_2[0xd];
      fVar27 = fVar27 * fVar9;
      if (DAT_18207a300 <= fVar27) {
        fVar27 = DAT_18207a300;
      }
      local_488 = *(undefined1 (*) [16])(param_2 + 0xe);
      local_478 = *(undefined1 (*) [16])(param_2 + 0x10);
      local_548 = local_528;
      uStack_540 = uVar5;
      FUN_180882de0(&local_548,local_4f8,uVar2,fVar3 * fVar9,fVar26 * param_5 * fVar27);
      local_548 = puVar23;
      uStack_540 = uVar5;
      FUN_180001100(puVar23,iVar21);
      iVar21 = iStack_520;
      if ((int)param_1[0x10] == 1) {
        iStack_500 = *(int *)((longlong)param_1 + 0x84);
        local_548 = (uint *)*param_1;
        iStack_4fc = iStack_500 * 4;
        uStack_540 = CONCAT44(iStack_4fc,iStack_500);
        local_508 = local_548;
        FUN_180001340(puVar23,local_548,iStack_500);
        local_530 = pcVar10;
      }
      else {
        local_558[0] = 1.0;
        local_558[0] = *(float *)(pcVar10 + 0x14) * fVar9;
        fVar27 = (fVar6 - *(float *)(pcVar10 + 0x14)) * fVar9;
        local_548 = (uint *)CONCAT44(local_548._4_4_,fVar27);
        ppuVar15 = (uint **)local_res20;
        if (0.0 <= fVar27) {
          ppuVar15 = &local_548;
        }
        ppuVar14 = (uint **)local_558;
        if (fVar27 <= fVar6) {
          ppuVar14 = ppuVar15;
        }
        ppuVar15 = (uint **)local_res20;
        if (0.0 <= local_558[0]) {
          ppuVar15 = (uint **)local_558;
        }
        local_518[0] = *(float *)ppuVar14;
        local_548 = (uint *)CONCAT44(local_548._4_4_,0x3f800000);
        local_res20[0] = 0;
        ppuVar14 = &local_548;
        if (local_558[0] <= fVar6) {
          ppuVar14 = ppuVar15;
        }
        local_518[1] = *(float *)ppuVar14;
        iVar4 = *(int *)(pcVar10 + 0x18);
        local_4f8[0] = 0;
        local_558[0] = (float)param_6[3];
        lVar19 = (longlong)iStack_520;
        FUN_181798f42(local_4f8 + 1,0);
        puVar23 = local_528;
        uVar17 = *(uint *)(param_6 + 3);
        local_f0 = lVar19 << 2;
        lVar19 = 0;
        local_f8 = 2;
        local_f4 = iVar21;
        do {
          uVar13 = iVar21 + uVar17;
          local_4f8[lVar19] = *param_6 + (longlong)(int)uVar17 * 4;
          uVar17 = (uVar13 - (uVar13 & 0xf)) + 0x10;
          if ((uVar13 & 0xf) == 0) {
            uVar17 = uVar13;
          }
          lVar19 = lVar19 + 1;
          *(uint *)(param_6 + 3) = uVar17;
        } while (lVar19 < 2);
        plVar20 = local_4f8;
        pfVar22 = local_518;
        lVar19 = 2;
        do {
          if (dVar7 <= (double)*pfVar22) {
            if ((double)*pfVar22 <= dVar8) {
              FUN_1801c84d0(puVar23);
            }
            else {
              FUN_1800010a0(puVar23,*plVar20,iVar21);
            }
          }
          else {
            FUN_180001040(fVar6,*plVar20,iVar21);
          }
          pfVar22 = pfVar22 + 1;
          plVar20 = plVar20 + 1;
          lVar19 = lVar19 + -1;
        } while (lVar19 != 0);
        puVar23 = (uint *)*param_3;
        local_548 = (uint *)param_3[1];
        if (puVar23 != (uint *)param_3[1]) {
          do {
            uVar17 = *puVar23;
            uVar24 = (ulonglong)uVar17;
            uVar13 = *(uint *)(local_530 + 0x18);
            if (uVar13 == 0) goto LAB_18087f642;
            if (uVar13 == 1) {
              bVar25 = uVar17 != 10;
LAB_18087f63e:
              if (bVar25) {
LAB_18087f642:
                puVar11 = local_528;
                iVar21 = 0;
                lVar19 = 0;
                if (0 < (int)puVar23[4]) {
                  uVar2 = *(undefined4 *)((longlong)param_1 + 0x84);
                  do {
                    if ((puVar23[4] == 2) || ((cVar1 != '\0' && (1 < iVar4 - 9U)))) {
                      puVar16 = (uint *)local_4f8[lVar19];
                      lVar18 = param_1[*(longlong *)(puVar23 + 2) + lVar19];
                    }
                    else {
                      lVar18 = param_1[*(longlong *)(puVar23 + 2) + lVar19];
                      puVar16 = puVar11;
                    }
                    FUN_180001340(puVar16,lVar18,uVar2);
                    iVar21 = iVar21 + 1;
                    lVar19 = lVar19 + 1;
                  } while (iVar21 < (int)puVar23[4]);
                }
              }
            }
            else {
              if (uVar13 == 2) {
                bVar25 = uVar17 != 9;
                goto LAB_18087f63e;
              }
              if (uVar13 == 3) {
                if (uVar17 - 9 < 2) goto LAB_18087f69e;
                goto LAB_18087f642;
              }
              if (uVar13 == 5) {
                if (uVar17 - 0x10 < 3) goto LAB_18087f642;
              }
              else if (uVar13 == 4) {
                if (2 < uVar17 - 8) goto LAB_18087f642;
              }
              else if (uVar13 == 6) {
                cVar12 = FUN_18061b790(4,uVar24);
                if ((cVar12 != '\0') &&
                   (cVar12 = FUN_18061b790(5,uVar24 & 0xffffffff), cVar12 == '\0'))
                goto LAB_18087f642;
              }
              else {
                if (uVar13 != 7) {
                  bVar25 = uVar13 == uVar17;
                  goto LAB_18087f63e;
                }
                if (uVar17 - 8 < 2) goto LAB_18087f642;
              }
            }
LAB_18087f69e:
            puVar23 = puVar23 + 6;
          } while (puVar23 != local_548);
        }
        *(float *)(param_6 + 3) = local_558[0];
      }
    }
    local_530 = local_530 + 0x20;
    if (local_530 == local_510) {
      *(int *)(param_6 + 3) = local_538;
      return;
    }
  } while( true );
}

 (GhidraScript)  

 (GhidraScript)  

float FUN_1808b2680(ulonglong *param_1,undefined4 param_2)

{
  float *pfVar1;
  longlong lVar2;
  float fVar3;
  uint uVar4;
  ulonglong uVar5;
  ulonglong uVar6;
  longlong *plVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  undefined8 *puVar10;
  ulonglong uVar11;
  ulonglong uVar12;
  ulonglong uVar13;
  longlong *plVar14;
  int iVar15;
  undefined8 in_RDX;
  ulonglong uVar16;
  ulonglong uVar17;
  longlong lVar18;
  ulonglong uVar19;
  uint uVar20;
  float *pfVar21;
  ulonglong uVar22;
  float fVar23;
  longlong lVar24;
  uint uVar25;
  longlong local_90;
  int local_88;
  
  fVar23 = (float)FUN_1808b2c30(param_1 + 0x31,in_RDX,param_1 + 8);
  fVar3 = DAT_182079f9c;
  uVar5 = param_1[0x18];
  uVar6 = param_1[0x1b];
  if ((0x20 < *param_1) && ((param_1[0x28] & 0x1f) == 0)) {
3;
    uVar19 = 1;
    if (1 < uVar11) {
      do {
        plVar7 = *(longlong **)(param_1[0x1e] + uVar19 * 8);
        uVar4 = *(uint *)(plVar7 + 3);
        uVar22 = (ulonglong)(int)uVar4;
1;
        if ((param_1[0x28] & uVar17 - 1) == 0) {
          iVar15 = 0;
          local_90 = 0;
          local_88 = (int)param_1[0x43];
          if (0 < (int)param_1[0x43]) {
            plVar14 = &local_90;
            do {
              iVar15 = iVar15 + 1;
              *plVar14 = *(longlong *)
                          ((longlong)param_1 + (0x210 - (longlong)&local_90) + (longlong)plVar14);
              plVar14 = plVar14 + 1;
            } while (iVar15 < local_88);
          }
          lVar18 = local_90;
          uVar16 = param_1[0x28] - uVar17 & param_1[0x29];
          uVar12 = *param_1 - uVar16;
          uVar13 = uVar17;
          if (uVar12 < uVar17) {
            uVar13 = uVar12;
          }
          uVar20 = (uVar4 - (uVar4 & 0xf)) + 0x10;
          if ((uVar22 & 0xf) == 0) {
            uVar20 = uVar4;
          }
          lVar24 = local_90;
          uVar25 = uVar4;
          local_88 = (int)uVar13;
          FUN_1800010a0(uVar5 + (longlong)(int)uVar16 * 4,local_90,uVar13 & 0xffffffff);
          local_88 = (int)(uVar17 - uVar13);
          FUN_1800010a0(uVar5,lVar18 + (longlong)(int)uVar13 * 4,uVar17 - uVar13 & 0xffffffff);
          FUN_1800010d0(lVar18 + (longlong)(int)uVar17 * 4,uVar22 - uVar17);
          lVar2 = lVar18 + (longlong)(int)uVar20 * 4;
          if (uVar17 < 0x100) {
            FUN_180001010(lVar18,lVar2,*(undefined8 *)(*plVar7 + 8),*(undefined8 *)plVar7[1],uVar11,
                          lVar24,uVar25);
            puVar8 = *(undefined8 **)(param_1[0x21] + uVar19 * 8);
            local_88 = *(int *)(puVar8 + 2);
1) + 1);
            FUN_180001280(lVar2,lVar18,*(undefined8 *)(*plVar7 + 8),*(undefined8 *)plVar7[1]);
            FUN_180001220(fVar3 / (float)(int)plVar7[3],lVar18,uVar4);
          }
          else {
            FUN_180001010(lVar18,lVar2,*(undefined8 *)(*plVar7 + 8),*(undefined8 *)plVar7[1],uVar11,
                          lVar24,uVar25);
            puVar8 = *(undefined8 **)(param_1[0x24] + param_1[0x27] * 8);
            uVar9 = *puVar8;
            puVar10 = *(undefined8 **)(param_1[0x21] + uVar19 * 8);
            local_88 = *(int *)(puVar10 + 2);
            FUN_1800015e0(lVar2,*puVar10,uVar9,*(undefined4 *)(puVar8 + 2));
            FUN_180001280(uVar9,lVar18,*(undefined8 *)(*plVar7 + 8),*(undefined8 *)plVar7[1]);
            FUN_180001220(fVar3 / (float)(int)plVar7[3],lVar18,uVar4);
            FUN_1800010d0(uVar9);
            uVar19 = uVar19 + 1;
            lVar18 = 1;
3;
3)) {
              do {
                uVar13 = param_1[0x27] + lVar18;
                lVar18 = lVar18 + 1;
                puVar8 = *(undefined8 **)(param_1[0x24] + (uVar13 % uVar17) * 8);
                FUN_1800015e0(lVar2,**(undefined8 **)(param_1[0x21] + uVar19 * 8),*puVar8,
                              *(undefined4 *)(puVar8 + 2));
                uVar19 = uVar19 + 1;
3));
            }
            param_1[0x27] = (param_1[0x27] + 1) % uVar17;
          }
          uVar17 = 0;
          if (uVar22 < 4) {
LAB_1808b2b4c:
            if (uVar22 <= uVar17) goto LAB_1808b2b93;
          }
          else {
            pfVar21 = (float *)(lVar24 + 8);
            do {
              uVar13 = param_1[0x28] + uVar17 & param_1[0x29];
              *(float *)(uVar6 + uVar13 * 4) = *(float *)(uVar6 + uVar13 * 4) + pfVar21[-2];
              uVar13 = param_1[0x28] + 1 + uVar17 & param_1[0x29];
              *(float *)(uVar6 + uVar13 * 4) = *(float *)(uVar6 + uVar13 * 4) + pfVar21[-1];
              uVar13 = param_1[0x28] + 2 + uVar17 & param_1[0x29];
              *(float *)(uVar6 + uVar13 * 4) = *(float *)(uVar6 + uVar13 * 4) + *pfVar21;
              uVar13 = param_1[0x28] + 3 + uVar17;
              uVar17 = uVar17 + 4;
              uVar13 = uVar13 & param_1[0x29];
              pfVar1 = pfVar21 + 1;
              pfVar21 = pfVar21 + 4;
              *(float *)(uVar6 + uVar13 * 4) = *(float *)(uVar6 + uVar13 * 4) + *pfVar1;
            } while (uVar17 < uVar22 - 3);
            if (uVar22 <= uVar17) goto LAB_1808b2b4c;
          }
          do {
            lVar18 = uVar17 * 4;
            uVar13 = param_1[0x28] + uVar17;
            uVar17 = uVar17 + 1;
            uVar13 = uVar13 & param_1[0x29];
            *(float *)(uVar6 + uVar13 * 4) =
                 *(float *)(lVar24 + lVar18) + *(float *)(uVar6 + uVar13 * 4);
          } while (uVar17 < uVar22);
        }
LAB_1808b2b93:
        uVar19 = uVar19 + 1;
      } while (uVar19 < uVar11);
    }
  }
  fVar3 = *(float *)(uVar6 + param_1[0x28] * 4);
  *(undefined4 *)(uVar5 + param_1[0x28] * 4) = param_2;
  *(undefined4 *)(uVar6 + param_1[0x28] * 4) = 0;
  param_1[0x28] = param_1[0x28] + 1 & param_1[0x29];
  return fVar23 + fVar3;
}

 (GhidraScript)  

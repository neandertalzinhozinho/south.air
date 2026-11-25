 (GhidraScript)  

void FUN_18087fd60(longlong param_1,longlong *param_2,char param_3)

{
  char cVar1;
  longlong lVar2;
  undefined8 uVar3;
  uint uVar4;
  longlong lVar5;
  undefined8 *puVar6;
  uint uVar7;
  ulonglong uVar8;
  int iVar9;
  uint uVar10;
  ulonglong uVar11;
  int iVar12;
  float fVar13;
  int local_res8 [2];
  undefined4 local_res20 [2];
  undefined4 local_358;
  float local_354 [2];
  uint local_34c;
  longlong local_348 [14];
  undefined8 uStack_2d8;
  undefined8 local_2d0;
  uint local_2c8;
  int iStack_2c4;
  undefined8 uStack_2c0;
  undefined8 local_2b8 [16];
  int local_238;
  int iStack_234;
  longlong lStack_230;
  longlong *local_228;
  longlong *local_220;
  longlong local_218;
  int *local_210;
  float *local_208;
  float *local_200;
  undefined4 *local_1f8;
  undefined4 *local_1f0;
  undefined8 local_1e8 [16];
  int local_168;
  int local_164;
  longlong local_160;
  undefined8 local_158 [4];
  undefined8 local_138;
  undefined8 uStack_130;
  undefined8 local_128;
  undefined8 uStack_120;
  undefined8 local_118;
  undefined8 uStack_110;
  undefined8 local_108;
  undefined8 uStack_100;
  undefined8 local_f8;
  undefined8 uStack_f0;
  undefined8 local_e8;
  undefined8 uStack_e0;
  undefined8 local_d8;
  longlong lStack_d0;
  longlong local_c8 [4];
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined4 local_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  uint local_48;
  int iStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  
  local_358 = 0x43960000;
  local_354[1] = 2000.0;
  local_res20[0] = 0x40000000;
  fVar13 = *(float *)(*(longlong *)(param_1 + 0x2c38) + 4) - DAT_182079ea8;
  if (fVar13 <= 0.0) {
    fVar13 = 0.0;
  }
  fVar13 = fVar13 * DAT_18207a188;
  if (fVar13 <= 0.0) {
    fVar13 = 0.0;
  }
  if (DAT_182079f9c <= fVar13) {
    fVar13 = DAT_182079f9c;
  }
  local_354[0] = DAT_182079ed4 - fVar13 * DAT_182079ea8;
  if (param_3 == '\0') {
    iVar12 = 2;
    *(int *)(param_1 + 0x2bcc) =
         (int)((ulonglong)(longlong)*(int *)(param_1 + 0x2bcc) % *(ulonglong *)(param_1 + 0x48));
  }
  else {
    iVar12 = *(int *)(param_1 + 0x48);
    *(undefined4 *)(param_1 + 0x2bcc) = 0;
  }
  if ((ulonglong)(longlong)*(int *)(param_1 + 0x2bcc) < *(ulonglong *)(param_1 + 0x48)) {
    do {
      uVar8 = 0;
      if (param_3 == '\0') {
        lVar5 = **(longlong **)(param_1 + 0x10);
        lVar2 = (*(longlong **)(param_1 + 0x10))[1];
        if (lVar5 != lVar2) {
          do {
            if (((longlong)*(int *)(param_1 + 0x2bcc) == *(longlong *)(lVar5 + 8)) &&
               (*(int *)(lVar5 + 0x10) == 1)) {
              iVar12 = 1;
              break;
            }
            lVar5 = lVar5 + 0x18;
          } while (lVar5 != lVar2);
        }
      }
      local_res8[0] = *(int *)(param_1 + 0x2bcc);
      *(int *)(param_1 + 0x2bcc) = *(int *)(param_1 + 0x2bcc) + 1;
      cVar1 = *(char *)((longlong)local_res8[0] + 0x2bb8 + param_1);
      *(undefined1 *)((longlong)local_res8[0] + 0x2bb8 + param_1) = 0;
      if (cVar1 != '\0') {
        local_d8._0_4_ = *(uint *)(param_1 + 0x738);
        uVar7 = *(uint *)(param_2 + 3);
        local_d8._4_4_ = *(int *)(param_1 + 0x740);
        iVar9 = *(int *)(param_1 + 0x740);
        if (0 < (int)(uint)local_d8) {
          puVar6 = local_158;
          uVar11 = uVar8;
          do {
            uVar10 = (int)uVar11 + 1;
            uVar11 = (ulonglong)uVar10;
            *puVar6 = *(undefined8 *)(((param_1 + 0x6b8) - (longlong)local_158) + (longlong)puVar6);
            puVar6 = puVar6 + 1;
          } while ((int)uVar10 < (int)(uint)local_d8);
          iVar9 = local_d8._4_4_;
        }
        local_348[0] = 0;
        local_2d0 = 0;
        uStack_2c0 = (longlong)iVar9 << 2;
        local_348[1] = 0;
        local_348[2] = 0;
        local_348[3] = 0;
        local_348[4] = 0;
        local_348[5] = 0;
        local_348[6] = 0;
        local_348[7] = 0;
        local_348[8] = 0;
        local_348[9] = 0;
        local_348[10] = 0;
        local_348[0xb] = 0;
        local_348[0xc] = 0;
        local_348[0xd] = 0;
        uStack_2d8 = 0;
        local_2c8 = (uint)local_d8;
        iStack_2c4 = iVar9;
        if (0 < (int)(uint)local_d8) {
          uVar11 = uVar8;
          uVar10 = uVar7;
          do {
            uVar4 = uVar10 + iVar9;
            local_348[uVar11] = *param_2 + (longlong)(int)uVar10 * 4;
            uVar10 = (uVar4 - (uVar4 & 0xf)) + 0x10;
            if ((uVar4 & 0xf) == 0) {
              uVar10 = uVar4;
            }
            uVar11 = uVar11 + 1;
            *(uint *)(param_2 + 3) = uVar10;
          } while ((longlong)uVar11 < (longlong)(int)(uint)local_d8);
        }
        iVar9 = iStack_2c4;
        local_164 = *(int *)(param_1 + 0xa10);
        local_1e8[0xf] = 0;
        local_1e8[0] = 0;
        local_168 = *(int *)(param_1 + 0xa08);
        local_160 = (longlong)*(int *)(param_1 + 0xa10) << 2;
        local_1e8[1] = 0;
        local_1e8[2] = 0;
        local_1e8[3] = 0;
        local_1e8[4] = 0;
        local_1e8[5] = 0;
        local_1e8[6] = 0;
        local_1e8[7] = 0;
        local_1e8[8] = 0;
        local_1e8[9] = 0;
        local_1e8[10] = 0;
        local_1e8[0xb] = 0;
        local_1e8[0xc] = 0;
        local_1e8[0xd] = 0;
        local_1e8[0xe] = 0;
        if (0 < *(int *)(param_1 + 0xa08)) {
          puVar6 = local_1e8;
          uVar11 = uVar8;
          do {
            uVar10 = (int)uVar11 + 1;
            uVar11 = (ulonglong)uVar10;
            *puVar6 = *(undefined8 *)(((param_1 + 0x988) - (longlong)local_1e8) + (longlong)puVar6);
            puVar6 = puVar6 + 1;
          } while ((int)uVar10 < local_168);
        }
        local_2b8[0] = 0;
        local_2b8[0xf] = 0;
        uVar3 = local_1e8[local_res8[0]];
        iStack_234 = *(int *)(param_1 + 0x740);
        local_238 = *(int *)(param_1 + 0x738);
        lStack_230 = (longlong)*(int *)(param_1 + 0x740) << 2;
        local_2b8[1] = 0;
        local_2b8[2] = 0;
        local_2b8[3] = 0;
        local_2b8[4] = 0;
        local_2b8[5] = 0;
        local_2b8[6] = 0;
        local_2b8[7] = 0;
        local_2b8[8] = 0;
        local_2b8[9] = 0;
        local_2b8[10] = 0;
        local_2b8[0xb] = 0;
        local_2b8[0xc] = 0;
        local_2b8[0xd] = 0;
        local_2b8[0xe] = 0;
        if (0 < *(int *)(param_1 + 0x738)) {
          puVar6 = local_2b8;
          uVar11 = uVar8;
          do {
            uVar10 = (int)uVar11 + 1;
            uVar11 = (ulonglong)uVar10;
            *puVar6 = *(undefined8 *)(((param_1 + 0x6b8) - (longlong)local_2b8) + (longlong)puVar6);
            puVar6 = puVar6 + 1;
          } while ((int)uVar10 < local_238);
        }
        local_158[0] = local_2b8[0];
        local_158[1] = local_2b8[1];
        local_158[2] = local_2b8[2];
        local_158[3] = local_2b8[3];
        local_138 = local_2b8[4];
        uStack_130 = local_2b8[5];
        local_128 = local_2b8[6];
        uStack_120 = local_2b8[7];
        local_118 = local_2b8[8];
        uStack_110 = local_2b8[9];
        local_108 = local_2b8[10];
        uStack_100 = local_2b8[0xb];
        local_f8 = local_2b8[0xc];
        uStack_f0 = local_2b8[0xd];
        local_e8 = local_2b8[0xe];
        uStack_e0 = local_2b8[0xf];
        local_c8[0] = local_348[0];
        local_c8[1] = local_348[1];
        local_a8 = local_348[4];
        uStack_a0 = local_348[5];
        local_88 = local_348[8];
        uStack_80 = local_348[9];
        local_68 = local_348[0xc];
        uStack_60 = local_348[0xd];
        local_48 = local_2c8;
        iStack_44 = iStack_2c4;
        uStack_40 = (undefined4)uStack_2c0;
        uStack_3c = uStack_2c0._4_4_;
        local_d8 = CONCAT44(iStack_234,local_238);
        lStack_d0 = lStack_230;
        local_c8[2] = local_348[2];
        local_c8[3] = local_348[3];
        local_98 = local_348[6];
        uStack_90 = local_348[7];
        local_78 = local_348[10];
        uStack_70 = local_348[0xb];
        local_58 = (undefined4)uStack_2d8;
        uStack_54 = uStack_2d8._4_4_;
        uStack_50 = (undefined4)local_2d0;
        uStack_4c = local_2d0._4_4_;
        local_34c = uVar7;
        if (local_2c8 == 1) {
          FUN_180001190(local_2b8[0],uVar3,local_348[0],iStack_2c4);
        }
        else if (0 < (int)local_2c8) {
          uVar11 = (ulonglong)local_2c8;
          do {
            FUN_180001190(*(undefined8 *)((longlong)local_158 + uVar8),uVar3,
                          *(undefined8 *)((longlong)local_c8 + uVar8),iVar9);
            uVar8 = uVar8 + 8;
            uVar11 = uVar11 - 1;
          } while (uVar11 != 0);
          uVar7 = local_34c;
        }
        local_220 = local_348;
        local_210 = local_res8;
        local_208 = local_354 + 1;
        local_200 = local_354;
        local_1f8 = &local_358;
        local_1f0 = local_res20;
        local_228 = param_2;
        local_218 = param_1;
        if (DAT_1826b1818 == 4) {
          FUN_18088e3f0(&local_228);
        }
        else if (DAT_1826b1818 == 1) {
          FUN_1808a1ff0(&local_228);
        }
        if (DAT_1826b1818 == 4) {
          FUN_180860f50((longlong)local_res8[0] * 0xb0 + 0x20b8 + param_1,local_348[0]);
        }
        else if (DAT_1826b1818 == 1) {
          FUN_1808b3840((longlong)local_res8[0] * 0xb0 + 0x20b8 + param_1,local_348[0]);
        }
        *(uint *)(param_2 + 3) = uVar7;
        iVar12 = iVar12 + -1;
        if (iVar12 == 0) {
          return;
        }
      }
    } while ((ulonglong)(longlong)*(int *)(param_1 + 0x2bcc) < *(ulonglong *)(param_1 + 0x48));
  }
  *(undefined1 *)(param_1 + 0x2bc8) = 0;
  return;
}

 (GhidraScript)  

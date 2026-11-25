// FUN_1808634a0 @ 0x1808634a0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

longlong * FUN_1808634a0(longlong *param_1,longlong param_2,uint *param_3,float param_4)

{
  double *pdVar1;
  longlong *plVar2;
  ulonglong *puVar3;
  int *piVar4;
  double dVar5;
  float fVar6;
  undefined4 uVar7;
  longlong lVar8;
  double *pdVar9;
  longlong lVar10;
  int iVar11;
  undefined8 *puVar12;
  longlong **pplVar13;
  int iVar14;
  ulonglong uVar15;
  int iVar16;
  ulonglong *puVar17;
  ulonglong uVar18;
  uint *puVar19;
  int iVar20;
  float fVar21;
  float fVar22;
  float local_res10 [2];
  uint *local_res18;
  float local_res20 [2];
  undefined4 local_2b8 [2];
  undefined8 local_2b0;
  int iStack_2a8;
  int iStack_2a4;
  longlong local_2a0;
  undefined8 local_298;
  int iStack_290;
  int iStack_28c;
  longlong local_288;
  undefined8 local_280;
  int iStack_278;
  int iStack_274;
  longlong local_270;
  undefined8 local_268;
  int iStack_260;
  int iStack_25c;
  longlong local_258;
  undefined4 uStack_250;
  undefined4 uStack_24c;
  longlong *local_248 [3];
  longlong *local_230 [16];
  uint local_1b0;
  uint uStack_1ac;
  longlong lStack_1a8;
  undefined8 local_198;
  undefined8 uStack_190;
  longlong local_188;
  undefined8 local_178;
  undefined8 uStack_170;
  longlong local_168;
  undefined8 local_158;
  int iStack_150;
  int iStack_14c;
  longlong local_148;
  undefined4 uStack_140;
  undefined4 uStack_13c;
  undefined4 uStack_120;
  undefined4 uStack_11c;
  undefined8 local_118;
  int iStack_110;
  int iStack_10c;
  longlong local_108;
  undefined4 uStack_100;
  undefined4 uStack_fc;
  longlong *local_f8 [4];
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  longlong lStack_70;
  
  *param_1 = param_2;
  param_1[1] = (longlong)param_3;
  puVar19 = param_3;
  local_res18 = param_3;
  local_res20[0] = param_4;
  uVar7 = FUN_18056b140(*param_3);
  *(undefined4 *)(param_1 + 2) = uVar7;
  uVar7 = FUN_18056b140(puVar19[2]);
  *(undefined4 *)((longlong)param_1 + 0x14) = uVar7;
  lVar8 = FUN_18085e6c0(*puVar19);
  param_1[3] = lVar8;
  lVar8 = FUN_18085e6c0(param_3[2]);
  fVar6 = DAT_182079f9c;
  *(float *)(param_1 + 5) = local_res20[0];
  param_1[4] = lVar8;
  iVar11 = (int)((local_res20[0] + fVar6) * _DAT_182079d04);
  iVar16 = 1;
  if (1 < iVar11) {
    iVar16 = iVar11;
  }
  *(int *)((longlong)param_1 + 0x2c) = iVar16;
  FUN_180868b50(param_1 + 6);
  (**(code **)(param_2 + 0x18))(param_2,0,"reduction_curve_freq_points_lo",0);
  (**(code **)(param_2 + 0x18))(param_2,1,"reduction_curve_freq_points_hi",0);
  (**(code **)(param_2 + 0x18))(param_2,2,"reduction_curve_magnitudes_lo",0);
  (**(code **)(param_2 + 0x18))(param_2,3,"reduction_curve_magnitudes_hi",0);
  (**(code **)(param_2 + 0x18))(param_2,4,"offset_curve_freq_points",0);
  (**(code **)(param_2 + 0x18))(param_2,5,"detail_offset_curve",0);
  (**(code **)(param_2 + 0x18))(param_2,6,"attack_offset_curve",0);
  (**(code **)(param_2 + 0x18))(param_2,7,"release_offset_curve",0);
  (**(code **)(param_2 + 0x18))(param_2,8,"max_cut_per_channel",0);
  (**(code **)(param_2 + 0x18))(param_2,9,"band_solo_channels",0);
  (**(code **)(param_2 + 0x18))(param_2,10,"input_channel_layout",1);
  (**(code **)(param_2 + 0x18))(param_2,0xc,"samplerate",1);
  (**(code **)(param_2 + 0x18))(param_2,0xd,"sidechain_input_level",1);
  local_2b8[0] = 0;
  (**(code **)(param_2 + 0x20))(param_2,0xd,local_2b8,1);
  iVar11 = 0;
  *(undefined2 *)((longlong)param_1 + 0x49) = 0;
  *(undefined8 *)((longlong)param_1 + 0x4c) = 0;
  FUN_180864070((longlong)param_1 + 0x54);
  *(undefined1 *)((longlong)param_1 + 0x234) = 0;
  *(undefined2 *)((longlong)param_1 + 0x235) = 0;
  puVar17 = (ulonglong *)(param_1 + 0x47);
  *(undefined1 *)((longlong)param_1 + 0x237) = 0;
  *puVar17 = 0;
  param_1[0x48] = 0;
  param_1[0x49] = 0;
  iVar16 = *(int *)((longlong)param_1 + 0x2c) * 0x30;
  *(int *)(param_1 + 0x4a) = iVar16 / 2;
  uVar15 = *puVar17;
  if (uVar15 != 0) {
    (*DAT_181d8d738)((uVar15 - 1) - (ulonglong)*(byte *)(uVar15 - 1));
  }
  *puVar17 = 0;
  if (((longlong)iVar16 * 4 == 0) ||
     (lVar8 = (*DAT_181d8d730)((longlong)iVar16 * 4 + 0x40), lVar8 == 0)) {
    uVar15 = 0;
  }
  else {
    uVar15 = lVar8 + 0x40U & 0xffffffffffffffc0;
    *(char *)(uVar15 - 1) = (char)(char *)(uVar15 - 1) - (char)lVar8;
  }
  *puVar17 = uVar15;
  iVar14 = 0;
  param_1[0x49] = (longlong)iVar16;
  iStack_2a4 = iVar16;
  param_1[0x48] = 1;
  local_2b0 = 0;
  iStack_2a8 = 1;
  local_2a0 = (longlong)iVar16 << 2;
  puVar12 = &local_2b0;
  do {
    iVar14 = iVar14 + 1;
    *puVar12 = *(undefined8 *)(((longlong)puVar17 - (longlong)&local_2b0) + (longlong)puVar12);
    puVar12 = puVar12 + 1;
  } while (iVar14 < iStack_2a8);
  uStack_190 = CONCAT44(iStack_2a4,iStack_2a8);
  local_188 = local_2a0;
  local_198 = local_2b0;
  FUN_18086e8e0(&local_198);
  iVar16 = *(int *)((longlong)param_1 + 0x2c);
  iVar20 = 0;
  iVar14 = *(int *)((longlong)param_1 + 0x14);
  lVar8 = param_1[2];
  lVar10 = param_1[0x4a];
  iStack_28c = (int)param_1[0x49];
  local_298 = 0;
  iStack_290 = (int)param_1[0x48];
  local_288 = (longlong)(int)param_1[0x49] << 2;
  if (0 < (int)param_1[0x48]) {
    puVar12 = &local_298;
    do {
      iVar20 = iVar20 + 1;
      *puVar12 = *(undefined8 *)
                  ((longlong)param_1 + (0x238 - (longlong)&local_298) + (longlong)puVar12);
      puVar12 = puVar12 + 1;
    } while (iVar20 < iStack_290);
  }
  uStack_170 = CONCAT44(iStack_28c,iStack_290);
  local_178 = local_298;
  local_168 = local_288;
  FUN_180869fb0(param_1 + 0x4b,&local_178,(longlong)(int)lVar10,(longlong)(int)lVar8,
                (longlong)iVar14,(longlong)iVar16);
  puVar19 = local_res18;
  iVar16 = 0;
  iStack_274 = (int)param_1[8];
  local_280 = 0;
  iStack_278 = (int)param_1[7];
  local_270 = (longlong)(int)param_1[8] << 2;
  if (0 < (int)param_1[7]) {
    puVar12 = &local_280;
    do {
      iVar16 = iVar16 + 1;
      *puVar12 = *(undefined8 *)
                  ((longlong)param_1 + (0x30 - (longlong)&local_280) + (longlong)puVar12);
      puVar12 = puVar12 + 1;
    } while (iVar16 < iStack_278);
  }
  local_158 = local_280;
  iStack_150 = iStack_278;
  iStack_14c = iStack_274;
  local_258 = local_270;
  uStack_250 = 0;
  local_148 = local_270;
  uStack_140 = 0;
  uStack_13c = uStack_24c;
  FUN_18086a4e0(param_1 + 0xbf,param_2,local_res18,
                local_res20[0] / (float)*(int *)((longlong)param_1 + 0x2c),(longlong)param_1 + 0x54,
                param_1[3],param_1[4],&local_158);
  iVar16 = 0;
  iStack_25c = (int)param_1[8];
  local_268 = 0;
  iStack_260 = (int)param_1[7];
  local_258 = (longlong)(int)param_1[8] << 2;
  if (0 < (int)param_1[7]) {
    puVar12 = &local_268;
    do {
      iVar16 = iVar16 + 1;
      *puVar12 = *(undefined8 *)
                  ((longlong)param_1 + (0x30 - (longlong)&local_268) + (longlong)puVar12);
      puVar12 = puVar12 + 1;
    } while (iVar16 < iStack_260);
  }
  uStack_120 = 0;
  local_118 = local_268;
  iStack_110 = iStack_260;
  iStack_10c = iStack_25c;
  local_108 = local_258;
  uStack_100 = 0;
  uStack_fc = uStack_11c;
  FUN_18086a8c0(param_1 + 0xbda,param_2,puVar19,
                local_res20[0] / (float)*(int *)((longlong)param_1 + 0x2c),(longlong)param_1 + 0x54,
                param_1[3],param_1[4],&local_118);
  pdVar1 = (double *)(param_1 + 0x16f5);
  pdVar9 = pdVar1;
  lVar8 = 0x10;
  do {
    lVar10 = lVar8;
    *pdVar9 = 48000.0;
    *(undefined4 *)(pdVar9 + 1) = 0;
    pdVar9[2] = 1000.0;
    pdVar9[3] = 1.0;
    pdVar9[4] = 1000.0;
    pdVar9[5] = 1.0;
    pdVar9[6] = 20.0;
    pdVar9[7] = 1.0;
    pdVar9[8] = 0.0;
    pdVar9[9] = 0.0;
    pdVar9[10] = 1.0;
    pdVar9[0xb] = 0.0;
    pdVar9[0xc] = 0.0;
    pdVar9[0xd] = 0.0;
    pdVar9[0xe] = 0.0;
    pdVar9 = pdVar9 + 0xf;
    lVar8 = lVar10 + -1;
  } while (lVar8 != 0);
  dVar5 = (double)local_res20[0];
  if ((double)local_res20[0] <= DAT_18207a138) {
    dVar5 = DAT_18207a138;
  }
  uVar15 = (ulonglong)((int)lVar10 + 0xf);
  pdVar9 = pdVar1;
  do {
    *pdVar9 = dVar5;
    FUN_180861b00(pdVar9);
    FUN_180861b60(pdVar9,pdVar9[4],pdVar9[5]);
    pdVar9[6] = 30.0;
    FUN_180861b00(pdVar9);
    pdVar9 = pdVar9 + 0xf;
    uVar15 = uVar15 - 1;
  } while (uVar15 != 0);
  FUN_1808685f0(pdVar1);
  fVar22 = DAT_18207a744;
  fVar21 = DAT_18207a744 / local_res20[0];
  *(undefined4 *)(param_1 + 0x17e5) = 0;
  *(undefined8 *)((longlong)param_1 + 0xbf2c) = 0x3f800000;
  fVar21 = (float)FUN_181c9a9d7(fVar21);
  *(float *)(param_1 + 0x17e6) = fVar6 - fVar21;
  *(int *)((longlong)param_1 + 0xbf2c) = (int)param_1[0x17e5];
  *(undefined4 *)((longlong)param_1 + 0xbf34) = 0x3f800000;
  param_1[0x17e7] = 0x3f800000;
  fVar21 = (float)FUN_181c9a9d7(fVar22 / local_res20[0]);
  *(float *)((longlong)param_1 + 0xbf3c) = fVar6 - fVar21;
  *(undefined4 *)(param_1 + 0x17e7) = *(undefined4 *)((longlong)param_1 + 0xbf34);
  *(undefined4 *)(param_1 + 0x17e8) = 0x3f800000;
  *(undefined8 *)((longlong)param_1 + 0xbf44) = 0x3f800000;
  fVar21 = (float)FUN_181c9a9d7(fVar22 / local_res20[0]);
  *(float *)(param_1 + 0x17e9) = fVar6 - fVar21;
  *(int *)((longlong)param_1 + 0xbf44) = (int)param_1[0x17e8];
  *(undefined4 *)((longlong)param_1 + 0xbf4c) = 0;
  param_1[0x17ea] = 0x3f800000;
  fVar22 = (float)FUN_181c9a9d7(fVar22 / local_res20[0]);
  *(float *)((longlong)param_1 + 0xbf54) = fVar6 - fVar22;
  *(undefined4 *)(param_1 + 0x17ea) = *(undefined4 *)((longlong)param_1 + 0xbf4c);
  *(undefined4 *)(param_1 + 0x17eb) = 0x3f800000;
  *(undefined8 *)((longlong)param_1 + 0xbf5c) = 0x3f800000;
  fVar22 = (float)FUN_181c9a9d7();
  plVar2 = param_1 + 0x17ed;
  *(float *)(param_1 + 0x17ec) = fVar6 - fVar22;
  *(int *)((longlong)param_1 + 0xbf5c) = (int)param_1[0x17eb];
  *plVar2 = 0;
  param_1[0x17ee] = 0;
  param_1[0x17ef] = 0;
  param_1[0x17f0] = 0;
  param_1[0x17f1] = 0;
  param_1[0x17f2] = 0;
  param_1[0x17f3] = 0;
  param_1[0x17f4] = 0;
  param_1[0x17f5] = 0;
  param_1[0x17f6] = 0;
  param_1[0x17f7] = 0;
  param_1[0x17f8] = 0;
  param_1[0x17f9] = 0;
  param_1[0x17fa] = 0;
  param_1[0x17fb] = 0;
  param_1[0x17fc] = 0;
  param_1[0x17fd] = 0;
  param_1[0x17fe] = 0;
  FUN_180868590(plVar2);
  FUN_180868590(plVar2);
  lVar8 = 0;
  do {
    lVar10 = (*DAT_181d8d730)(0x1040);
    if (lVar10 == 0) {
      uVar15 = 0;
    }
    else {
      uVar15 = lVar10 + 0x40U & 0xffffffffffffffc0;
      *(char *)(uVar15 - 1) = (char)(char *)(uVar15 - 1) - (char)lVar10;
    }
    plVar2[lVar8] = uVar15;
    lVar8 = lVar8 + 1;
  } while (lVar8 < 0x10);
  param_1[0x17fd] = 0x10;
  param_1[0x17fe] = 0x400;
  param_1[0x17ff] = 0;
  param_1[0x1800] = 0;
  param_1[0x1801] = 0;
  param_1[0x1802] = 0;
  param_1[0x1803] = 0;
  param_1[0x1804] = 0;
  param_1[0x1805] = 0;
  param_1[0x1806] = 0;
  param_1[0x1807] = 0;
  param_1[0x1808] = 0;
  param_1[0x1809] = 0;
  param_1[0x180a] = 0;
  param_1[0x180b] = 0;
  param_1[0x180c] = 0;
  param_1[0x180d] = 0;
  param_1[0x180e] = 0;
  param_1[0x180f] = 0;
  param_1[0x1810] = 0;
  param_1[0x1811] = 0;
  param_1[0x1812] = 0;
  param_1[0x1813] = 0;
  param_1[0x1814] = 0;
  param_1[0x1815] = 0;
  param_1[0x1816] = 0;
  param_1[0x1817] = 0;
  param_1[0x1818] = 0;
  param_1[0x1819] = 0;
  param_1[0x181a] = 0;
  param_1[0x181b] = 0;
  param_1[0x181c] = 0;
  param_1[0x181d] = 0;
  param_1[0x181e] = 0;
  param_1[0x181f] = 0;
  param_1[0x1820] = 0;
  param_1[0x1821] = 0;
  param_1[0x1822] = 0;
  param_1[0x1823] = 0;
  param_1[0x1824] = 0;
  param_1[0x1825] = 0;
  param_1[0x1826] = 0;
  param_1[0x1827] = 0;
  param_1[0x1828] = 0;
  param_1[0x1829] = 0;
  param_1[0x182a] = 0;
  param_1[0x182b] = 0;
  param_1[0x182c] = 0;
  param_1[0x182d] = 0;
  param_1[0x182e] = 0;
  param_1[0x182f] = 0;
  param_1[0x1830] = 0;
  param_1[0x1831] = 0;
  param_1[0x1832] = 0;
  param_1[0x1833] = 0;
  param_1[0x1834] = 0;
  local_res10[0] = (float)*local_res18;
  (**(code **)(param_2 + 0x20))(param_2,10,local_res10,1);
  (**(code **)(param_2 + 0x20))(param_2,0xc,local_res20,1);
  iVar16 = (int)(local_res20[0] * _DAT_182079d04);
  if (iVar16 < 1) {
    iVar16 = 1;
  }
  pplVar13 = local_248;
  local_res18 = (uint *)CONCAT44(local_res18._4_4_,iVar16 << 0xc);
  local_248[0] = param_1 + 0x17ff;
  local_248[1] = param_1 + 0x1811;
  local_248[2] = param_1 + 0x1823;
  if (local_248 != local_230) {
    do {
      puVar17 = (ulonglong *)*pplVar13;
      iVar14 = FUN_18086aca0();
      FUN_180868840(puVar17);
      *(int *)((longlong)puVar17 + 0x8c) = iVar14;
      iVar20 = 0;
      *(int *)(puVar17 + 0x11) = iVar16 << 0xc;
      if (0 < iVar14) {
        puVar3 = puVar17 + 0x11;
        piVar4 = (int *)((longlong)puVar17 + 0x8c);
        do {
          lVar8 = (longlong)(int)*puVar3 * 4;
          if ((lVar8 == 0) || (lVar8 = (*DAT_181d8d730)(lVar8 + 0x40), lVar8 == 0)) {
            uVar15 = 0;
          }
          else {
            uVar15 = lVar8 + 0x40U & 0xffffffffffffffc0;
            *(char *)(uVar15 - 1) = (char)(char *)(uVar15 - 1) - (char)lVar8;
          }
          *puVar17 = uVar15;
          iVar20 = iVar20 + 1;
          puVar17 = puVar17 + 1;
        } while (iVar20 < *piVar4);
      }
      pplVar13 = pplVar13 + 1;
    } while (pplVar13 != local_230);
  }
  uVar15 = (ulonglong)(int)*(uint *)(param_1 + 0x17fe);
  local_230[0] = (longlong *)0x0;
  local_230[0xf] = (longlong *)0x0;
  local_1b0 = *(uint *)(param_1 + 0x17fd);
  uStack_1ac = *(uint *)(param_1 + 0x17fe);
  lStack_1a8 = uVar15 << 2;
  local_230[1] = (longlong *)0x0;
  local_230[2] = (longlong *)0x0;
  local_230[3] = (longlong *)0x0;
  local_230[4] = (longlong *)0x0;
  local_230[5] = (longlong *)0x0;
  local_230[6] = (longlong *)0x0;
  local_230[7] = (longlong *)0x0;
  local_230[8] = (longlong *)0x0;
  local_230[9] = (longlong *)0x0;
  local_230[10] = (longlong *)0x0;
  local_230[0xb] = (longlong *)0x0;
  local_230[0xc] = (longlong *)0x0;
  local_230[0xd] = (longlong *)0x0;
  local_230[0xe] = (longlong *)0x0;
  if (0 < (int)*(uint *)(param_1 + 0x17fd)) {
    pplVar13 = local_230;
    do {
      iVar11 = iVar11 + 1;
      *pplVar13 = *(longlong **)
                   ((longlong)param_1 + (49000 - (longlong)local_230) + (longlong)pplVar13);
      pplVar13 = pplVar13 + 1;
    } while (iVar11 < (int)local_1b0);
    uVar15 = (ulonglong)uStack_1ac;
  }
  uVar18 = (ulonglong)local_1b0;
  local_f8[0] = local_230[0];
  local_f8[1] = local_230[1];
  local_f8[2] = local_230[2];
  local_f8[3] = local_230[3];
  local_d8 = local_230[4];
  uStack_d0 = local_230[5];
  local_c8 = local_230[6];
  uStack_c0 = local_230[7];
  local_b8 = local_230[8];
  uStack_b0 = local_230[9];
  local_a8 = local_230[10];
  uStack_a0 = local_230[0xb];
  local_98 = local_230[0xc];
  uStack_90 = local_230[0xd];
  local_88 = local_230[0xe];
  uStack_80 = local_230[0xf];
  local_78 = CONCAT44(uStack_1ac,local_1b0);
  lStack_70 = lStack_1a8;
  if (0 < (int)local_1b0) {
    pplVar13 = local_f8;
    do {
      FUN_1800010d0(*pplVar13,uVar15 & 0xffffffff);
      pplVar13 = pplVar13 + 1;
      uVar18 = uVar18 - 1;
    } while (uVar18 != 0);
  }
  FUN_1808689d0(param_1,1);
  LOCK();
  *(undefined1 *)((longlong)param_1 + 0x4a) = 1;
  UNLOCK();
  return param_1;
}


// FUN_18006ce80 @ 0x18006ce80

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18006ce80(undefined1 (*param_1) [32],undefined1 (*param_2) [32],undefined1 (*param_3) [32],
                  uint param_4,int param_5,undefined8 param_6,int param_7)

{
  undefined1 (*pauVar1) [32];
  undefined1 (*pauVar2) [32];
  float fVar3;
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
  undefined1 auVar34 [16];
  undefined1 auVar35 [16];
  float fVar36;
  float fVar37;
  float fVar38;
  float fVar39;
  float fVar40;
  float fVar41;
  float fVar42;
  float fVar43;
  float fVar44;
  float fVar45;
  float fVar46;
  float fVar47;
  float fVar48;
  float fVar49;
  float fVar50;
  float fVar51;
  float fVar52;
  float fVar53;
  float fVar54;
  float fVar55;
  float fVar56;
  float fVar57;
  float fVar58;
  float fVar59;
  float fVar60;
  float fVar61;
  float fVar62;
  float fVar63;
  float fVar64;
  float fVar65;
  float fVar66;
  float fVar67;
  float fVar68;
  float fVar69;
  float fVar70;
  float fVar71;
  float fVar72;
  float fVar73;
  float fVar74;
  float fVar75;
  float fVar76;
  float fVar77;
  float fVar78;
  float fVar79;
  undefined1 *puVar80;
  undefined1 *puVar81;
  undefined1 (*pauVar82) [32];
  undefined1 (*pauVar83) [32];
  undefined1 (*pauVar84) [32];
  undefined1 (*pauVar85) [32];
  undefined1 (*pauVar86) [32];
  undefined1 (*pauVar87) [32];
  undefined1 (*pauVar88) [32];
  undefined1 (*pauVar89) [32];
  undefined1 (*pauVar90) [32];
  undefined1 (*pauVar91) [32];
  undefined1 (*pauVar92) [32];
  undefined1 (*pauVar93) [32];
  undefined1 (*pauVar94) [32];
  undefined1 (*pauVar95) [32];
  uint uVar96;
  longlong lVar97;
  int iVar98;
  int iVar99;
  float fVar100;
  float fVar101;
  float fVar102;
  float fVar104;
  float fVar105;
  float fVar106;
  float fVar107;
  float fVar108;
  float fVar109;
  float fVar110;
  float fVar111;
  float fVar112;
  undefined1 auVar103 [32];
  float fVar114;
  float fVar115;
  float fVar116;
  undefined1 auVar113 [32];
  undefined1 auVar117 [32];
  undefined1 auVar118 [32];
  undefined1 auVar119 [32];
  undefined1 auVar120 [32];
  float fVar121;
  float fVar122;
  float fVar123;
  
  if (((ulonglong)param_3 & 0x3c) != 0) {
    uVar96 = 0x10 - (((uint)param_3 & 0x3c) >> 2);
    if ((int)param_4 <= (int)uVar96) {
      uVar96 = param_4;
    }
    param_4 = param_4 - uVar96;
    if (7 < (int)uVar96) {
      puVar80 = *param_1;
      fVar7 = *(float *)(*param_1 + 4);
      fVar8 = *(float *)(*param_1 + 8);
      fVar14 = *(float *)(*param_1 + 0xc);
      fVar15 = *(float *)(*param_1 + 0x10);
      fVar21 = *(float *)(*param_1 + 0x14);
      fVar22 = *(float *)(*param_1 + 0x18);
      fVar28 = *(float *)(*param_1 + 0x1c);
      param_1 = param_1 + 1;
      puVar81 = *param_2;
      fVar29 = *(float *)(*param_2 + 4);
      fVar9 = *(float *)(*param_2 + 8);
      fVar10 = *(float *)(*param_2 + 0xc);
      fVar11 = *(float *)(*param_2 + 0x10);
      fVar12 = *(float *)(*param_2 + 0x14);
      fVar16 = *(float *)(*param_2 + 0x18);
      fVar17 = *(float *)(*param_2 + 0x1c);
      fVar3 = *(float *)(*param_3 + 4);
      fVar4 = *(float *)(*param_3 + 8);
      fVar5 = *(float *)(*param_3 + 0xc);
      fVar6 = *(float *)(*param_3 + 0x10);
      fVar13 = *(float *)(*param_3 + 0x14);
      fVar20 = *(float *)(*param_3 + 0x18);
      fVar27 = *(float *)(*param_3 + 0x1c);
      param_2 = param_2 + 1;
      *(float *)*param_3 = *(float *)puVar81 * *(float *)puVar80 + *(float *)*param_3;
      *(float *)(*param_3 + 4) = fVar29 * fVar7 + fVar3;
      *(float *)(*param_3 + 8) = fVar9 * fVar8 + fVar4;
      *(float *)(*param_3 + 0xc) = fVar10 * fVar14 + fVar5;
      *(float *)(*param_3 + 0x10) = fVar11 * fVar15 + fVar6;
      *(float *)(*param_3 + 0x14) = fVar12 * fVar21 + fVar13;
      *(float *)(*param_3 + 0x18) = fVar16 * fVar22 + fVar20;
      *(float *)(*param_3 + 0x1c) = fVar17 * fVar28 + fVar27;
      param_3 = param_3 + 1;
      uVar96 = uVar96 - 8;
    }
    if (uVar96 != 0) {
      lVar97 = (longlong)(int)uVar96;
      auVar34 = vpsllw_avx(_DAT_181dfa050,ZEXT416(-uVar96 + 0xc));
      auVar35 = vpsllw_avx(_DAT_181dfa050,ZEXT416(-uVar96 + 8));
      auVar120 = vperm2f128_avx(ZEXT1632(auVar35),ZEXT1632(auVar34),0x20);
      auVar103 = vmaskmovps_avx(auVar120,*param_1);
      param_1 = (undefined1 (*) [32])(*param_1 + lVar97 * 4);
      auVar113 = vmaskmovps_avx(auVar120,*param_2);
      param_2 = (undefined1 (*) [32])(*param_2 + lVar97 * 4);
      auVar118 = vmaskmovps_avx(auVar120,*param_3);
      auVar117._0_4_ = auVar113._0_4_ * auVar103._0_4_ + auVar118._0_4_;
      auVar117._4_4_ = auVar113._4_4_ * auVar103._4_4_ + auVar118._4_4_;
      auVar117._8_4_ = auVar113._8_4_ * auVar103._8_4_ + auVar118._8_4_;
      auVar117._12_4_ = auVar113._12_4_ * auVar103._12_4_ + auVar118._12_4_;
      auVar117._16_4_ = auVar113._16_4_ * auVar103._16_4_ + auVar118._16_4_;
      auVar117._20_4_ = auVar113._20_4_ * auVar103._20_4_ + auVar118._20_4_;
      auVar117._24_4_ = auVar113._24_4_ * auVar103._24_4_ + auVar118._24_4_;
      auVar117._28_4_ = auVar113._28_4_ * auVar103._28_4_ + auVar118._28_4_;
      auVar103 = vmaskmovps_avx(auVar120,auVar117);
      *param_3 = auVar103;
      param_3 = (undefined1 (*) [32])(*param_3 + lVar97 * 4);
    }
  }
  iVar99 = (int)param_4 >> 5;
  if ((((ulonglong)param_1 | (ulonglong)param_2) & 0x1f) == 0) {
    if (param_5 == 0 && param_7 == 0) {
      iVar98 = 0;
      uVar96 = param_4 & 0x1f;
      if (0 < iVar99) {
        do {
          fVar9 = *(float *)(*param_1 + 4);
          fVar10 = *(float *)(*param_1 + 8);
          fVar11 = *(float *)(*param_1 + 0xc);
          fVar12 = *(float *)(*param_1 + 0x10);
          fVar16 = *(float *)(*param_1 + 0x14);
          fVar17 = *(float *)(*param_1 + 0x18);
          fVar18 = *(float *)(*param_1 + 0x1c);
          iVar98 = iVar98 + 1;
          fVar19 = *(float *)param_1[1];
          fVar23 = *(float *)(param_1[1] + 4);
          fVar24 = *(float *)(param_1[1] + 8);
          fVar25 = *(float *)(param_1[1] + 0xc);
          fVar26 = *(float *)(param_1[1] + 0x10);
          fVar30 = *(float *)(param_1[1] + 0x14);
          fVar31 = *(float *)(param_1[1] + 0x18);
          fVar32 = *(float *)(param_1[1] + 0x1c);
          fVar33 = *(float *)(*param_2 + 4);
          fVar36 = *(float *)(*param_2 + 8);
          fVar37 = *(float *)(*param_2 + 0xc);
          fVar38 = *(float *)(*param_2 + 0x10);
          fVar39 = *(float *)(*param_2 + 0x14);
          fVar40 = *(float *)(*param_2 + 0x18);
          fVar41 = *(float *)(*param_2 + 0x1c);
          fVar42 = *(float *)param_2[1];
          fVar43 = *(float *)(param_2[1] + 4);
          fVar44 = *(float *)(param_2[1] + 8);
          fVar45 = *(float *)(param_2[1] + 0xc);
          fVar46 = *(float *)(param_2[1] + 0x10);
          fVar114 = *(float *)(param_2[1] + 0x14);
          fVar115 = *(float *)(param_2[1] + 0x18);
          fVar116 = *(float *)(param_2[1] + 0x1c);
          fVar47 = *(float *)param_1[2];
          fVar48 = *(float *)(param_1[2] + 4);
          fVar49 = *(float *)(param_1[2] + 8);
          fVar50 = *(float *)(param_1[2] + 0xc);
          fVar51 = *(float *)(param_1[2] + 0x10);
          fVar52 = *(float *)(param_1[2] + 0x14);
          fVar53 = *(float *)(param_1[2] + 0x18);
          fVar54 = *(float *)(param_1[2] + 0x1c);
          fVar55 = *(float *)param_1[3];
          fVar56 = *(float *)(param_1[3] + 4);
          fVar57 = *(float *)(param_1[3] + 8);
          fVar58 = *(float *)(param_1[3] + 0xc);
          fVar59 = *(float *)(param_1[3] + 0x10);
          fVar60 = *(float *)(param_1[3] + 0x14);
          fVar61 = *(float *)(param_1[3] + 0x18);
          fVar62 = *(float *)(param_1[3] + 0x1c);
          fVar4 = *(float *)(*param_3 + 4);
          fVar6 = *(float *)(*param_3 + 8);
          fVar20 = *(float *)(*param_3 + 0xc);
          fVar7 = *(float *)(*param_3 + 0x10);
          fVar14 = *(float *)(*param_3 + 0x14);
          fVar21 = *(float *)(*param_3 + 0x18);
          fVar28 = *(float *)(*param_3 + 0x1c);
          fVar3 = *(float *)param_3[1];
          fVar5 = *(float *)(param_3[1] + 4);
          fVar13 = *(float *)(param_3[1] + 8);
          fVar27 = *(float *)(param_3[1] + 0xc);
          fVar8 = *(float *)(param_3[1] + 0x10);
          fVar15 = *(float *)(param_3[1] + 0x14);
          fVar22 = *(float *)(param_3[1] + 0x18);
          fVar29 = *(float *)(param_3[1] + 0x1c);
          fVar63 = *(float *)param_2[2];
          fVar64 = *(float *)(param_2[2] + 4);
          fVar65 = *(float *)(param_2[2] + 8);
          fVar66 = *(float *)(param_2[2] + 0xc);
          fVar67 = *(float *)(param_2[2] + 0x10);
          fVar68 = *(float *)(param_2[2] + 0x14);
          fVar69 = *(float *)(param_2[2] + 0x18);
          fVar70 = *(float *)(param_2[2] + 0x1c);
          fVar71 = *(float *)param_2[3];
          fVar72 = *(float *)(param_2[3] + 4);
          fVar73 = *(float *)(param_2[3] + 8);
          fVar74 = *(float *)(param_2[3] + 0xc);
          fVar75 = *(float *)(param_2[3] + 0x10);
          fVar76 = *(float *)(param_2[3] + 0x14);
          fVar77 = *(float *)(param_2[3] + 0x18);
          fVar78 = *(float *)(param_2[3] + 0x1c);
          *(float *)*param_3 = *(float *)*param_2 * *(float *)*param_1 + *(float *)*param_3;
          *(float *)(*param_3 + 4) = fVar33 * fVar9 + fVar4;
          *(float *)(*param_3 + 8) = fVar36 * fVar10 + fVar6;
          *(float *)(*param_3 + 0xc) = fVar37 * fVar11 + fVar20;
          *(float *)(*param_3 + 0x10) = fVar38 * fVar12 + fVar7;
          *(float *)(*param_3 + 0x14) = fVar39 * fVar16 + fVar14;
          *(float *)(*param_3 + 0x18) = fVar40 * fVar17 + fVar21;
          *(float *)(*param_3 + 0x1c) = fVar41 * fVar18 + fVar28;
          *(float *)param_3[1] = fVar42 * fVar19 + fVar3;
          *(float *)(param_3[1] + 4) = fVar43 * fVar23 + fVar5;
          *(float *)(param_3[1] + 8) = fVar44 * fVar24 + fVar13;
          *(float *)(param_3[1] + 0xc) = fVar45 * fVar25 + fVar27;
          *(float *)(param_3[1] + 0x10) = fVar46 * fVar26 + fVar8;
          *(float *)(param_3[1] + 0x14) = fVar114 * fVar30 + fVar15;
          *(float *)(param_3[1] + 0x18) = fVar115 * fVar31 + fVar22;
          *(float *)(param_3[1] + 0x1c) = fVar116 * fVar32 + fVar29;
          fVar4 = *(float *)(param_3[2] + 4);
          fVar6 = *(float *)(param_3[2] + 8);
          fVar20 = *(float *)(param_3[2] + 0xc);
          fVar7 = *(float *)(param_3[2] + 0x10);
          fVar14 = *(float *)(param_3[2] + 0x14);
          fVar21 = *(float *)(param_3[2] + 0x18);
          fVar28 = *(float *)(param_3[2] + 0x1c);
          fVar3 = *(float *)param_3[3];
          fVar5 = *(float *)(param_3[3] + 4);
          fVar13 = *(float *)(param_3[3] + 8);
          fVar27 = *(float *)(param_3[3] + 0xc);
          fVar8 = *(float *)(param_3[3] + 0x10);
          fVar15 = *(float *)(param_3[3] + 0x14);
          fVar22 = *(float *)(param_3[3] + 0x18);
          fVar29 = *(float *)(param_3[3] + 0x1c);
          *(float *)param_3[2] = fVar63 * fVar47 + *(float *)param_3[2];
          *(float *)(param_3[2] + 4) = fVar64 * fVar48 + fVar4;
          *(float *)(param_3[2] + 8) = fVar65 * fVar49 + fVar6;
          *(float *)(param_3[2] + 0xc) = fVar66 * fVar50 + fVar20;
          *(float *)(param_3[2] + 0x10) = fVar67 * fVar51 + fVar7;
          *(float *)(param_3[2] + 0x14) = fVar68 * fVar52 + fVar14;
          *(float *)(param_3[2] + 0x18) = fVar69 * fVar53 + fVar21;
          *(float *)(param_3[2] + 0x1c) = fVar70 * fVar54 + fVar28;
          *(float *)param_3[3] = fVar71 * fVar55 + fVar3;
          *(float *)(param_3[3] + 4) = fVar72 * fVar56 + fVar5;
          *(float *)(param_3[3] + 8) = fVar73 * fVar57 + fVar13;
          *(float *)(param_3[3] + 0xc) = fVar74 * fVar58 + fVar27;
          *(float *)(param_3[3] + 0x10) = fVar75 * fVar59 + fVar8;
          *(float *)(param_3[3] + 0x14) = fVar76 * fVar60 + fVar15;
          *(float *)(param_3[3] + 0x18) = fVar77 * fVar61 + fVar22;
          *(float *)(param_3[3] + 0x1c) = fVar78 * fVar62 + fVar29;
          param_1 = param_1 + 4;
          param_2 = param_2 + 4;
          param_3 = param_3 + 4;
        } while (iVar98 < iVar99);
      }
      if ((param_4 & 0x10) != 0) {
        fVar9 = *(float *)(*param_1 + 4);
        fVar10 = *(float *)(*param_1 + 8);
        fVar11 = *(float *)(*param_1 + 0xc);
        fVar12 = *(float *)(*param_1 + 0x10);
        fVar16 = *(float *)(*param_1 + 0x14);
        fVar17 = *(float *)(*param_1 + 0x18);
        fVar18 = *(float *)(*param_1 + 0x1c);
        uVar96 = uVar96 - 0x10;
        fVar19 = *(float *)param_1[1];
        fVar23 = *(float *)(param_1[1] + 4);
        fVar24 = *(float *)(param_1[1] + 8);
        fVar25 = *(float *)(param_1[1] + 0xc);
        fVar26 = *(float *)(param_1[1] + 0x10);
        fVar30 = *(float *)(param_1[1] + 0x14);
        fVar31 = *(float *)(param_1[1] + 0x18);
        fVar32 = *(float *)(param_1[1] + 0x1c);
        fVar33 = *(float *)(*param_2 + 4);
        fVar36 = *(float *)(*param_2 + 8);
        fVar37 = *(float *)(*param_2 + 0xc);
        fVar38 = *(float *)(*param_2 + 0x10);
        fVar39 = *(float *)(*param_2 + 0x14);
        fVar40 = *(float *)(*param_2 + 0x18);
        fVar41 = *(float *)(*param_2 + 0x1c);
        fVar42 = *(float *)param_2[1];
        fVar43 = *(float *)(param_2[1] + 4);
        fVar44 = *(float *)(param_2[1] + 8);
        fVar45 = *(float *)(param_2[1] + 0xc);
        fVar46 = *(float *)(param_2[1] + 0x10);
        fVar114 = *(float *)(param_2[1] + 0x14);
        fVar115 = *(float *)(param_2[1] + 0x18);
        fVar116 = *(float *)(param_2[1] + 0x1c);
        fVar4 = *(float *)(*param_3 + 4);
        fVar6 = *(float *)(*param_3 + 8);
        fVar20 = *(float *)(*param_3 + 0xc);
        fVar7 = *(float *)(*param_3 + 0x10);
        fVar14 = *(float *)(*param_3 + 0x14);
        fVar21 = *(float *)(*param_3 + 0x18);
        fVar28 = *(float *)(*param_3 + 0x1c);
        fVar3 = *(float *)param_3[1];
        fVar5 = *(float *)(param_3[1] + 4);
        fVar13 = *(float *)(param_3[1] + 8);
        fVar27 = *(float *)(param_3[1] + 0xc);
        fVar8 = *(float *)(param_3[1] + 0x10);
        fVar15 = *(float *)(param_3[1] + 0x14);
        fVar22 = *(float *)(param_3[1] + 0x18);
        fVar29 = *(float *)(param_3[1] + 0x1c);
        *(float *)*param_3 = *(float *)*param_2 * *(float *)*param_1 + *(float *)*param_3;
        *(float *)(*param_3 + 4) = fVar33 * fVar9 + fVar4;
        *(float *)(*param_3 + 8) = fVar36 * fVar10 + fVar6;
        *(float *)(*param_3 + 0xc) = fVar37 * fVar11 + fVar20;
        *(float *)(*param_3 + 0x10) = fVar38 * fVar12 + fVar7;
        *(float *)(*param_3 + 0x14) = fVar39 * fVar16 + fVar14;
        *(float *)(*param_3 + 0x18) = fVar40 * fVar17 + fVar21;
        *(float *)(*param_3 + 0x1c) = fVar41 * fVar18 + fVar28;
        *(float *)param_3[1] = fVar42 * fVar19 + fVar3;
        *(float *)(param_3[1] + 4) = fVar43 * fVar23 + fVar5;
        *(float *)(param_3[1] + 8) = fVar44 * fVar24 + fVar13;
        *(float *)(param_3[1] + 0xc) = fVar45 * fVar25 + fVar27;
        *(float *)(param_3[1] + 0x10) = fVar46 * fVar26 + fVar8;
        *(float *)(param_3[1] + 0x14) = fVar114 * fVar30 + fVar15;
        *(float *)(param_3[1] + 0x18) = fVar115 * fVar31 + fVar22;
        *(float *)(param_3[1] + 0x1c) = fVar116 * fVar32 + fVar29;
        param_1 = param_1 + 2;
        param_2 = param_2 + 2;
        param_3 = param_3 + 2;
      }
    }
    else {
      iVar99 = 0;
      uVar96 = param_4 & 0xf;
      if (0 < (int)param_4 >> 4) {
        do {
          fVar9 = *(float *)param_1[1];
          fVar10 = *(float *)(param_1[1] + 4);
          fVar11 = *(float *)(param_1[1] + 8);
          fVar12 = *(float *)(param_1[1] + 0xc);
          fVar30 = *(float *)(*param_2 + 4);
          fVar31 = *(float *)(*param_2 + 8);
          fVar32 = *(float *)(*param_2 + 0xc);
          fVar23 = *(float *)(*param_1 + 0x10);
          fVar24 = *(float *)(*param_1 + 0x14);
          fVar25 = *(float *)(*param_1 + 0x18);
          fVar26 = *(float *)(*param_1 + 0x1c);
          fVar116 = *(float *)(*param_1 + 0xc);
          fVar115 = *(float *)(*param_1 + 8);
          fVar114 = *(float *)(*param_1 + 4);
          fVar16 = *(float *)(param_1[1] + 0x10);
          fVar17 = *(float *)(param_1[1] + 0x14);
          fVar18 = *(float *)(param_1[1] + 0x18);
          fVar19 = *(float *)(param_1[1] + 0x1c);
          fVar39 = *(float *)param_2[1];
          fVar40 = *(float *)(param_2[1] + 4);
          fVar41 = *(float *)(param_2[1] + 8);
          fVar42 = *(float *)(param_2[1] + 0xc);
          fVar33 = *(float *)(*param_2 + 0x10);
          fVar36 = *(float *)(*param_2 + 0x14);
          fVar37 = *(float *)(*param_2 + 0x18);
          fVar38 = *(float *)(*param_2 + 0x1c);
          fVar4 = *(float *)(*param_3 + 4);
          fVar6 = *(float *)(*param_3 + 8);
          fVar20 = *(float *)(*param_3 + 0xc);
          fVar7 = *(float *)(*param_3 + 0x10);
          fVar14 = *(float *)(*param_3 + 0x14);
          fVar21 = *(float *)(*param_3 + 0x18);
          fVar28 = *(float *)(*param_3 + 0x1c);
          fVar43 = *(float *)(param_2[1] + 0x10);
          fVar44 = *(float *)(param_2[1] + 0x14);
          fVar45 = *(float *)(param_2[1] + 0x18);
          fVar46 = *(float *)(param_2[1] + 0x1c);
          fVar3 = *(float *)param_3[1];
          fVar5 = *(float *)(param_3[1] + 4);
          fVar13 = *(float *)(param_3[1] + 8);
          fVar27 = *(float *)(param_3[1] + 0xc);
          fVar8 = *(float *)(param_3[1] + 0x10);
          fVar15 = *(float *)(param_3[1] + 0x14);
          fVar22 = *(float *)(param_3[1] + 0x18);
          fVar29 = *(float *)(param_3[1] + 0x1c);
          *(float *)*param_3 = *(float *)*param_2 * *(float *)*param_1 + *(float *)*param_3;
          *(float *)(*param_3 + 4) = fVar30 * fVar114 + fVar4;
          *(float *)(*param_3 + 8) = fVar31 * fVar115 + fVar6;
          *(float *)(*param_3 + 0xc) = fVar32 * fVar116 + fVar20;
          *(float *)(*param_3 + 0x10) = fVar33 * fVar23 + fVar7;
          *(float *)(*param_3 + 0x14) = fVar36 * fVar24 + fVar14;
          *(float *)(*param_3 + 0x18) = fVar37 * fVar25 + fVar21;
          *(float *)(*param_3 + 0x1c) = fVar38 * fVar26 + fVar28;
          *(float *)param_3[1] = fVar39 * fVar9 + fVar3;
          *(float *)(param_3[1] + 4) = fVar40 * fVar10 + fVar5;
          *(float *)(param_3[1] + 8) = fVar41 * fVar11 + fVar13;
          *(float *)(param_3[1] + 0xc) = fVar42 * fVar12 + fVar27;
          *(float *)(param_3[1] + 0x10) = fVar43 * fVar16 + fVar8;
          *(float *)(param_3[1] + 0x14) = fVar44 * fVar17 + fVar15;
          *(float *)(param_3[1] + 0x18) = fVar45 * fVar18 + fVar22;
          *(float *)(param_3[1] + 0x1c) = fVar46 * fVar19 + fVar29;
          iVar99 = iVar99 + 1;
          param_1 = param_1 + 2;
          param_2 = param_2 + 2;
          param_3 = param_3 + 2;
        } while (iVar99 < (int)param_4 >> 4);
      }
    }
  }
  else {
    iVar98 = 0;
    uVar96 = param_4 & 0x1f;
    if (param_5 == 0 && param_7 == 0) {
      if (0 < iVar99) {
        do {
          pauVar1 = param_1 + 3;
          pauVar82 = param_1 + 3;
          pauVar83 = param_1 + 3;
          pauVar84 = param_1 + 3;
          iVar98 = iVar98 + 1;
          auVar120._0_4_ = *(float *)*param_2 * *(float *)*param_1 + *(float *)*param_3;
          auVar120._4_4_ =
               *(float *)(*param_2 + 4) * *(float *)(*param_1 + 4) + *(float *)(*param_3 + 4);
          auVar120._8_4_ =
               *(float *)(*param_2 + 8) * *(float *)(*param_1 + 8) + *(float *)(*param_3 + 8);
          auVar120._12_4_ =
               *(float *)(*param_2 + 0xc) * *(float *)(*param_1 + 0xc) + *(float *)(*param_3 + 0xc);
          auVar120._16_4_ =
               *(float *)(*param_2 + 0x10) * *(float *)(*param_1 + 0x10) +
               *(float *)(*param_3 + 0x10);
          auVar120._20_4_ =
               *(float *)(*param_2 + 0x14) * *(float *)(*param_1 + 0x14) +
               *(float *)(*param_3 + 0x14);
          auVar120._24_4_ =
               *(float *)(*param_2 + 0x18) * *(float *)(*param_1 + 0x18) +
               *(float *)(*param_3 + 0x18);
          auVar120._28_4_ =
               *(float *)(*param_2 + 0x1c) * *(float *)(*param_1 + 0x1c) +
               *(float *)(*param_3 + 0x1c);
          auVar118._0_4_ = *(float *)param_2[1] * *(float *)param_1[1] + *(float *)param_3[1];
          auVar118._4_4_ =
               *(float *)(param_2[1] + 4) * *(float *)(param_1[1] + 4) + *(float *)(param_3[1] + 4);
          auVar118._8_4_ =
               *(float *)(param_2[1] + 8) * *(float *)(param_1[1] + 8) + *(float *)(param_3[1] + 8);
          auVar118._12_4_ =
               *(float *)(param_2[1] + 0xc) * *(float *)(param_1[1] + 0xc) +
               *(float *)(param_3[1] + 0xc);
          auVar118._16_4_ =
               *(float *)(param_2[1] + 0x10) * *(float *)(param_1[1] + 0x10) +
               *(float *)(param_3[1] + 0x10);
          auVar118._20_4_ =
               *(float *)(param_2[1] + 0x14) * *(float *)(param_1[1] + 0x14) +
               *(float *)(param_3[1] + 0x14);
          auVar118._24_4_ =
               *(float *)(param_2[1] + 0x18) * *(float *)(param_1[1] + 0x18) +
               *(float *)(param_3[1] + 0x18);
          auVar118._28_4_ =
               *(float *)(param_2[1] + 0x1c) * *(float *)(param_1[1] + 0x1c) +
               *(float *)(param_3[1] + 0x1c);
          pauVar2 = param_2 + 3;
          pauVar85 = param_2 + 3;
          pauVar86 = param_2 + 3;
          pauVar87 = param_2 + 3;
          auVar113._0_4_ = *(float *)param_2[2] * *(float *)param_1[2] + *(float *)param_3[2];
          auVar113._4_4_ =
               *(float *)(param_2[2] + 4) * *(float *)(param_1[2] + 4) + *(float *)(param_3[2] + 4);
          auVar113._8_4_ =
               *(float *)(param_2[2] + 8) * *(float *)(param_1[2] + 8) + *(float *)(param_3[2] + 8);
          auVar113._12_4_ =
               *(float *)(param_2[2] + 0xc) * *(float *)(param_1[2] + 0xc) +
               *(float *)(param_3[2] + 0xc);
          auVar113._16_4_ =
               *(float *)(param_2[2] + 0x10) * *(float *)(param_1[2] + 0x10) +
               *(float *)(param_3[2] + 0x10);
          auVar113._20_4_ =
               *(float *)(param_2[2] + 0x14) * *(float *)(param_1[2] + 0x14) +
               *(float *)(param_3[2] + 0x14);
          auVar113._24_4_ =
               *(float *)(param_2[2] + 0x18) * *(float *)(param_1[2] + 0x18) +
               *(float *)(param_3[2] + 0x18);
          auVar113._28_4_ =
               *(float *)(param_2[2] + 0x1c) * *(float *)(param_1[2] + 0x1c) +
               *(float *)(param_3[2] + 0x1c);
          pauVar88 = param_1 + 3;
          pauVar89 = param_1 + 3;
          pauVar90 = param_1 + 3;
          pauVar91 = param_1 + 3;
          param_1 = param_1 + 4;
          pauVar92 = param_2 + 3;
          pauVar93 = param_2 + 3;
          pauVar94 = param_2 + 3;
          pauVar95 = param_2 + 3;
          param_2 = param_2 + 4;
          auVar103._0_4_ = *(float *)*pauVar2 * *(float *)*pauVar1 + *(float *)param_3[3];
          auVar103._4_4_ =
               *(float *)(*pauVar85 + 4) * *(float *)(*pauVar82 + 4) + *(float *)(param_3[3] + 4);
          auVar103._8_4_ =
               *(float *)(*pauVar86 + 8) * *(float *)(*pauVar83 + 8) + *(float *)(param_3[3] + 8);
          auVar103._12_4_ =
               *(float *)(*pauVar87 + 0xc) * *(float *)(*pauVar84 + 0xc) +
               *(float *)(param_3[3] + 0xc);
          auVar103._16_4_ =
               *(float *)(*pauVar92 + 0x10) * *(float *)(*pauVar88 + 0x10) +
               *(float *)(param_3[3] + 0x10);
          auVar103._20_4_ =
               *(float *)(*pauVar93 + 0x14) * *(float *)(*pauVar89 + 0x14) +
               *(float *)(param_3[3] + 0x14);
          auVar103._24_4_ =
               *(float *)(*pauVar94 + 0x18) * *(float *)(*pauVar90 + 0x18) +
               *(float *)(param_3[3] + 0x18);
          auVar103._28_4_ =
               *(float *)(*pauVar95 + 0x1c) * *(float *)(*pauVar91 + 0x1c) +
               *(float *)(param_3[3] + 0x1c);
          *param_3 = auVar120;
          param_3[1] = auVar118;
          param_3[2] = auVar113;
          param_3[3] = auVar103;
          param_3 = param_3 + 4;
        } while (iVar98 < iVar99);
        FUN_18006d291();
        return;
      }
    }
    else if (0 < iVar99) {
      do {
        fVar68 = *(float *)param_1[1];
        fVar69 = *(float *)(param_1[1] + 4);
        fVar70 = *(float *)(param_1[1] + 8);
        fVar71 = *(float *)(param_1[1] + 0xc);
        fVar60 = *(float *)param_1[2];
        fVar61 = *(float *)(param_1[2] + 4);
        fVar62 = *(float *)(param_1[2] + 8);
        fVar63 = *(float *)(param_1[2] + 0xc);
        fVar76 = *(float *)(*param_1 + 0x10);
        fVar77 = *(float *)(*param_1 + 0x14);
        fVar78 = *(float *)(*param_1 + 0x18);
        fVar79 = *(float *)(*param_1 + 0x1c);
        fVar123 = *(float *)(*param_1 + 0xc);
        fVar122 = *(float *)(*param_1 + 8);
        fVar121 = *(float *)(*param_1 + 4);
        puVar80 = *param_1;
        fVar72 = *(float *)(param_1[1] + 0x10);
        fVar73 = *(float *)(param_1[1] + 0x14);
        fVar74 = *(float *)(param_1[1] + 0x18);
        fVar75 = *(float *)(param_1[1] + 0x1c);
        fVar52 = *(float *)param_1[3];
        fVar53 = *(float *)(param_1[3] + 4);
        fVar54 = *(float *)(param_1[3] + 8);
        fVar55 = *(float *)(param_1[3] + 0xc);
        fVar115 = *(float *)(*param_2 + 4);
        fVar116 = *(float *)(*param_2 + 8);
        fVar47 = *(float *)(*param_2 + 0xc);
        fVar64 = *(float *)(param_1[2] + 0x10);
        fVar65 = *(float *)(param_1[2] + 0x14);
        fVar66 = *(float *)(param_1[2] + 0x18);
        fVar67 = *(float *)(param_1[2] + 0x1c);
        fVar56 = *(float *)(param_1[3] + 0x10);
        fVar57 = *(float *)(param_1[3] + 0x14);
        fVar58 = *(float *)(param_1[3] + 0x18);
        fVar59 = *(float *)(param_1[3] + 0x1c);
        iVar98 = iVar98 + 1;
        fVar48 = *(float *)(*param_2 + 0x10);
        fVar49 = *(float *)(*param_2 + 0x14);
        fVar50 = *(float *)(*param_2 + 0x18);
        fVar51 = *(float *)(*param_2 + 0x1c);
        param_1 = param_1 + 4;
        fVar36 = *(float *)(param_2[1] + 0x10);
        fVar37 = *(float *)(param_2[1] + 0x14);
        fVar38 = *(float *)(param_2[1] + 0x18);
        fVar39 = *(float *)(param_2[1] + 0x1c);
        fVar110 = *(float *)(param_2[1] + 0xc);
        fVar107 = *(float *)(param_2[1] + 8);
        fVar104 = *(float *)(param_2[1] + 4);
        fVar100 = *(float *)param_2[1];
        fVar6 = *(float *)(*param_3 + 4);
        fVar7 = *(float *)(*param_3 + 8);
        fVar21 = *(float *)(*param_3 + 0xc);
        fVar9 = *(float *)(*param_3 + 0x10);
        fVar16 = *(float *)(*param_3 + 0x14);
        fVar23 = *(float *)(*param_3 + 0x18);
        fVar30 = *(float *)(*param_3 + 0x1c);
        fVar3 = *(float *)param_3[1];
        fVar13 = *(float *)(param_3[1] + 4);
        fVar8 = *(float *)(param_3[1] + 8);
        fVar22 = *(float *)(param_3[1] + 0xc);
        fVar10 = *(float *)(param_3[1] + 0x10);
        fVar17 = *(float *)(param_3[1] + 0x14);
        fVar24 = *(float *)(param_3[1] + 0x18);
        fVar31 = *(float *)(param_3[1] + 0x1c);
        fVar40 = *(float *)(param_2[2] + 0x10);
        fVar41 = *(float *)(param_2[2] + 0x14);
        fVar42 = *(float *)(param_2[2] + 0x18);
        fVar43 = *(float *)(param_2[2] + 0x1c);
        fVar111 = *(float *)(param_2[2] + 0xc);
        fVar108 = *(float *)(param_2[2] + 8);
        fVar105 = *(float *)(param_2[2] + 4);
        fVar101 = *(float *)param_2[2];
        fVar4 = *(float *)param_3[2];
        fVar20 = *(float *)(param_3[2] + 4);
        fVar14 = *(float *)(param_3[2] + 8);
        fVar28 = *(float *)(param_3[2] + 0xc);
        fVar11 = *(float *)(param_3[2] + 0x10);
        fVar18 = *(float *)(param_3[2] + 0x14);
        fVar25 = *(float *)(param_3[2] + 0x18);
        fVar32 = *(float *)(param_3[2] + 0x1c);
        fVar44 = *(float *)(param_2[3] + 0x10);
        fVar45 = *(float *)(param_2[3] + 0x14);
        fVar46 = *(float *)(param_2[3] + 0x18);
        fVar114 = *(float *)(param_2[3] + 0x1c);
        fVar112 = *(float *)(param_2[3] + 0xc);
        fVar109 = *(float *)(param_2[3] + 8);
        fVar106 = *(float *)(param_2[3] + 4);
        fVar102 = *(float *)param_2[3];
        fVar5 = *(float *)param_3[3];
        fVar27 = *(float *)(param_3[3] + 4);
        fVar15 = *(float *)(param_3[3] + 8);
        fVar29 = *(float *)(param_3[3] + 0xc);
        fVar12 = *(float *)(param_3[3] + 0x10);
        fVar19 = *(float *)(param_3[3] + 0x14);
        fVar26 = *(float *)(param_3[3] + 0x18);
        fVar33 = *(float *)(param_3[3] + 0x1c);
        *(float *)*param_3 = *(float *)*param_2 * *(float *)puVar80 + *(float *)*param_3;
        *(float *)(*param_3 + 4) = fVar115 * fVar121 + fVar6;
        *(float *)(*param_3 + 8) = fVar116 * fVar122 + fVar7;
        *(float *)(*param_3 + 0xc) = fVar47 * fVar123 + fVar21;
        *(float *)(*param_3 + 0x10) = fVar48 * fVar76 + fVar9;
        *(float *)(*param_3 + 0x14) = fVar49 * fVar77 + fVar16;
        *(float *)(*param_3 + 0x18) = fVar50 * fVar78 + fVar23;
        *(float *)(*param_3 + 0x1c) = fVar51 * fVar79 + fVar30;
        *(float *)param_3[1] = fVar100 * fVar68 + fVar3;
        *(float *)(param_3[1] + 4) = fVar104 * fVar69 + fVar13;
        *(float *)(param_3[1] + 8) = fVar107 * fVar70 + fVar8;
        *(float *)(param_3[1] + 0xc) = fVar110 * fVar71 + fVar22;
        *(float *)(param_3[1] + 0x10) = fVar36 * fVar72 + fVar10;
        *(float *)(param_3[1] + 0x14) = fVar37 * fVar73 + fVar17;
        *(float *)(param_3[1] + 0x18) = fVar38 * fVar74 + fVar24;
        *(float *)(param_3[1] + 0x1c) = fVar39 * fVar75 + fVar31;
        *(float *)param_3[2] = fVar101 * fVar60 + fVar4;
        *(float *)(param_3[2] + 4) = fVar105 * fVar61 + fVar20;
        *(float *)(param_3[2] + 8) = fVar108 * fVar62 + fVar14;
        *(float *)(param_3[2] + 0xc) = fVar111 * fVar63 + fVar28;
        *(float *)(param_3[2] + 0x10) = fVar40 * fVar64 + fVar11;
        *(float *)(param_3[2] + 0x14) = fVar41 * fVar65 + fVar18;
        *(float *)(param_3[2] + 0x18) = fVar42 * fVar66 + fVar25;
        *(float *)(param_3[2] + 0x1c) = fVar43 * fVar67 + fVar32;
        *(float *)param_3[3] = fVar102 * fVar52 + fVar5;
        *(float *)(param_3[3] + 4) = fVar106 * fVar53 + fVar27;
        *(float *)(param_3[3] + 8) = fVar109 * fVar54 + fVar15;
        *(float *)(param_3[3] + 0xc) = fVar112 * fVar55 + fVar29;
        *(float *)(param_3[3] + 0x10) = fVar44 * fVar56 + fVar12;
        *(float *)(param_3[3] + 0x14) = fVar45 * fVar57 + fVar19;
        *(float *)(param_3[3] + 0x18) = fVar46 * fVar58 + fVar26;
        *(float *)(param_3[3] + 0x1c) = fVar114 * fVar59 + fVar33;
        param_2 = param_2 + 4;
        param_3 = param_3 + 4;
      } while (iVar98 < iVar99);
    }
    if ((param_4 & 0x10) != 0) {
      fVar9 = *(float *)param_1[1];
      fVar10 = *(float *)(param_1[1] + 4);
      fVar11 = *(float *)(param_1[1] + 8);
      fVar12 = *(float *)(param_1[1] + 0xc);
      puVar80 = *param_2;
      fVar30 = *(float *)(*param_2 + 4);
      fVar31 = *(float *)(*param_2 + 8);
      fVar32 = *(float *)(*param_2 + 0xc);
      fVar39 = *(float *)param_2[1];
      fVar40 = *(float *)(param_2[1] + 4);
      fVar41 = *(float *)(param_2[1] + 8);
      fVar42 = *(float *)(param_2[1] + 0xc);
      uVar96 = uVar96 - 0x10;
      fVar23 = *(float *)(*param_1 + 0x10);
      fVar24 = *(float *)(*param_1 + 0x14);
      fVar25 = *(float *)(*param_1 + 0x18);
      fVar26 = *(float *)(*param_1 + 0x1c);
      fVar116 = *(float *)(*param_1 + 0xc);
      fVar115 = *(float *)(*param_1 + 8);
      fVar114 = *(float *)(*param_1 + 4);
      puVar81 = *param_1;
      fVar16 = *(float *)(param_1[1] + 0x10);
      fVar17 = *(float *)(param_1[1] + 0x14);
      fVar18 = *(float *)(param_1[1] + 0x18);
      fVar19 = *(float *)(param_1[1] + 0x1c);
      param_1 = param_1 + 2;
      fVar33 = *(float *)(*param_2 + 0x10);
      fVar36 = *(float *)(*param_2 + 0x14);
      fVar37 = *(float *)(*param_2 + 0x18);
      fVar38 = *(float *)(*param_2 + 0x1c);
      fVar43 = *(float *)(param_2[1] + 0x10);
      fVar44 = *(float *)(param_2[1] + 0x14);
      fVar45 = *(float *)(param_2[1] + 0x18);
      fVar46 = *(float *)(param_2[1] + 0x1c);
      param_2 = param_2 + 2;
      fVar4 = *(float *)(*param_3 + 4);
      fVar6 = *(float *)(*param_3 + 8);
      fVar20 = *(float *)(*param_3 + 0xc);
      fVar7 = *(float *)(*param_3 + 0x10);
      fVar14 = *(float *)(*param_3 + 0x14);
      fVar21 = *(float *)(*param_3 + 0x18);
      fVar28 = *(float *)(*param_3 + 0x1c);
      fVar3 = *(float *)param_3[1];
      fVar5 = *(float *)(param_3[1] + 4);
      fVar13 = *(float *)(param_3[1] + 8);
      fVar27 = *(float *)(param_3[1] + 0xc);
      fVar8 = *(float *)(param_3[1] + 0x10);
      fVar15 = *(float *)(param_3[1] + 0x14);
      fVar22 = *(float *)(param_3[1] + 0x18);
      fVar29 = *(float *)(param_3[1] + 0x1c);
      *(float *)*param_3 = *(float *)puVar80 * *(float *)puVar81 + *(float *)*param_3;
      *(float *)(*param_3 + 4) = fVar30 * fVar114 + fVar4;
      *(float *)(*param_3 + 8) = fVar31 * fVar115 + fVar6;
      *(float *)(*param_3 + 0xc) = fVar32 * fVar116 + fVar20;
      *(float *)(*param_3 + 0x10) = fVar33 * fVar23 + fVar7;
      *(float *)(*param_3 + 0x14) = fVar36 * fVar24 + fVar14;
      *(float *)(*param_3 + 0x18) = fVar37 * fVar25 + fVar21;
      *(float *)(*param_3 + 0x1c) = fVar38 * fVar26 + fVar28;
      *(float *)param_3[1] = fVar39 * fVar9 + fVar3;
      *(float *)(param_3[1] + 4) = fVar40 * fVar10 + fVar5;
      *(float *)(param_3[1] + 8) = fVar41 * fVar11 + fVar13;
      *(float *)(param_3[1] + 0xc) = fVar42 * fVar12 + fVar27;
      *(float *)(param_3[1] + 0x10) = fVar43 * fVar16 + fVar8;
      *(float *)(param_3[1] + 0x14) = fVar44 * fVar17 + fVar15;
      *(float *)(param_3[1] + 0x18) = fVar45 * fVar18 + fVar22;
      *(float *)(param_3[1] + 0x1c) = fVar46 * fVar19 + fVar29;
      param_3 = param_3 + 2;
    }
  }
  if (uVar96 != 0) {
    if (7 < (int)uVar96) {
      puVar80 = *param_1;
      fVar7 = *(float *)(*param_1 + 4);
      fVar8 = *(float *)(*param_1 + 8);
      fVar14 = *(float *)(*param_1 + 0xc);
      fVar15 = *(float *)(*param_1 + 0x10);
      fVar21 = *(float *)(*param_1 + 0x14);
      fVar22 = *(float *)(*param_1 + 0x18);
      fVar28 = *(float *)(*param_1 + 0x1c);
      param_1 = param_1 + 1;
      puVar81 = *param_2;
      fVar29 = *(float *)(*param_2 + 4);
      fVar9 = *(float *)(*param_2 + 8);
      fVar10 = *(float *)(*param_2 + 0xc);
      fVar11 = *(float *)(*param_2 + 0x10);
      fVar12 = *(float *)(*param_2 + 0x14);
      fVar16 = *(float *)(*param_2 + 0x18);
      fVar17 = *(float *)(*param_2 + 0x1c);
      fVar3 = *(float *)(*param_3 + 4);
      fVar4 = *(float *)(*param_3 + 8);
      fVar5 = *(float *)(*param_3 + 0xc);
      fVar6 = *(float *)(*param_3 + 0x10);
      fVar13 = *(float *)(*param_3 + 0x14);
      fVar20 = *(float *)(*param_3 + 0x18);
      fVar27 = *(float *)(*param_3 + 0x1c);
      param_2 = param_2 + 1;
      *(float *)*param_3 = *(float *)puVar81 * *(float *)puVar80 + *(float *)*param_3;
      *(float *)(*param_3 + 4) = fVar29 * fVar7 + fVar3;
      *(float *)(*param_3 + 8) = fVar9 * fVar8 + fVar4;
      *(float *)(*param_3 + 0xc) = fVar10 * fVar14 + fVar5;
      *(float *)(*param_3 + 0x10) = fVar11 * fVar15 + fVar6;
      *(float *)(*param_3 + 0x14) = fVar12 * fVar21 + fVar13;
      *(float *)(*param_3 + 0x18) = fVar16 * fVar22 + fVar20;
      *(float *)(*param_3 + 0x1c) = fVar17 * fVar28 + fVar27;
      param_3 = param_3 + 1;
      uVar96 = uVar96 - 8;
      if (uVar96 == 0) {
        return;
      }
    }
    auVar34 = vpsllw_avx(_DAT_181dfa050,ZEXT416(-uVar96 + 0xc));
    auVar35 = vpsllw_avx(_DAT_181dfa050,ZEXT416(-uVar96 + 8));
    auVar120 = vperm2f128_avx(ZEXT1632(auVar35),ZEXT1632(auVar34),0x20);
    auVar103 = vmaskmovps_avx(auVar120,*param_1);
    auVar113 = vmaskmovps_avx(auVar120,*param_2);
    auVar118 = vmaskmovps_avx(auVar120,*param_3);
    auVar119._0_4_ = auVar113._0_4_ * auVar103._0_4_ + auVar118._0_4_;
    auVar119._4_4_ = auVar113._4_4_ * auVar103._4_4_ + auVar118._4_4_;
    auVar119._8_4_ = auVar113._8_4_ * auVar103._8_4_ + auVar118._8_4_;
    auVar119._12_4_ = auVar113._12_4_ * auVar103._12_4_ + auVar118._12_4_;
    auVar119._16_4_ = auVar113._16_4_ * auVar103._16_4_ + auVar118._16_4_;
    auVar119._20_4_ = auVar113._20_4_ * auVar103._20_4_ + auVar118._20_4_;
    auVar119._24_4_ = auVar113._24_4_ * auVar103._24_4_ + auVar118._24_4_;
    auVar119._28_4_ = auVar113._28_4_ * auVar103._28_4_ + auVar118._28_4_;
    auVar103 = vmaskmovps_avx(auVar120,auVar119);
    *param_3 = auVar103;
  }
  return;
}


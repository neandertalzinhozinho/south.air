// IDA 9.3  rva=0x8c02f0  start=0x1808c02f0  size=2079
void __fastcall sub_1808C02F0(__m128i *a1, __int128 *a2, __m128i *a3, __m128i *a4, __int64 a5)
{
  __int64 *v5; // r10
  __int64 v6; // r12
  __int128 *v7; // rbx
  __int128 *v9; // rax
  __int64 v10; // rdx
  __int128 v11; // xmm0
  __int128 v12; // xmm1
  __int128 v13; // xmm0
  __int128 v14; // xmm1
  __int128 v15; // xmm0
  __int128 v16; // xmm1
  __int128 v17; // xmm0
  __int128 v18; // xmm1
  __int128 v19; // xmm0
  __int64 v20; // rdi
  unsigned int v21; // esi
  __int64 v22; // r8
  __int64 v23; // r15
  int v24; // edx
  int v25; // ecx
  __int128 *v26; // rax
  __m128i v27; // xmm1
  __int64 v28; // rcx
  __m128i v29; // xmm2
  __m128i v30; // xmm0
  __m128i v31; // xmm1
  __m128i v32; // xmm0
  __m128i v33; // xmm1
  __m128i v34; // xmm0
  __m128i v35; // xmm1
  __int128 v36; // xmm0
  __int128 v37; // xmm1
  __int128 v38; // xmm0
  __int128 v39; // xmm1
  __int128 v40; // xmm0
  __int128 v41; // xmm1
  __int128 v42; // xmm0
  __int128 v43; // xmm1
  __m128i *v44; // rcx
  __int64 v45; // rdx
  __m128i *v46; // rax
  __m128i v47; // xmm0
  __m128i v48; // xmm1
  __m128i v49; // xmm0
  __m128i v50; // xmm1
  __m128i v51; // xmm0
  __m128i v52; // xmm1
  __m128i v53; // xmm0
  __m128i v54; // xmm1
  int v55; // eax
  __int64 v56; // rbx
  __int64 v57; // r14
  __int64 v58; // rbx
  __int64 v59; // r14
  int v60; // r9d
  unsigned int v61; // r14d
  __int64 v62; // r8
  int v63; // edx
  int v64; // ecx
  __m128i *v65; // rax
  __int64 v66; // rdx
  __m128i *v67; // rcx
  __m128i v68; // xmm0
  __m128i v69; // xmm1
  __m128i v70; // xmm0
  __m128i v71; // xmm1
  __m128i v72; // xmm0
  __m128i v73; // xmm1
  __m128i v74; // xmm0
  __m128i v75; // xmm1
  __m128i v76; // xmm0
  __int128 *v77; // rcx
  __int64 v78; // rdx
  __int128 *v79; // rax
  __int128 v80; // xmm0
  __int128 v81; // xmm1
  __int128 v82; // xmm0
  __int128 v83; // xmm1
  __int128 v84; // xmm0
  __int128 v85; // xmm1
  __int128 v86; // xmm0
  __int128 v87; // xmm1
  __int64 v88; // rbx
  __m128i *v89; // rax
  __int64 v90; // rdx
  __m128i *v91; // rcx
  __m128i v92; // xmm0
  __m128i v93; // xmm1
  __m128i v94; // xmm0
  __m128i v95; // xmm1
  __m128i v96; // xmm0
  __m128i v97; // xmm1
  __m128i v98; // xmm0
  __m128i v99; // xmm1
  _QWORD *v100; // rbx
  __int64 v101; // rdi
  __m128i *v102; // rcx
  __int64 v103; // rdx
  __m128i v104; // xmm1
  __m128i v105; // xmm0
  __m128i v106; // xmm1
  __m128i v107; // xmm0
  __m128i v108; // xmm1
  __m128i v109; // xmm0
  __m128i v110; // xmm1
  __m128i *v111; // rax
  __m128i v112; // xmm0
  __m128i v113; // xmm1
  __m128i v114; // xmm0
  __m128i v115; // xmm1
  __m128i v116; // xmm0
  __m128i v117; // xmm1
  __m128i v118; // xmm0
  __m128i v119; // xmm1
  __m128i v120; // xmm1
  __m128i v121; // xmm0
  __m128i v122; // xmm1
  __m128i v123; // xmm0
  __m128i v124; // xmm1
  __m128i v125; // xmm0
  __m128i v126; // xmm1
  __m128i v127; // xmm0
  __m128i v128; // xmm1
  __int128 *v129; // rcx
  __m128i v130; // xmm1
  __m128i v131; // xmm0
  __m128i v132; // xmm1
  __m128i v133; // xmm0
  __m128i v134; // xmm1
  __m128i v135; // xmm0
  __m128i v136; // xmm1
  __int128 *v137; // rax
  __int128 v138; // xmm0
  __int128 v139; // xmm1
  __int128 v140; // xmm0
  __int128 v141; // xmm1
  __int128 v142; // xmm0
  __int128 v143; // xmm1
  __int128 v144; // xmm0
  __int128 v145; // xmm1
  __m128i v146; // xmm1
  __m128i v147; // xmm0
  __m128i v148; // xmm1
  __m128i v149; // xmm0
  __m128i v150; // xmm1
  __m128i v151; // xmm0
  __m128i v152; // xmm1
  __m128i v153; // xmm0
  __m128i v154; // xmm1
  __m128i v155; // [rsp+30h] [rbp-D0h] BYREF
  __m128i v156; // [rsp+40h] [rbp-C0h]
  __m128i v157; // [rsp+50h] [rbp-B0h]
  __m128i v158; // [rsp+60h] [rbp-A0h]
  __m128i v159; // [rsp+70h] [rbp-90h]
  __m128i v160; // [rsp+80h] [rbp-80h]
  __m128i v161; // [rsp+90h] [rbp-70h]
  __m128i v162; // [rsp+A0h] [rbp-60h]
  __m128i v163; // [rsp+B0h] [rbp-50h]
  __m128i v164; // [rsp+440h] [rbp+340h] BYREF
  __m128i v165; // [rsp+450h] [rbp+350h]
  __m128i v166; // [rsp+460h] [rbp+360h]
  __m128i v167; // [rsp+470h] [rbp+370h]
  __m128i v168; // [rsp+480h] [rbp+380h]
  __m128i v169; // [rsp+490h] [rbp+390h]
  __m128i v170; // [rsp+4A0h] [rbp+3A0h]
  __m128i v171; // [rsp+4B0h] [rbp+3B0h]
  __m128i v172; // [rsp+4C0h] [rbp+3C0h]
  unsigned __int64 v173; // [rsp+840h] [rbp+740h]
  __int64 v174; // [rsp+848h] [rbp+748h]
  __int64 v175; // [rsp+850h] [rbp+750h] BYREF
  char v176[1016]; // [rsp+858h] [rbp+758h] BYREF
  unsigned __int64 v177; // [rsp+C50h] [rbp+B50h]
  __int64 v178; // [rsp+C58h] [rbp+B58h]
  _QWORD v179[138]; // [rsp+C60h] [rbp+B60h] BYREF
  int v180; // [rsp+10C8h] [rbp+FC8h]

  v5 = &v175;
  v6 = 8;
  v7 = a2;
  v180 = *(_DWORD *)(a5 + 24);
  v9 = a2;
  v10 = 8;
  do
  {
    v5 += 16;
    v11 = *v9;
    v12 = v9[1];
    v9 += 8;
    *((_OWORD *)v5 - 8) = v11;
    v13 = *(v9 - 6);
    *((_OWORD *)v5 - 7) = v12;
    v14 = *(v9 - 5);
    *((_OWORD *)v5 - 6) = v13;
    v15 = *(v9 - 4);
    *((_OWORD *)v5 - 5) = v14;
    v16 = *(v9 - 3);
    *((_OWORD *)v5 - 4) = v15;
    v17 = *(v9 - 2);
    *((_OWORD *)v5 - 3) = v16;
    v18 = *(v9 - 1);
    *((_OWORD *)v5 - 2) = v17;
    *((_OWORD *)v5 - 1) = v18;
    --v10;
  }
  while ( v10 );
  v19 = *v9;
  v20 = 0;
  v164.m128i_i64[0] = 0;
  *(_OWORD *)v5 = v19;
  ((void (__fastcall *)(unsigned __int64 *, _QWORD, __int64))unk_181798F42)(&v164.m128i_u64[1], 0, 1016);
  v21 = HIDWORD(v177);
  v22 = 0;
  v23 = (int)v177;
  v173 = v177;
  v174 = 4LL * SHIDWORD(v177);
  if ( (int)v177 > 0 )
  {
    v24 = *(_DWORD *)(a5 + 24);
    do
    {
      v164.m128i_i64[v22] = *(_QWORD *)a5 + 4LL * v24;
      v25 = v24 + v21;
      v24 = v24 + v21 - (((_BYTE)v24 + (_BYTE)v21) & 0xF) + 16;
      if ( (v25 & 0xF) == 0 )
        v24 = v25;
      ++v22;
      *(_DWORD *)(a5 + 24) = v24;
    }
    while ( v22 < v23 );
    v21 = HIDWORD(v173);
    LODWORD(v23) = v173;
  }
  v26 = (__int128 *)v179;
  v27 = a1[1];
  v28 = 8;
  v29 = a1[8];
  v155 = *a1;
  v30 = a1[2];
  v156 = v27;
  v31 = a1[3];
  v157 = v30;
  v32 = a1[4];
  v158 = v31;
  v33 = a1[5];
  v159 = v32;
  v34 = a1[6];
  v160 = v33;
  v35 = a1[7];
  v161 = v34;
  v162 = v35;
  v163 = v29;
  do
  {
    v26 += 8;
    v36 = *v7;
    v37 = v7[1];
    v7 += 8;
    *(v26 - 8) = v36;
    v38 = *(v7 - 6);
    *(v26 - 7) = v37;
    v39 = *(v7 - 5);
    *(v26 - 6) = v38;
    v40 = *(v7 - 4);
    *(v26 - 5) = v39;
    v41 = *(v7 - 3);
    *(v26 - 4) = v40;
    v42 = *(v7 - 2);
    *(v26 - 3) = v41;
    v43 = *(v7 - 1);
    *(v26 - 2) = v42;
    *(v26 - 1) = v43;
    --v28;
  }
  while ( v28 );
  v44 = &v164;
  v45 = 8;
  *v26 = *v7;
  v46 = (__m128i *)&v175;
  do
  {
    v46 += 8;
    v47 = *v44;
    v48 = v44[1];
    v44 += 8;
    v46[-8] = v47;
    v49 = v44[-6];
    v46[-7] = v48;
    v50 = v44[-5];
    v46[-6] = v49;
    v51 = v44[-4];
    v46[-5] = v50;
    v52 = v44[-3];
    v46[-4] = v51;
    v53 = v44[-2];
    v46[-3] = v52;
    v54 = v44[-1];
    v46[-2] = v53;
    v46[-1] = v54;
    --v45;
  }
  while ( v45 );
  *v46 = *v44;
  v55 = _mm_cvtsi128_si32(v29);
  if ( (_DWORD)v23 == v55 )
  {
    if ( (int)v23 > 0 )
    {
      v56 = 0;
      v57 = (unsigned int)v23;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD, _QWORD))unk_1800011C0)(
          v155.m128i_i64[v56],
          v179[v56],
          *(_QWORD *)&v176[v56 * 8 - 8],
          v21);
        ++v56;
        --v57;
      }
      while ( v57 );
    }
  }
  else if ( v55 == 1 && (int)v23 > 0 )
  {
    v58 = 0;
    v59 = (unsigned int)v23;
    do
    {
      ((void (__fastcall *)(__int64, _QWORD, _QWORD, _QWORD))unk_1800011C0)(
        v155.m128i_i64[0],
        v179[v58],
        *(_QWORD *)&v176[v58 * 8 - 8],
        v21);
      ++v58;
      --v59;
    }
    while ( v59 );
  }
  v175 = 0;
  ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)(v176, 0, 1016);
  v60 = v23;
  v61 = v21;
  v177 = __PAIR64__(v21, v23);
  v62 = 0;
  v178 = 4LL * (int)v21;
  if ( (int)v23 > 0 )
  {
    v63 = *(_DWORD *)(a5 + 24);
    do
    {
      *(_QWORD *)&v176[8 * v62 - 8] = *(_QWORD *)a5 + 4LL * v63;
      v64 = v21 + v63;
      v63 = v21 + v63 - (((_BYTE)v21 + (_BYTE)v63) & 0xF) + 16;
      if ( (v64 & 0xF) == 0 )
        v63 = v64;
      ++v62;
      *(_DWORD *)(a5 + 24) = v63;
    }
    while ( v62 < (int)v23 );
    v61 = HIDWORD(v177);
    v60 = v177;
  }
  v65 = &v155;
  v66 = 8;
  v67 = &v164;
  do
  {
    v65 += 8;
    v68 = *v67;
    v69 = v67[1];
    v67 += 8;
    v65[-8] = v68;
    v70 = v67[-6];
    v65[-7] = v69;
    v71 = v67[-5];
    v65[-6] = v70;
    v72 = v67[-4];
    v65[-5] = v71;
    v73 = v67[-3];
    v65[-4] = v72;
    v74 = v67[-2];
    v65[-3] = v73;
    v75 = v67[-1];
    v65[-2] = v74;
    v65[-1] = v75;
    --v66;
  }
  while ( v66 );
  v76 = *v67;
  v77 = (__int128 *)&v175;
  v78 = 8;
  *v65 = v76;
  v79 = (__int128 *)v179;
  do
  {
    v79 += 8;
    v80 = *v77;
    v81 = v77[1];
    v77 += 8;
    *(v79 - 8) = v80;
    v82 = *(v77 - 6);
    *(v79 - 7) = v81;
    v83 = *(v77 - 5);
    *(v79 - 6) = v82;
    v84 = *(v77 - 4);
    *(v79 - 5) = v83;
    v85 = *(v77 - 3);
    *(v79 - 4) = v84;
    v86 = *(v77 - 2);
    *(v79 - 3) = v85;
    v87 = *(v77 - 1);
    *(v79 - 2) = v86;
    *(v79 - 1) = v87;
    --v78;
  }
  while ( v78 );
  *v79 = *v77;
  if ( v60 > 0 )
  {
    v88 = (unsigned int)v60;
    do
    {
      ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001250)(v155.m128i_i64[v20], v179[v20], v61);
      ++v20;
      --v88;
    }
    while ( v88 );
  }
  v89 = (__m128i *)v179;
  v90 = 8;
  v91 = &v164;
  do
  {
    v89 += 8;
    v92 = *v91;
    v93 = v91[1];
    v91 += 8;
    v89[-8] = v92;
    v94 = v91[-6];
    v89[-7] = v93;
    v95 = v91[-5];
    v89[-6] = v94;
    v96 = v91[-4];
    v89[-5] = v95;
    v97 = v91[-3];
    v89[-4] = v96;
    v98 = v91[-2];
    v89[-3] = v97;
    v99 = v91[-1];
    v89[-2] = v98;
    v89[-1] = v99;
    --v90;
  }
  while ( v90 );
  *v89 = *v91;
  if ( (int)v23 > 0 )
  {
    v100 = v179;
    v101 = (unsigned int)v23;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*v100++, v21, v62, 0);
      --v101;
    }
    while ( v101 );
  }
  v102 = &v164;
  v103 = 8;
  v104 = a3[1];
  v155 = *a3;
  v157 = a3[2];
  v105 = a3[4];
  v156 = v104;
  v106 = a3[3];
  v159 = v105;
  v107 = a3[6];
  v158 = v106;
  v108 = a3[5];
  v161 = v107;
  v109 = a3[8];
  v160 = v108;
  v110 = a3[7];
  v111 = (__m128i *)v179;
  v163 = v109;
  v162 = v110;
  do
  {
    v111 += 8;
    v112 = *v102;
    v113 = v102[1];
    v102 += 8;
    v111[-8] = v112;
    v114 = v102[-6];
    v111[-7] = v113;
    v115 = v102[-5];
    v111[-6] = v114;
    v116 = v102[-4];
    v111[-5] = v115;
    v117 = v102[-3];
    v111[-4] = v116;
    v118 = v102[-2];
    v111[-3] = v117;
    v119 = v102[-1];
    v111[-2] = v118;
    v111[-1] = v119;
    --v103;
  }
  while ( v103 );
  v120 = *a1;
  *v111 = *v102;
  v121 = a1[1];
  v164 = v120;
  v122 = a1[2];
  v165 = v121;
  v123 = a1[3];
  v166 = v122;
  v124 = a1[4];
  v167 = v123;
  v125 = a1[5];
  v168 = v124;
  v126 = a1[6];
  v169 = v125;
  v127 = a1[7];
  v170 = v126;
  v128 = a1[8];
  v171 = v127;
  v172 = v128;
  sub_1808CAE90(&v164, v179, &v155);
  v129 = (__int128 *)&v175;
  v130 = a4[1];
  v164 = *a4;
  v166 = a4[2];
  v131 = a4[4];
  v165 = v130;
  v132 = a4[3];
  v168 = v131;
  v133 = a4[6];
  v167 = v132;
  v134 = a4[5];
  v170 = v133;
  v135 = a4[8];
  v169 = v134;
  v136 = a4[7];
  v137 = (__int128 *)v179;
  v172 = v135;
  v171 = v136;
  do
  {
    v137 += 8;
    v138 = *v129;
    v139 = v129[1];
    v129 += 8;
    *(v137 - 8) = v138;
    v140 = *(v129 - 6);
    *(v137 - 7) = v139;
    v141 = *(v129 - 5);
    *(v137 - 6) = v140;
    v142 = *(v129 - 4);
    *(v137 - 5) = v141;
    v143 = *(v129 - 3);
    *(v137 - 4) = v142;
    v144 = *(v129 - 2);
    *(v137 - 3) = v143;
    v145 = *(v129 - 1);
    *(v137 - 2) = v144;
    *(v137 - 1) = v145;
    --v6;
  }
  while ( v6 );
  v146 = *a1;
  *v137 = *v129;
  v147 = a1[1];
  v155 = v146;
  v148 = a1[2];
  v156 = v147;
  v149 = a1[3];
  v157 = v148;
  v150 = a1[4];
  v158 = v149;
  v151 = a1[5];
  v159 = v150;
  v152 = a1[6];
  v160 = v151;
  v153 = a1[7];
  v161 = v152;
  v154 = a1[8];
  v162 = v153;
  v163 = v154;
  sub_1808CAE90(&v155, v179, &v164);
  *(_DWORD *)(a5 + 24) = v180;
}

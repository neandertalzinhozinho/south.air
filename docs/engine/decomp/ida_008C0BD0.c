// IDA 9.3  rva=0x8c0bd0  start=0x1808c0bd0  size=2150
void __fastcall sub_1808C0BD0(__int64 a1, __int64 a2, __int64 *a3, __int64 a4)
{
  __int64 v5; // r14
  __int64 v6; // rax
  __int64 v7; // rsi
  __int64 v8; // rbx
  __int64 v9; // rdi
  int v10; // edx
  __int64 *v11; // rcx
  __int64 v12; // r8
  int v13; // r14d
  __int64 v14; // r8
  int v15; // edx
  int v16; // ecx
  _OWORD *v17; // rax
  __int64 v18; // rdx
  __int128 *v19; // rcx
  __int128 v20; // xmm0
  __int128 v21; // xmm1
  __int128 v22; // xmm0
  __int128 v23; // xmm1
  __int128 v24; // xmm0
  __int128 v25; // xmm1
  __int128 v26; // xmm0
  __int128 v27; // xmm1
  __int128 v28; // xmm0
  __int128 *v29; // rcx
  __int64 v30; // rdx
  _OWORD *v31; // rax
  __int128 v32; // xmm0
  __int128 v33; // xmm1
  __int128 v34; // xmm0
  __int128 v35; // xmm1
  __int128 v36; // xmm0
  __int128 v37; // xmm1
  __int128 v38; // xmm0
  __int128 v39; // xmm1
  __int128 v40; // xmm0
  __int128 *v41; // rcx
  __int64 v42; // rdx
  __int128 *v43; // rax
  __int128 v44; // xmm0
  __int128 v45; // xmm1
  __int128 v46; // xmm0
  __int128 v47; // xmm1
  __int128 v48; // xmm0
  __int128 v49; // xmm1
  __int128 v50; // xmm0
  __int128 v51; // xmm1
  unsigned int v52; // r15d
  __int64 v53; // rbx
  __int64 v54; // rsi
  __int64 v55; // rsi
  unsigned int v56; // r15d
  __int64 v57; // rbx
  __int64 v58; // r12
  __int64 v59; // r9
  unsigned int v60; // ecx
  int v61; // r8d
  __int64 v62; // r12
  __int128 *v63; // rax
  int v64; // ecx
  __int64 v65; // rdx
  __int128 *v66; // rcx
  __int128 v67; // xmm0
  __int128 v68; // xmm1
  __int128 v69; // xmm0
  __int128 v70; // xmm1
  __int128 v71; // xmm0
  __int128 v72; // xmm1
  __int128 v73; // xmm0
  __int128 v74; // xmm1
  __int64 v75; // rsi
  _QWORD *v76; // rbx
  __int128 *v77; // rax
  __int64 v78; // rdx
  __int128 *v79; // rcx
  __int128 v80; // xmm0
  __int128 v81; // xmm1
  __int128 v82; // xmm0
  __int128 v83; // xmm1
  __int128 v84; // xmm0
  __int128 v85; // xmm1
  __int128 v86; // xmm0
  __int128 v87; // xmm1
  __int64 v88; // r8
  __int64 v89; // rsi
  _QWORD *v90; // rbx
  __int64 v91; // r15
  unsigned int v92; // r9d
  int v93; // r8d
  __int128 *v94; // rax
  __int64 v95; // rdx
  __int128 *v96; // rcx
  __int128 v97; // xmm0
  __int128 v98; // xmm1
  __int128 v99; // xmm0
  __int128 v100; // xmm1
  __int128 v101; // xmm0
  __int128 v102; // xmm1
  __int128 v103; // xmm0
  __int128 v104; // xmm1
  __int64 v105; // rsi
  unsigned int v106; // r14d
  _QWORD *v107; // rbx
  __int128 *v108; // rax
  __int128 *v109; // rdx
  __int64 v110; // r8
  __int128 v111; // xmm0
  __int128 v112; // xmm1
  __int128 v113; // xmm0
  __int128 v114; // xmm1
  __int128 v115; // xmm0
  __int128 v116; // xmm1
  __int128 v117; // xmm0
  __int128 v118; // xmm1
  unsigned int v119; // esi
  _QWORD *v120; // rbx
  unsigned int v121; // [rsp+20h] [rbp-E0h]
  int v122; // [rsp+4Ch] [rbp-B4h]
  __int64 i; // [rsp+50h] [rbp-B0h]
  __int64 v124; // [rsp+70h] [rbp-90h]
  __int64 v125; // [rsp+80h] [rbp-80h]
  __int64 v126; // [rsp+A0h] [rbp-60h] BYREF
  _BYTE v127[1016]; // [rsp+A8h] [rbp-58h] BYREF
  unsigned int v128; // [rsp+4A0h] [rbp+3A0h]
  int v129; // [rsp+4A4h] [rbp+3A4h]
  __int64 v130; // [rsp+4A8h] [rbp+3A8h]
  _QWORD v131[128]; // [rsp+4B0h] [rbp+3B0h] BYREF
  unsigned int v132; // [rsp+8B4h] [rbp+7B4h]
  __int64 v133; // [rsp+8C0h] [rbp+7C0h] BYREF
  _BYTE v134[1016]; // [rsp+8C8h] [rbp+7C8h] BYREF
  int v135; // [rsp+CC0h] [rbp+BC0h]
  int v136; // [rsp+CC4h] [rbp+BC4h]
  __int64 v137; // [rsp+CC8h] [rbp+BC8h]
  _QWORD v138[128]; // [rsp+CD0h] [rbp+BD0h] BYREF
  unsigned int v139; // [rsp+10D4h] [rbp+FD4h]
  _QWORD v140[130]; // [rsp+10E0h] [rbp+FE0h] BYREF

  v5 = a1;
  if ( *(_DWORD *)(a1 + 1024) != 1 )
  {
    v6 = a3[1];
    v7 = *a3;
    v121 = *(_DWORD *)(a1 + 1028);
    v125 = v6;
    for ( i = *a3; v7 != v6; i = v7 )
    {
      if ( *(_DWORD *)(v7 + 16) == 2 )
      {
        v8 = *(int *)(v5 + 1028);
        v126 = 0;
        ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v127, 0, 1016);
        v9 = *(unsigned int *)(v7 + 16);
        v10 = 0;
        v128 = v9;
        v129 = v8;
        v130 = 4 * v8;
        if ( (int)v9 > 0 )
        {
          v11 = &v126;
          v12 = 8LL * *(int *)(v7 + 8) - (_QWORD)&v126 + v5;
          do
          {
            ++v10;
            *v11 = *(__int64 *)((char *)v11 + v12);
            ++v11;
            v9 = v128;
          }
          while ( v10 < (int)v128 );
          LODWORD(v8) = v129;
        }
        v122 = *(_DWORD *)(a4 + 24);
        v133 = 0;
        ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v134, 0, 1016);
        v13 = v9;
        v14 = 0;
        v135 = v9;
        v136 = v8;
        v137 = 4LL * (int)v8;
        if ( (int)v9 > 0 )
        {
          v15 = *(_DWORD *)(a4 + 24);
          do
          {
            *(_QWORD *)&v134[8 * v14 - 8] = *(_QWORD *)a4 + 4LL * v15;
            v16 = v15 + v8;
            v15 = v15 + v8 - (((_BYTE)v15 + (_BYTE)v8) & 0xF) + 16;
            if ( (v16 & 0xF) == 0 )
              v15 = v16;
            ++v14;
            *(_DWORD *)(a4 + 24) = v15;
          }
          while ( v14 < (int)v9 );
          v13 = v135;
        }
        v17 = v140;
        v18 = 8;
        v19 = (__int128 *)&v126;
        do
        {
          v17 += 8;
          v20 = *v19;
          v21 = v19[1];
          v19 += 8;
          *(v17 - 8) = v20;
          v22 = *(v19 - 6);
          *(v17 - 7) = v21;
          v23 = *(v19 - 5);
          *(v17 - 6) = v22;
          v24 = *(v19 - 4);
          *(v17 - 5) = v23;
          v25 = *(v19 - 3);
          *(v17 - 4) = v24;
          v26 = *(v19 - 2);
          *(v17 - 3) = v25;
          v27 = *(v19 - 1);
          *(v17 - 2) = v26;
          *(v17 - 1) = v27;
          --v18;
        }
        while ( v18 );
        v28 = *v19;
        v29 = (__int128 *)&v126;
        v30 = 8;
        *v17 = v28;
        v31 = v138;
        do
        {
          v31 += 8;
          v32 = *v29;
          v33 = v29[1];
          v29 += 8;
          *(v31 - 8) = v32;
          v34 = *(v29 - 6);
          *(v31 - 7) = v33;
          v35 = *(v29 - 5);
          *(v31 - 6) = v34;
          v36 = *(v29 - 4);
          *(v31 - 5) = v35;
          v37 = *(v29 - 3);
          *(v31 - 4) = v36;
          v38 = *(v29 - 2);
          *(v31 - 3) = v37;
          v39 = *(v29 - 1);
          *(v31 - 2) = v38;
          *(v31 - 1) = v39;
          --v30;
        }
        while ( v30 );
        v40 = *v29;
        v41 = (__int128 *)&v133;
        v42 = 8;
        *v31 = v40;
        v43 = (__int128 *)v131;
        do
        {
          v43 += 8;
          v44 = *v41;
          v45 = v41[1];
          v41 += 8;
          *(v43 - 8) = v44;
          v46 = *(v41 - 6);
          *(v43 - 7) = v45;
          v47 = *(v41 - 5);
          *(v43 - 6) = v46;
          v48 = *(v41 - 4);
          *(v43 - 5) = v47;
          v49 = *(v41 - 3);
          *(v43 - 4) = v48;
          v50 = *(v41 - 2);
          *(v43 - 3) = v49;
          v51 = *(v41 - 1);
          *(v43 - 2) = v50;
          *(v43 - 1) = v51;
          --v42;
        }
        while ( v42 );
        *v43 = *v41;
        if ( v13 == (_DWORD)v9 )
        {
          if ( v13 > 0 )
          {
            v52 = v132;
            v53 = 0;
            v54 = (unsigned int)v13;
            do
            {
              ((void (__fastcall *)(_QWORD, _QWORD, _QWORD, _QWORD))unk_180001190)(v138[v53], v140[v53], v131[v53], v52);
              ++v53;
              --v54;
            }
            while ( v54 );
          }
        }
        else if ( (_DWORD)v9 == 1 && v13 > 0 )
        {
          v55 = (unsigned int)v13;
          v56 = v132;
          v57 = 0;
          v58 = v140[0];
          do
          {
            ((void (__fastcall *)(_QWORD, __int64, _QWORD, _QWORD))unk_180001190)(v138[v57], v58, v131[v57], v56);
            ++v57;
            --v55;
          }
          while ( v55 );
        }
        v59 = *(_QWORD *)a4 + 4LL * *(int *)(a4 + 24);
        v60 = v121 + *(_DWORD *)(a4 + 24);
        v124 = v59;
        v61 = v60 - (v60 & 0xF) + 16;
        if ( (v60 & 0xF) == 0 )
          v61 = v121 + *(_DWORD *)(a4 + 24);
        *(_DWORD *)(a4 + 24) = v61;
        v62 = *(_QWORD *)a4 + 4LL * v61;
        v63 = (__int128 *)v138;
        v64 = v61 + v121 - (((_BYTE)v61 + (_BYTE)v121) & 0xF) + 16;
        if ( (((_BYTE)v61 + (_BYTE)v121) & 0xF) == 0 )
          v64 = v61 + v121;
        v65 = 8;
        *(_DWORD *)(a4 + 24) = v64;
        v66 = (__int128 *)&v133;
        do
        {
          v63 += 8;
          v67 = *v66;
          v68 = v66[1];
          v66 += 8;
          *(v63 - 8) = v67;
          v69 = *(v66 - 6);
          *(v63 - 7) = v68;
          v70 = *(v66 - 5);
          *(v63 - 6) = v69;
          v71 = *(v66 - 4);
          *(v63 - 5) = v70;
          v72 = *(v66 - 3);
          *(v63 - 4) = v71;
          v73 = *(v66 - 2);
          *(v63 - 3) = v72;
          v74 = *(v66 - 1);
          *(v63 - 2) = v73;
          *(v63 - 1) = v74;
          --v65;
        }
        while ( v65 );
        *v63 = *v66;
        ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v59, v121);
        if ( v13 > 0 )
        {
          v75 = (unsigned int)v13;
          v76 = v138;
          do
          {
            ((void (__fastcall *)(_QWORD, __int64, _QWORD))unk_180001370)(*v76++, v124, v121);
            --v75;
          }
          while ( v75 );
        }
        v77 = (__int128 *)v140;
        v78 = 8;
        v79 = (__int128 *)&v126;
        do
        {
          v77 += 8;
          v80 = *v79;
          v81 = v79[1];
          v79 += 8;
          *(v77 - 8) = v80;
          v82 = *(v79 - 6);
          *(v77 - 7) = v81;
          v83 = *(v79 - 5);
          *(v77 - 6) = v82;
          v84 = *(v79 - 4);
          *(v77 - 5) = v83;
          v85 = *(v79 - 3);
          *(v77 - 4) = v84;
          v86 = *(v79 - 2);
          *(v77 - 3) = v85;
          v87 = *(v79 - 1);
          *(v77 - 2) = v86;
          *(v77 - 1) = v87;
          --v78;
        }
        while ( v78 );
        *v77 = *v79;
        ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v62, v121);
        if ( (int)v9 > 0 )
        {
          v89 = (unsigned int)v9;
          v90 = v140;
          do
          {
            ((void (__fastcall *)(_QWORD, __int64, _QWORD))unk_180001370)(*v90++, v62, v121);
            --v89;
          }
          while ( v89 );
        }
        ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001100)(v62, v121, v88, 0);
        v91 = *(_QWORD *)a4 + 4LL * *(int *)(a4 + 24);
        v92 = v121 + *(_DWORD *)(a4 + 24);
        v93 = v92 - (v92 & 0xF) + 16;
        if ( (v92 & 0xF) == 0 )
          v93 = v121 + *(_DWORD *)(a4 + 24);
        *(_DWORD *)(a4 + 24) = v93;
        ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001550)(v62, v124, v91, v121);
        v94 = (__int128 *)v138;
        v95 = 8;
        v96 = (__int128 *)&v126;
        do
        {
          v94 += 8;
          v97 = *v96;
          v98 = v96[1];
          v96 += 8;
          *(v94 - 8) = v97;
          v99 = *(v96 - 6);
          *(v94 - 7) = v98;
          v100 = *(v96 - 5);
          *(v94 - 6) = v99;
          v101 = *(v96 - 4);
          *(v94 - 5) = v100;
          v102 = *(v96 - 3);
          *(v94 - 4) = v101;
          v103 = *(v96 - 2);
          *(v94 - 3) = v102;
          v104 = *(v96 - 1);
          *(v94 - 2) = v103;
          *(v94 - 1) = v104;
          --v95;
        }
        while ( v95 );
        *v94 = *v96;
        if ( (int)v9 > 0 )
        {
          v105 = (unsigned int)v9;
          v106 = v139;
          v107 = v138;
          do
          {
            ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v96, *v107++, v106);
            --v105;
          }
          while ( v105 );
        }
        v108 = (__int128 *)v131;
        v109 = (__int128 *)&v126;
        v110 = 8;
        do
        {
          v108 += 8;
          v111 = *v109;
          v112 = v109[1];
          v109 += 8;
          *(v108 - 8) = v111;
          v113 = *(v109 - 6);
          *(v108 - 7) = v112;
          v114 = *(v109 - 5);
          *(v108 - 6) = v113;
          v115 = *(v109 - 4);
          *(v108 - 5) = v114;
          v116 = *(v109 - 3);
          *(v108 - 4) = v115;
          v117 = *(v109 - 2);
          *(v108 - 3) = v116;
          v118 = *(v109 - 1);
          *(v108 - 2) = v117;
          *(v108 - 1) = v118;
          --v110;
        }
        while ( v110 );
        *v108 = *v109;
        if ( (_DWORD)v9 == 1 )
        {
          ((void (__fastcall *)(__int64, __int128 *, __int64, _QWORD))unk_1800011F0)(v91, v109, v126, v132);
        }
        else if ( (int)v9 >= 2 )
        {
          v119 = v132;
          v120 = v131;
          do
          {
            ((void (__fastcall *)(__int64, __int128 *, _QWORD, _QWORD))unk_1800011F0)(v91, v109, *v120++, v119);
            --v9;
          }
          while ( v9 );
        }
        v7 = i;
        v5 = a1;
        *(_DWORD *)(a4 + 24) = v122;
        v6 = v125;
      }
      v7 += 24;
    }
  }
}

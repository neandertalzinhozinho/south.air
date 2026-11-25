// IDA 9.3  rva=0x8bf650  start=0x1808bf650  size=1411
void __fastcall sub_1808BF650(char *a1, __int128 *a2, __int64 *a3)
{
  __int64 v3; // rsi
  char *v5; // rdi
  __int128 *v6; // rax
  __int64 v7; // rdx
  __int64 *v8; // rcx
  __int128 v10; // xmm0
  __int128 v11; // xmm1
  __int128 v12; // xmm0
  __int128 v13; // xmm1
  __int128 v14; // xmm0
  __int128 v15; // xmm1
  __int128 v16; // xmm0
  __int128 v17; // xmm1
  unsigned int v18; // r14d
  __int64 *v19; // rbx
  __int64 v20; // rsi
  __int64 *v21; // rax
  __int128 v22; // xmm1
  __int128 v23; // xmm0
  __int128 v24; // xmm1
  __int128 v25; // xmm0
  __int128 v26; // xmm1
  __int128 v27; // xmm0
  __int128 v28; // xmm1
  __int128 v29; // xmm0
  __int128 v30; // xmm0
  __int128 v31; // xmm1
  __int128 v32; // xmm0
  __int128 v33; // xmm1
  __int128 v34; // xmm0
  __int128 v35; // xmm1
  __int128 v36; // xmm0
  __int128 v37; // xmm1
  __int128 v38; // xmm0
  __int64 v39; // rbx
  int v40; // r14d
  _QWORD *v41; // rcx
  signed __int64 v42; // rdi
  __int128 v43; // xmm1
  __int128 *v44; // rcx
  __int128 v45; // xmm0
  __int128 v46; // xmm1
  __int128 v47; // xmm0
  __int128 v48; // xmm1
  __int128 v49; // xmm0
  __int128 v50; // xmm1
  __int128 v51; // xmm0
  __int128 v52; // xmm0
  __int128 v53; // xmm1
  __int128 v54; // xmm0
  __int128 v55; // xmm1
  __int128 v56; // xmm0
  __int128 v57; // xmm1
  __int128 v58; // xmm0
  __int128 v59; // xmm1
  __int64 v60; // rsi
  __int64 v61; // rcx
  int v62; // edx
  __int64 v63; // r13
  __int64 v64; // rax
  __int64 v65; // rbx
  int v66; // esi
  int v67; // edx
  __int64 *v68; // rcx
  char *v69; // r8
  __int128 *v70; // rcx
  __int64 v71; // rdx
  __int128 *v72; // rax
  __int128 v73; // xmm0
  __int128 v74; // xmm1
  __int128 v75; // xmm0
  __int128 v76; // xmm1
  __int128 v77; // xmm0
  __int128 v78; // xmm1
  __int128 v79; // xmm0
  __int128 v80; // xmm1
  __int128 v81; // [rsp+20h] [rbp-E0h] BYREF
  _OWORD v82[8]; // [rsp+30h] [rbp-D0h] BYREF
  __int64 v83; // [rsp+B0h] [rbp-50h]
  _OWORD v84[9]; // [rsp+D0h] [rbp-30h] BYREF
  __int64 v85; // [rsp+160h] [rbp+60h]
  int v86; // [rsp+4D0h] [rbp+3D0h]
  int v87; // [rsp+4D4h] [rbp+3D4h]
  __int64 v88; // [rsp+4D8h] [rbp+3D8h]
  __int64 v89; // [rsp+4E0h] [rbp+3E0h] BYREF
  char v90[1016]; // [rsp+4E8h] [rbp+3E8h] BYREF
  int v91; // [rsp+8E0h] [rbp+7E0h]
  unsigned int v92; // [rsp+8E4h] [rbp+7E4h]
  __int64 v93; // [rsp+8E8h] [rbp+7E8h]
  _BYTE v94[1040]; // [rsp+8F0h] [rbp+7F0h] BYREF
  __int64 v95; // [rsp+D40h] [rbp+C40h]
  __int64 v96; // [rsp+D48h] [rbp+C48h]
  __int64 v97; // [rsp+D58h] [rbp+C58h]

  v3 = 8;
  v5 = a1;
  v6 = (__int128 *)a1;
  v7 = 8;
  v8 = &v89;
  do
  {
    v8 += 16;
    v10 = *v6;
    v11 = v6[1];
    v6 += 8;
    *((_OWORD *)v8 - 8) = v10;
    v12 = *(v6 - 6);
    *((_OWORD *)v8 - 7) = v11;
    v13 = *(v6 - 5);
    *((_OWORD *)v8 - 6) = v12;
    v14 = *(v6 - 4);
    *((_OWORD *)v8 - 5) = v13;
    v15 = *(v6 - 3);
    *((_OWORD *)v8 - 4) = v14;
    v16 = *(v6 - 2);
    *((_OWORD *)v8 - 3) = v15;
    v17 = *(v6 - 1);
    *((_OWORD *)v8 - 2) = v16;
    *((_OWORD *)v8 - 1) = v17;
    --v7;
  }
  while ( v7 );
  *(_OWORD *)v8 = *v6;
  if ( v91 > 0 )
  {
    v18 = v92;
    v19 = &v89;
    v20 = (unsigned int)v91;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD))unk_1800010D0)(*v19++, v18);
      --v20;
    }
    while ( v20 );
    v3 = 8;
  }
  if ( *(_DWORD *)a2 == 1 )
  {
    if ( *((_DWORD *)v5 + 256) == 1 )
    {
      v21 = &v89;
      v22 = a2[1];
      v81 = *a2;
      v23 = a2[2];
      v82[0] = v22;
      v24 = a2[3];
      v82[1] = v23;
      v25 = a2[4];
      v82[2] = v24;
      v26 = a2[5];
      v82[3] = v25;
      v27 = a2[6];
      v82[4] = v26;
      v28 = a2[7];
      v82[5] = v27;
      v29 = a2[8];
      v82[6] = v28;
      *(_QWORD *)&v28 = *((_QWORD *)a2 + 18);
      v82[7] = v29;
      v83 = v28;
      do
      {
        v21 += 16;
        v30 = *(_OWORD *)v5;
        v31 = *((_OWORD *)v5 + 1);
        v5 += 128;
        *((_OWORD *)v21 - 8) = v30;
        v32 = *((_OWORD *)v5 - 6);
        *((_OWORD *)v21 - 7) = v31;
        v33 = *((_OWORD *)v5 - 5);
        *((_OWORD *)v21 - 6) = v32;
        v34 = *((_OWORD *)v5 - 4);
        *((_OWORD *)v21 - 5) = v33;
        v35 = *((_OWORD *)v5 - 3);
        *((_OWORD *)v21 - 4) = v34;
        v36 = *((_OWORD *)v5 - 2);
        *((_OWORD *)v21 - 3) = v35;
        v37 = *((_OWORD *)v5 - 1);
        *((_OWORD *)v21 - 2) = v36;
        *((_OWORD *)v21 - 1) = v37;
        --v3;
      }
      while ( v3 );
      v38 = *(_OWORD *)v5;
    }
    else
    {
      v39 = *((int *)v5 + 257);
      v40 = 0;
      *(_QWORD *)&v84[0] = 0;
      ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)((char *)v84 + 8, 0, 1016);
      v86 = 2;
      v41 = v84;
      v88 = 4 * v39;
      v42 = v5 - (char *)v84;
      v87 = v39;
      do
      {
        ++v40;
        *v41 = *(_QWORD *)((char *)v41 + v42);
        ++v41;
      }
      while ( v40 < v86 );
      v21 = &v89;
      v43 = a2[1];
      v44 = v84;
      v81 = *a2;
      v45 = a2[2];
      v82[0] = v43;
      v46 = a2[3];
      v82[1] = v45;
      v47 = a2[4];
      v82[2] = v46;
      v48 = a2[5];
      v82[3] = v47;
      v49 = a2[6];
      v82[4] = v48;
      v50 = a2[7];
      v82[5] = v49;
      v51 = a2[8];
      v82[6] = v50;
      *(_QWORD *)&v50 = *((_QWORD *)a2 + 18);
      v82[7] = v51;
      v83 = v50;
      do
      {
        v21 += 16;
        v52 = *v44;
        v53 = v44[1];
        v44 += 8;
        *((_OWORD *)v21 - 8) = v52;
        v54 = *(v44 - 6);
        *((_OWORD *)v21 - 7) = v53;
        v55 = *(v44 - 5);
        *((_OWORD *)v21 - 6) = v54;
        v56 = *(v44 - 4);
        *((_OWORD *)v21 - 5) = v55;
        v57 = *(v44 - 3);
        *((_OWORD *)v21 - 4) = v56;
        v58 = *(v44 - 2);
        *((_OWORD *)v21 - 3) = v57;
        v59 = *(v44 - 1);
        *((_OWORD *)v21 - 2) = v58;
        *((_OWORD *)v21 - 1) = v59;
        --v3;
      }
      while ( v3 );
      v38 = *v44;
    }
    *(_OWORD *)v21 = v38;
    sub_1808CAB40(&v89, &v81);
  }
  else
  {
    v60 = *a3;
    v96 = a3[1];
    v97 = *a3;
    if ( *a3 != v96 )
    {
      v61 = *((_QWORD *)a2 + 1);
      v62 = *((_DWORD *)a2 + 36);
      v95 = 4LL * *((int *)v5 + 257);
      do
      {
        v63 = *(int *)(v60 + 16);
        v64 = *(_QWORD *)(v60 + 8);
        v65 = 0;
        *((_QWORD *)&v81 + 1) = v61;
        LODWORD(v81) = v63;
        memset(v82, 0, sizeof(v82));
        LODWORD(v83) = v62;
        if ( (int)v63 > 0 )
        {
          v66 = v64;
          ((void (__fastcall *)(_OWORD *, char *, __int64))unk_181798F36)(v82, (char *)a2 + 8 * (int)v64 + 16, 8 * v63);
          do
          {
            ++v65;
            ++v66;
          }
          while ( v65 < v63 );
          v60 = v97;
        }
        v89 = 0;
        ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)(v90, 0, 1016);
        v67 = 0;
        v92 = *((_DWORD *)v5 + 257);
        v93 = v95;
        v91 = v63;
        if ( (int)v63 > 0 )
        {
          v68 = &v89;
          v69 = &v5[8LL * *(int *)(v60 + 8) - (_QWORD)&v89];
          do
          {
            ++v67;
            *v68 = *(__int64 *)((char *)v68 + (_QWORD)v69);
            ++v68;
          }
          while ( v67 < v91 );
        }
        v70 = (__int128 *)v94;
        v71 = 8;
        v72 = (__int128 *)&v89;
        v84[0] = v81;
        v84[1] = v82[0];
        v84[2] = v82[1];
        v84[3] = v82[2];
        v84[4] = v82[3];
        v84[5] = v82[4];
        v84[6] = v82[5];
        v84[7] = v82[6];
        v84[8] = v82[7];
        v85 = v83;
        do
        {
          v70 += 8;
          v73 = *v72;
          v74 = v72[1];
          v72 += 8;
          *(v70 - 8) = v73;
          v75 = *(v72 - 6);
          *(v70 - 7) = v74;
          v76 = *(v72 - 5);
          *(v70 - 6) = v75;
          v77 = *(v72 - 4);
          *(v70 - 5) = v76;
          v78 = *(v72 - 3);
          *(v70 - 4) = v77;
          v79 = *(v72 - 2);
          *(v70 - 3) = v78;
          v80 = *(v72 - 1);
          *(v70 - 2) = v79;
          *(v70 - 1) = v80;
          --v71;
        }
        while ( v71 );
        *v70 = *v72;
        sub_1808CAB40(v94, v84);
        v61 = *((_QWORD *)a2 + 1);
        v60 += 24;
        v62 = *((_DWORD *)a2 + 36);
        v97 = v60;
      }
      while ( v60 != v96 );
    }
  }
}

// IDA 9.3  rva=0x8bfd30  start=0x1808bfd30  size=1275
void __fastcall sub_1808BFD30(__int64 a1, __int64 a2)
{
  __int64 v2; // r9
  __int64 v4; // r10
  int v5; // edx
  __int64 v6; // r14
  unsigned int **v7; // rax
  unsigned int *v8; // r12
  unsigned int *v9; // r15
  unsigned int v10; // r8d
  bool v11; // al
  unsigned int v12; // r8d
  __int64 v13; // rsi
  int v14; // r8d
  int v15; // edx
  __int64 *v16; // rcx
  __int64 v17; // r9
  __int128 *v18; // rax
  __int64 v19; // rdx
  __int128 *v20; // rcx
  __int128 v21; // xmm0
  __int128 v22; // xmm1
  __int128 v23; // xmm0
  __int128 v24; // xmm1
  __int128 v25; // xmm0
  __int128 v26; // xmm1
  __int128 v27; // xmm0
  __int128 v28; // xmm1
  _QWORD *v29; // rbx
  __int64 v30; // rdi
  unsigned int v31; // r8d
  bool v32; // al
  unsigned int v33; // r8d
  __int64 v34; // rsi
  int v35; // r8d
  int v36; // edx
  __int64 *v37; // rcx
  __int64 v38; // r9
  __int128 *v39; // rax
  __int64 v40; // rdx
  __int128 *v41; // rcx
  __int128 v42; // xmm0
  __int128 v43; // xmm1
  __int128 v44; // xmm0
  __int128 v45; // xmm1
  __int128 v46; // xmm0
  __int128 v47; // xmm1
  __int128 v48; // xmm0
  __int128 v49; // xmm1
  _QWORD *v50; // rbx
  __int64 v51; // rdi
  __int64 v52; // [rsp+28h] [rbp-E0h]
  __int64 v53; // [rsp+38h] [rbp-D0h] BYREF
  _BYTE v54[1016]; // [rsp+40h] [rbp-C8h] BYREF
  int v55; // [rsp+438h] [rbp+330h]
  int v56; // [rsp+43Ch] [rbp+334h]
  __int64 v57; // [rsp+440h] [rbp+338h]
  _BYTE v58[1032]; // [rsp+448h] [rbp+340h] BYREF
  int v60; // [rsp+8C0h] [rbp+7B8h]

  v2 = 0;
  v52 = 0;
  v60 = 0;
  v4 = a1;
  do
  {
    v5 = dword_182014360[v2];
    v6 = v5;
    v7 = *(unsigned int ***)(v4 + 16);
    v8 = v7[1];
    v9 = *v7;
    if ( !*(_BYTE *)(*(_QWORD *)(v4 + 11320) + 8 * v2 + 444) )
    {
      if ( v9 == v8 )
        goto LABEL_75;
      while ( 1 )
      {
        v10 = *v9;
        switch ( v6 )
        {
          case 0LL:
            goto LABEL_27;
          case 1LL:
            v11 = v10 != 10;
            break;
          case 2LL:
            v11 = v10 != 9;
            break;
          case 3LL:
            if ( v10 - 9 <= 1 )
              goto LABEL_37;
            goto LABEL_27;
          case 5LL:
            if ( v10 - 16 <= 2 )
              goto LABEL_27;
            goto LABEL_37;
          case 4LL:
            if ( v10 - 8 <= 2 )
              goto LABEL_37;
            goto LABEL_27;
          case 6LL:
            if ( !(unsigned __int8)sub_18061B790(4, v10) || (unsigned __int8)sub_18061B790(5, v12) )
            {
LABEL_36:
              v5 = v6;
              goto LABEL_37;
            }
LABEL_27:
            v13 = *(int *)(a2 + 1028);
            v53 = 0;
            ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v54, 0, 1016);
            v14 = v9[4];
            v15 = 0;
            v55 = v14;
            v56 = v13;
            v57 = 4 * v13;
            if ( v14 > 0 )
            {
              v16 = &v53;
              v17 = a2 + 8LL * (int)v9[2] - (_QWORD)&v53;
              do
              {
                ++v15;
                *v16 = *(__int64 *)((char *)v16 + v17);
                ++v16;
                v14 = v55;
              }
              while ( v15 < v55 );
              LODWORD(v13) = v56;
            }
            v18 = (__int128 *)v58;
            v19 = 8;
            v20 = (__int128 *)&v53;
            do
            {
              v18 += 8;
              v21 = *v20;
              v22 = v20[1];
              v20 += 8;
              *(v18 - 8) = v21;
              v23 = *(v20 - 6);
              *(v18 - 7) = v22;
              v24 = *(v20 - 5);
              *(v18 - 6) = v23;
              v25 = *(v20 - 4);
              *(v18 - 5) = v24;
              v26 = *(v20 - 3);
              *(v18 - 4) = v25;
              v27 = *(v20 - 2);
              *(v18 - 3) = v26;
              v28 = *(v20 - 1);
              *(v18 - 2) = v27;
              *(v18 - 1) = v28;
              --v19;
            }
            while ( v19 );
            *v18 = *v20;
            if ( v14 > 0 )
            {
              v29 = v58;
              v30 = (unsigned int)v14;
              do
              {
                ((void (__fastcall *)(_QWORD, _QWORD))unk_1800010D0)(*v29++, (unsigned int)v13);
                --v30;
              }
              while ( v30 );
            }
            goto LABEL_36;
          case 7LL:
            if ( v10 - 8 <= 1 )
              goto LABEL_27;
            goto LABEL_37;
          default:
            v11 = v5 == v10;
            break;
        }
        if ( v11 )
          goto LABEL_27;
LABEL_37:
        v9 += 6;
        if ( v9 == v8 )
        {
          v2 = v52;
          goto LABEL_75;
        }
      }
    }
    for ( ; v9 != v8; v9 += 6 )
    {
      v31 = *v9;
      switch ( v6 )
      {
        case 0LL:
          goto LABEL_63;
        case 1LL:
          v32 = v31 != 10;
          break;
        case 2LL:
          v32 = v31 != 9;
          break;
        case 3LL:
          if ( v31 - 9 <= 1 )
            continue;
          goto LABEL_63;
        case 5LL:
          if ( v31 - 16 <= 2 )
            goto LABEL_63;
          continue;
        case 4LL:
          if ( v31 - 8 <= 2 )
            continue;
          goto LABEL_63;
        case 6LL:
          if ( !(unsigned __int8)sub_18061B790(4, v31) || (unsigned __int8)sub_18061B790(5, v33) )
          {
LABEL_73:
            v5 = v6;
            continue;
          }
LABEL_63:
          v34 = *(int *)(a2 + 1028);
          v53 = 0;
          ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v54, 0, 1016);
          v35 = v9[4];
          v36 = 0;
          v55 = v35;
          v56 = v34;
          v57 = 4 * v34;
          if ( v35 > 0 )
          {
            v37 = &v53;
            v38 = a2 + 8LL * (int)v9[2] - (_QWORD)&v53;
            do
            {
              ++v36;
              *v37 = *(__int64 *)((char *)v37 + v38);
              ++v37;
              v35 = v55;
            }
            while ( v36 < v55 );
            LODWORD(v34) = v56;
          }
          v39 = (__int128 *)v58;
          v40 = 8;
          v41 = (__int128 *)&v53;
          do
          {
            v39 += 8;
            v42 = *v41;
            v43 = v41[1];
            v41 += 8;
            *(v39 - 8) = v42;
            v44 = *(v41 - 6);
            *(v39 - 7) = v43;
            v45 = *(v41 - 5);
            *(v39 - 6) = v44;
            v46 = *(v41 - 4);
            *(v39 - 5) = v45;
            v47 = *(v41 - 3);
            *(v39 - 4) = v46;
            v48 = *(v41 - 2);
            *(v39 - 3) = v47;
            v49 = *(v41 - 1);
            *(v39 - 2) = v48;
            *(v39 - 1) = v49;
            --v40;
          }
          while ( v40 );
          *v39 = *v41;
          if ( v35 > 0 )
          {
            v50 = v58;
            v51 = (unsigned int)v35;
            do
            {
              ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v41, *v50++, (unsigned int)v34);
              --v51;
            }
            while ( v51 );
          }
          v2 = v52;
          goto LABEL_73;
        case 7LL:
          if ( v31 - 8 <= 1 )
            goto LABEL_63;
          continue;
        default:
          v32 = v5 == v31;
          break;
      }
      if ( v32 )
        goto LABEL_63;
    }
LABEL_75:
    ++v2;
    v4 = a1;
    ++v60;
    v52 = v2;
  }
  while ( (unsigned __int64)v60 < 5 );
}

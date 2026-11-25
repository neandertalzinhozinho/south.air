// IDA 9.3  rva=0x8c3f10  start=0x1808c3f10  size=952
void __fastcall sub_1808C3F10(__int64 a1, __int64 a2, __int64 a3, unsigned int **a4)
{
  __int64 v4; // r8
  unsigned int **v5; // rdi
  __int64 v7; // rbx
  char v8; // r9
  __int64 v9; // rcx
  __int64 v10; // rdx
  char v11; // al
  int *v12; // rax
  int v13; // ecx
  _BYTE *v14; // r15
  unsigned int *v15; // r14
  unsigned int *v16; // r12
  __int64 v17; // r13
  unsigned int v18; // r8d
  bool v19; // al
  unsigned int v20; // r8d
  __int64 v21; // rsi
  int v22; // r8d
  int v23; // edx
  __int64 *v24; // rax
  __int64 v25; // r9
  __int128 *v26; // rax
  __int64 v27; // rdx
  __int128 *v28; // rcx
  __int128 v29; // xmm0
  __int128 v30; // xmm1
  __int128 v31; // xmm0
  __int128 v32; // xmm1
  __int128 v33; // xmm0
  __int128 v34; // xmm1
  __int128 v35; // xmm0
  __int128 v36; // xmm1
  _QWORD *v37; // rbx
  __int64 v38; // rdi
  int *v39; // [rsp+20h] [rbp-878h]
  __int64 v40; // [rsp+28h] [rbp-870h] BYREF
  char v41[1016]; // [rsp+30h] [rbp-868h] BYREF
  int v42; // [rsp+428h] [rbp-470h]
  int v43; // [rsp+42Ch] [rbp-46Ch]
  __int64 v44; // [rsp+430h] [rbp-468h]
  _BYTE v45[1048]; // [rsp+440h] [rbp-458h] BYREF
  int v47; // [rsp+8A8h] [rbp+10h]
  char v48; // [rsp+8B0h] [rbp+18h]

  v4 = a2 + 440;
  v5 = a4;
  v7 = a1;
  if ( a2 + 440 == a2 + 480 )
  {
LABEL_4:
    v8 = 0;
  }
  else
  {
    while ( !*(_BYTE *)(v4 + 5) )
    {
      v4 += 8;
      if ( v4 == a2 + 480 )
        goto LABEL_4;
    }
    v8 = 1;
  }
  v9 = a2 + 440;
  v48 = v8;
  v10 = a2 + 480;
  if ( v9 == v10 )
  {
LABEL_8:
    v11 = 0;
  }
  else
  {
    while ( !*(_BYTE *)(v9 + 6) )
    {
      v9 += 8;
      if ( v9 == v10 )
        goto LABEL_8;
    }
    v11 = 1;
  }
  if ( !v8 && !v11 )
    return;
  v12 = dword_182014360;
  v13 = 0;
  v14 = (_BYTE *)(a2 + 445);
  v47 = 0;
  v39 = dword_182014360;
  do
  {
    v15 = *v5;
    v16 = v5[1];
    v17 = *v12;
    if ( *v5 == v16 )
      goto LABEL_54;
    do
    {
      v18 = *v15;
      if ( (_DWORD)v17 )
      {
        switch ( v17 )
        {
          case 1LL:
            v19 = v18 != 10;
            goto LABEL_37;
          case 2LL:
            v19 = v18 != 9;
            goto LABEL_37;
          case 3LL:
            if ( v18 - 9 <= 1 )
              goto LABEL_52;
            break;
          case 5LL:
            if ( v18 - 16 > 2 )
              goto LABEL_52;
            break;
          case 4LL:
            if ( v18 - 8 <= 2 )
              goto LABEL_52;
            break;
          case 6LL:
            if ( !(unsigned __int8)sub_18061B790(4, v18) || (unsigned __int8)sub_18061B790(5, v20) )
              goto LABEL_52;
            break;
          case 7LL:
            if ( v18 - 8 > 1 )
              goto LABEL_52;
            break;
          default:
            v19 = (_DWORD)v17 == v18;
LABEL_37:
            if ( !v19 )
              goto LABEL_52;
            break;
        }
      }
      if ( !*v14 && (v8 || !v14[1]) )
      {
        v21 = *(int *)(v7 + 1028);
        v40 = 0;
        ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)(v41, 0, 1016);
        v22 = v15[4];
        v23 = 0;
        v42 = v22;
        v43 = v21;
        v44 = 4 * v21;
        if ( v22 > 0 )
        {
          v24 = &v40;
          v25 = v7 + 8LL * (int)v15[2] - (_QWORD)&v40;
          do
          {
            ++v23;
            *v24 = *(__int64 *)((char *)v24 + v25);
            ++v24;
            v22 = v42;
          }
          while ( v23 < v42 );
          LODWORD(v21) = v43;
        }
        v26 = (__int128 *)v45;
        v27 = 8;
        v28 = (__int128 *)&v40;
        do
        {
          v26 += 8;
          v29 = *v28;
          v30 = v28[1];
          v28 += 8;
          *(v26 - 8) = v29;
          v31 = *(v28 - 6);
          *(v26 - 7) = v30;
          v32 = *(v28 - 5);
          *(v26 - 6) = v31;
          v33 = *(v28 - 4);
          *(v26 - 5) = v32;
          v34 = *(v28 - 3);
          *(v26 - 4) = v33;
          v35 = *(v28 - 2);
          *(v26 - 3) = v34;
          v36 = *(v28 - 1);
          *(v26 - 2) = v35;
          *(v26 - 1) = v36;
          --v27;
        }
        while ( v27 );
        *v26 = *v28;
        if ( v22 > 0 )
        {
          v37 = v45;
          v38 = (unsigned int)v22;
          do
          {
            ((void (__fastcall *)(_QWORD, _QWORD))unk_1800010D0)(*v37++, (unsigned int)v21);
            --v38;
          }
          while ( v38 );
          v7 = a1;
        }
        v8 = v48;
      }
LABEL_52:
      v15 += 6;
    }
    while ( v15 != v16 );
    v12 = v39;
    v13 = v47;
    v5 = a4;
LABEL_54:
    ++v13;
    v39 = v12 + 1;
    v14 += 8;
    v47 = v13;
    ++v12;
  }
  while ( (unsigned __int64)v13 < 5 );
}

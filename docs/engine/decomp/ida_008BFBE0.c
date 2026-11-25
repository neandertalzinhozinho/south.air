// IDA 9.3  rva=0x8bfbe0  start=0x1808bfbe0  size=199
void __fastcall sub_1808BFBE0(__int64 a1, _QWORD *a2, __int64 *a3)
{
  int v3; // eax
  _QWORD *v4; // rbx
  _QWORD *v5; // rdi
  __int64 v6; // rbp
  unsigned int v7; // r14d
  __int64 v8; // rsi
  char *v9; // rdi
  __int64 v10; // rbp
  unsigned int v11; // r14d
  __int64 v12; // rsi
  __int64 v13; // rbx

  v3 = *((_DWORD *)a3 + 32);
  v4 = a3;
  v5 = a2;
  if ( *(_DWORD *)(a1 + 1024) == v3 )
  {
    v6 = *(int *)(a1 + 1024);
    if ( v6 > 0 )
    {
      v7 = *(_DWORD *)(a1 + 1028);
      v8 = a1 - (_QWORD)a3;
      v9 = (char *)((char *)a2 - (char *)a3);
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD, _QWORD))unk_180001190)(
          *(_QWORD *)((char *)v4 + (_QWORD)v9),
          *v4,
          *(_QWORD *)((char *)v4 + v8),
          v7);
        ++v4;
        --v6;
      }
      while ( v6 );
    }
  }
  else if ( v3 == 1 )
  {
    v10 = *(int *)(a1 + 1024);
    if ( v10 > 0 )
    {
      v11 = *(_DWORD *)(a1 + 1028);
      v12 = a1 - (_QWORD)a2;
      v13 = *a3;
      do
      {
        ((void (__fastcall *)(_QWORD, __int64, _QWORD, _QWORD))unk_180001190)(
          *v5,
          v13,
          *(_QWORD *)((char *)v5 + v12),
          v11);
        ++v5;
        --v10;
      }
      while ( v10 );
    }
  }
}

// IDA 9.3  rva=0x8c0230  start=0x1808c0230  size=177
void __fastcall sub_1808C0230(__int64 a1, __int64 *a2)
{
  int v2; // eax
  _QWORD *v3; // rbx
  __int64 v5; // rsi
  unsigned int v6; // ebp
  __int64 v7; // rdi
  __int64 v8; // rbp
  __int64 v9; // rsi
  __int64 v10; // rbx
  unsigned int v11; // r14d

  v2 = *((_DWORD *)a2 + 32);
  v3 = a2;
  if ( *(_DWORD *)(a1 + 1024) == v2 )
  {
    v5 = *(int *)(a1 + 1024);
    if ( v5 > 0 )
    {
      v6 = *(_DWORD *)(a1 + 1028);
      v7 = a1 - (_QWORD)a2;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001340)(*v3, *(_QWORD *)((char *)v3 + v7), v6);
        ++v3;
        --v5;
      }
      while ( v5 );
    }
  }
  else if ( v2 == 1 )
  {
    v8 = *(int *)(a1 + 1024);
    v9 = 0;
    if ( v8 > 0 )
    {
      v10 = *a2;
      v11 = *(_DWORD *)(a1 + 1028);
      do
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v10, *(_QWORD *)(a1 + 8 * v9++), v11);
      while ( v9 < v8 );
    }
  }
}

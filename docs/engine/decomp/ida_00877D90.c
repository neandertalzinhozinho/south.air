// sub_180877D90 @ 0x180877D90
__int64 __fastcall sub_180877D90(__int64 a1)
{
  int v1; // edx
  _BYTE *v2; // r8
  __int64 result; // rax

  v1 = 0;
  *(_BYTE *)(a1 + 11208) = 1;
  if ( *(_QWORD *)(a1 + 72) )
  {
    v2 = (_BYTE *)(a1 + 11192);
    do
    {
      ++v1;
      *v2 = 1;
      result = v1;
      ++v2;
    }
    while ( (unsigned __int64)v1 < *(_QWORD *)(a1 + 72) );
  }
  return result;
}

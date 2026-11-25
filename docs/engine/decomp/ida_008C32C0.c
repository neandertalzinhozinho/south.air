// IDA 9.3  rva=0x8c32c0  start=0x1808c32c0  size=266
void __fastcall sub_1808C32C0(__int64 a1, __int128 *a2, __int128 *a3)
{
  __int64 v3; // r10
  __int128 *v4; // rax
  __int64 v5; // r11
  __int128 v6; // xmm0
  __int128 v7; // xmm1
  __int128 v8; // xmm0
  __int128 v9; // xmm1
  __int128 v10; // xmm0
  __int128 v11; // xmm1
  __int128 v12; // xmm0
  __int128 v13; // xmm1
  __int128 *v14; // rax
  __int128 v15; // xmm0
  __int128 v16; // xmm1
  __int128 v17; // xmm0
  __int128 v18; // xmm1
  __int128 v19; // xmm0
  __int128 v20; // xmm1
  __int128 v21; // xmm0
  __int128 v22; // xmm1
  _BYTE v23[1040]; // [rsp+20h] [rbp-828h] BYREF
  _BYTE v24[1048]; // [rsp+430h] [rbp-418h] BYREF

  v3 = 8;
  v4 = (__int128 *)v23;
  v5 = 8;
  do
  {
    v4 += 8;
    v6 = *a3;
    v7 = a3[1];
    a3 += 8;
    *(v4 - 8) = v6;
    v8 = *(a3 - 6);
    *(v4 - 7) = v7;
    v9 = *(a3 - 5);
    *(v4 - 6) = v8;
    v10 = *(a3 - 4);
    *(v4 - 5) = v9;
    v11 = *(a3 - 3);
    *(v4 - 4) = v10;
    v12 = *(a3 - 2);
    *(v4 - 3) = v11;
    v13 = *(a3 - 1);
    *(v4 - 2) = v12;
    *(v4 - 1) = v13;
    --v5;
  }
  while ( v5 );
  *v4 = *a3;
  v14 = (__int128 *)v24;
  do
  {
    v14 += 8;
    v15 = *a2;
    v16 = a2[1];
    a2 += 8;
    *(v14 - 8) = v15;
    v17 = *(a2 - 6);
    *(v14 - 7) = v16;
    v18 = *(a2 - 5);
    *(v14 - 6) = v17;
    v19 = *(a2 - 4);
    *(v14 - 5) = v18;
    v20 = *(a2 - 3);
    *(v14 - 4) = v19;
    v21 = *(a2 - 2);
    *(v14 - 3) = v20;
    v22 = *(a2 - 1);
    *(v14 - 2) = v21;
    *(v14 - 1) = v22;
    --v3;
  }
  while ( v3 );
  *v14 = *a2;
  sub_1808CB040(v24, v23, a1 + 416);
}

// IDA 9.3  rva=0x8c3c20  start=0x1808c3c20  size=465
void __fastcall sub_1808C3C20(__int64 a1)
{
  __int64 v1; // rsi
  __int64 v2; // r11
  __int64 v3; // r10
  __int64 v5; // rbx
  float *v6; // rdx
  __int64 v7; // rax
  float v8; // xmm2_4
  float *v9; // rcx
  unsigned __int64 v10; // r8
  float v11; // xmm2_4
  float v12; // xmm0_4
  float v13; // xmm1_4
  float v14; // xmm2_4
  float v15; // xmm1_4
  float v16; // xmm2_4
  __int64 v17; // rcx
  unsigned __int64 v18; // r9
  float *v19; // r8
  float v20; // xmm2_4
  float v21; // xmm0_4
  float v22; // xmm1_4
  float v23; // xmm2_4
  float v24; // xmm1_4
  float v25; // xmm2_4

  v1 = *(int *)(a1 + 1024);
  v2 = 0;
  v3 = *(int *)(a1 + 1028);
  if ( v1 > 0 )
  {
    v5 = v3 - 2;
    do
    {
      v6 = *(float **)(a1 + 8 * v2);
      v7 = 0;
      v8 = *v6;
      if ( v3 >= 4 )
      {
        v9 = v6 + 2;
        v10 = ((unsigned __int64)(v3 - 4) >> 2) + 1;
        v7 = 4 * v10;
        do
        {
          v11 = v8 + (float)((float)(*(v9 - 2) - v8) * 0.1);
          v12 = *v9;
          v13 = *(v9 - 1) - v11;
          *(v9 - 2) = v11;
          v14 = v11 + (float)(v13 * 0.1);
          v15 = v9[1];
          *(v9 - 1) = v14;
          v16 = v14 + (float)((float)(v12 - v14) * 0.1);
          *v9 = v16;
          v8 = v16 + (float)((float)(v15 - v16) * 0.1);
          v9[1] = v8;
          v9 += 4;
          --v10;
        }
        while ( v10 );
      }
      for ( ; v7 < v3; ++v7 )
      {
        v8 = v8 + (float)((float)(v6[v7] - v8) * 0.1);
        v6[v7] = v8;
      }
      v17 = v3 - 2;
      if ( v5 >= 0 )
      {
        if ( v5 + 1 >= 4 )
        {
          v18 = (unsigned __int64)(v3 - 1) >> 2;
          v19 = &v6[v3 - 4];
          v17 = v5 - 4 * v18;
          do
          {
            v20 = v8 + (float)((float)(v19[2] - v8) * 0.1);
            v21 = *v19;
            v22 = v19[1] - v20;
            v19[2] = v20;
            v23 = v20 + (float)(v22 * 0.1);
            v24 = *(v19 - 1);
            v19[1] = v23;
            v25 = v23 + (float)((float)(v21 - v23) * 0.1);
            *v19 = v25;
            v8 = v25 + (float)((float)(v24 - v25) * 0.1);
            *(v19 - 1) = v8;
            v19 -= 4;
            --v18;
          }
          while ( v18 );
        }
        for ( ; v17 >= 0; --v17 )
        {
          v8 = v8 + (float)((float)(v6[v17] - v8) * 0.1);
          v6[v17] = v8;
        }
      }
      ++v2;
    }
    while ( v2 < v1 );
  }
}

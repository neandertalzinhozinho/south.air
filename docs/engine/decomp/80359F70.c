// FUN_180359f70 @ 0x180359f70

/* WARNING: Instruction at (ram,0x00018035a314) overlaps instruction at (ram,0x00018035a312)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x00018035a540) */
/* WARNING: Removing unreachable block (ram,0x00018035a0e4) */
/* WARNING: Removing unreachable block (ram,0x000180359ff2) */
/* WARNING: Removing unreachable block (ram,0x00018035a017) */
/* WARNING: Removing unreachable block (ram,0x00018035a312) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

undefined8 FUN_180359f70(longlong param_1,undefined8 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined8 uVar3;
  uint uVar4;
  uint uVar5;
  uint *puVar6;
  uint uVar7;
  ulonglong uVar8;
  undefined4 *puVar9;
  ulonglong uVar10;
  uint uVar11;
  longlong *plVar12;
  bool bVar13;
  undefined1 local_res0;
  undefined1 auStack_198 [32];
  uint local_178;
  undefined8 local_170;
  uint auStack_168 [2];
  uint *local_160;
  undefined8 local_150;
  uint uStack_148;
  uint local_140;
  uint local_130;
  undefined4 uStack_118;
  undefined4 uStack_114;
  longlong lStack_108;
  undefined *puStack_100;
  longlong lStack_f0;
  undefined1 uStack_e8;
  undefined1 local_e0 [40];
  undefined1 local_b8 [16];
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 local_90;
  ulonglong local_48;
  
  local_48 = DAT_1821c7640 ^ (ulonglong)auStack_198;
  uVar5 = (uint)&local_res0;
  if (((ulonglong)&local_res0 & 0x1e8) == 0) {
    uVar4 = ((uVar5 & 0x15ff) + 1) * (uVar5 & 0x15ff) + 0x67a3 & 0x80000001;
  }
  else {
    uVar4 = (((uVar5 & 0x1fff) + 1) * (uVar5 & 0x1fff) + 7) % 0x51;
  }
  local_130 = ((int)(-uVar4 | uVar4) >> 0x1f) * -0x608 ^ 0xc38;
  if (((((uVar5 & 0x29ff) + 1) * (uVar5 & 0x29ff) + 7) % 0x51 & 0x40) == 0) {
    uVar5 = (uVar5 & 0x13ff) * (uVar5 & 0x13ff) * 0x10 + 4;
    iVar2 = (uVar5 / 0x13) * 0x13;
  }
  else {
    uVar5 = ((uVar5 & 0x31ff) + 1) * (uVar5 & 0x31ff) + 7;
    iVar2 = (uVar5 / 0x51) * 0x51;
  }
  local_140 = ((int)(-(uVar5 - iVar2) | uVar5 - iVar2) >> 0x1f) * -0xb096 ^ 0xb086;
  local_a8 = 0;
  uStack_a0 = 0;
  uVar5 = 0;
  local_98 = 0;
  local_90 = 0;
  FUN_18032aec0(&local_a8,param_2,(longlong)param_3);
  FUN_180348880(local_e0,&local_a8);
  uVar3 = FUN_180364e50(local_b8,local_e0);
  FUN_180827f40(param_1 + 0x1c0,uVar3);
  local_150 = 0x100;
  local_160 = &DAT_1809eed8c;
  local_170 = &DAT_1809eee8c;
  local_178 = (((((DAT_1809eed8c ^ 0x811c9ddb) * 0x1000193 ^ DAT_1809eed90) * 0x1000193 ^
                DAT_1809eed94) * 0x1000193 ^ DAT_1809eed98) * 0x1000193 ^ DAT_1809eed9c) * 0x1000193
  ;
  do {
    FUN_1803d4d50();
    FUN_180359a3c();
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  do {
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  local_178 = (((((((((((((local_178 ^ DAT_1809eeda0) * 0x1000193 ^ DAT_1809eeda4) * 0x1000193 ^
                        DAT_1809eeda8) * 0x1000193 ^ DAT_1809eedac) * 0x1000193 ^ DAT_1809eedb0) *
                      0x1000193 ^ DAT_1809eedb4) * 0x1000193 ^ _UNK_1809eedb8) * 0x1000193 ^
                   _UNK_1809eedbc) * 0x1000193 ^ _UNK_1809eedc0) * 0x1000193 ^ _UNK_1809eedc4) *
                 0x1000193 ^ _UNK_1809eedc8) * 0x1000193 ^ _UNK_1809eedcc) * 0x1000193 ^
              _UNK_1809eedd0) * 0x1000193;
  do {
    local_178 = local_178 ^ _UNK_1809eedd4;
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  local_178 = (local_178 * 0x1000193 ^ _UNK_1809eedd8) * 0x1000193;
  lStack_f0 = param_1 + 0xef0;
  uStack_e8 = 0;
  iVar2 = (*DAT_181d8c870)(lStack_f0,&UNK_1809eedd4,0);
  if (iVar2 != 0) {
    (*DAT_181d8c848)(5);
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if (*(int *)(param_1 + 0xf3c) == 0x7fffffff) {
    *(int *)(param_1 + 0xf3c) = *(int *)(param_1 + 0xf3c) + -1;
    (*DAT_181d8c848)(6);
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  uStack_e8 = 1;
  uVar11 = (local_178 ^ _UNK_1809eeddc) * 0x1000193;
  uVar4 = uVar11 & 0x11ff;
  uVar4 = (uVar4 - 1) * uVar4 - 1 & 1;
  uVar4 = (int)(-uVar4 | uVar4) >> 0x1f;
  uVar8 = (longlong)(((int)(-uVar4 | uVar4) >> 0x1f) * -0x5b61) ^ 0x5b41;
  do {
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  uVar4 = ((((uVar11 ^ *(uint *)(&UNK_1809eedc0 + uVar8)) * 0x1000193 ^
            *(uint *)(&UNK_1809eedc4 + uVar8)) * 0x1000193 ^ *(uint *)(&UNK_1809eedc8 + uVar8)) *
           0x1000193 ^ *(uint *)(&UNK_1809eedcc + uVar8)) * 0x1000193 ^
          *(uint *)(&UNK_1809eedd0 + uVar8);
  local_178 = uVar4 * 0x1000193;
  do {
    bVar13 = (POPCOUNT(uVar4 & 0xff) & 1U) == 0;
    func_0x000180358891(0xde3c);
    if (!bVar13) {
      uVar5 = ~(~uVar5 + 1) + 1;
    }
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  local_178 = (local_178 ^ *(uint *)(&UNK_1809eedd4 + uVar8)) * 0x1000193;
  do {
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  do {
    func_0x00018035bd8d(0xde3c);
    FUN_180359f61();
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  local_178 = ((local_178 ^ *(uint *)(&UNK_1809eedd8 + uVar8)) * 0x1000193 ^
              *(uint *)(&UNK_1809eeddc + uVar8)) * 0x1000193;
  do {
    plVar12 = &lStack_108;
    puVar9 = &uStack_118;
    puVar6 = auStack_168;
                    /* WARNING: Call to offcut address within same function */
    func_0x00018035a30f();
    *puVar6 = 0x788c7792;
    *puVar9 = 0x22;
    *plVar12 = (longlong)&UNK_18035a807;
    uVar4 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar4 != 0);
  uVar11 = ((auStack_168[0] ^ 0x9275c65e) & 0xf0f0f0f) << 4 |
           (auStack_168[0] ^ 0x9275c65e) >> 4 & 0xf0f0f0f;
  uVar4 = uVar11 >> 10;
  uVar11 = uVar11 << 0x16 | uVar4;
  uVar11 = (uVar11 >> 0x10 | uVar4 << 0x10) & 0xdd6b2294 |
           (uVar4 << 0x10 | uVar11 >> 0x10) & 0x2294dd6b;
  uVar4 = (uVar11 >> 8 ^ uVar11) >> 0xc & 1;
  uVar7 = uVar11 ^ (uVar4 << 8 | uVar4) << 0xc;
  uVar4 = uVar7 >> 8;
  uVar11 = (uVar4 | uVar11 << 0x18) & 0x8c738c73 | (uVar7 << 8 | uVar11 >> 0x18) & 0x738c738c;
  uVar11 = ((uVar11 >> 2 | uVar4 << 0x1e) & 0x99999999 | (uVar11 << 2 | uVar11 >> 0x1e) & 0x66666666
           ) + 0x1fd25b68;
  uVar4 = (uVar11 >> 9 ^ uVar11) >> 0xe & 0x7f;
  do {
    uStack_114 = 0x54;
    puStack_100 = &UNK_18035a907;
    uVar7 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar7 < 0) {
      uVar7 = (uVar7 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar7 != 0);
  lStack_108 = (int)(uVar11 ^ (uVar4 << 9 | uVar4) << 0xe) + lStack_108;
  uVar10 = (ulonglong)((uint)((ulonglong)dvs_0x4259caa4_mfort6317_ >> 0x1d) & 0x9500100) +
           *(longlong *)(lStack_108 + 4);
  uVar10 = ~((uVar10 * 0x10 | uVar10 >> 0x3c) & 0xb4b4b4b4b4b4b4b4 |
            (uVar10 >> 4 | *(longlong *)(lStack_108 + 4) << 0x3c) & 0x4b4b4b4b4b4b4b4b);
  uVar4 = (uint)((uVar10 >> 0x1b ^ uVar10) >> 10) & 0xffffff;
  uVar10 = ((ulonglong)uVar4 << 0x1b | (ulonglong)uVar4) << 10 ^ uVar10 ^ 0xe4fdfcc99d6a4fae;
  uVar10 = (uVar10 & 0x3333333333333333) << 2 | uVar10 >> 2 & 0x3333333333333333;
  uVar10 = uVar10 << 0x2a | uVar10 >> 0x16;
  uVar4 = (uint)((uVar10 >> 0x1e ^ uVar10) >> 6) & 0xfffffff;
  uVar10 = ((ulonglong)uVar4 << 0x1e | (ulonglong)uVar4) << 6 ^ uVar10;
  uVar10 = (uVar10 >> 8 | uVar10 << 0x38) & 0xf20df20df20df20d |
           (uVar10 << 8 | uVar10 >> 0x38) & 0xdf20df20df20df2;
  uVar10 = (uVar10 >> 0x10 | uVar10 << 0x30) & 0xcb5f34a0cb5f34a0 |
           (uVar10 << 0x10 | uVar10 >> 0x30) & 0x34a0cb5f34a0cb5f;
  *(ulonglong *)(lStack_108 + 4) = uVar10;
  dvs_0x4259caa4_mfort6317_ =
       (uint *)((longlong)dvs_0x4259caa4_mfort6317_ + (uVar10 >> 0x1f & 0xa008381d));
  local_170 = (undefined *)
              (CONCAT44(local_170._4_4_,(int)(*(ulonglong *)(lStack_108 + 4) >> 6)) &
              0xffffffff7fffffff);
  local_150 = CONCAT44(local_150._4_4_,(int)(*(ulonglong *)(lStack_108 + 4) >> 0x16)) ^ 0x2ec99aeb;
  local_160 = (uint *)(*(ulonglong *)(lStack_108 + 4) ^ 0x931bb1b4fa19c26e);
  local_178 = (((((((((((local_178 ^ *(uint *)(&UNK_1809eede0 + uVar8)) * 0x1000193 ^
                       *(uint *)(&UNK_1809eede4 + uVar8)) * 0x1000193 ^
                      *(uint *)(&UNK_1809eede8 + uVar8)) * 0x1000193 ^
                     *(uint *)(&UNK_1809eedec + uVar8)) * 0x1000193 ^
                    *(uint *)(&UNK_1809eedf0 + uVar8)) * 0x1000193 ^
                   *(uint *)(&UNK_1809eedf4 + uVar8)) * 0x1000193 ^
                  *(uint *)(&UNK_1809eedf8 + uVar8)) * 0x1000193 ^ *(uint *)(&UNK_1809eedfc + uVar8)
                 ) * 0x1000193 ^ *(uint *)(&UNK_1809eee00 + uVar8)) * 0x1000193 ^
               *(uint *)(&UNK_1809eee04 + uVar8)) * 0x1000193 ^ *(uint *)(&UNK_1809eee08 + uVar8)) *
              0x1000193;
  auStack_168[0] = uVar5;
  uStack_148 = uVar5;
  func_0x00018035bcad();
  func_0x00018035abf5();
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}


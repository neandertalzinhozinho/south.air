// FUN_1803589b0 @ 0x1803589b0

char FUN_1803589b0(longlong param_1,undefined8 param_2)

{
  char cVar1;
  uint uVar2;
  uint *puVar3;
  int unaff_retaddr;
  undefined1 auStack_178 [32];
  undefined4 local_158;
  undefined8 local_150;
  undefined8 local_148;
  undefined *local_140;
  uint local_118;
  int local_114;
  longlong local_108;
  undefined8 local_d0;
  undefined1 local_c8 [16];
  undefined1 local_b8 [120];
  ulonglong local_40;
  
  local_40 = DAT_1821c7640 ^ (ulonglong)auStack_178;
  local_150 = CONCAT44(local_150._4_4_,1);
  local_108 = param_1;
  local_d0 = param_2;
  FUN_180826210(param_1 + 0x1c0,local_c8);
  FUN_18034aaa0(local_b8,local_c8);
  do {
    puVar3 = &local_118;
    FUN_18035704c();
    *puVar3 = 0x54816363;
    FUN_180359f61();
    uVar2 = (unaff_retaddr + 1) * unaff_retaddr & 0x80000001;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar2 != 0);
  uVar2 = ~(local_118 << 6 | local_118 >> 0x1a) + 0x3081f790;
  uVar2 = (uVar2 * 0x20 | uVar2 >> 0x1b) + 0x7b2721b1;
  local_114 = ~((uVar2 * 0x8000000 | uVar2 >> 5) + 0xc52c3310) + 0xaeafdf61;
  local_140 = &DAT_1817d18c0;
  local_158 = 0x5bd1e995;
  local_148 = 0x3a82babbfb4ac6da;
  local_150 = 0x1fb4ac6da;
  cVar1 = FUN_180358566();
  return cVar1 + -0x75;
}


// FUN_180350f20 @ 0x180350f20

/* WARNING: Removing unreachable block (ram,0x000180351037) */
/* WARNING: Removing unreachable block (ram,0x00018035104b) */
/* WARNING: Removing unreachable block (ram,0x00018035101b) */

longlong FUN_180350f20(undefined8 param_1,undefined8 param_2,undefined4 param_3)

{
  undefined8 uVar1;
  ulonglong uVar2;
  uint uVar3;
  uint *puVar4;
  int unaff_retaddr;
  undefined1 auStack_138 [36];
  uint local_114;
  undefined8 local_110;
  undefined4 local_104;
  undefined4 local_fc;
  undefined8 local_f8;
  code *local_f0;
  undefined8 local_d8;
  undefined4 local_d0;
  ulonglong local_58;
  
  local_58 = DAT_1821c7640 ^ (ulonglong)auStack_138;
  local_d0 = 0x3a0;
  local_d8 = 0x100;
  local_f8 = 0x180a999ac;
  local_104 = 0xbf0;
  local_110 = 0x180a99aac;
  local_fc = param_3;
  do {
    puVar4 = &local_114;
                    /* WARNING: Call to offcut address within same function */
    func_0x000180351272(puVar4,&local_114);
    uVar1 = rdtsc();
    *puVar4 = (uint)uVar1 ^ (uint)((ulonglong)uVar1 >> 0x20);
    uVar3 = (unaff_retaddr + 1) * unaff_retaddr & 0x80000001;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar3 != 0);
  local_114 = (local_114 * -0x166a13ad >> 0x18 ^ local_114 * -0x166a13ad) * -0x50285029;
  uVar2 = (ulonglong)local_114;
  if (local_114 < 0x147ae13f) {
    do {
      local_f0 = FUN_180612ae0;
      uVar3 = (unaff_retaddr + 1) * unaff_retaddr & 0x80000001;
      if ((int)uVar3 < 0) {
        uVar3 = (uVar3 - 1 | 0xfffffffe) + 1;
      }
    } while (uVar3 != 0);
    uVar2 = FUN_180612ae0(0,0xbe57);
    if (1 < uVar2) {
      uVar2 = FUN_180330280();
    }
  }
  return ~((uVar2 ^ 0xffffffffffffffff) + 1) + 1;
}


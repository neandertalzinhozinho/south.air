// FUN_18034db80 @ 0x18034db80

/* WARNING: Instruction at (ram,0x00018034dcc7) overlaps instruction at (ram,0x00018034dcc6)
    */

longlong FUN_18034db80(undefined8 param_1,undefined1 param_2)

{
  ulonglong uVar1;
  longlong lVar2;
  undefined8 *puVar3;
  undefined1 local_180 [48];
  undefined8 local_150;
  undefined1 auStack_138 [32];
  undefined4 local_118;
  undefined1 local_114;
  undefined4 local_104;
  undefined4 local_d0;
  undefined8 local_c8;
  ulonglong local_40;
  
  local_40 = DAT_1821c7640 ^ (ulonglong)auStack_138;
  local_118 = 0xc5;
  lVar2 = 0x34e970;
  local_104 = 0xac0;
  local_d0 = 0x8f0;
                    /* WARNING: Call to offcut address within same function */
  local_150 = 0x18034dc7d;
  local_114 = param_2;
  local_c8 = param_1;
  uVar1 = func_0x00018034dca3();
  puVar3 = (undefined8 *)(local_180 + 0x38);
  lVar2 = lVar2 + -1;
  if (lVar2 != 0) {
    puVar3 = (undefined8 *)((ulonglong)local_180 & 0xffffffff);
  }
  local_180[lVar2 * 4 + 0x1ac] = local_180[lVar2 * 4 + 0x1ac] - (char)lVar2;
  *puVar3 = 0x1f1;
  puVar3[-1] = 0x844;
  puVar3[-2] = 0x71a;
  puVar3[-3] = 0x6dd;
  puVar3[-4] = 0xffffffffffff9ce9;
  puVar3[-5] = 0x714;
  puVar3[-6] = 0xffffffffffff9e5e;
  puVar3[-7] = 0x6dd;
  puVar3[-8] = 0x38ce;
  return (-(uVar1 & 0xffffffffffffff49) ^ 0xffffffffffffffff) + 1;
}


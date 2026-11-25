// FUN_180354f90 @ 0x180354f90

/* WARNING: Instruction at (ram,0x000180355272) overlaps instruction at (ram,0x00018035526f)
    */
/* WARNING: Removing unreachable block (ram,0x000180354ffe) */
/* WARNING: Removing unreachable block (ram,0x000180355069) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_180354f90(undefined8 param_1,undefined4 param_2)

{
  uint uVar1;
  ulonglong uVar2;
  int iVar3;
  uint uVar4;
  ulonglong uVar5;
  ulonglong uVar6;
  ulonglong uVar7;
  undefined1 local_res0;
  undefined1 auStack_118 [32];
  int local_f8;
  undefined *local_f0;
  undefined *local_e8;
  undefined4 local_c8;
  undefined8 local_b0;
  ulonglong local_40;
  
  local_40 = DAT_1821c7640 ^ (ulonglong)auStack_118;
  uVar1 = (uint)&local_res0;
  if ((uVar1 >> 9 & 1) == 0) {
    uVar4 = uVar1 & 0x37f;
    iVar3 = (uVar4 + 2) * (uVar4 + 1) * uVar4;
    uVar4 = 0xb875 << ((byte)(((iVar3 >> 1) - (iVar3 >> 3)) + iVar3 * 0x55555555 >> 0x1e) & 0x1f);
  }
  else {
    uVar4 = 0xb875;
  }
  uVar1 = uVar1 & 0x2ff;
  uVar7 = (ulonglong)(((uVar1 + 2) * (uVar1 + 1) * uVar1) % 3 + 0xb415 ^ uVar4);
  uVar5 = 0x104d0c80;
  local_f0 = &UNK_180826864;
  local_e8 = &UNK_180826964;
  local_f8 = ((((((((((((_UNK_180826864 * 0x25 + _UNK_180826868) * 0x25 + _UNK_18082686c) * 0x25 +
                      _UNK_180826870) * 0x25 + _UNK_180826874) * 0x25 + _UNK_180826878) * 0x25 +
                   _UNK_18082687c) * 0x25 + _UNK_180826880) * 0x25 + _UNK_180826884) * 0x25 +
                _UNK_180826888) * 0x25 + _UNK_18082688c) * 0x25 + _UNK_180826890) * 0x25 +
             _UNK_180826894) * 0x25 + _UNK_180826898;
  local_c8 = param_2;
  local_b0 = param_1;
  do {
    uVar2 = 0;
    FUN_1803561ea();
    uVar6 = uVar5 ^ uVar7;
    if ((uVar2 & 0x42) == 0) {
      uVar7 = uVar5;
    }
    uVar5 = uVar7;
    uVar7 = uVar6 ^ uVar5;
    uVar1 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar1 < 0) {
      uVar1 = (uVar1 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar1 != 0);
  local_f8 = (((((local_f8 * 0x25 + _UNK_18082689c) * 0x25 + _UNK_1808268a0) * 0x25 + _UNK_1808268a4
               ) * 0x25 + _UNK_1808268a8) * 0x25 + _UNK_1808268ac) * 0x25 + _UNK_1808268b0;
                    /* WARNING: Call to offcut address within same function */
  func_0x000180355333();
                    /* WARNING: Could not recover jumptable at 0x0001803554d0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)(uVar5 + 0xd2))();
  return;
}


// FUN_180356970 @ 0x180356970

/* WARNING: Removing unreachable block (ram,0x000180356a47) */
/* WARNING: Removing unreachable block (ram,0x0001803569d8) */
/* WARNING: Removing unreachable block (ram,0x000180356a26) */
/* WARNING: Removing unreachable block (ram,0x000180356a98) */

void FUN_180356970(undefined8 param_1,undefined8 param_2,undefined4 param_3)

{
  undefined8 uVar1;
  uint uVar2;
  ulonglong uVar3;
  ulonglong uVar4;
  uint uVar5;
  uint *puVar6;
  undefined4 *puVar7;
  longlong lVar8;
  longlong *plVar9;
  undefined1 local_res0;
  undefined1 auStack_148 [32];
  uint local_128;
  undefined4 *local_120;
  undefined *local_118;
  uint local_110;
  undefined1 local_10c [8];
  uint local_104 [4];
  undefined4 local_f4;
  uint local_e4;
  uint local_e0;
  undefined8 local_d8;
  undefined8 local_d0;
  undefined8 local_c8;
  undefined4 local_bc;
  undefined4 local_b8 [2];
  longlong local_b0;
  longlong local_a8 [13];
  ulonglong local_40;
  
  local_40 = DAT_1821c7640 ^ (ulonglong)auStack_148;
  uVar2 = (uint)&local_res0 & 0x1aff;
  uVar2 = (uVar2 + 1) * uVar2 + 7;
  local_e0 = -(0 >> ((char)uVar2 + (char)(uVar2 / 0x51) * -0x51 & 0x1fU)) - 0x1289U & 0x4466 ^
             0x4906;
  local_120 = &DAT_180c19870;
  local_118 = &DAT_180c19970;
  uVar2 = DAT_180c19870 >> 0x1c ^ (DAT_180c19870 ^ 0xb50) << 4 ^ DAT_180c19874;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c19878;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c1987c;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c19880;
  local_128 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c19884;
  local_f4 = param_3;
  local_d8 = param_2;
  local_d0 = param_1;
  local_c8 = param_2;
  do {
    func_0x00018035764a();
    FUN_18044f65b();
    uVar2 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar2 != 0);
  uVar2 = local_128 >> 0x1c ^ local_128 << 4 ^ DAT_180c19888;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c1988c;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c19890;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c19894;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c19898;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c1989c;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198a0;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198a4;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198a8;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198ac;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198b0;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198b4;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198b8;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198bc;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198c0;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198c4;
  uVar2 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198c8;
  local_128 = uVar2 >> 0x1c ^ uVar2 << 4 ^ DAT_180c198cc;
  do {
    FUN_180354f6f(0x6528);
    uVar2 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar2 != 0);
  local_128 = local_128 >> 0x1c ^ local_128 << 4 ^ DAT_180c198d0;
  do {
    local_110 = 0xa3bbf99b;
    local_bc = 0x58;
    local_b0 = 0x180356de7;
    FUN_18035704c();
    uVar2 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar2 != 0);
  uVar5 = ~((local_110 << 0x10 | local_110 >> 0x10) & 0xb71748e8 |
           (local_110 >> 0x10 | local_110 << 0x10) & 0x48e8b717);
  uVar2 = (uVar5 >> 9 ^ uVar5) >> 4 & 7;
  uVar5 = ~((uVar2 << 9 | uVar2) << 4 ^ uVar5);
  uVar2 = (uVar5 >> 0x15 ^ uVar5) & 0x3f;
  uVar2 = uVar5 ^ (uVar2 << 0x15 | uVar2);
  uVar5 = ((uVar2 >> 4 | uVar2 << 0x1c) & 0xd2d2d2d2 | (uVar2 << 4 | uVar5 >> 0x1c) & 0x2d2d2d2d) ^
          0x83306ff4;
  uVar2 = (uVar5 >> 7 ^ uVar5) >> 0xc & 0x3f;
  uVar5 = uVar5 ^ (uVar2 << 7 | uVar2) << 0xc;
  local_110 = (uVar5 << 0x10 | uVar5 >> 0x10) & 0xa2755d8a |
              (uVar5 >> 0x10 | uVar5 << 0x10) & 0x5d8aa275;
  do {
    plVar9 = local_a8;
    puVar7 = local_b8;
    puVar6 = local_104;
    FUN_180355f0d();
    *puVar6 = 0x3c51f523;
    *puVar7 = 0x18;
    *plVar9 = 0x180356ee7;
    func_0x000180355271();
    uVar2 = (_local_res0 + 1) * _local_res0 & 0x80000001;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar2 != 0);
  uVar2 = (local_104[0] >> 2 ^ local_104[0]) & 3;
  uVar2 = local_104[0] ^ (uVar2 * 4 | uVar2);
  uVar5 = ~((uVar2 >> 2 & 0xcccccccc | uVar2 << 0x1e |
            (uVar2 & 0xccccccc) << 2 | local_104[0] >> 0x1e) + 0x446a7ac1);
  uVar2 = (uVar5 >> 2 ^ uVar5) >> 3 & 3;
  uVar5 = (uVar2 * 4 | uVar2) << 3 ^ uVar5 ^ 0xdf8ef083;
  uVar2 = uVar5 >> 1;
  uVar2 = (uVar2 & 0x33333333) << 2 | (uVar5 << 0x1f | uVar2 & 0xcccccccc) >> 2;
  lVar8 = (longlong)(int)local_110;
  local_110 = 0;
  local_104[0] = 0;
  plVar9 = (longlong *)(lVar8 + local_b0 + 4);
  *plVar9 = *plVar9 + (ulonglong)
                      ((uint)(*(ulonglong *)
                               (((longlong)(int)(uVar2 << 4 | uVar2 >> 0x1c) & 0xffffffffa5a5a5a5U |
                                (ulonglong)((uVar2 >> 4 | uVar2 << 0x1c) & 0x5a5a5a5a)) +
                                local_a8[0] + 4) >> 0xe) & 0x37401080);
  uVar1 = rdtsc();
  local_e4 = (uint)uVar1 ^ (uint)((ulonglong)uVar1 >> 0x20);
  uVar4 = (((ulonglong)(local_e4 >> 0xc) | (ulonglong)local_e4 << 0x34) - 0x67996518) +
          (ulonglong)local_e4 * 4;
  uVar3 = uVar4 * 0x1000 | uVar4 >> 0x34;
  uVar4 = ((-uVar3 ^ 0xffffffffffffffff) + 1) - ((uVar4 & 0xfffffffffffff) >> 2 | uVar3 << 0x32);
  FUN_18035704d(local_10c,uVar4 >> 0xd | uVar4 << 0x33);
  return;
}


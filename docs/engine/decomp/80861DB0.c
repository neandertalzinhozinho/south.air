// FUN_180861db0 @ 0x180861db0

/* WARNING: Removing unreachable block (ram,0x000180861dfc) */
/* WARNING: Removing unreachable block (ram,0x000180861e99) */
/* WARNING: Removing unreachable block (ram,0x000180861e0b) */

void FUN_180861db0(void)

{
  uint uVar1;
  longlong unaff_R15;
  int unaff_retaddr;
  
  do {
    uVar1 = (unaff_retaddr + 1) * unaff_retaddr & 0x80000001;
    if ((int)uVar1 < 0) {
      uVar1 = (uVar1 - 1 | 0xfffffffe) + 1;
    }
  } while (uVar1 != 0);
                    /* WARNING: Call to offcut address within same function */
  func_0x000180862040();
  func_0x00010bd25fc2();
                    /* WARNING: Could not recover jumptable at 0x0001808621d6. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)(unaff_R15 + 0x108897))();
  return;
}


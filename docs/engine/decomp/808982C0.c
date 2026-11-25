// FUN_1808982c0 @ 0x1808982c0

int * FUN_1808982c0(longlong param_1,int *param_2)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x14);
  param_2[4] = 0;
  param_2[5] = 0;
  param_2[6] = *(int *)(param_1 + 0xc);
  *param_2 = iVar1;
  *(longlong *)(param_2 + 2) = param_1;
  if (0 < (longlong)iVar1) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(param_2 + 4,param_1,(longlong)iVar1 << 3);
  }
  return param_2;
}


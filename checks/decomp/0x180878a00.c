 (GhidraScript)  

void FUN_180878a00(longlong *param_1)

{
  code *pcVar1;
  longlong lVar2;
  ulonglong uVar3;
  longlong lVar4;
  
  if (*param_1 == 0) {
    return;
  }
  lVar2 = param_1[1];
  for (lVar4 = *param_1; lVar4 != lVar2; lVar4 = lVar4 + 8) {
    FUN_180878920(lVar4);
  }
  lVar4 = *param_1;
  uVar3 = param_1[2] - *param_1 & 0xfffffffffffffff8;
  lVar2 = lVar4;
  if (0xfff < uVar3) {
    lVar2 = *(longlong *)(lVar4 + -8);
    if (0x1f < (lVar4 - lVar2) - 8U) {
      (*DAT_181d8d900)(lVar4 - lVar2,uVar3 + 0x27);
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  thunk_FUN_181798f60(lVar2);
}

 (GhidraScript)  

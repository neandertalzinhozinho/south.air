 (GhidraScript)  

void FUN_180878a90(longlong *param_1)

{
  longlong lVar1;
  code *pcVar2;
  longlong lVar3;
  ulonglong uVar4;
  
  if (*param_1 == 0) {
    return;
  }
  FUN_180881a20(*param_1,param_1[1]);
  lVar1 = *param_1;
  uVar4 = param_1[2] - *param_1 & 0xfffffffffffffff8;
  lVar3 = lVar1;
  if (0xfff < uVar4) {
    lVar3 = *(longlong *)(lVar1 + -8);
    if (0x1f < (lVar1 - lVar3) - 8U) {
      (*DAT_181d8d900)(lVar1 - lVar3,uVar4 + 0x27);
      pcVar2 = (code *)swi(3);
      (*pcVar2)();
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  thunk_FUN_181798f60(lVar3);
}

 (GhidraScript)  

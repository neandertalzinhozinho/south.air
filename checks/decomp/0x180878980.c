 (GhidraScript)  

void FUN_180878980(longlong *param_1)

{
  longlong lVar1;
  
  lVar1 = param_1[4];
  if (lVar1 != 0) {
    (*DAT_181d8d738)((lVar1 + -1) - (ulonglong)*(byte *)(lVar1 + -1));
  }
  param_1[4] = 0;
  lVar1 = param_1[2];
  if (lVar1 != 0) {
    (*DAT_181d8d738)((lVar1 + -1) - (ulonglong)*(byte *)(lVar1 + -1));
    param_1[2] = 0;
  }
  lVar1 = *param_1;
  if (lVar1 != 0) {
    (*DAT_181d8d738)((lVar1 + -1) - (ulonglong)*(byte *)(lVar1 + -1));
    *param_1 = 0;
  }
  return;
}

 (GhidraScript)  

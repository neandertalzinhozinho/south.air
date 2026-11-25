 (GhidraScript)  

undefined8 FUN_180002c80(longlong param_1,longlong param_2,int param_3)

{
  if ((param_1 == 0) || (param_2 == 0)) {
    return 0xfffffff8;
  }
  if (param_3 < 1) {
    return 0xfffffffa;
  }
  if (0x1fffffff < param_3) {
    do {
      FUN_180026540(param_1,param_2,0x7fffffe0);
      param_3 = param_3 + -0x1ffffff8;
      param_1 = param_1 + 0x7fffffe0;
      param_2 = param_2 + 0x7fffffe0;
    } while (0x1fffffff < param_3);
  }
  FUN_180026540(param_1,param_2,param_3 << 2);
  return 0;
}

 (GhidraScript)  

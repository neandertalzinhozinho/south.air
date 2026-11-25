 (GhidraScript)  

undefined8 FUN_180026540(longlong param_1,longlong param_2,int param_3)

{
  if ((param_1 == 0) || (param_2 == 0)) {
    return 0xfffffff8;
  }
  if (param_3 < 1) {
    return 0xfffffffa;
  }
  if (param_3 < 0x8000) {
    FUN_181d2eb40();
  }
  else {
    FUN_1800699c0();
  }
  return 0;
}

 (GhidraScript)  

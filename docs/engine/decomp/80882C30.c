// FUN_180882c30 @ 0x180882c30

void FUN_180882c30(undefined8 *param_1,undefined8 *param_2,float param_3)

{
  undefined8 uVar1;
  ulonglong uVar2;
  undefined4 uVar3;
  double dVar4;
  
  FUN_180001310(*param_2,param_2,*param_1,param_1[1] & 0xffffffff);
  FUN_180001220();
  uVar1 = *param_1;
  uVar2 = param_1[1];
  dVar4 = (double)FUN_181c9a5ad(DAT_18207a190,DAT_18207a078);
  FUN_180001100(uVar1,uVar2 & 0xffffffff,(float)(dVar4 * (double)param_3),4);
  FUN_1801c84d0();
  uVar3 = DAT_182079f9c;
  FUN_1800012e0();
  FUN_1801c8530(*param_1,*param_1,param_1[1] & 0xffffffff);
  FUN_180001100(*param_1,param_1[1] & 0xffffffff,0,0);
  FUN_1801c84d0();
  FUN_180001100(*param_1,param_1[1] & 0xffffffff,uVar3,4);
  return;
}


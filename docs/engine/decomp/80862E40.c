// FUN_180862e40 @ 0x180862e40

void FUN_180862e40(undefined8 param_1,undefined8 param_2,double param_3)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  
  uVar1 = FUN_181796cf4(0xc1a8);
  uVar1 = FUN_1808634a0(uVar1,param_1,param_2,(float)param_3);
  puVar2 = (undefined8 *)FUN_181796cf4(0x58);
  puVar2[1] = &LAB_180862ef0;
  puVar2[2] = &LAB_180862f00;
  puVar2[3] = FUN_180862f10;
  puVar2[4] = FUN_180862f40;
  puVar2[5] = FUN_180863020;
  puVar2[6] = 0;
  puVar2[7] = 0;
  puVar2[8] = 0;
  puVar2[9] = 0;
  *puVar2 = uVar1;
  puVar2[10] = &LAB_180863070;
  return;
}


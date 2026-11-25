 (GhidraScript)  

void FUN_180880390(longlong *param_1,longlong param_2)

{
  ulonglong *puVar1;
  longlong lVar2;
  ulonglong uVar3;
  longlong *plVar4;
  longlong lVar5;
  int iVar6;
  ulonglong uVar7;
  ulonglong uVar8;
  undefined8 *puVar9;
  int iVar10;
  ulonglong uVar11;
  ulonglong uVar12;
  int local_res18;
  longlong local_res20;
  undefined8 local_68;
  int local_60;
  
  local_res18 = 0;
3 != 0) {
    local_res20 = 0;
    do {
      puVar1 = *(ulonglong **)(local_res20 + *param_1);
      lVar2 = *(longlong *)(local_res20 + param_2);
      FUN_1800010a0(lVar2,puVar1 + 8,0x20);
      uVar11 = 0x20;
      uVar12 = 1;
      if (0x20 < *puVar1) {
3) - 1;
        do {
          uVar3 = puVar1[0x42];
          uVar8 = uVar12;
          if (uVar7 < uVar12) {
            uVar8 = uVar7;
          }
          plVar4 = *(longlong **)(puVar1[0x1e] + uVar8 * 8);
          lVar5 = *(longlong *)(puVar1[0x21] + uVar12 * 8);
          iVar6 = (int)plVar4[3] / 2;
          FUN_1800010a0(lVar2 + (longlong)(int)uVar11 * 4,uVar3,iVar6);
          FUN_1800010d0();
          local_60 = *(int *)(lVar5 + 8);
          iVar10 = 0;
          local_68 = 0;
          if (0 < local_60) {
            puVar9 = &local_68;
            do {
              iVar10 = iVar10 + 1;
              *puVar9 = *(undefined8 *)((lVar5 - (longlong)&local_68) + (longlong)puVar9);
              puVar9 = puVar9 + 1;
            } while (iVar10 < local_60);
          }
          FUN_180001010(uVar3,local_68,*(undefined8 *)(*plVar4 + 8),*(undefined8 *)plVar4[1]);
          uVar11 = uVar11 + (longlong)iVar6;
          uVar12 = uVar12 + 1;
        } while (uVar11 < *puVar1);
      }
      local_res18 = local_res18 + 1;
      local_res20 = local_res20 + 8;
3));
  }
  return;
}

 (GhidraScript)  

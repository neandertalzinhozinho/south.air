 (GhidraScript)  

void FUN_1808784a0(ulonglong *param_1,int param_2)

{
  int iVar1;
  int iVar2;
  ulonglong *puVar3;
  undefined8 uVar4;
  double dVar5;
  int *piVar6;
  undefined8 uVar7;
  longlong lVar8;
  longlong *plVar9;
  undefined8 *puVar10;
  byte *pbVar11;
  ulonglong uVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  double dVar16;
  int local_res8 [2];
  int local_res10 [2];
  longlong local_res18;
  longlong *local_res20;
  int local_78;
  int local_74;
  longlong *local_70 [6];
  
  *param_1 = (longlong)param_2;
  dVar5 = DAT_18207a250;
  uVar4 = DAT_18207a190;
  iVar14 = 0;
  if (param_2 != 0) {
    local_78 = 0x100;
    local_res8[0] = 0;
    iVar15 = -1;
    iVar13 = 0;
    do {
      local_res10[0] = iVar15;
      piVar6 = local_res10;
      if (iVar15 < 1) {
        piVar6 = local_res8;
      }
      dVar16 = (double)FUN_181c9a5ad(uVar4,(double)*piVar6);
      local_74 = (int)(dVar16 * dVar5);
      piVar6 = &local_78;
      if ((int)(dVar16 * dVar5) < 0x101) {
        piVar6 = &local_74;
      }
      iVar2 = *piVar6;
      iVar1 = (iVar2 * 2) / 2 + 1;
      if (iVar13 < 0x100) {
        uVar7 = FUN_181796cf4(0x20);
        lVar8 = FUN_180619ea0(uVar7);
        if (param_1[0x1f] == param_1[0x20]) {
          local_res18 = lVar8;
          FUN_18088cbd0(param_1 + 0x1e,param_1[0x1f],&local_res18);
        }
        else {
          local_res18 = 0;
          *(longlong *)param_1[0x1f] = lVar8;
          param_1[0x1f] = param_1[0x1f] + 8;
        }
        lVar8 = local_res18;
        if (local_res18 != 0) {
          FUN_180616770(local_res18);
                    /* WARNING: Subroutine does not return */
          thunk_FUN_181798f60(lVar8,0x20);
        }
      }
      plVar9 = (longlong *)FUN_181796cf4(0x18);
      *plVar9 = 0;
      plVar9[1] = 0;
      plVar9[2] = 0;
      if (param_1[0x22] == param_1[0x23]) {
        local_res20 = plVar9;
        puVar10 = (undefined8 *)FUN_18088ce30(param_1 + 0x21,param_1[0x22],&local_res20);
      }
      else {
        local_res20 = (longlong *)0x0;
        *(longlong **)param_1[0x22] = plVar9;
        puVar10 = (undefined8 *)param_1[0x22];
        param_1[0x22] = param_1[0x22] + 8;
      }
      plVar9 = local_res20;
      if (local_res20 != (longlong *)0x0) {
        if (*local_res20 != 0) {
          pbVar11 = (byte *)(*local_res20 + -1);
          (*DAT_181d8d738)((longlong)pbVar11 - (ulonglong)*pbVar11);
        }
        *plVar9 = 0;
                    /* WARNING: Subroutine does not return */
        thunk_FUN_181798f60(plVar9,0x18);
      }
      puVar3 = (ulonglong *)*puVar10;
      if (*puVar3 != 0) {
        pbVar11 = (byte *)(*puVar3 - 1);
        (*DAT_181d8d738)((longlong)pbVar11 - (ulonglong)*pbVar11);
      }
      *puVar3 = 0;
      lVar8 = (longlong)iVar1 * 8;
      if ((lVar8 == 0) ||
         (lVar8 = (*DAT_181d8d730)((lVar8 + 0x3fU & 0xffffffffffffffc0) + 0x40), lVar8 == 0)) {
        uVar12 = 0;
      }
      else {
        uVar12 = lVar8 + 0x40U & 0xffffffffffffffc0;
        *(char *)(uVar12 - 1) = (char)(char *)(uVar12 - 1) - (char)lVar8;
      }
      *puVar3 = uVar12;
      puVar3[1] = 1;
      puVar3[2] = (longlong)iVar1;
      if (iVar2 == 0x100) {
        plVar9 = (longlong *)FUN_181796cf4(0x18);
        *plVar9 = 0;
        plVar9[1] = 0;
        plVar9[2] = 0;
        if (param_1[0x25] == param_1[0x26]) {
          local_70[0] = plVar9;
          puVar10 = (undefined8 *)FUN_18088ce30(param_1 + 0x24,param_1[0x25],local_70);
        }
        else {
          local_70[0] = (longlong *)0x0;
          *(longlong **)param_1[0x25] = plVar9;
          puVar10 = (undefined8 *)param_1[0x25];
          param_1[0x25] = param_1[0x25] + 8;
        }
        plVar9 = local_70[0];
        if (local_70[0] != (longlong *)0x0) {
          if (*local_70[0] != 0) {
            pbVar11 = (byte *)(*local_70[0] + -1);
            (*DAT_181d8d738)((longlong)pbVar11 - (ulonglong)*pbVar11);
          }
          *plVar9 = 0;
                    /* WARNING: Subroutine does not return */
          thunk_FUN_181798f60(plVar9,0x18);
        }
        puVar3 = (ulonglong *)*puVar10;
        if (*puVar3 != 0) {
          pbVar11 = (byte *)(*puVar3 - 1);
          (*DAT_181d8d738)((longlong)pbVar11 - (ulonglong)*pbVar11);
        }
        *puVar3 = 0;
        lVar8 = (*DAT_181d8d730)(0x880);
        if (lVar8 == 0) {
          uVar12 = 0;
        }
        else {
          uVar12 = lVar8 + 0x40U & 0xffffffffffffffc0;
          *(char *)(uVar12 - 1) = (char)(char *)(uVar12 - 1) - (char)lVar8;
        }
        *puVar3 = uVar12;
        puVar3[1] = 1;
        puVar3[2] = 0x101;
      }
      iVar15 = iVar15 + 1;
      iVar14 = iVar14 + iVar2;
      iVar13 = iVar2;
    } while ((ulonglong)(longlong)iVar14 < *param_1);
  }
  FUN_180328990(param_1 + 0x18,*param_1);
  FUN_180328990(param_1 + 0x1b,*param_1);
  param_1[0x29] = *param_1 - 1;
  FUN_1808693d0(param_1);
  return;
}

 (GhidraScript)  

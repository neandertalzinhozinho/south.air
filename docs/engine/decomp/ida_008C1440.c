// IDA 9.3  rva=0x8c1440  start=0x1808c1440  size=7800
void __fastcall sub_1808C1440(__int64 a1, __int64 a2, __int64 *a3)
{
  __int64 v4; // rsi
  unsigned int v5; // r15d
  int v6; // ecx
  int v7; // r8d
  int v8; // edx
  unsigned int v9; // r12d
  int v10; // ecx
  int v11; // edx
  int v12; // ecx
  int v13; // edx
  unsigned int v14; // edi
  int v15; // ecx
  int v16; // edx
  int v17; // ecx
  int v18; // edx
  unsigned int v19; // r13d
  int v20; // ecx
  int v21; // edx
  int v22; // ecx
  int v23; // edx
  unsigned int v24; // r14d
  int v25; // ecx
  __m128i v26; // xmm0
  int v27; // edx
  int v28; // edx
  int v29; // ecx
  __int64 v30; // rbx
  __int64 v31; // rbx
  __int64 v32; // rbx
  __int64 v33; // rbx
  __int64 v34; // rbx
  __int64 v35; // rbx
  unsigned int v36; // edi
  __int64 v37; // rbx
  unsigned int v38; // edi
  __int64 v39; // rbx
  unsigned int v40; // edi
  __int64 v41; // r8
  __int64 v42; // rax
  __int64 v43; // rcx
  int v44; // r9d
  __int64 v45; // r14
  unsigned int **v46; // rax
  __int64 v47; // xmm15_8
  __int64 v48; // xmm13_8
  __m128i v49; // xmm14
  unsigned int *v50; // r13
  __m128i v51; // xmm6
  unsigned int v52; // r8d
  bool v53; // al
  unsigned int v54; // r8d
  __int64 v55; // rbx
  __int64 *v56; // rcx
  int v57; // edx
  __int64 v58; // r8
  int v59; // esi
  _OWORD *v60; // rax
  __int64 v61; // rdx
  __int128 *v62; // rcx
  __int128 v63; // xmm0
  __int128 v64; // xmm1
  __int128 v65; // xmm0
  __int128 v66; // xmm1
  __int128 v67; // xmm0
  __int128 v68; // xmm1
  __int128 v69; // xmm0
  __int128 v70; // xmm1
  __int128 v71; // xmm0
  __int128 *v72; // rcx
  __int64 v73; // rdx
  __int128 *v74; // rax
  __int128 v75; // xmm0
  __int128 v76; // xmm1
  __int128 v77; // xmm0
  __int128 v78; // xmm1
  __int128 v79; // xmm0
  __int128 v80; // xmm1
  __int128 v81; // xmm0
  __int128 v82; // xmm1
  __int64 v83; // rdi
  __int64 i; // rbx
  __int64 j; // rbx
  __int128 *v86; // rax
  __int64 v87; // rdx
  __int128 *v88; // rcx
  __int128 v89; // xmm0
  __int128 v90; // xmm1
  __int128 v91; // xmm0
  __int128 v92; // xmm1
  __int128 v93; // xmm0
  __int128 v94; // xmm1
  __int128 v95; // xmm0
  __int128 v96; // xmm1
  __int64 k; // rbx
  __int64 m; // rbx
  __int64 v99; // rax
  __int64 v100; // rbx
  __int64 v101; // rdi
  __int64 v102; // rbx
  unsigned int *v103; // rdx
  unsigned int v104; // r8d
  bool v105; // al
  bool v106; // cc
  char v107; // al
  __m128i *v108; // rsi
  unsigned int v109; // r8d
  char v110; // al
  __m128i *v111; // r13
  __int64 v112; // rbx
  int v113; // edi
  int v114; // edx
  __int64 *v115; // rcx
  __int64 v116; // r8
  _OWORD *v117; // rax
  __int64 v118; // rdx
  __int128 *v119; // rcx
  __int128 v120; // xmm0
  __int128 v121; // xmm1
  __int128 v122; // xmm0
  __int128 v123; // xmm1
  __int128 v124; // xmm0
  __int128 v125; // xmm1
  __int128 v126; // xmm0
  __int128 v127; // xmm1
  __int128 v128; // xmm0
  __int128 *v129; // rcx
  __int64 v130; // rdx
  __int128 *v131; // rax
  __int128 v132; // xmm0
  __int128 v133; // xmm1
  __int128 v134; // xmm0
  __int128 v135; // xmm1
  __int128 v136; // xmm0
  __int128 v137; // xmm1
  __int128 v138; // xmm0
  __int128 v139; // xmm1
  __m128i v140; // xmm1
  __int64 v141; // xmm0_8
  __int64 v142; // rsi
  unsigned int v143; // r13d
  __int64 n; // rbx
  unsigned int v145; // r13d
  __int64 ii; // rbx
  __int128 *v147; // rax
  __int64 v148; // rdx
  __int128 *v149; // rcx
  __int128 v150; // xmm0
  __int128 v151; // xmm1
  __int128 v152; // xmm0
  __int128 v153; // xmm1
  __int128 v154; // xmm0
  __int128 v155; // xmm1
  __int128 v156; // xmm0
  __int128 v157; // xmm1
  unsigned int v158; // edi
  __int64 jj; // rbx
  unsigned int v160; // edi
  __int64 kk; // rbx
  __int64 v162; // rbx
  __m128i v163; // xmm7
  __int64 v164; // rbx
  __int64 v165; // xmm8_8
  __m128i v166; // xmm9
  __int64 v167; // rbx
  unsigned int v168; // edi
  __int64 v169; // xmm10_8
  __m128i v170; // xmm11
  __int64 v171; // rbx
  unsigned int v172; // edi
  __int64 v173; // xmm12_8
  __int64 v174; // rax
  __int64 v175; // rcx
  __int64 v176; // xmm14_8
  int v177; // ecx
  int v178; // r8d
  __m128i v179; // xmm13
  int v180; // ecx
  __int64 v181; // rbx
  __int64 v182; // rcx
  __int64 v183; // rax
  __int64 v184; // xmm7_8
  int v185; // ecx
  int v186; // r8d
  __m128i v187; // xmm6
  int v188; // ecx
  __int64 v189; // rbx
  __int64 v190; // rcx
  __int64 v191; // rax
  __int64 v192; // xmm9_8
  int v193; // ecx
  int v194; // r8d
  __m128i v195; // xmm8
  int v196; // ecx
  __int64 v197; // rbx
  unsigned int v198; // edi
  __int64 v199; // rcx
  __int64 v200; // rax
  __int64 v201; // xmm11_8
  int v202; // ecx
  int v203; // r8d
  __m128i v204; // xmm10
  int v205; // ecx
  __int64 v206; // rbx
  __int64 v207; // rcx
  __int64 v208; // rax
  unsigned int v209; // r13d
  __int64 v210; // r9
  int v211; // ecx
  int v212; // r8d
  unsigned int v213; // edi
  int v214; // edx
  unsigned __int32 v215; // esi
  __int64 v216; // r12
  int v217; // ecx
  int v218; // edx
  unsigned __int32 v219; // r14d
  int v220; // edx
  int v221; // ecx
  __int64 v222; // r15
  __int64 mm; // rbx
  __int64 v224; // r15
  __int64 nn; // rbx
  __int64 i1; // rbx
  __int64 v227; // rdi
  __int64 i2; // rbx
  char *v229; // rcx
  __int64 v230; // rdx
  int v231; // r9d
  __int64 v232; // rsi
  unsigned int **v233; // rax
  unsigned int *v234; // r13
  unsigned int *v235; // r12
  __int64 v236; // xmm7_8
  __m128i v237; // xmm9
  unsigned int v238; // r8d
  bool v239; // al
  unsigned int v240; // r8d
  __int64 v241; // rbx
  __int64 *v242; // rcx
  int v243; // edx
  __int64 v244; // rax
  __int64 v245; // rdi
  __int128 *v246; // rax
  __int64 v247; // rdx
  __int128 *v248; // rcx
  __int128 v249; // xmm0
  __int128 v250; // xmm1
  __int128 v251; // xmm0
  __int128 v252; // xmm1
  __int128 v253; // xmm0
  __int128 v254; // xmm1
  __int128 v255; // xmm0
  __int128 v256; // xmm1
  unsigned int v257; // r15d
  _QWORD *v258; // rbx
  __int64 v259; // r14
  __int128 *v260; // rax
  __int128 *v261; // rcx
  __int64 v262; // rdx
  __int128 v263; // xmm0
  __int128 v264; // xmm1
  __int128 v265; // xmm0
  __int128 v266; // xmm1
  __int128 v267; // xmm0
  __int128 v268; // xmm1
  __int128 v269; // xmm0
  __int128 v270; // xmm1
  __int64 v271; // rbx
  __int64 v272; // rdi
  unsigned int v273; // edi
  __int64 v274; // rbx
  __int64 v275; // rdx
  unsigned int *v276; // rdx
  unsigned int *v277; // r13
  unsigned int v278; // r8d
  bool v279; // al
  bool v280; // cc
  char v281; // al
  __m128i *v282; // r12
  unsigned int v283; // r8d
  char v284; // al
  __m128i *v285; // r14
  __int64 v286; // rbx
  __int64 *v287; // rcx
  int v288; // edx
  __int64 v289; // rax
  __int64 v290; // rdi
  __int128 *v291; // rax
  __int64 v292; // rdx
  __int128 *v293; // rcx
  __int128 v294; // xmm0
  __int128 v295; // xmm1
  __int128 v296; // xmm0
  __int128 v297; // xmm1
  __int128 v298; // xmm0
  __int128 v299; // xmm1
  __int128 v300; // xmm0
  __int128 v301; // xmm1
  unsigned int v302; // r15d
  _QWORD *v303; // rbx
  __int64 v304; // r14
  __int128 *v305; // rax
  __int64 v306; // rdx
  __int64 v307; // xmm1_8
  __int128 *v308; // rcx
  __int128 v309; // xmm0
  __int128 v310; // xmm1
  __int128 v311; // xmm0
  __int128 v312; // xmm1
  __int128 v313; // xmm0
  __int128 v314; // xmm1
  __int128 v315; // xmm0
  __int128 v316; // xmm1
  __int64 v317; // rbx
  __int64 v318; // rdi
  unsigned int v319; // edi
  __int64 v320; // rbx
  __int64 v321; // rdx
  int v322; // [rsp+24h] [rbp-DCh]
  int v323; // [rsp+24h] [rbp-DCh]
  unsigned int *v324; // [rsp+28h] [rbp-D8h]
  unsigned int *v325; // [rsp+30h] [rbp-D0h]
  unsigned int v326; // [rsp+38h] [rbp-C8h]
  unsigned int v327; // [rsp+3Ch] [rbp-C4h]
  unsigned int v328; // [rsp+40h] [rbp-C0h]
  unsigned int v329; // [rsp+44h] [rbp-BCh]
  unsigned int v330; // [rsp+48h] [rbp-B8h]
  unsigned int *v331; // [rsp+50h] [rbp-B0h]
  __m128i v332; // [rsp+60h] [rbp-A0h]
  __int64 v333; // [rsp+70h] [rbp-90h]
  __int64 v334; // [rsp+80h] [rbp-80h]
  __m128i v335; // [rsp+90h] [rbp-70h]
  __int64 v336; // [rsp+A0h] [rbp-60h]
  __m128i *v337; // [rsp+B0h] [rbp-50h]
  unsigned int *v338; // [rsp+B8h] [rbp-48h]
  __m128i v339; // [rsp+C0h] [rbp-40h] BYREF
  __int64 v340; // [rsp+D0h] [rbp-30h]
  __m128i v341; // [rsp+E0h] [rbp-20h] BYREF
  __int64 v342; // [rsp+F0h] [rbp-10h]
  __m128i v343; // [rsp+100h] [rbp+0h] BYREF
  __int64 v344; // [rsp+110h] [rbp+10h]
  __m128i v345; // [rsp+120h] [rbp+20h] BYREF
  __int64 v346; // [rsp+130h] [rbp+30h]
  __m128i v347; // [rsp+140h] [rbp+40h] BYREF
  __int64 v348; // [rsp+150h] [rbp+50h]
  __m128i v349; // [rsp+160h] [rbp+60h] BYREF
  __int64 v350; // [rsp+170h] [rbp+70h]
  __m128i v351; // [rsp+180h] [rbp+80h] BYREF
  __int64 v352; // [rsp+190h] [rbp+90h]
  __m128i v353; // [rsp+1A0h] [rbp+A0h] BYREF
  __int64 v354; // [rsp+1B0h] [rbp+B0h]
  int v355; // [rsp+1C0h] [rbp+C0h]
  int v356; // [rsp+1C4h] [rbp+C4h]
  int v357; // [rsp+1C8h] [rbp+C8h]
  int v358; // [rsp+1E0h] [rbp+E0h]
  __m128i v359; // [rsp+1F0h] [rbp+F0h]
  __int64 v360; // [rsp+200h] [rbp+100h]
  __m128i v361; // [rsp+220h] [rbp+120h]
  __int64 v362; // [rsp+230h] [rbp+130h]
  __m128i v363; // [rsp+240h] [rbp+140h] BYREF
  __int64 v364; // [rsp+250h] [rbp+150h]
  __m128i v365; // [rsp+260h] [rbp+160h] BYREF
  __int64 v366; // [rsp+270h] [rbp+170h]
  __m128i v367; // [rsp+280h] [rbp+180h] BYREF
  __int64 v368; // [rsp+290h] [rbp+190h]
  __m128i v369; // [rsp+2A0h] [rbp+1A0h]
  __int64 v370; // [rsp+2B0h] [rbp+1B0h]
  __m128i v371; // [rsp+2C0h] [rbp+1C0h] BYREF
  __int64 v372; // [rsp+2D0h] [rbp+1D0h]
  __m128i v373; // [rsp+2E0h] [rbp+1E0h]
  __int64 v374; // [rsp+2F0h] [rbp+1F0h]
  __m128i v375; // [rsp+300h] [rbp+200h]
  __int64 v376; // [rsp+310h] [rbp+210h]
  __m128i v377; // [rsp+320h] [rbp+220h]
  __int64 v378; // [rsp+330h] [rbp+230h]
  __m128i v379; // [rsp+340h] [rbp+240h]
  __int64 v380; // [rsp+350h] [rbp+250h]
  __m128i v381; // [rsp+360h] [rbp+260h]
  __int64 v382; // [rsp+370h] [rbp+270h]
  __m128i v383; // [rsp+380h] [rbp+280h]
  __int64 v384; // [rsp+390h] [rbp+290h]
  __int64 v385; // [rsp+3A0h] [rbp+2A0h] BYREF
  _BYTE v386[1016]; // [rsp+3A8h] [rbp+2A8h] BYREF
  int v387; // [rsp+7A0h] [rbp+6A0h]
  unsigned int v388; // [rsp+7A4h] [rbp+6A4h]
  __int64 v389; // [rsp+7A8h] [rbp+6A8h]
  _QWORD v390[130]; // [rsp+7B0h] [rbp+6B0h] BYREF
  _QWORD v391[130]; // [rsp+BC0h] [rbp+AC0h] BYREF
  _QWORD v392[130]; // [rsp+FD0h] [rbp+ED0h] BYREF
  char v396; // [rsp+14E8h] [rbp+13E8h]

  v4 = a2;
  if ( *(int *)(a2 + 1024) <= 2 )
    return;
  v358 = *((_DWORD *)a3 + 6);
  v5 = *(_DWORD *)(a2 + 1028);
  HIDWORD(v344) = 4 * v5;
  v343.m128i_i64[0] = *a3 + 4LL * v358;
  v6 = v5 + *((_DWORD *)a3 + 6);
  v326 = v5;
  LODWORD(v344) = v5;
  v7 = v6 - (v6 & 0xF) + 16;
  if ( (v6 & 0xF) == 0 )
    v7 = v6;
  *((_DWORD *)a3 + 6) = v7;
  v343.m128i_i64[1] = *a3 + 4LL * v7;
  v8 = v7 + v5 - (((_BYTE)v7 + (_BYTE)v5) & 0xF) + 16;
  if ( (((_BYTE)v7 + (_BYTE)v5) & 0xF) == 0 )
    v8 = v7 + v5;
  *((_DWORD *)a3 + 6) = v8;
  v9 = *(_DWORD *)(v4 + 1028);
  v327 = v9;
  LODWORD(v348) = v9;
  HIDWORD(v348) = 4 * v9;
  v347.m128i_i64[0] = *a3 + 4LL * v8;
  v10 = v8 + v9;
  v11 = v8 + v9 - (((_BYTE)v8 + (_BYTE)v9) & 0xF) + 16;
  if ( (v10 & 0xF) == 0 )
    v11 = v10;
  *((_DWORD *)a3 + 6) = v11;
  v347.m128i_i64[1] = *a3 + 4LL * v11;
  v12 = v11 + v9;
  v13 = v11 + v9 - (((_BYTE)v11 + (_BYTE)v9) & 0xF) + 16;
  if ( (v12 & 0xF) == 0 )
    v13 = v12;
  *((_DWORD *)a3 + 6) = v13;
  v14 = *(_DWORD *)(v4 + 1028);
  v329 = v14;
  LODWORD(v354) = v14;
  HIDWORD(v354) = 4 * v14;
  v353.m128i_i64[0] = *a3 + 4LL * v13;
  v15 = v13 + v14;
  v16 = v13 + v14 - (((_BYTE)v13 + (_BYTE)v14) & 0xF) + 16;
  if ( (v15 & 0xF) == 0 )
    v16 = v15;
  *((_DWORD *)a3 + 6) = v16;
  v353.m128i_i64[1] = *a3 + 4LL * v16;
  v17 = v16 + v14;
  v18 = v16 + v14 - (((_BYTE)v16 + (_BYTE)v14) & 0xF) + 16;
  if ( (v17 & 0xF) == 0 )
    v18 = v17;
  *((_DWORD *)a3 + 6) = v18;
  v19 = *(_DWORD *)(v4 + 1028);
  v328 = v19;
  LODWORD(v350) = v19;
  HIDWORD(v350) = 4 * v19;
  v349.m128i_i64[0] = *a3 + 4LL * v18;
  v20 = v18 + v19;
  v21 = v18 + v19 - (((_BYTE)v18 + (_BYTE)v19) & 0xF) + 16;
  if ( (v20 & 0xF) == 0 )
    v21 = v20;
  *((_DWORD *)a3 + 6) = v21;
  v349.m128i_i64[1] = *a3 + 4LL * v21;
  v22 = v21 + v19;
  v23 = v21 + v19 - (((_BYTE)v21 + (_BYTE)v19) & 0xF) + 16;
  if ( (v22 & 0xF) == 0 )
    v23 = v22;
  *((_DWORD *)a3 + 6) = v23;
  v24 = *(_DWORD *)(v4 + 1028);
  v330 = v24;
  LODWORD(v352) = v24;
  HIDWORD(v352) = 4 * v24;
  v351.m128i_i64[0] = *a3 + 4LL * v23;
  v25 = v23 + v24;
  v26 = 0;
  v27 = v23 + v24 - (((_BYTE)v23 + (_BYTE)v24) & 0xF) + 16;
  v341 = 0;
  if ( (v25 & 0xF) == 0 )
    v27 = v25;
  *((_DWORD *)a3 + 6) = v27;
  v351.m128i_i64[1] = *a3 + 4LL * v27;
  v28 = v27 + v24;
  v29 = v28 - (v28 & 0xF) + 16;
  if ( (v28 & 0xF) == 0 )
    v29 = v28;
  *((_DWORD *)a3 + 6) = v29;
  LODWORD(v342) = *(_DWORD *)(v4 + 1028);
  HIDWORD(v342) = 4 * v342;
  *(double *)v26.m128i_i64 = ((double (__fastcall *)(__int64 *, __m128i *))unk_1808CAFD0)(a3, &v341);
  LODWORD(v346) = *(_DWORD *)(v4 + 1028);
  v345 = v26;
  HIDWORD(v346) = 4 * v346;
  *(double *)v26.m128i_i64 = ((double (__fastcall *)(__int64 *, __m128i *))unk_1808CAFD0)(a3, &v345);
  LODWORD(v340) = *(_DWORD *)(v4 + 1028);
  v339 = v26;
  HIDWORD(v340) = 4 * v340;
  ((void (__fastcall *)(__int64 *, __m128i *))unk_1808CAFD0)(a3, &v339);
  v30 = 0;
  v332 = v343;
  v333 = v344;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v332.m128i_i64[v30++], v5);
  while ( v30 < 2 );
  v31 = 0;
  v335 = v347;
  v336 = v348;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v335.m128i_i64[v31++], v9);
  while ( v31 < 2 );
  v32 = 0;
  v367 = v353;
  v368 = v354;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v367.m128i_i64[v32++], v14);
  while ( v32 < 2 );
  v33 = 0;
  v365 = v349;
  v366 = v350;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v365.m128i_i64[v33++], v19);
  while ( v33 < 2 );
  v34 = 0;
  v363 = v351;
  v364 = v352;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v363.m128i_i64[v34++], v24);
  while ( v34 < 2 );
  v35 = 0;
  v36 = v342;
  v359 = v341;
  v360 = v342;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v359.m128i_i64[v35++], v36);
  while ( v35 < 2 );
  v37 = 0;
  v38 = v346;
  v371 = v345;
  v372 = v346;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v371.m128i_i64[v37++], v38);
  while ( v37 < 2 );
  v39 = 0;
  v40 = v340;
  v369 = v339;
  v370 = v340;
  do
    ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v369.m128i_i64[v39++], v40);
  while ( v39 < 2 );
  v41 = a1;
  v355 = *(_DWORD *)(*(_QWORD *)(a1 + 11320) + 44LL);
  v356 = *(_DWORD *)(*(_QWORD *)(a1 + 11320) + 48LL);
  v357 = *(_DWORD *)(*(_QWORD *)(a1 + 11320) + 52LL);
  v42 = *(_QWORD *)(a1 + 11320);
  if ( *(_BYTE *)(v42 + 447) || (v396 = 1, *(_BYTE *)(v42 + 455)) )
    v396 = 0;
  v43 = 0;
  v322 = 0;
  v334 = 0;
  do
  {
    v44 = dword_182014360[v43];
    v45 = v44;
    v46 = *(unsigned int ***)(v41 + 16);
    v47 = v344;
    v48 = v348;
    v49 = v347;
    v50 = *v46;
    if ( *(_BYTE *)(*(_QWORD *)(v41 + 11320) + 8 * v43 + 447) )
    {
      v338 = v46[1];
      if ( v50 == v338 )
        goto LABEL_166;
      v51 = v343;
      while ( 1 )
      {
        v52 = *v50;
        if ( !v45 )
        {
LABEL_68:
          if ( v50[4] == 2 )
          {
            v55 = *(int *)(v4 + 1028);
            v385 = 0;
            ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v386, 0, 1016);
            v387 = 2;
            v388 = v55;
            v56 = &v385;
            v389 = 4 * v55;
            v57 = 0;
            v58 = 8LL * (int)v50[2] - (_QWORD)&v385 + v4;
            do
            {
              ++v57;
              *v56 = *(__int64 *)((char *)v56 + v58);
              ++v56;
              v59 = v387;
            }
            while ( v57 < v387 );
            v60 = v392;
            v61 = 8;
            v62 = (__int128 *)&v385;
            do
            {
              v60 += 8;
              v63 = *v62;
              v64 = v62[1];
              v62 += 8;
              *(v60 - 8) = v63;
              v65 = *(v62 - 6);
              *(v60 - 7) = v64;
              v66 = *(v62 - 5);
              *(v60 - 6) = v65;
              v67 = *(v62 - 4);
              *(v60 - 5) = v66;
              v68 = *(v62 - 3);
              *(v60 - 4) = v67;
              v69 = *(v62 - 2);
              *(v60 - 3) = v68;
              v70 = *(v62 - 1);
              *(v60 - 2) = v69;
              *(v60 - 1) = v70;
              --v61;
            }
            while ( v61 );
            v71 = *v62;
            v72 = (__int128 *)&v385;
            v73 = 8;
            *v60 = v71;
            v74 = (__int128 *)v390;
            do
            {
              v74 += 8;
              v75 = *v72;
              v76 = v72[1];
              v72 += 8;
              *(v74 - 8) = v75;
              v77 = *(v72 - 6);
              *(v74 - 7) = v76;
              v78 = *(v72 - 5);
              *(v74 - 6) = v77;
              v79 = *(v72 - 4);
              *(v74 - 5) = v78;
              v80 = *(v72 - 3);
              *(v74 - 4) = v79;
              v81 = *(v72 - 2);
              *(v74 - 3) = v80;
              v82 = *(v72 - 1);
              *(v74 - 2) = v81;
              *(v74 - 1) = v82;
              --v73;
            }
            while ( v73 );
            v83 = v385;
            v332 = v51;
            v333 = v47;
            *v74 = *v72;
            if ( v59 == 2 )
            {
              for ( i = 0; i < 2; ++i )
                ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001580)(
                  v390[i],
                  v392[i],
                  v332.m128i_i64[i],
                  v5);
            }
            else if ( v59 == 1 )
            {
              for ( j = 0; j < 2; ++j )
                ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001580)(v83, v83, v332.m128i_i64[j], v5);
            }
            v86 = (__int128 *)v391;
            v87 = 8;
            v88 = (__int128 *)&v385;
            do
            {
              v86 += 8;
              v89 = *v88;
              v90 = v88[1];
              v88 += 8;
              *(v86 - 8) = v89;
              v91 = *(v88 - 6);
              *(v86 - 7) = v90;
              v92 = *(v88 - 5);
              *(v86 - 6) = v91;
              v93 = *(v88 - 4);
              *(v86 - 5) = v92;
              v94 = *(v88 - 3);
              *(v86 - 4) = v93;
              v95 = *(v88 - 2);
              *(v86 - 3) = v94;
              v96 = *(v88 - 1);
              *(v86 - 2) = v95;
              *(v86 - 1) = v96;
              --v87;
            }
            while ( v87 );
            v335 = v49;
            v336 = v48;
            *v86 = *v88;
            if ( v59 == 2 )
            {
              for ( k = 0; k < 2; ++k )
                ((void (__fastcall *)(_QWORD, __int64, _QWORD))unk_180001370)(v391[k], v335.m128i_i64[k], v9);
            }
            else if ( v59 == 1 )
            {
              for ( m = 0; m < 2; ++m )
                ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v83, v335.m128i_i64[m], v9);
            }
            v4 = a2;
          }
          else
          {
            v99 = *((_QWORD *)v50 + 1);
            v100 = 0;
            v369 = v51;
            v370 = v47;
            v101 = *(_QWORD *)(v4 + 8 * v99);
            do
              ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001580)(
                v101,
                v101,
                v369.m128i_i64[v100++],
                v5);
            while ( v100 < 2 );
            v332 = v49;
            v102 = 0;
            v333 = v48;
            do
              ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v101, v332.m128i_i64[v102++], v9);
            while ( v102 < 2 );
          }
          v44 = v45;
          goto LABEL_89;
        }
        if ( v45 == 1 )
          break;
        switch ( v45 )
        {
          case 2LL:
            v53 = v52 != 9;
LABEL_67:
            if ( v53 )
              goto LABEL_68;
            goto LABEL_89;
          case 3LL:
            if ( v52 - 9 > 1 )
              goto LABEL_68;
            goto LABEL_89;
          case 5LL:
            if ( v52 - 16 <= 2 )
              goto LABEL_68;
            goto LABEL_89;
          case 4LL:
            if ( v52 - 8 > 2 )
              goto LABEL_68;
            goto LABEL_89;
        }
        if ( v45 != 6 )
        {
          if ( v45 == 7 )
          {
            if ( v52 - 8 <= 1 )
              goto LABEL_68;
            goto LABEL_89;
          }
          v53 = v44 == v52;
          goto LABEL_67;
        }
        if ( (unsigned __int8)sub_18061B790(4, v52) && !(unsigned __int8)sub_18061B790(5, v54) )
          goto LABEL_68;
LABEL_89:
        v50 += 6;
        if ( v50 == v338 )
          goto LABEL_166;
      }
      v53 = v52 != 10;
      goto LABEL_67;
    }
    v103 = v46[1];
    v325 = v103;
    v331 = *v46;
    if ( v50 == v103 )
      goto LABEL_167;
    do
    {
      v104 = *v50;
      switch ( v45 )
      {
        case 0LL:
          goto LABEL_112;
        case 1LL:
          v105 = v104 != 10;
          goto LABEL_130;
        case 2LL:
          v105 = v104 != 9;
          goto LABEL_130;
        case 3LL:
          if ( v104 - 9 <= 1 )
            goto LABEL_164;
          goto LABEL_112;
        case 5LL:
          v106 = v104 - 16 <= 2;
LABEL_111:
          if ( !v106 )
            goto LABEL_164;
LABEL_112:
          v107 = 0;
          goto LABEL_113;
        case 4LL:
          if ( v104 - 8 <= 2 )
            goto LABEL_164;
          goto LABEL_112;
        case 6LL:
          if ( !(unsigned __int8)sub_18061B790(4, v104) )
            goto LABEL_163;
          v110 = sub_18061B790(5, v109);
          v103 = v325;
          if ( v110 )
            goto LABEL_164;
          goto LABEL_112;
        case 7LL:
          v106 = v104 - 8 <= 1;
          goto LABEL_111;
      }
      v105 = v44 == v104;
LABEL_130:
      if ( !v105 )
        goto LABEL_164;
      if ( (unsigned __int64)(v45 - 8) > 1 )
        goto LABEL_112;
      v107 = 1;
LABEL_113:
      if ( v107 )
      {
        if ( !v396 )
          goto LABEL_164;
        v108 = &v353;
LABEL_118:
        if ( v107 )
        {
          v337 = &v349;
        }
        else
        {
          v111 = &v341;
          if ( v44 != 6 )
            v111 = &v339;
          v337 = v111;
          v50 = v331;
        }
        v112 = *(int *)(a2 + 1028);
        v385 = 0;
        ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v386, 0, 1016);
        v113 = v50[4];
        v114 = 0;
        v387 = v113;
        v388 = v112;
        v389 = 4 * v112;
        if ( v113 > 0 )
        {
          v115 = &v385;
          v116 = 8LL * (int)v50[2] - (_QWORD)&v385 + a2;
          do
          {
            ++v114;
            *v115 = *(__int64 *)((char *)v115 + v116);
            ++v115;
            v113 = v387;
          }
          while ( v114 < v387 );
        }
        v117 = v391;
        v118 = 8;
        v119 = (__int128 *)&v385;
        do
        {
          v117 += 8;
          v120 = *v119;
          v121 = v119[1];
          v119 += 8;
          *(v117 - 8) = v120;
          v122 = *(v119 - 6);
          *(v117 - 7) = v121;
          v123 = *(v119 - 5);
          *(v117 - 6) = v122;
          v124 = *(v119 - 4);
          *(v117 - 5) = v123;
          v125 = *(v119 - 3);
          *(v117 - 4) = v124;
          v126 = *(v119 - 2);
          *(v117 - 3) = v125;
          v127 = *(v119 - 1);
          *(v117 - 2) = v126;
          *(v117 - 1) = v127;
          --v118;
        }
        while ( v118 );
        v128 = *v119;
        v129 = (__int128 *)&v385;
        v130 = 8;
        *v117 = v128;
        v131 = (__int128 *)v390;
        do
        {
          v131 += 8;
          v132 = *v129;
          v133 = v129[1];
          v129 += 8;
          *(v131 - 8) = v132;
          v134 = *(v129 - 6);
          *(v131 - 7) = v133;
          v135 = *(v129 - 5);
          *(v131 - 6) = v134;
          v136 = *(v129 - 4);
          *(v131 - 5) = v135;
          v137 = *(v129 - 3);
          *(v131 - 4) = v136;
          v138 = *(v129 - 2);
          *(v131 - 3) = v137;
          v139 = *(v129 - 1);
          *(v131 - 2) = v138;
          *(v131 - 1) = v139;
          --v130;
        }
        while ( v130 );
        v140 = *v108;
        *v131 = *v129;
        v141 = v108[1].m128i_i64[0];
        v142 = v385;
        v336 = v141;
        v335 = v140;
        if ( v113 == 2 )
        {
          v143 = v336;
          for ( n = 0; n < 2; ++n )
            ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001580)(
              v390[n],
              v391[n],
              v335.m128i_i64[n],
              v143);
        }
        else
        {
          if ( v113 != 1 )
            goto LABEL_153;
          v145 = v336;
          for ( ii = 0; ii < 2; ++ii )
            ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001580)(
              v142,
              v142,
              v335.m128i_i64[ii],
              v145);
        }
        v50 = v331;
LABEL_153:
        v147 = (__int128 *)v392;
        v148 = 8;
        v149 = (__int128 *)&v385;
        do
        {
          v147 += 8;
          v150 = *v149;
          v151 = v149[1];
          v149 += 8;
          *(v147 - 8) = v150;
          v152 = *(v149 - 6);
          *(v147 - 7) = v151;
          v153 = *(v149 - 5);
          *(v147 - 6) = v152;
          v154 = *(v149 - 4);
          *(v147 - 5) = v153;
          v155 = *(v149 - 3);
          *(v147 - 4) = v154;
          v156 = *(v149 - 2);
          *(v147 - 3) = v155;
          v157 = *(v149 - 1);
          *(v147 - 2) = v156;
          *(v147 - 1) = v157;
          --v148;
        }
        while ( v148 );
        *v147 = *v149;
        v333 = v337[1].m128i_i64[0];
        v332 = *v337;
        if ( v113 == 2 )
        {
          v158 = v333;
          for ( jj = 0; jj < 2; ++jj )
            ((void (__fastcall *)(_QWORD, __int64, _QWORD))unk_180001370)(v392[jj], v332.m128i_i64[jj], v158);
        }
        else if ( v113 == 1 )
        {
          v160 = v333;
          for ( kk = 0; kk < 2; ++kk )
            ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v142, v332.m128i_i64[kk], v160);
        }
        v44 = v45;
LABEL_163:
        v103 = v325;
        goto LABEL_164;
      }
      if ( v44 == 6 || v45 == 5 )
      {
        v108 = &v351;
        if ( v44 != 6 )
          v108 = &v345;
        goto LABEL_118;
      }
LABEL_164:
      v50 += 6;
      v331 = v50;
    }
    while ( v50 != v103 );
    v5 = v326;
    v9 = v327;
    v4 = a2;
LABEL_166:
    v41 = a1;
LABEL_167:
    v43 = v334 + 1;
    ++v322;
    ++v334;
  }
  while ( (unsigned __int64)v322 < 5 );
  v162 = 0;
  v369 = v49;
  v370 = v48;
  do
    ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001100)(v369.m128i_i64[v162++], v9, v41, 0);
  while ( v162 < 2 );
  v163 = v349;
  v164 = 0;
  v165 = v350;
  v332 = v349;
  v333 = v350;
  do
    ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001100)(v332.m128i_i64[v164++], v328, v41, 0);
  while ( v164 < 2 );
  v166 = _mm_loadu_si128(&v341);
  v167 = 0;
  v168 = v342;
  v169 = v342;
  v335 = v166;
  v336 = v342;
  do
    ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001100)(v335.m128i_i64[v167++], v168, v41, 0);
  while ( v167 < 2 );
  v170 = _mm_loadu_si128(&v339);
  v171 = 0;
  v172 = v340;
  v173 = v340;
  v349 = v170;
  v350 = v340;
  do
    ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001100)(v349.m128i_i64[v171++], v172, v41, 0);
  while ( v171 < 2 );
  HIDWORD(v360) = 4 * v5;
  v380 = v48;
  v174 = *a3;
  v175 = *((int *)a3 + 6);
  LODWORD(v360) = v5;
  v379 = v49;
  v176 = v360;
  v342 = v47;
  v359.m128i_i64[0] = v174 + 4 * v175;
  v177 = v5 + *((_DWORD *)a3 + 6);
  v341 = v343;
  v340 = v360;
  v178 = v177 - (v177 & 0xF) + 16;
  if ( (v177 & 0xF) == 0 )
    v178 = v177;
  *((_DWORD *)a3 + 6) = v178;
  v359.m128i_i64[1] = *a3 + 4LL * v178;
  v179 = v359;
  v339 = v359;
  v180 = v178 + v5 - (((_BYTE)v178 + (_BYTE)v5) & 0xF) + 16;
  if ( (((_BYTE)v178 + (_BYTE)v5) & 0xF) == 0 )
    v180 = v178 + v5;
  v181 = 0;
  *((_DWORD *)a3 + 6) = v180;
  do
  {
    ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001550)(
      v379.m128i_i64[v181],
      v341.m128i_i64[v181],
      v339.m128i_i64[v181],
      v5);
    ++v181;
  }
  while ( v181 < 2 );
  v182 = *((int *)a3 + 6);
  LODWORD(v364) = v329;
  HIDWORD(v364) = 4 * v329;
  v183 = *a3;
  v383 = v163;
  v184 = v364;
  v384 = v165;
  v381 = v353;
  v363.m128i_i64[0] = v183 + 4 * v182;
  v185 = v329 + *((_DWORD *)a3 + 6);
  v382 = v354;
  v354 = v364;
  v186 = v185 - (v185 & 0xF) + 16;
  if ( (v185 & 0xF) == 0 )
    v186 = v185;
  *((_DWORD *)a3 + 6) = v186;
  v363.m128i_i64[1] = *a3 + 4LL * v186;
  v187 = v363;
  v353 = v363;
  v188 = v186 + v329 - (((_BYTE)v186 + (_BYTE)v329) & 0xF) + 16;
  if ( (((_BYTE)v186 + (_BYTE)v329) & 0xF) == 0 )
    v188 = v186 + v329;
  v189 = 0;
  *((_DWORD *)a3 + 6) = v188;
  do
  {
    ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001550)(
      v383.m128i_i64[v189],
      v381.m128i_i64[v189],
      v353.m128i_i64[v189],
      v329);
    ++v189;
  }
  while ( v189 < 2 );
  v190 = *((int *)a3 + 6);
  LODWORD(v366) = v330;
  HIDWORD(v366) = 4 * v330;
  v191 = *a3;
  v375 = v166;
  v192 = v366;
  v376 = v169;
  v373 = v351;
  v365.m128i_i64[0] = v191 + 4 * v190;
  v193 = v330 + *((_DWORD *)a3 + 6);
  v374 = v352;
  v352 = v366;
  v194 = v193 - (v193 & 0xF) + 16;
  if ( (v193 & 0xF) == 0 )
    v194 = v193;
  *((_DWORD *)a3 + 6) = v194;
  v365.m128i_i64[1] = *a3 + 4LL * v194;
  v195 = v365;
  v351 = v365;
  v196 = v194 + v330 - (((_BYTE)v194 + (_BYTE)v330) & 0xF) + 16;
  if ( (((_BYTE)v194 + (_BYTE)v330) & 0xF) == 0 )
    v196 = v194 + v330;
  v197 = 0;
  *((_DWORD *)a3 + 6) = v196;
  do
  {
    ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001550)(
      v375.m128i_i64[v197],
      v373.m128i_i64[v197],
      v351.m128i_i64[v197],
      v330);
    ++v197;
  }
  while ( v197 < 2 );
  v198 = v346;
  v199 = *((int *)a3 + 6);
  LODWORD(v368) = v346;
  HIDWORD(v368) = 4 * v346;
  v200 = *a3;
  v361 = v170;
  v201 = v368;
  v362 = v173;
  v377 = v345;
  v367.m128i_i64[0] = v200 + 4 * v199;
  v202 = v346 + *((_DWORD *)a3 + 6);
  v378 = v346;
  v346 = v368;
  v203 = v202 - (v202 & 0xF) + 16;
  if ( (v202 & 0xF) == 0 )
    v203 = v202;
  *((_DWORD *)a3 + 6) = v203;
  v367.m128i_i64[1] = *a3 + 4LL * v203;
  v204 = v367;
  v345 = v367;
  v205 = v198 + v203 - (((_BYTE)v198 + (_BYTE)v203) & 0xF) + 16;
  if ( (((_BYTE)v198 + (_BYTE)v203) & 0xF) == 0 )
    v205 = v198 + v203;
  v206 = 0;
  *((_DWORD *)a3 + 6) = v205;
  do
  {
    ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_180001550)(
      v361.m128i_i64[v206],
      v377.m128i_i64[v206],
      v345.m128i_i64[v206],
      v198);
    ++v206;
  }
  while ( v206 < 2 );
  v207 = *((int *)a3 + 6);
  v208 = *a3;
  v209 = *(_DWORD *)(v4 + 1028);
  v361 = v179;
  v210 = v208 + 4 * v207;
  v362 = v176;
  v211 = v209 + *((_DWORD *)a3 + 6);
  v334 = v210;
  v212 = v211 - (v211 & 0xF) + 16;
  if ( (v211 & 0xF) == 0 )
    v212 = v211;
  *((_DWORD *)a3 + 6) = v212;
  v213 = *(_DWORD *)(v4 + 1028);
  v371.m128i_i32[2] = v213;
  v371.m128i_i32[3] = 4 * v213;
  v371.m128i_i64[0] = *a3 + 4LL * v212;
  v214 = v213 + v212 - (((_BYTE)v213 + (_BYTE)v212) & 0xF) + 16;
  if ( (((_BYTE)v213 + (_BYTE)v212) & 0xF) == 0 )
    v214 = v213 + v212;
  *((_DWORD *)a3 + 6) = v214;
  v215 = *(_DWORD *)(v4 + 1028);
  v343.m128i_i32[2] = v215;
  v343.m128i_i32[3] = 4 * v215;
  v216 = *a3 + 4LL * v214;
  v343.m128i_i64[0] = v216;
  v217 = v215 + v214;
  v218 = v215 + v214 - (((_BYTE)v215 + (_BYTE)v214) & 0xF) + 16;
  if ( (v217 & 0xF) == 0 )
    v218 = v217;
  *((_DWORD *)a3 + 6) = v218;
  v219 = *(_DWORD *)(a2 + 1028);
  v347.m128i_i32[2] = v219;
  v347.m128i_i32[3] = 4 * v219;
  v347.m128i_i64[0] = *a3 + 4LL * v218;
  v220 = v219 + v218;
  v221 = v220 - (v220 & 0xF) + 16;
  if ( (v220 & 0xF) == 0 )
    v221 = v220;
  *((_DWORD *)a3 + 6) = v221;
  ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v210, v209);
  v222 = v334;
  for ( mm = 0; mm < 2; ++mm )
    ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v361.m128i_i64[mm], v222, v209);
  v224 = v371.m128i_i64[0];
  v377 = v187;
  v378 = v184;
  ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v371.m128i_i64[0], v213);
  for ( nn = 0; nn < 2; ++nn )
    ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v377.m128i_i64[nn], v224, v213);
  v375 = v195;
  v376 = v192;
  ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v216, v215);
  for ( i1 = 0; i1 < 2; ++i1 )
    ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v375.m128i_i64[i1], v216, v215);
  v227 = v347.m128i_i64[0];
  v373 = v204;
  v374 = v201;
  ((void (__fastcall *)(__int64, _QWORD))unk_1800010D0)(v347.m128i_i64[0], v219);
  for ( i2 = 0; i2 < 2; ++i2 )
    ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001370)(v373.m128i_i64[i2], v227, v219);
  v229 = nullptr;
  v230 = a1;
  v338 = nullptr;
  v323 = 0;
  while ( 2 )
  {
    v231 = dword_182014360[(_QWORD)v229];
    v232 = v231;
    v233 = *(unsigned int ***)(v230 + 16);
    if ( !*(_BYTE *)(*(_QWORD *)(v230 + 11320) + 8LL * (_QWORD)v229 + 447) )
    {
      v276 = v233[1];
      v277 = *v233;
      v324 = v276;
      if ( *v233 == v276 )
      {
LABEL_319:
        v230 = a1;
        goto LABEL_320;
      }
      while ( 1 )
      {
        v278 = *v277;
        if ( v232 )
        {
          switch ( v232 )
          {
            case 1LL:
              v279 = v278 != 10;
              break;
            case 2LL:
              v279 = v278 != 9;
              break;
            case 3LL:
              if ( v278 - 9 <= 1 )
                goto LABEL_318;
              goto LABEL_273;
            case 5LL:
              v280 = v278 - 16 <= 2;
              goto LABEL_272;
            case 4LL:
              if ( v278 - 8 <= 2 )
                goto LABEL_318;
              goto LABEL_273;
            case 6LL:
              if ( !(unsigned __int8)sub_18061B790(4, v278) )
                goto LABEL_317;
              v284 = sub_18061B790(5, v283);
              v276 = v324;
              if ( v284 )
                goto LABEL_318;
              goto LABEL_273;
            case 7LL:
              v280 = v278 - 8 <= 1;
LABEL_272:
              if ( !v280 )
                goto LABEL_318;
              goto LABEL_273;
            default:
              v279 = v231 == v278;
              break;
          }
          if ( !v279 )
            goto LABEL_318;
          if ( (unsigned __int64)(v232 - 8) <= 1 )
          {
            v281 = 1;
            goto LABEL_274;
          }
        }
LABEL_273:
        v281 = 0;
LABEL_274:
        if ( !v281 )
        {
          if ( v231 != 6 && v232 != 5 )
            goto LABEL_318;
LABEL_277:
          if ( v281 )
          {
            v282 = &v363;
          }
          else
          {
            v282 = &v365;
            if ( v231 != 6 )
              v282 = &v367;
          }
          if ( v281 )
          {
            v285 = &v371;
          }
          else
          {
            v285 = &v343;
            if ( v231 != 6 )
              v285 = &v347;
          }
          if ( v277[4] == 2 )
          {
            v385 = 0;
            v286 = *(int *)(a2 + 1028);
            ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v386, 0, 1016);
            v388 = v286;
            v287 = &v385;
            v288 = 0;
            v389 = 4 * v286;
            v289 = (int)v277[2];
            v387 = 2;
            do
            {
              ++v288;
              *v287 = *(__int64 *)((char *)v287 + 8 * v289 - (_QWORD)&v385 + a2);
              ++v287;
              v290 = (unsigned int)v387;
            }
            while ( v288 < v387 );
            v291 = (__int128 *)v391;
            v292 = 8;
            v293 = (__int128 *)&v385;
            do
            {
              v291 += 8;
              v294 = *v293;
              v295 = v293[1];
              v293 += 8;
              *(v291 - 8) = v294;
              v296 = *(v293 - 6);
              *(v291 - 7) = v295;
              v297 = *(v293 - 5);
              *(v291 - 6) = v296;
              v298 = *(v293 - 4);
              *(v291 - 5) = v297;
              v299 = *(v293 - 3);
              *(v291 - 4) = v298;
              v300 = *(v293 - 2);
              *(v291 - 3) = v299;
              v301 = *(v293 - 1);
              *(v291 - 2) = v300;
              *(v291 - 1) = v301;
              --v292;
            }
            while ( v292 );
            v302 = v388;
            *v291 = *v293;
            if ( (int)v290 > 0 )
            {
              v303 = v391;
              v304 = v290;
              do
              {
                ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v293, *v303++, v302);
                --v304;
              }
              while ( v304 );
            }
            v305 = (__int128 *)v390;
            v306 = 8;
            v307 = v282[1].m128i_i64[0];
            v308 = (__int128 *)&v385;
            v361 = *v282;
            v362 = v307;
            do
            {
              v305 += 8;
              v309 = *v308;
              v310 = v308[1];
              v308 += 8;
              *(v305 - 8) = v309;
              v311 = *(v308 - 6);
              *(v305 - 7) = v310;
              v312 = *(v308 - 5);
              *(v305 - 6) = v311;
              v313 = *(v308 - 4);
              *(v305 - 5) = v312;
              v314 = *(v308 - 3);
              *(v305 - 4) = v313;
              v315 = *(v308 - 2);
              *(v305 - 3) = v314;
              v316 = *(v308 - 1);
              *(v305 - 2) = v315;
              *(v305 - 1) = v316;
              --v306;
            }
            while ( v306 );
            *v305 = *v308;
            if ( (_DWORD)v290 == 2 )
            {
              v317 = 0;
              v318 = 2;
              do
              {
                ((void (__fastcall *)(__int64, __int64, _QWORD, _QWORD))unk_1800011F0)(
                  v361.m128i_i64[v317],
                  v306,
                  v390[v317],
                  v302);
                ++v317;
                --v318;
              }
              while ( v318 );
            }
          }
          else
          {
            v319 = *(_DWORD *)(a2 + 1028);
            v320 = *(_QWORD *)(a2 + 8LL * *((_QWORD *)v277 + 1));
            ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001220)(a2, v320, v319);
            ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_1800011F0)(
              v285->m128i_i64[0],
              v321,
              v320,
              v319);
          }
          v231 = v232;
LABEL_317:
          v276 = v324;
          goto LABEL_318;
        }
        if ( v396 )
          goto LABEL_277;
LABEL_318:
        v277 += 6;
        if ( v277 == v276 )
          goto LABEL_319;
      }
    }
    v234 = v233[1];
    v235 = *v233;
    if ( *v233 != v234 )
    {
      v236 = v360;
      v237 = v359;
      while ( 1 )
      {
        v238 = *v235;
        if ( !v232 )
        {
LABEL_243:
          if ( v235[4] == 2 )
          {
            v385 = 0;
            v241 = *(int *)(a2 + 1028);
            ((void (__fastcall *)(_BYTE *, _QWORD, __int64))unk_181798F42)(v386, 0, 1016);
            v388 = v241;
            v242 = &v385;
            v243 = 0;
            v389 = 4 * v241;
            v244 = (int)v235[2];
            v387 = 2;
            do
            {
              ++v243;
              *v242 = *(__int64 *)((char *)v242 + 8 * v244 - (_QWORD)&v385 + a2);
              ++v242;
              v245 = (unsigned int)v387;
            }
            while ( v243 < v387 );
            v246 = (__int128 *)v391;
            v247 = 8;
            v248 = (__int128 *)&v385;
            do
            {
              v246 += 8;
              v249 = *v248;
              v250 = v248[1];
              v248 += 8;
              *(v246 - 8) = v249;
              v251 = *(v248 - 6);
              *(v246 - 7) = v250;
              v252 = *(v248 - 5);
              *(v246 - 6) = v251;
              v253 = *(v248 - 4);
              *(v246 - 5) = v252;
              v254 = *(v248 - 3);
              *(v246 - 4) = v253;
              v255 = *(v248 - 2);
              *(v246 - 3) = v254;
              v256 = *(v248 - 1);
              *(v246 - 2) = v255;
              *(v246 - 1) = v256;
              --v247;
            }
            while ( v247 );
            v257 = v388;
            *v246 = *v248;
            if ( (int)v245 > 0 )
            {
              v258 = v391;
              v259 = v245;
              do
              {
                ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v248, *v258++, v257);
                --v259;
              }
              while ( v259 );
            }
            v361 = v237;
            v260 = (__int128 *)v390;
            v362 = v236;
            v261 = (__int128 *)&v385;
            v262 = 8;
            do
            {
              v260 += 8;
              v263 = *v261;
              v264 = v261[1];
              v261 += 8;
              *(v260 - 8) = v263;
              v265 = *(v261 - 6);
              *(v260 - 7) = v264;
              v266 = *(v261 - 5);
              *(v260 - 6) = v265;
              v267 = *(v261 - 4);
              *(v260 - 5) = v266;
              v268 = *(v261 - 3);
              *(v260 - 4) = v267;
              v269 = *(v261 - 2);
              *(v260 - 3) = v268;
              v270 = *(v261 - 1);
              *(v260 - 2) = v269;
              *(v260 - 1) = v270;
              --v262;
            }
            while ( v262 );
            *v260 = *v261;
            if ( (_DWORD)v245 == 2 )
            {
              v271 = 0;
              v272 = 2;
              do
              {
                ((void (__fastcall *)(__int64, __int64, _QWORD, _QWORD))unk_1800011F0)(
                  v361.m128i_i64[v271],
                  v262,
                  v390[v271],
                  v257);
                ++v271;
                --v272;
              }
              while ( v272 );
            }
          }
          else
          {
            v273 = *(_DWORD *)(a2 + 1028);
            v274 = *(_QWORD *)(a2 + 8LL * *((_QWORD *)v235 + 1));
            ((void (__fastcall *)(__int64, __int64, _QWORD))unk_180001220)(a2, v274, v273);
            ((void (__fastcall *)(__int64, __int64, __int64, _QWORD))unk_1800011F0)(v334, v275, v274, v273);
          }
          v231 = v232;
          goto LABEL_259;
        }
        if ( v232 == 1 )
          break;
        switch ( v232 )
        {
          case 2LL:
            v239 = v238 != 9;
LABEL_242:
            if ( v239 )
              goto LABEL_243;
            goto LABEL_259;
          case 3LL:
            if ( v238 - 9 > 1 )
              goto LABEL_243;
            goto LABEL_259;
          case 5LL:
            if ( v238 - 16 <= 2 )
              goto LABEL_243;
            goto LABEL_259;
          case 4LL:
            if ( v238 - 8 > 2 )
              goto LABEL_243;
            goto LABEL_259;
        }
        if ( v232 != 6 )
        {
          if ( v232 == 7 )
          {
            if ( v238 - 8 <= 1 )
              goto LABEL_243;
            goto LABEL_259;
          }
          v239 = v231 == v238;
          goto LABEL_242;
        }
        if ( (unsigned __int8)sub_18061B790(4, v238) && !(unsigned __int8)sub_18061B790(5, v240) )
          goto LABEL_243;
LABEL_259:
        v235 += 6;
        if ( v235 == v234 )
          goto LABEL_319;
      }
      v239 = v238 != 10;
      goto LABEL_242;
    }
LABEL_320:
    v229 = (char *)v338 + 1;
    ++v323;
    v338 = (unsigned int *)((char *)v338 + 1);
    if ( (unsigned __int64)v323 < 5 )
      continue;
    break;
  }
  *((_DWORD *)a3 + 6) = v358;
}

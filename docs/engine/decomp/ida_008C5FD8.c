// IDA 9.3  rva=0x8c5fd8  start=0x1808c5c40  size=20209
__int64 sub_1808C5C40(__int64 a1, __int64 a2, __int128 *a3, ...)
{
  __int64 *v6; // rcx
  __int64 v7; // rdx
  __int128 *v8; // rax
  bool v9; // r12
  __int128 v10; // xmm0
  __int128 v11; // xmm1
  __int128 v12; // xmm0
  __int128 v13; // xmm1
  __int128 v14; // xmm0
  __int128 v15; // xmm1
  __int128 v16; // xmm0
  __int128 v17; // xmm1
  unsigned int v18; // r14d
  __int64 *v19; // rdi
  __int64 v20; // rsi
  __int128 *v21; // rax
  __int64 *v22; // rcx
  __int64 v23; // rdx
  __int128 v24; // xmm0
  __int128 v25; // xmm1
  __int128 v26; // xmm0
  __int128 v27; // xmm1
  __int128 v28; // xmm0
  __int128 v29; // xmm1
  __int128 v30; // xmm0
  __int128 v31; // xmm1
  unsigned int v32; // r14d
  __int64 *v33; // rdi
  __int64 v34; // rsi
  __int64 v35; // r15
  int v36; // edx
  int v37; // ecx
  _QWORD *v38; // rcx
  __m128i *v39; // rax
  int v40; // ecx
  _QWORD *v41; // rcx
  __m128i v42; // xmm1
  __m128i v43; // xmm6
  __m128i v44; // xmm0
  __m128i v45; // xmm1
  __m128i v46; // xmm0
  __m128i v47; // xmm1
  __m128i v48; // xmm0
  __m128i v49; // xmm1
  unsigned __int32 v50; // edi
  int v51; // edx
  __int64 v52; // rcx
  __int64 v53; // rax
  __m128i v54; // xmm7
  __int128 v55; // xmm8
  __int128 v56; // xmm9
  __int128 v57; // xmm10
  __int128 v58; // xmm11
  __int128 v59; // xmm12
  __int128 v60; // xmm13
  __int128 v61; // xmm14
  __m128i v62; // xmm15
  __int64 v63; // xmm6_8
  __int128 *v64; // rax
  __int128 *v65; // rcx
  __int64 v66; // rdx
  __int128 v67; // xmm0
  __int128 v68; // xmm1
  __int128 v69; // xmm0
  __int128 v70; // xmm1
  __int128 v71; // xmm0
  __int128 v72; // xmm1
  __int128 v73; // xmm0
  __int128 v74; // xmm1
  __int64 v75; // r12
  int v76; // esi
  __int64 v77; // rax
  __int64 v78; // rax
  __int128 *v79; // rcx
  __int64 v80; // rdx
  __int128 v81; // xmm0
  __int128 v82; // xmm1
  __int128 v83; // xmm0
  __int128 v84; // xmm1
  __int128 v85; // xmm0
  __int128 v86; // xmm1
  __int128 v87; // xmm0
  __m128i v88; // xmm1
  __int128 *v89; // rax
  __int128 v90; // xmm0
  __int128 v91; // xmm1
  __int128 v92; // xmm0
  __int128 v93; // xmm1
  __int128 v94; // xmm0
  __int128 v95; // xmm1
  __int128 v96; // xmm0
  __int128 v97; // xmm1
  __int64 *v98; // r8
  int v99; // edx
  __int64 v100; // rcx
  __int128 *v101; // rcx
  __int128 *v102; // rax
  __int128 *v103; // rdx
  __int64 v104; // r8
  __int128 v105; // xmm0
  __int128 v106; // xmm1
  __int128 v107; // xmm0
  __int128 v108; // xmm1
  __int128 v109; // xmm0
  __int128 v110; // xmm1
  __int128 v111; // xmm0
  __int128 v112; // xmm1
  __int128 v113; // xmm0
  __int64 v114; // rdx
  __int128 *v115; // rax
  __int128 v116; // xmm0
  __int128 v117; // xmm1
  __int128 v118; // xmm0
  __int128 v119; // xmm1
  __int128 v120; // xmm0
  __int128 v121; // xmm1
  __int128 v122; // xmm0
  __int128 v123; // xmm1
  int v124; // edx
  __int64 v125; // rcx
  int v126; // edx
  __m128i v127; // xmm6
  __int128 v128; // xmm7
  __int128 v129; // xmm8
  __int128 v130; // xmm9
  __int128 v131; // xmm10
  __int128 v132; // xmm11
  __int128 v133; // xmm12
  __int128 v134; // xmm13
  __m128i v135; // xmm14
  __int64 v136; // rax
  __int64 v137; // rdx
  __int128 v138; // xmm0
  __int128 v139; // xmm1
  __int128 v140; // xmm0
  __int128 v141; // xmm1
  __int128 v142; // xmm0
  __int128 v143; // xmm1
  __int128 v144; // xmm0
  __int128 v145; // xmm1
  __int128 *v146; // rax
  __int128 *v147; // rcx
  __int64 v148; // rdx
  __int128 v149; // xmm0
  __int128 v150; // xmm1
  __int128 v151; // xmm0
  __int128 v152; // xmm1
  __int128 v153; // xmm0
  __int128 v154; // xmm1
  __int128 v155; // xmm0
  __int128 v156; // xmm1
  __int64 v157; // rdx
  __int64 *v158; // rax
  __int64 v159; // rcx
  __int128 v160; // xmm0
  __int128 v161; // xmm1
  __int128 v162; // xmm0
  __int128 v163; // xmm1
  __int128 v164; // xmm0
  __int128 v165; // xmm1
  __int128 v166; // xmm0
  __int128 v167; // xmm1
  __int128 *v168; // r14
  __int128 *v169; // rcx
  __int64 v170; // rdx
  __int128 *v171; // rax
  __int128 v172; // xmm0
  __int128 v173; // xmm1
  __int128 v174; // xmm0
  __int128 v175; // xmm1
  __int128 v176; // xmm0
  __int128 v177; // xmm1
  __int128 v178; // xmm0
  __int128 v179; // xmm1
  __int128 v180; // xmm0
  int v181; // eax
  __int64 v182; // rbx
  __int64 v183; // rdi
  __int64 v184; // r9
  __int64 v185; // r8
  __int128 *v186; // rax
  __int64 v187; // rdx
  __int128 *v188; // rcx
  __int128 v189; // xmm0
  __int128 v190; // xmm1
  __int128 v191; // xmm0
  __int128 v192; // xmm1
  __int128 v193; // xmm0
  __int128 v194; // xmm1
  __int128 v195; // xmm0
  __int128 v196; // xmm1
  __int64 v197; // rdi
  unsigned int v198; // esi
  __int128 *v199; // rbx
  __int128 *v200; // rax
  __int128 *v201; // rcx
  __int64 v202; // rdx
  __int128 v203; // xmm0
  __int128 v204; // xmm1
  __int128 v205; // xmm0
  __int128 v206; // xmm1
  __int128 v207; // xmm0
  __int128 v208; // xmm1
  __int128 v209; // xmm0
  __int128 v210; // xmm1
  __int128 v211; // xmm0
  __int128 *v212; // rax
  __int64 v213; // rdx
  float *v214; // rcx
  __int128 v215; // xmm0
  __int128 v216; // xmm1
  __int128 v217; // xmm0
  __int128 v218; // xmm1
  __int128 v219; // xmm0
  __int128 v220; // xmm1
  __int128 v221; // xmm0
  __int128 v222; // xmm1
  unsigned int v223; // esi
  __int64 v224; // rbx
  int v225; // ebx
  float **v226; // rdi
  float *v227; // r10
  int v228; // r8d
  float v229; // xmm6_4
  __int64 v230; // r9
  __int64 v231; // r11
  float v232; // xmm5_4
  unsigned int v233; // eax
  __int64 v234; // rdx
  float v235; // xmm4_4
  double v236; // xmm2_8
  double v237; // xmm0_8
  float v238; // xmm5_4
  float v239; // xmm3_4
  double v240; // xmm2_8
  double v241; // xmm0_8
  float v242; // xmm4_4
  float v243; // xmm3_4
  double v244; // xmm2_8
  double v245; // xmm0_8
  float v246; // xmm3_4
  __int64 v247; // r8
  float v248; // xmm3_4
  float v249; // xmm0_4
  double v250; // xmm2_8
  double v251; // xmm0_8
  char v252; // r14
  __int128 *v253; // rax
  __int64 v254; // rdx
  __int128 *v255; // rcx
  __int128 v256; // xmm0
  __int128 v257; // xmm1
  __int128 v258; // xmm0
  __int128 v259; // xmm1
  __int128 v260; // xmm0
  __int128 v261; // xmm1
  __int128 v262; // xmm0
  __int128 v263; // xmm1
  __int128 *v264; // rax
  __int128 *v265; // rcx
  __int64 v266; // rdx
  __int128 v267; // xmm1
  __int128 v268; // xmm0
  __int128 v269; // xmm2
  __int128 v270; // xmm1
  __int128 v271; // xmm1
  __int128 v272; // xmm0
  __int128 v273; // xmm1
  __int128 v274; // xmm0
  __int128 v275; // xmm0
  __int128 *v276; // rcx
  __int64 v277; // rdx
  __int128 *v278; // rax
  __int128 v279; // xmm0
  __int128 v280; // xmm1
  __int128 v281; // xmm0
  __int128 v282; // xmm1
  __int128 v283; // xmm0
  __int128 v284; // xmm1
  __int128 v285; // xmm0
  __int128 v286; // xmm1
  unsigned int v287; // esi
  __int64 v288; // rbx
  __int64 v289; // rdi
  int v290; // ecx
  int v291; // edx
  _QWORD *v292; // rcx
  __int128 *v293; // rax
  __int64 v294; // rdx
  __int128 *v295; // rcx
  __int128 v296; // xmm0
  __int128 v297; // xmm1
  __int128 v298; // xmm0
  __int128 v299; // xmm1
  __int128 v300; // xmm0
  __int128 v301; // xmm1
  __int128 v302; // xmm0
  __int128 v303; // xmm1
  int v304; // r14d
  __int64 *v305; // r12
  __int64 v306; // rcx
  __int128 *v307; // rax
  __int128 *v308; // rcx
  __int64 v309; // rdx
  __int128 v310; // xmm0
  __int128 v311; // xmm1
  __int128 v312; // xmm0
  __int128 v313; // xmm1
  __int128 v314; // xmm0
  __int128 v315; // xmm1
  __int128 v316; // xmm0
  __int128 v317; // xmm1
  int v318; // edx
  unsigned int v319; // esi
  __int128 *v320; // rbx
  __int64 v321; // rdi
  __int128 *v322; // rax
  __int64 v323; // r8
  __int128 *v324; // rcx
  __int128 v325; // xmm0
  __int128 v326; // xmm1
  __int128 v327; // xmm0
  __int128 v328; // xmm1
  __int128 v329; // xmm0
  __int128 v330; // xmm1
  __int128 v331; // xmm0
  __int128 v332; // xmm1
  unsigned int v333; // esi
  __int128 *v334; // rbx
  __int64 v335; // rdi
  int v336; // ecx
  int v337; // edx
  _QWORD *v338; // rcx
  int v339; // ecx
  int v340; // edx
  _QWORD *v341; // rcx
  int v342; // ecx
  int v343; // edx
  _QWORD *v344; // rcx
  __int128 *v345; // rax
  __int64 v346; // rdx
  __int128 *v347; // rcx
  __int128 v348; // xmm0
  __int128 v349; // xmm1
  __int128 v350; // xmm0
  __int128 v351; // xmm1
  __int128 v352; // xmm0
  __int128 v353; // xmm1
  __int128 v354; // xmm0
  __int128 v355; // xmm1
  __m128i v356; // xmm1
  int v357; // ecx
  int v358; // edx
  _QWORD *v359; // rcx
  __int128 *v360; // rax
  __int64 v361; // rdx
  __int128 *v362; // rcx
  __int128 v363; // xmm0
  __int128 v364; // xmm1
  __int128 v365; // xmm0
  __int128 v366; // xmm1
  __int128 v367; // xmm0
  __int128 v368; // xmm1
  __int128 v369; // xmm0
  __int128 v370; // xmm1
  __int128 *v371; // rax
  __int64 v372; // rdx
  __int128 *v373; // rcx
  __int128 v374; // xmm0
  __int128 v375; // xmm1
  __int128 v376; // xmm0
  __int128 v377; // xmm1
  __int128 v378; // xmm0
  __int128 v379; // xmm1
  __int128 v380; // xmm0
  __int128 v381; // xmm1
  __int64 v382; // rdi
  unsigned int v383; // esi
  __int128 *v384; // rbx
  va_list v385; // rcx
  __int128 *v386; // rax
  __int128 *v387; // rcx
  __int64 v388; // rdx
  __int128 v389; // xmm0
  __int128 v390; // xmm1
  __int128 v391; // xmm0
  __int128 v392; // xmm1
  __int128 v393; // xmm0
  __int128 v394; // xmm1
  __int128 v395; // xmm0
  __int128 v396; // xmm1
  unsigned int v397; // esi
  __int128 *v398; // rbx
  __int64 v399; // r10
  _QWORD *v400; // r12
  __int64 v401; // rcx
  int v402; // r14d
  __int64 v403; // rsi
  __int64 v404; // rbx
  int v405; // edx
  __int64 v406; // r8
  int v407; // edi
  __int64 v408; // rbx
  int v409; // edx
  __int64 v410; // r8
  __int64 v411; // r8
  int v412; // r8d
  __int64 v413; // rsi
  int v414; // edx
  _QWORD *v415; // rcx
  __int64 *v416; // rax
  __int128 *v417; // rcx
  __int64 v418; // rdx
  __int128 v419; // xmm0
  __int128 v420; // xmm1
  __int128 v421; // xmm0
  __int128 v422; // xmm1
  __int128 v423; // xmm0
  __int128 v424; // xmm1
  __int128 v425; // xmm0
  __int128 v426; // xmm1
  unsigned int v427; // esi
  __int64 v428; // rbx
  unsigned int v429; // r14d
  __int64 *v430; // rbx
  __int128 *v431; // rax
  __int64 v432; // rdx
  __int128 *v433; // rcx
  __int128 v434; // xmm0
  __int128 v435; // xmm1
  __int128 v436; // xmm0
  __int128 v437; // xmm1
  __int128 v438; // xmm0
  __int128 v439; // xmm1
  __int128 v440; // xmm0
  __int128 v441; // xmm1
  __int64 *v442; // r8
  int v443; // r8d
  __int64 v444; // rsi
  int v445; // edx
  _QWORD *v446; // rcx
  __int64 *v447; // rax
  __int64 v448; // rdx
  __int128 *v449; // rcx
  __int128 v450; // xmm0
  __int128 v451; // xmm1
  __int128 v452; // xmm0
  __int128 v453; // xmm1
  __int128 v454; // xmm0
  __int128 v455; // xmm1
  __int128 v456; // xmm0
  __int128 v457; // xmm1
  __int64 v458; // rdx
  unsigned int v459; // esi
  __int64 v460; // rbx
  __int64 v461; // rdi
  unsigned int v462; // r14d
  __int64 *v463; // rbx
  __int64 v464; // rdi
  __int128 *v465; // rax
  __int64 v466; // r8
  __int128 *v467; // rcx
  __int128 v468; // xmm0
  __int128 v469; // xmm1
  __int128 v470; // xmm0
  __int128 v471; // xmm1
  __int128 v472; // xmm0
  __int128 v473; // xmm1
  __int128 v474; // xmm0
  __int128 v475; // xmm1
  __int128 v476; // xmm0
  __int128 *v477; // rcx
  __int64 v478; // r8
  __int128 *v479; // rax
  __int128 v480; // xmm0
  __int128 v481; // xmm1
  __int128 v482; // xmm0
  __int128 v483; // xmm1
  __int128 v484; // xmm0
  __int128 v485; // xmm1
  __int128 v486; // xmm0
  __int128 v487; // xmm1
  unsigned int v488; // esi
  __int64 v489; // rbx
  __int64 v490; // rdi
  __int64 *v491; // rax
  __int64 v492; // r8
  __int128 *v493; // rcx
  __int128 v494; // xmm0
  __int128 v495; // xmm1
  __int128 v496; // xmm0
  __int128 v497; // xmm1
  __int128 v498; // xmm0
  __int128 v499; // xmm1
  __int128 v500; // xmm0
  __int128 v501; // xmm1
  unsigned int v502; // esi
  __int64 *v503; // rbx
  __int64 v504; // rdi
  __int64 v505; // r12
  __int128 *v506; // rcx
  __int128 *v507; // rdx
  __int128 *v508; // rax
  __int64 v509; // r8
  __int128 v510; // xmm0
  __int128 v511; // xmm1
  __int128 v512; // xmm0
  __int128 v513; // xmm1
  __int128 v514; // xmm0
  __int128 v515; // xmm1
  __int128 v516; // xmm0
  __int128 v517; // xmm1
  __int128 v518; // xmm0
  __int64 v519; // rdx
  __int64 *v520; // rax
  __int128 v521; // xmm0
  __int128 v522; // xmm1
  __int128 v523; // xmm0
  __int128 v524; // xmm1
  __int128 v525; // xmm0
  __int128 v526; // xmm1
  __int128 v527; // xmm0
  __int128 v528; // xmm1
  unsigned int v529; // esi
  __int64 v530; // rbx
  __int64 v531; // rdi
  __int128 *v532; // rax
  __int64 *v533; // rcx
  __int64 v534; // rdx
  __int128 v535; // xmm1
  __int128 v536; // xmm0
  __int128 v537; // xmm1
  __int128 v538; // xmm0
  __int128 v539; // xmm1
  __int128 v540; // xmm0
  __int128 v541; // xmm1
  __int128 v542; // xmm0
  __int64 *v543; // rbx
  __int64 v544; // rdi
  unsigned int v545; // esi
  __int128 *v546; // rax
  __int64 v547; // rdx
  __int128 *v548; // rcx
  __int128 v549; // xmm0
  __int128 v550; // xmm1
  __int128 v551; // xmm0
  __int128 v552; // xmm1
  __int128 v553; // xmm0
  __int128 v554; // xmm1
  __int128 v555; // xmm0
  __int128 v556; // xmm1
  __int128 v557; // xmm0
  __int128 *v558; // rcx
  __int64 v559; // rdx
  __int128 *v560; // rax
  __int128 v561; // xmm0
  __int128 v562; // xmm1
  __int128 v563; // xmm0
  __int128 v564; // xmm1
  __int128 v565; // xmm0
  __int128 v566; // xmm1
  __int128 v567; // xmm0
  __int128 v568; // xmm1
  __int64 v569; // r8
  int v570; // esi
  __int64 v571; // r14
  __int64 *v572; // rdi
  __int64 v573; // rbx
  __int64 v574; // rdx
  __int64 v575; // rdx
  __int64 v576; // rdx
  __int64 v577; // rsi
  int v578; // ecx
  int v579; // edx
  _QWORD *v580; // rcx
  __int128 *v581; // rax
  __int64 v582; // rdx
  __int128 *v583; // rcx
  __int128 v584; // xmm0
  __int128 v585; // xmm1
  __int128 v586; // xmm0
  __int128 v587; // xmm1
  __int128 v588; // xmm0
  __int128 v589; // xmm1
  __int128 v590; // xmm0
  __int128 v591; // xmm1
  __m128i v592; // xmm1
  int v593; // ebx
  int v594; // edx
  __int32 v595; // esi
  __m128i *v596; // rcx
  __int64 v597; // r8
  __int64 v598; // r9
  int v599; // edx
  int v600; // ecx
  int v601; // ecx
  int v602; // edx
  _QWORD *v603; // rcx
  __m128i v604; // xmm7
  __int128 v605; // xmm8
  __int128 v606; // xmm9
  __int128 v607; // xmm10
  __int128 v608; // xmm11
  __int128 v609; // xmm12
  __int128 v610; // xmm13
  __int128 v611; // xmm14
  __m128i v612; // xmm15
  __int64 v613; // rdi
  __int64 v614; // r12
  __int64 v615; // r8
  _OWORD *v616; // rax
  __int128 *v617; // rcx
  __int64 v618; // rdx
  __int128 v619; // xmm0
  __int128 v620; // xmm1
  __int128 v621; // xmm0
  __int128 v622; // xmm1
  __int128 v623; // xmm0
  __int128 v624; // xmm1
  __int128 v625; // xmm0
  __int128 v626; // xmm1
  __int128 v627; // xmm0
  __m128i *v628; // rcx
  __int64 v629; // rdx
  __m128i *v630; // rax
  __m128i v631; // xmm0
  __m128i v632; // xmm1
  __m128i v633; // xmm0
  __m128i v634; // xmm1
  __m128i v635; // xmm0
  __m128i v636; // xmm1
  __m128i v637; // xmm0
  __m128i v638; // xmm1
  __int64 v639; // r12
  __int64 v640; // rdi
  __int64 v641; // rbx
  __int64 v642; // rsi
  __int64 v643; // rsi
  __int64 v644; // rbx
  __int64 v645; // r12
  __int128 *v646; // rax
  __int64 v647; // rdx
  __int128 *v648; // rcx
  __int128 v649; // xmm0
  __int128 v650; // xmm1
  __int128 v651; // xmm0
  __int128 v652; // xmm1
  __int128 v653; // xmm0
  __int128 v654; // xmm1
  __int128 v655; // xmm0
  __int128 v656; // xmm1
  _QWORD *v657; // rbx
  __int64 v658; // rsi
  int v659; // ebx
  unsigned int v660; // esi
  __int64 v661; // r8
  __int64 v662; // r9
  __int64 v663; // r10
  int v664; // edx
  int v665; // ecx
  __int128 *v666; // rax
  __int64 v667; // rdx
  __int128 *v668; // rcx
  __int128 v669; // xmm0
  __int128 v670; // xmm1
  __int128 v671; // xmm0
  __int128 v672; // xmm1
  __int128 v673; // xmm0
  __int128 v674; // xmm1
  __int128 v675; // xmm0
  __int128 v676; // xmm1
  __int128 v677; // xmm0
  __int128 *v678; // rcx
  __int64 v679; // rdx
  __int128 *v680; // rax
  __int128 v681; // xmm0
  __int128 v682; // xmm1
  __int128 v683; // xmm0
  __int128 v684; // xmm1
  __int128 v685; // xmm0
  __int128 v686; // xmm1
  __int128 v687; // xmm0
  __int128 v688; // xmm1
  __int64 v689; // rdi
  __int64 v690; // rbx
  __int64 v691; // rdi
  _QWORD *v692; // rbx
  __int128 *v693; // rax
  __int64 v694; // rdx
  __int128 *v695; // rcx
  __int128 v696; // xmm0
  __int128 v697; // xmm1
  __int128 v698; // xmm0
  __int128 v699; // xmm1
  __int128 v700; // xmm0
  __int128 v701; // xmm1
  __int128 v702; // xmm0
  __int128 v703; // xmm1
  __int128 *v704; // rax
  __int64 v705; // rdx
  __int128 *v706; // rcx
  __int128 v707; // xmm0
  __int128 v708; // xmm1
  __int128 v709; // xmm0
  __int128 v710; // xmm1
  __int128 v711; // xmm0
  __int128 v712; // xmm1
  __int128 v713; // xmm0
  __int128 v714; // xmm1
  __int64 v715; // r12
  _QWORD *v716; // rbx
  _OWORD *v717; // rax
  __int64 v718; // rdx
  __int128 *v719; // rcx
  __int128 v720; // xmm0
  __int128 v721; // xmm1
  __int128 v722; // xmm0
  __int128 v723; // xmm1
  __int128 v724; // xmm0
  __int128 v725; // xmm1
  __int128 v726; // xmm0
  __int128 v727; // xmm1
  __int128 v728; // xmm0
  __int128 *v729; // rcx
  __int64 v730; // rdx
  __int128 *v731; // rax
  __int128 v732; // xmm0
  __int128 v733; // xmm1
  __int128 v734; // xmm0
  __int128 v735; // xmm1
  __int128 v736; // xmm0
  __int128 v737; // xmm1
  __int128 v738; // xmm0
  __int128 v739; // xmm1
  __int64 v740; // rbx
  __int64 v741; // rsi
  __int128 *v742; // rbx
  __int64 v743; // rsi
  _OWORD *v744; // rax
  __int64 v745; // rdx
  __int128 *v746; // rcx
  __int128 v747; // xmm0
  __int128 v748; // xmm1
  __int128 v749; // xmm0
  __int128 v750; // xmm1
  __int128 v751; // xmm0
  __int128 v752; // xmm1
  __int128 v753; // xmm0
  __int128 v754; // xmm1
  __int128 v755; // xmm0
  __int128 *v756; // rcx
  __int64 v757; // rdx
  __int128 *v758; // rax
  __int128 v759; // xmm0
  __int128 v760; // xmm1
  __int128 v761; // xmm0
  __int128 v762; // xmm1
  __int128 v763; // xmm0
  __int128 v764; // xmm1
  __int128 v765; // xmm0
  __int128 v766; // xmm1
  __int64 v767; // rbx
  __int64 v768; // rdi
  __int64 v769; // rdi
  __int128 *v770; // rbx
  __int64 v771; // rsi
  __int128 *v772; // rax
  __int64 v773; // rdx
  __int128 *v774; // rcx
  __int128 v775; // xmm0
  __int128 v776; // xmm1
  __int128 v777; // xmm0
  __int128 v778; // xmm1
  __int128 v779; // xmm0
  __int128 v780; // xmm1
  __int128 v781; // xmm0
  __int128 v782; // xmm1
  _QWORD *v783; // rbx
  __int64 v784; // rdi
  __int64 v785; // r8
  __int64 v786; // r9
  int v787; // edx
  int v788; // ecx
  _OWORD *v789; // rax
  __int64 v790; // rdx
  __int128 *v791; // rcx
  __int128 v792; // xmm0
  __int128 v793; // xmm1
  __int128 v794; // xmm0
  __int128 v795; // xmm1
  __int128 v796; // xmm0
  __int128 v797; // xmm1
  __int128 v798; // xmm0
  __int128 v799; // xmm1
  __int128 v800; // xmm0
  __int128 *v801; // rcx
  __int64 v802; // rdx
  __int128 *v803; // rax
  __int128 v804; // xmm0
  __int128 v805; // xmm1
  __int128 v806; // xmm0
  __int128 v807; // xmm1
  __int128 v808; // xmm0
  __int128 v809; // xmm1
  __int128 v810; // xmm0
  __int128 v811; // xmm1
  __int64 v812; // rbx
  __int64 v813; // rdi
  unsigned int v814; // ebx
  __int64 v815; // r8
  __int64 v816; // rsi
  int v817; // edx
  int v818; // ecx
  __int128 *v819; // rax
  __int64 v820; // rdx
  __int128 *v821; // rcx
  __int128 v822; // xmm0
  __int128 v823; // xmm1
  __int128 v824; // xmm0
  __int128 v825; // xmm1
  __int128 v826; // xmm0
  __int128 v827; // xmm1
  __int128 v828; // xmm0
  __int128 v829; // xmm1
  __int128 v830; // xmm0
  __int128 *v831; // rcx
  __int64 v832; // rdx
  __int128 *v833; // rax
  __int128 v834; // xmm0
  __int128 v835; // xmm1
  __int128 v836; // xmm0
  __int128 v837; // xmm1
  __int128 v838; // xmm0
  __int128 v839; // xmm1
  __int128 v840; // xmm0
  __int128 v841; // xmm1
  __int128 *v842; // rax
  __int64 v843; // rdx
  __int128 *v844; // rcx
  __int128 v845; // xmm0
  __int128 v846; // xmm1
  __int128 v847; // xmm0
  __int128 v848; // xmm1
  __int128 v849; // xmm0
  __int128 v850; // xmm1
  __int128 v851; // xmm0
  __int128 v852; // xmm1
  _QWORD *v853; // rdi
  __int64 v854; // r14
  __int128 *v855; // rax
  __int64 v856; // rdx
  __int128 *v857; // rcx
  __int128 v858; // xmm0
  __int128 v859; // xmm1
  __int128 v860; // xmm0
  __int128 v861; // xmm1
  __int128 v862; // xmm0
  __int128 v863; // xmm1
  __int128 v864; // xmm0
  __int128 v865; // xmm1
  __int128 *v866; // rdi
  __int64 v867; // r14
  __int128 *v868; // rax
  __int128 *v869; // rcx
  __int64 v870; // rdx
  __int128 v871; // xmm1
  __int128 v872; // xmm0
  __int128 v873; // xmm2
  __int128 v874; // xmm1
  __int128 v875; // xmm1
  __int128 v876; // xmm0
  __int128 v877; // xmm1
  __int128 v878; // xmm0
  __int128 *v879; // rdi
  __int64 v880; // r14
  int v881; // r8d
  __int64 v882; // r12
  int v883; // edx
  _QWORD *v884; // rcx
  __int128 *v885; // rax
  __int64 v886; // rdx
  __int128 *v887; // rcx
  __int128 v888; // xmm0
  __int128 v889; // xmm1
  __int128 v890; // xmm0
  __int128 v891; // xmm1
  __int128 v892; // xmm0
  __int128 v893; // xmm1
  __int128 v894; // xmm0
  __int128 v895; // xmm1
  __int64 v896; // rdi
  __int64 v897; // r14
  __int128 *v898; // rdi
  __int64 v899; // r14
  __int64 v900; // r14
  unsigned int v901; // edi
  __int64 v902; // r8
  __int64 v903; // r9
  int v904; // edx
  int v905; // ecx
  _OWORD *v906; // rax
  __int64 v907; // rdx
  __int128 *v908; // rcx
  __int128 v909; // xmm0
  __int128 v910; // xmm1
  __int128 v911; // xmm0
  __int128 v912; // xmm1
  __int128 v913; // xmm0
  __int128 v914; // xmm1
  __int128 v915; // xmm0
  __int128 v916; // xmm1
  __int128 v917; // xmm0
  __int128 *v918; // rcx
  __int64 v919; // rdx
  __int128 *v920; // rax
  __int128 v921; // xmm0
  __int128 v922; // xmm1
  __int128 v923; // xmm0
  __int128 v924; // xmm1
  __int128 v925; // xmm0
  __int128 v926; // xmm1
  __int128 v927; // xmm0
  __int128 v928; // xmm1
  __int128 v929; // xmm0
  __m128i *v930; // rcx
  __int64 v931; // rdx
  __int128 *v932; // rax
  __m128i v933; // xmm0
  __int128 v934; // xmm1
  __int128 v935; // xmm0
  __int128 v936; // xmm1
  __int128 v937; // xmm0
  __int128 v938; // xmm1
  __int128 v939; // xmm0
  __int128 v940; // xmm1
  __int64 v941; // rbx
  __int64 v942; // rsi
  __int64 v943; // r14
  __int64 v944; // rbx
  __int64 v945; // rsi
  __m128i *v946; // rax
  __int64 v947; // rdx
  __m128i *v948; // rcx
  __m128i v949; // xmm0
  __m128i v950; // xmm1
  __m128i v951; // xmm0
  __m128i v952; // xmm1
  __m128i v953; // xmm0
  __m128i v954; // xmm1
  __m128i v955; // xmm0
  __m128i v956; // xmm1
  __int64 *v957; // r8
  int v958; // r8d
  __int64 v959; // rsi
  int v960; // edx
  _QWORD *v961; // rcx
  __int128 *v962; // rax
  __int64 v963; // rdx
  __m128i *v964; // rcx
  __m128i v965; // xmm0
  __int128 v966; // xmm1
  __int128 v967; // xmm0
  __int128 v968; // xmm1
  __int128 v969; // xmm0
  __int128 v970; // xmm1
  __int128 v971; // xmm0
  __int128 v972; // xmm1
  __int64 v973; // rdx
  unsigned int v974; // esi
  __int64 v975; // rbx
  __int64 v976; // rdi
  unsigned int v977; // r14d
  __int128 *v978; // rbx
  __int64 v979; // rdi
  __m128i *v980; // rax
  __int64 v981; // r8
  __m128i *v982; // rcx
  __m128i v983; // xmm0
  __m128i v984; // xmm1
  __m128i v985; // xmm0
  __m128i v986; // xmm1
  __m128i v987; // xmm0
  __m128i v988; // xmm1
  __m128i v989; // xmm0
  __m128i v990; // xmm1
  unsigned int v991; // esi
  _QWORD *v992; // rbx
  __int64 v993; // rdi
  __int64 v994; // rax
  __m128i *v995; // rdx
  __int128 *v996; // rcx
  __int64 v997; // r8
  __m128i *v998; // rax
  __m128i v999; // xmm0
  __m128i v1000; // xmm1
  __m128i v1001; // xmm0
  __m128i v1002; // xmm1
  __m128i v1003; // xmm0
  __m128i v1004; // xmm1
  __m128i v1005; // xmm0
  __m128i v1006; // xmm1
  __m128i v1007; // xmm0
  __int64 v1008; // rdx
  __int64 *v1009; // rax
  __int128 v1010; // xmm0
  __int128 v1011; // xmm1
  __int128 v1012; // xmm0
  __int128 v1013; // xmm1
  __int128 v1014; // xmm0
  __int128 v1015; // xmm1
  __int128 v1016; // xmm0
  __int128 v1017; // xmm1
  unsigned int v1018; // esi
  __int64 v1019; // rbx
  __int64 v1020; // rdi
  __int128 *v1021; // rax
  __int64 *v1022; // rcx
  __int64 v1023; // rdx
  __int128 v1024; // xmm0
  __int128 v1025; // xmm1
  __int128 v1026; // xmm0
  __int128 v1027; // xmm1
  __int128 v1028; // xmm0
  __int128 v1029; // xmm1
  __int128 v1030; // xmm0
  __int128 v1031; // xmm1
  unsigned int v1032; // esi
  __int64 *v1033; // rbx
  __int64 v1034; // rdi
  __int64 v1035; // r8
  __int128 *v1036; // rax
  __int128 *v1037; // rcx
  __int64 v1038; // rdx
  __int128 v1039; // xmm0
  __int128 v1040; // xmm1
  __int128 v1041; // xmm0
  __int128 v1042; // xmm1
  __int128 v1043; // xmm0
  __int128 v1044; // xmm1
  __int128 v1045; // xmm0
  __int128 v1046; // xmm1
  unsigned int **v1047; // r9
  __int64 v1048; // rdx
  __int64 v1049; // r8
  bool v1050; // zf
  __int64 v1051; // rbx
  __int64 v1052; // rsi
  __int64 v1053; // r14
  __int64 v1054; // rdx
  int v1055; // edi
  int v1056; // edx
  _QWORD *v1057; // rcx
  int v1058; // ebx
  __int64 v1059; // r12
  int v1060; // edx
  _QWORD *v1061; // rcx
  int v1062; // ecx
  int v1063; // edx
  __int64 v1064; // rsi
  int v1065; // r9d
  __int64 v1066; // r10
  _QWORD *v1067; // rcx
  __int64 v1068; // rdx
  int v1069; // ecx
  __int64 v1070; // rdx
  int v1071; // r8d
  int v1072; // ecx
  __int64 v1073; // r8
  __int64 v1074; // r8
  __int64 v1075; // rbx
  __int64 v1076; // rdi
  int v1077; // edx
  int v1078; // ecx
  _QWORD *v1079; // rcx
  __int64 v1080; // r8
  __int128 *v1081; // rcx
  __int64 v1082; // rbx
  __int64 v1083; // rdx
  __int128 *v1084; // rax
  __int128 v1085; // xmm0
  __int128 v1086; // xmm1
  __int128 v1087; // xmm0
  __int128 v1088; // xmm1
  __int128 v1089; // xmm0
  __int128 v1090; // xmm1
  __int128 v1091; // xmm0
  __int128 v1092; // xmm1
  __int64 v1093; // r8
  __int64 v1094; // rax
  int v1095; // r8d
  __int64 v1096; // r13
  __int64 v1097; // rsi
  int v1098; // edx
  __int64 v1099; // r13
  _QWORD *v1100; // rcx
  __int64 *v1101; // rax
  __int128 v1102; // xmm0
  __int128 v1103; // xmm1
  __int128 v1104; // xmm0
  __int128 v1105; // xmm1
  __int128 v1106; // xmm0
  __int128 v1107; // xmm1
  __int128 v1108; // xmm0
  __int128 v1109; // xmm1
  __int64 result; // rax
  unsigned int v1111; // edi
  __int64 v1112; // rbx
  unsigned int v1113; // r14d
  __int64 *v1114; // rbx
  __int64 v1115; // rdi
  __int64 v1116; // [rsp+20h] [rbp-E0h]
  int v1117; // [rsp+38h] [rbp-C8h]
  __int64 v1118; // [rsp+38h] [rbp-C8h]
  int v1119; // [rsp+40h] [rbp-C0h]
  __m128i v1120; // [rsp+50h] [rbp-B0h] BYREF
  __int128 v1121; // [rsp+60h] [rbp-A0h]
  __int128 v1122; // [rsp+70h] [rbp-90h]
  __int128 v1123; // [rsp+80h] [rbp-80h]
  __int128 v1124; // [rsp+90h] [rbp-70h]
  __int128 v1125; // [rsp+A0h] [rbp-60h]
  __int128 v1126; // [rsp+B0h] [rbp-50h]
  __int128 v1127; // [rsp+C0h] [rbp-40h]
  __m128i v1128; // [rsp+D0h] [rbp-30h]
  __int64 v1129; // [rsp+E0h] [rbp-20h]
  float v1130; // [rsp+F0h] [rbp-10h]
  __int64 v1131; // [rsp+F8h] [rbp-8h]
  __int64 v1132; // [rsp+100h] [rbp+0h]
  int v1133; // [rsp+108h] [rbp+8h]
  _OWORD v1134[8]; // [rsp+110h] [rbp+10h] BYREF
  __m128i v1135; // [rsp+190h] [rbp+90h]
  _OWORD v1136[8]; // [rsp+520h] [rbp+420h] BYREF
  __m128i v1137; // [rsp+5A0h] [rbp+4A0h]
  _OWORD v1138[8]; // [rsp+930h] [rbp+830h] BYREF
  __m128i v1139; // [rsp+9B0h] [rbp+8B0h]
  unsigned int v1140; // [rsp+D30h] [rbp+C30h]
  unsigned int v1141; // [rsp+D34h] [rbp+C34h]
  __int64 v1142; // [rsp+D38h] [rbp+C38h]
  _BYTE v1143[1024]; // [rsp+D40h] [rbp+C40h] BYREF
  __int64 v1144; // [rsp+1140h] [rbp+1040h]
  __int128 v1145[65]; // [rsp+1150h] [rbp+1050h] BYREF
  __int64 v1146; // [rsp+1560h] [rbp+1460h] BYREF
  char v1147[1016]; // [rsp+1568h] [rbp+1468h] BYREF
  int v1148; // [rsp+1960h] [rbp+1860h]
  unsigned int v1149; // [rsp+1964h] [rbp+1864h]
  __int64 v1150; // [rsp+1968h] [rbp+1868h]
  __m128i v1151[64]; // [rsp+1970h] [rbp+1870h] BYREF
  __int64 v1152; // [rsp+1D70h] [rbp+1C70h]
  __int64 v1153; // [rsp+1D78h] [rbp+1C78h]
  __m128i v1154; // [rsp+1D80h] [rbp+1C80h] BYREF
  __int128 v1155; // [rsp+1D90h] [rbp+1C90h]
  __int128 v1156; // [rsp+1DA0h] [rbp+1CA0h]
  __int128 v1157; // [rsp+1DB0h] [rbp+1CB0h]
  __int128 v1158; // [rsp+1DC0h] [rbp+1CC0h]
  __int128 v1159; // [rsp+1DD0h] [rbp+1CD0h]
  __int128 v1160; // [rsp+1DE0h] [rbp+1CE0h]
  __int128 v1161; // [rsp+1DF0h] [rbp+1CF0h]
  __m128i v1162; // [rsp+1E00h] [rbp+1D00h]
  __int64 v1163; // [rsp+1E10h] [rbp+1D10h]
  _QWORD v1164[130]; // [rsp+2190h] [rbp+2090h] BYREF
  __int128 v1165[65]; // [rsp+25A0h] [rbp+24A0h] BYREF
  __int64 v1166; // [rsp+29B0h] [rbp+28B0h] BYREF
  char v1167[1016]; // [rsp+29B8h] [rbp+28B8h] BYREF
  unsigned int v1168; // [rsp+2DB0h] [rbp+2CB0h]
  int v1169; // [rsp+2DB4h] [rbp+2CB4h]
  __int64 v1170; // [rsp+2DB8h] [rbp+2CB8h]
  __int64 v1171; // [rsp+2DC0h] [rbp+2CC0h] BYREF
  char v1172[1016]; // [rsp+2DC8h] [rbp+2CC8h] BYREF
  __int64 v1173; // [rsp+31C0h] [rbp+30C0h]
  __int64 v1174; // [rsp+31C8h] [rbp+30C8h]
  __int64 v1175; // [rsp+31D0h] [rbp+30D0h] BYREF
  char v1176[1016]; // [rsp+31D8h] [rbp+30D8h] BYREF
  unsigned int v1177; // [rsp+35D0h] [rbp+34D0h]
  int v1178; // [rsp+35D4h] [rbp+34D4h]
  __int64 v1179; // [rsp+35D8h] [rbp+34D8h]
  _QWORD v1180[130]; // [rsp+35E0h] [rbp+34E0h] BYREF
  _BYTE v1181[1040]; // [rsp+39F0h] [rbp+38F0h] BYREF
  __int128 v1182[65]; // [rsp+3E00h] [rbp+3D00h] BYREF
  __int128 v1183[65]; // [rsp+4210h] [rbp+4110h] BYREF
  _QWORD v1184[130]; // [rsp+4620h] [rbp+4520h] BYREF
  bool v1185; // [rsp+4B20h] [rbp+4A20h]
  unsigned __int8 v1187; // [rsp+4B30h] [rbp+4A30h]
  __int128 *v1188; // [rsp+4B38h] [rbp+4A38h] BYREF
  va_list va; // [rsp+4B38h] [rbp+4A38h]
  __int64 v1190; // [rsp+4B40h] [rbp+4A40h]
  __int64 v1191; // [rsp+4B48h] [rbp+4A48h]
  __int64 v1192; // [rsp+4B50h] [rbp+4A50h]
  __int64 v1193; // [rsp+4B58h] [rbp+4A58h] BYREF
  va_list va1; // [rsp+4B58h] [rbp+4A58h]
  __int64 v1195; // [rsp+4B60h] [rbp+4A60h]
  va_list va2; // [rsp+4B68h] [rbp+4A68h] BYREF

  va_start(va2, a3);
  va_start(va1, a3);
  va_start(va, a3);
  v1188 = va_arg(va1, __int128 *);
  v1190 = va_arg(va1, _QWORD);
  v1191 = va_arg(va1, _QWORD);
  v1192 = va_arg(va1, _QWORD);
  va_copy(va2, va1);
  v1193 = va_arg(va2, _QWORD);
  v1195 = va_arg(va2, _QWORD);
  if ( *(_BYTE *)(a1 + 11208) )
    sub_18087FD60(a1, v1195, 0);
  v6 = &v1146;
  v7 = 8;
  v1187 = *(_BYTE *)(*(_QWORD *)(a1 + 11320) + 82LL);
  v1130 = **(float **)(a1 + 11320);
  LODWORD(v1132) = *(_DWORD *)(*(_QWORD *)(a1 + 11320) + 40LL);
  v1133 = *(_DWORD *)(*(_QWORD *)(a1 + 11320) + 60LL);
  v8 = (__int128 *)a2;
  v9 = *(_QWORD *)(a1 + 72) == *(_QWORD *)(a1 + 80);
  v1185 = *(_QWORD *)(a1 + 72) > 2u;
  do
  {
    v6 += 16;
    v10 = *v8;
    v11 = v8[1];
    v8 += 8;
    *((_OWORD *)v6 - 8) = v10;
    v12 = *(v8 - 6);
    *((_OWORD *)v6 - 7) = v11;
    v13 = *(v8 - 5);
    *((_OWORD *)v6 - 6) = v12;
    v14 = *(v8 - 4);
    *((_OWORD *)v6 - 5) = v13;
    v15 = *(v8 - 3);
    *((_OWORD *)v6 - 4) = v14;
    v16 = *(v8 - 2);
    *((_OWORD *)v6 - 3) = v15;
    v17 = *(v8 - 1);
    *((_OWORD *)v6 - 2) = v16;
    *((_OWORD *)v6 - 1) = v17;
    --v7;
  }
  while ( v7 );
  *(_OWORD *)v6 = *v8;
  if ( v1148 > 0 )
  {
    v18 = v1149;
    v19 = &v1146;
    v20 = (unsigned int)v1148;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD))unk_1800010D0)(*v19++, v18);
      --v20;
    }
    while ( v20 );
  }
  v21 = a3;
  v22 = &v1171;
  v23 = 8;
  do
  {
    v22 += 16;
    v24 = *v21;
    v25 = v21[1];
    v21 += 8;
    *((_OWORD *)v22 - 8) = v24;
    v26 = *(v21 - 6);
    *((_OWORD *)v22 - 7) = v25;
    v27 = *(v21 - 5);
    *((_OWORD *)v22 - 6) = v26;
    v28 = *(v21 - 4);
    *((_OWORD *)v22 - 5) = v27;
    v29 = *(v21 - 3);
    *((_OWORD *)v22 - 4) = v28;
    v30 = *(v21 - 2);
    *((_OWORD *)v22 - 3) = v29;
    v31 = *(v21 - 1);
    *((_OWORD *)v22 - 2) = v30;
    *((_OWORD *)v22 - 1) = v31;
    --v23;
  }
  while ( v23 );
  *(_OWORD *)v22 = *v21;
  if ( (int)v1173 > 0 )
  {
    v32 = HIDWORD(v1173);
    v33 = &v1171;
    v34 = (unsigned int)v1173;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD))unk_1800010D0)(*v33++, v32);
      --v34;
    }
    while ( v34 );
  }
  v35 = 0;
  v36 = 0;
  if ( (_BYTE)v1193 )
  {
    v37 = *(_DWORD *)(a1 + 264);
    v1135.m128i_i32[1] = *(_DWORD *)(a1 + 272);
    memset(v1134, 0, sizeof(v1134));
    v1135.m128i_i32[0] = v37;
    v1135.m128i_i64[1] = 4LL * v1135.m128i_i32[1];
    if ( v37 > 0 )
    {
      v38 = v1134;
      do
      {
        ++v36;
        *v38 = *(_QWORD *)((char *)v38 + a1 + 136 - (_QWORD)v1134);
        ++v38;
      }
      while ( v36 < v1135.m128i_i32[0] );
    }
    v39 = (__m128i *)v1134;
  }
  else
  {
    v40 = *(_DWORD *)(a1 + 408);
    v1139.m128i_i32[1] = *(_DWORD *)(a1 + 416);
    memset(v1138, 0, sizeof(v1138));
    v1139.m128i_i32[0] = v40;
    v1139.m128i_i64[1] = 4LL * v1139.m128i_i32[1];
    if ( v40 > 0 )
    {
      v41 = v1138;
      do
      {
        ++v36;
        *v41 = *(_QWORD *)((char *)v41 + a1 + 280 - (_QWORD)v1138);
        ++v41;
      }
      while ( v36 < v1139.m128i_i32[0] );
    }
    v39 = (__m128i *)v1138;
  }
  v42 = v39[1];
  v43 = v39[8];
  v1136[0] = *v39;
  v44 = v39[2];
  v1136[1] = v42;
  v45 = v39[3];
  v1136[2] = v44;
  v46 = v39[4];
  v1136[3] = v45;
  v47 = v39[5];
  v1136[4] = v46;
  v48 = v39[6];
  v1136[5] = v47;
  v49 = v39[7];
  v1136[6] = v48;
  v1136[7] = v49;
  v1137 = v43;
  if ( !(_BYTE)v1192 )
  {
    if ( !*(_BYTE *)(a1 + 88) )
    {
      v50 = v43.m128i_u32[1];
      v51 = 0;
      memset(v1134, 0, sizeof(v1134));
      v1135.m128i_i64[0] = __PAIR64__(v43.m128i_u32[1], _mm_cvtsi128_si32(v43));
      v1135.m128i_i64[1] = 4LL * v43.m128i_i32[1];
      if ( v1135.m128i_i32[0] > 0 )
      {
        v52 = 0;
        do
        {
          ++v51;
          *(_QWORD *)((char *)v1134 + v52) = *(_QWORD *)((char *)v1136 + v52);
          v52 += 8;
        }
        while ( v51 < v1135.m128i_i32[0] );
      }
      v53 = ((__int64 (__fastcall *)(__int64, __m128i *, _QWORD))unk_180868480)(
              v1190,
              &v1154,
              (unsigned int)-v43.m128i_i32[1]);
      v54 = *(__m128i *)v53;
      v55 = *(_OWORD *)(v53 + 16);
      v56 = *(_OWORD *)(v53 + 32);
      v57 = *(_OWORD *)(v53 + 48);
      v58 = *(_OWORD *)(v53 + 64);
      v59 = *(_OWORD *)(v53 + 80);
      v60 = *(_OWORD *)(v53 + 96);
      v61 = *(_OWORD *)(v53 + 112);
      v62 = *(__m128i *)(v53 + 128);
      v63 = *(_QWORD *)(v53 + 144);
      v64 = (__int128 *)sub_180867C20(a3, v1164, v50);
      v65 = v1145;
      v66 = 8;
      v1138[0] = v1134[0];
      v1138[1] = v1134[1];
      v1138[2] = v1134[2];
      v1138[3] = v1134[3];
      v1138[4] = v1134[4];
      v1138[5] = v1134[5];
      v1138[6] = v1134[6];
      v1138[7] = v1134[7];
      v1139 = v1135;
      v1120 = v54;
      v1121 = v55;
      v1122 = v56;
      v1123 = v57;
      v1124 = v58;
      v1125 = v59;
      v1126 = v60;
      v1127 = v61;
      v1128 = v62;
      v1129 = v63;
      do
      {
        v65 += 8;
        v67 = *v64;
        v68 = v64[1];
        v64 += 8;
        *(v65 - 8) = v67;
        v69 = *(v64 - 6);
        *(v65 - 7) = v68;
        v70 = *(v64 - 5);
        *(v65 - 6) = v69;
        v71 = *(v64 - 4);
        *(v65 - 5) = v70;
        v72 = *(v64 - 3);
        *(v65 - 4) = v71;
        v73 = *(v64 - 2);
        *(v65 - 3) = v72;
        v74 = *(v64 - 1);
        *(v65 - 2) = v73;
        *(v65 - 1) = v74;
        --v66;
      }
      while ( v66 );
LABEL_46:
      *v65 = *v64;
      sub_1808BA1B0(v1145, &v1120, v1138);
      v75 = v1195;
      goto LABEL_47;
    }
LABEL_41:
    v50 = v43.m128i_u32[1];
    v124 = 0;
    memset(v1134, 0, sizeof(v1134));
    v1135.m128i_i64[0] = __PAIR64__(v43.m128i_u32[1], _mm_cvtsi128_si32(v43));
    v1135.m128i_i64[1] = 4LL * v43.m128i_i32[1];
    if ( v1135.m128i_i32[0] > 0 )
    {
      v125 = 0;
      do
      {
        ++v124;
        *(_QWORD *)((char *)v1134 + v125) = *(_QWORD *)((char *)v1136 + v125);
        v125 += 8;
      }
      while ( v124 < v1135.m128i_i32[0] );
    }
    v126 = *(_DWORD *)(v1191 + 144) - v43.m128i_i32[1];
    v127 = *(__m128i *)v1191;
    v128 = *(_OWORD *)(v1191 + 16);
    v129 = *(_OWORD *)(v1191 + 32);
    v130 = *(_OWORD *)(v1191 + 48);
    v131 = *(_OWORD *)(v1191 + 64);
    v132 = *(_OWORD *)(v1191 + 80);
    v133 = *(_OWORD *)(v1191 + 96);
    v134 = *(_OWORD *)(v1191 + 112);
    v135 = *(__m128i *)(v1191 + 128);
    v136 = *(_QWORD *)(v1191 + 8);
    v1163 = *(_QWORD *)(v1191 + 144);
    LODWORD(v1163) = (*(_DWORD *)(v136 + 136) - 1) & v126;
    v64 = (__int128 *)sub_180867C20(a3, v1164, v50);
    v65 = v1145;
    v137 = 8;
    v1138[0] = v1134[0];
    v1138[1] = v1134[1];
    v1138[2] = v1134[2];
    v1138[3] = v1134[3];
    v1138[4] = v1134[4];
    v1138[5] = v1134[5];
    v1138[6] = v1134[6];
    v1138[7] = v1134[7];
    v1139 = v1135;
    v1129 = v1163;
    v1120 = v127;
    v1121 = v128;
    v1122 = v129;
    v1123 = v130;
    v1124 = v131;
    v1125 = v132;
    v1126 = v133;
    v1127 = v134;
    v1128 = v135;
    do
    {
      v65 += 8;
      v138 = *v64;
      v139 = v64[1];
      v64 += 8;
      *(v65 - 8) = v138;
      v140 = *(v64 - 6);
      *(v65 - 7) = v139;
      v141 = *(v64 - 5);
      *(v65 - 6) = v140;
      v142 = *(v64 - 4);
      *(v65 - 5) = v141;
      v143 = *(v64 - 3);
      *(v65 - 4) = v142;
      v144 = *(v64 - 2);
      *(v65 - 3) = v143;
      v145 = *(v64 - 1);
      *(v65 - 2) = v144;
      *(v65 - 1) = v145;
      --v137;
    }
    while ( v137 );
    goto LABEL_46;
  }
  if ( v9 )
    goto LABEL_41;
  v75 = v1195;
  v50 = v43.m128i_u32[1];
  v76 = *(_DWORD *)(v1195 + 24);
  sub_180619E10(v1195, &v1146, *(_QWORD *)(a1 + 72), v43.m128i_u32[1]);
  v77 = ((__int64 (__fastcall *)(__int64, __m128i *, _QWORD))unk_180868480)(
          v1191,
          &v1154,
          (unsigned int)-v43.m128i_i32[1]);
  v78 = ((__int64 (__fastcall *)(__int64, __m128i *, _QWORD, _QWORD))unk_1808BF5C0)(
          v77,
          v1151,
          *(unsigned int *)(a1 + 80),
          0);
  v79 = (__int128 *)&v1146;
  v80 = 8;
  v81 = *(_OWORD *)(v78 + 16);
  v1120 = *(__m128i *)v78;
  v82 = *(_OWORD *)(v78 + 32);
  v1121 = v81;
  v83 = *(_OWORD *)(v78 + 48);
  v1122 = v82;
  v84 = *(_OWORD *)(v78 + 64);
  v1123 = v83;
  v85 = *(_OWORD *)(v78 + 80);
  v1124 = v84;
  v86 = *(_OWORD *)(v78 + 96);
  v1125 = v85;
  v87 = *(_OWORD *)(v78 + 112);
  v1126 = v86;
  v88 = *(__m128i *)(v78 + 128);
  v1127 = v87;
  *(_QWORD *)&v87 = *(_QWORD *)(v78 + 144);
  v89 = v1145;
  v1128 = v88;
  v1129 = v87;
  do
  {
    v89 += 8;
    v90 = *v79;
    v91 = v79[1];
    v79 += 8;
    *(v89 - 8) = v90;
    v92 = *(v79 - 6);
    *(v89 - 7) = v91;
    v93 = *(v79 - 5);
    *(v89 - 6) = v92;
    v94 = *(v79 - 4);
    *(v89 - 5) = v93;
    v95 = *(v79 - 3);
    *(v89 - 4) = v94;
    v96 = *(v79 - 2);
    *(v89 - 3) = v95;
    v97 = *(v79 - 1);
    *(v89 - 2) = v96;
    *(v89 - 1) = v97;
    --v80;
  }
  while ( v80 );
  v98 = *(__int64 **)(a1 + 24);
  *v89 = *v79;
  sub_1808BF650((char *)v1145, (__int128 *)v1120.m128i_i8, v98);
  memset(v1134, 0, sizeof(v1134));
  v99 = 0;
  v1135.m128i_i64[0] = __PAIR64__(v43.m128i_u32[1], _mm_cvtsi128_si32(v43));
  v1135.m128i_i64[1] = 4LL * v43.m128i_i32[1];
  if ( v1135.m128i_i32[0] > 0 )
  {
    v100 = 0;
    do
    {
      ++v99;
      *(_QWORD *)((char *)v1134 + v100) = *(_QWORD *)((char *)v1136 + v100);
      v100 += 8;
    }
    while ( v99 < v1135.m128i_i32[0] );
  }
  v101 = (__int128 *)sub_180867C20(a3, v1164, v43.m128i_u32[1]);
  v102 = v1145;
  v103 = (__int128 *)&v1146;
  v104 = 8;
  v1138[0] = v1134[0];
  v1138[1] = v1134[1];
  v1138[2] = v1134[2];
  v1138[3] = v1134[3];
  v1138[4] = v1134[4];
  v1138[5] = v1134[5];
  v1138[6] = v1134[6];
  v1138[7] = v1134[7];
  v1139 = v1135;
  do
  {
    v102 += 8;
    v105 = *v103;
    v106 = v103[1];
    v103 += 8;
    *(v102 - 8) = v105;
    v107 = *(v103 - 6);
    *(v102 - 7) = v106;
    v108 = *(v103 - 5);
    *(v102 - 6) = v107;
    v109 = *(v103 - 4);
    *(v102 - 5) = v108;
    v110 = *(v103 - 3);
    *(v102 - 4) = v109;
    v111 = *(v103 - 2);
    *(v102 - 3) = v110;
    v112 = *(v103 - 1);
    *(v102 - 2) = v111;
    *(v102 - 1) = v112;
    --v104;
  }
  while ( v104 );
  v113 = *v103;
  v114 = 8;
  *v102 = v113;
  v115 = v1165;
  do
  {
    v115 += 8;
    v116 = *v101;
    v117 = v101[1];
    v101 += 8;
    *(v115 - 8) = v116;
    v118 = *(v101 - 6);
    *(v115 - 7) = v117;
    v119 = *(v101 - 5);
    *(v115 - 6) = v118;
    v120 = *(v101 - 4);
    *(v115 - 5) = v119;
    v121 = *(v101 - 3);
    *(v115 - 4) = v120;
    v122 = *(v101 - 2);
    *(v115 - 3) = v121;
    v123 = *(v101 - 1);
    *(v115 - 2) = v122;
    *(v115 - 1) = v123;
    --v114;
  }
  while ( v114 );
  *v115 = *v101;
  sub_1808BFBE0((__int64)v1165, v1145, (__int64 *)v1138);
  *(_DWORD *)(v75 + 24) = v76;
LABEL_47:
  if ( v1187 )
  {
    v146 = (__int128 *)sub_180867C20(a3, v1164, v50);
    v147 = v1145;
    v148 = 8;
    do
    {
      v147 += 8;
      v149 = *v146;
      v150 = v146[1];
      v146 += 8;
      *(v147 - 8) = v149;
      v151 = *(v146 - 6);
      *(v147 - 7) = v150;
      v152 = *(v146 - 5);
      *(v147 - 6) = v151;
      v153 = *(v146 - 4);
      *(v147 - 5) = v152;
      v154 = *(v146 - 3);
      *(v147 - 4) = v153;
      v155 = *(v146 - 2);
      *(v147 - 3) = v154;
      v156 = *(v146 - 1);
      *(v147 - 2) = v155;
      *(v147 - 1) = v156;
      --v148;
    }
    while ( v148 );
    v157 = *(_QWORD *)(a1 + 16);
    *v147 = *v146;
    sub_1808BA7B0(v1145, v157, v75);
  }
  v158 = &v1146;
  v159 = 8;
  do
  {
    v158 += 16;
    v160 = *a3;
    v161 = a3[1];
    a3 += 8;
    *((_OWORD *)v158 - 8) = v160;
    v162 = *(a3 - 6);
    *((_OWORD *)v158 - 7) = v161;
    v163 = *(a3 - 5);
    *((_OWORD *)v158 - 6) = v162;
    v164 = *(a3 - 4);
    *((_OWORD *)v158 - 5) = v163;
    v165 = *(a3 - 3);
    *((_OWORD *)v158 - 4) = v164;
    v166 = *(a3 - 2);
    *((_OWORD *)v158 - 3) = v165;
    v167 = *(a3 - 1);
    *((_OWORD *)v158 - 2) = v166;
    *((_OWORD *)v158 - 1) = v167;
    --v159;
  }
  while ( v159 );
  v168 = v1188;
  v169 = v1145;
  v170 = 8;
  *(_OWORD *)v158 = *a3;
  v171 = v168;
  do
  {
    v169 += 8;
    v172 = *v171;
    v173 = v171[1];
    v171 += 8;
    *(v169 - 8) = v172;
    v174 = *(v171 - 6);
    *(v169 - 7) = v173;
    v175 = *(v171 - 5);
    *(v169 - 6) = v174;
    v176 = *(v171 - 4);
    *(v169 - 5) = v175;
    v177 = *(v171 - 3);
    *(v169 - 4) = v176;
    v178 = *(v171 - 2);
    *(v169 - 3) = v177;
    v179 = *(v171 - 1);
    *(v169 - 2) = v178;
    *(v169 - 1) = v179;
    --v170;
  }
  while ( v170 );
  v180 = *v171;
  v181 = v1148;
  *v169 = v180;
  if ( v181 > 0 )
  {
    v182 = 0;
    v183 = (unsigned int)v181;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, _QWORD, _QWORD))unk_180001010)(
        *(_QWORD *)&v1147[v182 - 8],
        *(_QWORD *)((char *)v1145 + v182),
        *(_QWORD *)(*(_QWORD *)(a1 + 104) + 8LL),
        **(_QWORD **)(a1 + 112));
      v182 += 8;
      --v183;
    }
    while ( v183 );
  }
  v184 = *(_QWORD *)(a1 + 64);
  v185 = *(_QWORD *)(a1 + 72);
  LODWORD(v1192) = *(_DWORD *)(v75 + 24);
  sub_180619D90(v75, v1143, v185, v184);
  v186 = v1165;
  v187 = 8;
  v188 = (__int128 *)v1143;
  do
  {
    v186 += 8;
    v189 = *v188;
    v190 = v188[1];
    v188 += 8;
    *(v186 - 8) = v189;
    v191 = *(v188 - 6);
    *(v186 - 7) = v190;
    v192 = *(v188 - 5);
    *(v186 - 6) = v191;
    v193 = *(v188 - 4);
    *(v186 - 5) = v192;
    v194 = *(v188 - 3);
    *(v186 - 4) = v193;
    v195 = *(v188 - 2);
    *(v186 - 3) = v194;
    v196 = *(v188 - 1);
    *(v186 - 2) = v195;
    *(v186 - 1) = v196;
    --v187;
  }
  while ( v187 );
  v197 = (unsigned int)v1144;
  *v186 = *v188;
  if ( (int)v197 > 0 )
  {
    v198 = HIDWORD(v1144);
    v199 = v1165;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD))unk_1800010D0)(*(_QWORD *)v199, v198);
      v199 = (__int128 *)((char *)v199 + 8);
      --v197;
    }
    while ( v197 );
    v197 = (unsigned int)v1144;
  }
  v200 = (__int128 *)sub_1808B8DD0(v168, v1164, *(_QWORD *)(a1 + 64));
  v201 = v1145;
  v202 = 8;
  do
  {
    v201 += 8;
    v203 = *v200;
    v204 = v200[1];
    v200 += 8;
    *(v201 - 8) = v203;
    v205 = *(v200 - 6);
    *(v201 - 7) = v204;
    v206 = *(v200 - 5);
    *(v201 - 6) = v205;
    v207 = *(v200 - 4);
    *(v201 - 5) = v206;
    v208 = *(v200 - 3);
    *(v201 - 4) = v207;
    v209 = *(v200 - 2);
    *(v201 - 3) = v208;
    v210 = *(v200 - 1);
    *(v201 - 2) = v209;
    *(v201 - 1) = v210;
    --v202;
  }
  while ( v202 );
  v211 = *v200;
  v212 = v1165;
  v213 = 8;
  *v201 = v211;
  v214 = (float *)v1143;
  do
  {
    v212 += 8;
    v215 = *(_OWORD *)v214;
    v216 = *((_OWORD *)v214 + 1);
    v214 += 32;
    *(v212 - 8) = v215;
    v217 = *((_OWORD *)v214 - 6);
    *(v212 - 7) = v216;
    v218 = *((_OWORD *)v214 - 5);
    *(v212 - 6) = v217;
    v219 = *((_OWORD *)v214 - 4);
    *(v212 - 5) = v218;
    v220 = *((_OWORD *)v214 - 3);
    *(v212 - 4) = v219;
    v221 = *((_OWORD *)v214 - 2);
    *(v212 - 3) = v220;
    v222 = *((_OWORD *)v214 - 1);
    *(v212 - 2) = v221;
    *(v212 - 1) = v222;
    --v213;
  }
  while ( v213 );
  *v212 = *(_OWORD *)v214;
  if ( (int)v197 > 0 )
  {
    v223 = HIDWORD(v1144);
    v224 = 0;
    do
    {
      sub_1806167E0(*(_QWORD *)((char *)v1165 + v224), *(_QWORD *)((char *)v1145 + v224), v223);
      v224 += 8;
      --v197;
    }
    while ( v197 );
  }
  if ( v1185 )
  {
    sub_1808BFCB0(a1, v1143);
    sub_1808BFD30(a1, (__int64)v1143);
  }
  v225 = 0;
  if ( *(_QWORD *)(a1 + 72) )
  {
    v226 = (float **)v1143;
    do
    {
      v227 = *v226;
      v228 = 1;
      v229 = 0.0;
      v230 = *(_QWORD *)(a1 + 64) >> 2;
      v231 = 1;
      v232 = **v226;
      if ( (int)v230 > 1 )
      {
        if ( (int)v230 - 1 >= 4 )
        {
          v214 = v227 + 3;
          v233 = ((unsigned int)(v230 - 5) >> 2) + 1;
          v234 = v233;
          v228 = 4 * v233 + 1;
          v231 = 4LL * v233 + 1;
          do
          {
            v235 = *(v214 - 2);
            v236 = fabs(v235 - v232);
            v237 = v232;
            v238 = *(v214 - 1);
            v239 = v236 / (v237 + 0.0000001) + v229;
            v240 = fabs(v238 - v235);
            v241 = v235;
            v242 = *v214;
            v243 = v240 / (v241 + 0.0000001) + v239;
            v244 = fabs(*v214 - v238);
            v245 = v238;
            v232 = v214[1];
            v214 += 4;
            v246 = v244 / (v245 + 0.0000001) + v243;
            v229 = fabs(v232 - v242) / (v242 + 0.0000001) + v246;
            --v234;
          }
          while ( v234 );
        }
        if ( v228 < (int)v230 )
        {
          v214 = &v227[v231];
          v247 = (unsigned int)(v230 - v228);
          do
          {
            v248 = *v214;
            v249 = *v214++;
            v250 = fabs(v249 - v232);
            v251 = v232;
            v232 = v248;
            v229 = v250 / (v251 + 0.0000001) + v229;
            --v247;
          }
          while ( v247 );
        }
      }
      if ( (float)(v229 / (float)(int)v230) < 0.001 )
        ((void (__fastcall *)(float *, float *, _QWORD))unk_180001220)(v214, *v226, HIDWORD(v1144));
      ++v225;
      ++v226;
    }
    while ( (unsigned __int64)v225 < *(_QWORD *)(a1 + 72) );
  }
  v252 = v1193;
  if ( (_BYTE)v1193 )
  {
    v253 = v1145;
    v254 = 8;
    v255 = (__int128 *)v1143;
    do
    {
      v253 += 8;
      v256 = *v255;
      v257 = v255[1];
      v255 += 8;
      *(v253 - 8) = v256;
      v258 = *(v255 - 6);
      *(v253 - 7) = v257;
      v259 = *(v255 - 5);
      *(v253 - 6) = v258;
      v260 = *(v255 - 4);
      *(v253 - 5) = v259;
      v261 = *(v255 - 3);
      *(v253 - 4) = v260;
      v262 = *(v255 - 2);
      *(v253 - 3) = v261;
      v263 = *(v255 - 1);
      *(v253 - 2) = v262;
      *(v253 - 1) = v263;
      --v254;
    }
    while ( v254 );
    *v253 = *v255;
    sub_18086E780(v1145);
    ((void (*)(void))unk_181C9AA01)();
    v264 = v1165;
    v265 = (__int128 *)v1143;
    v266 = 8;
    do
    {
      v264 += 8;
      v267 = *v265;
      v268 = v265[3];
      v269 = v265[1];
      v265 += 8;
      *(v264 - 8) = v267;
      v270 = *(v265 - 6);
      *(v264 - 7) = v269;
      *(v264 - 6) = v270;
      v271 = *(v265 - 4);
      *(v264 - 5) = v268;
      v272 = *(v265 - 3);
      *(v264 - 4) = v271;
      v273 = *(v265 - 2);
      *(v264 - 3) = v272;
      v274 = *(v265 - 1);
      *(v264 - 2) = v273;
      *(v264 - 1) = v274;
      --v266;
    }
    while ( v266 );
    v275 = *v265;
    v276 = (__int128 *)v1143;
    v277 = 8;
    *v264 = v275;
    v278 = v1145;
    do
    {
      v278 += 8;
      v279 = *v276;
      v280 = v276[1];
      v276 += 8;
      *(v278 - 8) = v279;
      v281 = *(v276 - 6);
      *(v278 - 7) = v280;
      v282 = *(v276 - 5);
      *(v278 - 6) = v281;
      v283 = *(v276 - 4);
      *(v278 - 5) = v282;
      v284 = *(v276 - 3);
      *(v278 - 4) = v283;
      v285 = *(v276 - 2);
      *(v278 - 3) = v284;
      v286 = *(v276 - 1);
      *(v278 - 2) = v285;
      *(v278 - 1) = v286;
      --v277;
    }
    while ( v277 );
    *v278 = *v276;
    if ( (int)v1144 > 0 )
    {
      v287 = HIDWORD(v1144);
      v288 = 0;
      v289 = (unsigned int)v1144;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001250)(
          *(_QWORD *)((char *)v1165 + v288),
          *(_QWORD *)((char *)v1145 + v288),
          v287);
        v288 += 8;
        --v289;
      }
      while ( v289 );
    }
  }
  else
  {
    v290 = *(_DWORD *)(a1 + 840);
    v1137.m128i_i32[1] = *(_DWORD *)(a1 + 848);
    v291 = 0;
    memset(v1136, 0, sizeof(v1136));
    v1137.m128i_i32[0] = v290;
    v1137.m128i_i64[1] = 4LL * v1137.m128i_i32[1];
    if ( v290 > 0 )
    {
      v292 = v1136;
      do
      {
        ++v291;
        *v292 = *(_QWORD *)((char *)v292 + a1 + 712 - (_QWORD)v1136);
        ++v292;
      }
      while ( v291 < v1137.m128i_i32[0] );
    }
    v293 = v1145;
    v294 = 8;
    v295 = (__int128 *)v1143;
    v1134[0] = v1136[0];
    v1134[1] = v1136[1];
    v1134[2] = v1136[2];
    v1134[3] = v1136[3];
    v1134[4] = v1136[4];
    v1134[5] = v1136[5];
    v1134[6] = v1136[6];
    v1134[7] = v1136[7];
    v1135 = v1137;
    do
    {
      v293 += 8;
      v296 = *v295;
      v297 = v295[1];
      v295 += 8;
      *(v293 - 8) = v296;
      v298 = *(v295 - 6);
      *(v293 - 7) = v297;
      v299 = *(v295 - 5);
      *(v293 - 6) = v298;
      v300 = *(v295 - 4);
      *(v293 - 5) = v299;
      v301 = *(v295 - 3);
      *(v293 - 4) = v300;
      v302 = *(v295 - 2);
      *(v293 - 3) = v301;
      v303 = *(v295 - 1);
      *(v293 - 2) = v302;
      *(v293 - 1) = v303;
      --v294;
    }
    while ( v294 );
    *v293 = *v295;
    sub_1808C0230((__int64)v1145, (__int64 *)v1134);
    v304 = 0;
    if ( *(_QWORD *)(a1 + 72) )
    {
      ((void (*)(void))unk_181C9AA01)();
      v305 = (__int64 *)v1143;
      do
      {
        v306 = *v305;
        LODWORD(v1188) = 0;
        ((void (__fastcall *)(__int64, _DWORD *, __int64, __int128 **))unk_180001400)(
          v306,
          &dword_182014360[101576],
          32,
          (__int128 **)va);
        v307 = v1145;
        v308 = (__int128 *)v1143;
        v309 = 8;
        do
        {
          v307 += 8;
          v310 = *v308;
          v311 = v308[1];
          v308 += 8;
          *(v307 - 8) = v310;
          v312 = *(v308 - 6);
          *(v307 - 7) = v311;
          v313 = *(v308 - 5);
          *(v307 - 6) = v312;
          v314 = *(v308 - 4);
          *(v307 - 5) = v313;
          v315 = *(v308 - 3);
          *(v307 - 4) = v314;
          v316 = *(v308 - 2);
          *(v307 - 3) = v315;
          v317 = *(v308 - 1);
          *(v307 - 2) = v316;
          *(v307 - 1) = v317;
          --v309;
        }
        while ( v309 );
        v318 = v1144;
        *v307 = *v308;
        if ( v318 > 0 )
        {
          v319 = HIDWORD(v1144);
          v320 = v1145;
          v321 = (unsigned int)v318;
          do
          {
            ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001160)(v308, *(_QWORD *)v320, v319);
            v320 = (__int128 *)((char *)v320 + 8);
            --v321;
          }
          while ( v321 );
          v318 = v1144;
        }
        ++v304;
        ++v305;
      }
      while ( (unsigned __int64)v304 < *(_QWORD *)(a1 + 72) );
      v75 = v1195;
    }
    else
    {
      v318 = v1144;
    }
    v322 = v1145;
    v323 = 8;
    v324 = (__int128 *)v1143;
    do
    {
      v322 += 8;
      v325 = *v324;
      v326 = v324[1];
      v324 += 8;
      *(v322 - 8) = v325;
      v327 = *(v324 - 6);
      *(v322 - 7) = v326;
      v328 = *(v324 - 5);
      *(v322 - 6) = v327;
      v329 = *(v324 - 4);
      *(v322 - 5) = v328;
      v330 = *(v324 - 3);
      *(v322 - 4) = v329;
      v331 = *(v324 - 2);
      *(v322 - 3) = v330;
      v332 = *(v324 - 1);
      *(v322 - 2) = v331;
      *(v322 - 1) = v332;
      --v323;
    }
    while ( v323 );
    *v322 = *v324;
    if ( v318 > 0 )
    {
      v333 = HIDWORD(v1144);
      v334 = v1145;
      v335 = (unsigned int)v318;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*(_QWORD *)v334, v333, v323, 0);
        v334 = (__int128 *)((char *)v334 + 8);
        --v335;
      }
      while ( v335 );
    }
    v252 = v1193;
  }
  v336 = *(_DWORD *)(a1 + 3288);
  v1137.m128i_i32[1] = *(_DWORD *)(a1 + 3296);
  v337 = 0;
  memset(v1136, 0, sizeof(v1136));
  v1137.m128i_i32[0] = v336;
  v1137.m128i_i64[1] = 4LL * v1137.m128i_i32[1];
  if ( v336 > 0 )
  {
    v338 = v1136;
    do
    {
      ++v337;
      *v338 = *(_QWORD *)((char *)v338 + a1 + 3160 - (_QWORD)v1136);
      ++v338;
    }
    while ( v337 < v1137.m128i_i32[0] );
  }
  v339 = *(_DWORD *)(a1 + 3144);
  v1139.m128i_i32[1] = *(_DWORD *)(a1 + 3152);
  v340 = 0;
  memset(v1138, 0, sizeof(v1138));
  v1139.m128i_i32[0] = v339;
  v1139.m128i_i64[1] = 4LL * v1139.m128i_i32[1];
  if ( v339 > 0 )
  {
    v341 = v1138;
    do
    {
      ++v340;
      *v341 = *(_QWORD *)((char *)v341 + a1 + 3016 - (_QWORD)v1138);
      ++v341;
    }
    while ( v340 < v1139.m128i_i32[0] );
  }
  v342 = *(_DWORD *)(a1 + 2712);
  v1135.m128i_i32[1] = *(_DWORD *)(a1 + 2720);
  v343 = 0;
  memset(v1134, 0, sizeof(v1134));
  v1135.m128i_i32[0] = v342;
  v1135.m128i_i64[1] = 4LL * v1135.m128i_i32[1];
  if ( v342 > 0 )
  {
    v344 = v1134;
    do
    {
      ++v343;
      *v344 = *(_QWORD *)((char *)v344 + a1 + 2584 - (_QWORD)v1134);
      ++v344;
    }
    while ( v343 < v1135.m128i_i32[0] );
  }
  v345 = v1145;
  v346 = 8;
  v347 = (__int128 *)v1143;
  v1151[0] = (__m128i)v1136[0];
  v1151[1] = (__m128i)v1136[1];
  v1151[2] = (__m128i)v1136[2];
  v1151[3] = (__m128i)v1136[3];
  v1151[4] = (__m128i)v1136[4];
  v1151[5] = (__m128i)v1136[5];
  v1151[6] = (__m128i)v1136[6];
  v1151[7] = (__m128i)v1136[7];
  v1151[8] = v1137;
  v1154 = (__m128i)v1138[0];
  v1155 = v1138[1];
  v1156 = v1138[2];
  v1157 = v1138[3];
  v1158 = v1138[4];
  v1159 = v1138[5];
  v1160 = v1138[6];
  v1161 = v1138[7];
  v1162 = v1139;
  do
  {
    v345 += 8;
    v348 = *v347;
    v349 = v347[1];
    v347 += 8;
    *(v345 - 8) = v348;
    v350 = *(v347 - 6);
    *(v345 - 7) = v349;
    v351 = *(v347 - 5);
    *(v345 - 6) = v350;
    v352 = *(v347 - 4);
    *(v345 - 5) = v351;
    v353 = *(v347 - 3);
    *(v345 - 4) = v352;
    v354 = *(v347 - 2);
    *(v345 - 3) = v353;
    v355 = *(v347 - 1);
    *(v345 - 2) = v354;
    *(v345 - 1) = v355;
    --v346;
  }
  while ( v346 );
  v356 = (__m128i)v1134[0];
  *v345 = *v347;
  v1120 = v356;
  v1121 = v1134[1];
  v1122 = v1134[2];
  v1123 = v1134[3];
  v1124 = v1134[4];
  v1125 = v1134[5];
  v1126 = v1134[6];
  v1127 = v1134[7];
  v1128 = v1135;
  sub_1808C02F0(&v1120, v1145, &v1154, v1151, v75);
  v357 = *(_DWORD *)(a1 + 2712);
  v1135.m128i_i32[1] = *(_DWORD *)(a1 + 2720);
  v358 = 0;
  memset(v1134, 0, sizeof(v1134));
  v1135.m128i_i32[0] = v357;
  v1135.m128i_i64[1] = 4LL * v1135.m128i_i32[1];
  if ( v357 > 0 )
  {
    v359 = v1134;
    do
    {
      ++v358;
      *v359 = *(_QWORD *)((char *)v359 + a1 + 2584 - (_QWORD)v1134);
      ++v359;
    }
    while ( v358 < v1135.m128i_i32[0] );
  }
  v360 = v1145;
  v361 = 8;
  v362 = (__int128 *)v1143;
  v1120 = (__m128i)v1134[0];
  v1121 = v1134[1];
  v1122 = v1134[2];
  v1123 = v1134[3];
  v1124 = v1134[4];
  v1125 = v1134[5];
  v1126 = v1134[6];
  v1127 = v1134[7];
  v1128 = v1135;
  do
  {
    v360 += 8;
    v363 = *v362;
    v364 = v362[1];
    v362 += 8;
    *(v360 - 8) = v363;
    v365 = *(v362 - 6);
    *(v360 - 7) = v364;
    v366 = *(v362 - 5);
    *(v360 - 6) = v365;
    v367 = *(v362 - 4);
    *(v360 - 5) = v366;
    v368 = *(v362 - 3);
    *(v360 - 4) = v367;
    v369 = *(v362 - 2);
    *(v360 - 3) = v368;
    v370 = *(v362 - 1);
    *(v360 - 2) = v369;
    *(v360 - 1) = v370;
    --v361;
  }
  while ( v361 );
  *v360 = *v362;
  sub_1808C0B10((__int64)v1145, v1120.m128i_i64);
  if ( !*(_BYTE *)(*(_QWORD *)(a1 + 11320) + 83LL) )
    goto LABEL_140;
  v371 = v1145;
  v372 = 8;
  v373 = (__int128 *)v1143;
  do
  {
    v371 += 8;
    v374 = *v373;
    v375 = v373[1];
    v373 += 8;
    *(v371 - 8) = v374;
    v376 = *(v373 - 6);
    *(v371 - 7) = v375;
    v377 = *(v373 - 5);
    *(v371 - 6) = v376;
    v378 = *(v373 - 4);
    *(v371 - 5) = v377;
    v379 = *(v373 - 3);
    *(v371 - 4) = v378;
    v380 = *(v373 - 2);
    *(v371 - 3) = v379;
    v381 = *(v373 - 1);
    *(v371 - 2) = v380;
    *(v371 - 1) = v381;
    --v372;
  }
  while ( v372 );
  v382 = (unsigned int)v1144;
  *v371 = *v373;
  if ( (int)v382 > 0 )
  {
    v383 = HIDWORD(v1144);
    v384 = v1145;
    do
    {
      ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v373, *(_QWORD *)v384, v383);
      v384 = (__int128 *)((char *)v384 + 8);
      --v382;
    }
    while ( v382 );
LABEL_140:
    v382 = (unsigned int)v1144;
  }
  if ( v252 )
  {
    va_copy(v385, va1);
    LODWORD(v1193) = 0;
    *(float *)&v1188 = (float)(v1130 - 0.80000001) * 5.0000005;
    if ( *(float *)&v1188 >= 0.0 )
      va_copy(v385, va);
    ((void (__fastcall *)(va_list))unk_181C9A9D7)(v385);
    ((void (*)(void))unk_181C9AA01)();
    ((void (*)(void))unk_181C9A9FB)();
    ((void (*)(void))unk_181C9A9D7)();
    ((float (*)(void))unk_181C9AA01)();
    v386 = v1145;
    v387 = (__int128 *)v1143;
    v388 = 8;
    do
    {
      v386 += 8;
      v389 = *v387;
      v390 = v387[1];
      v387 += 8;
      *(v386 - 8) = v389;
      v391 = *(v387 - 6);
      *(v386 - 7) = v390;
      v392 = *(v387 - 5);
      *(v386 - 6) = v391;
      v393 = *(v387 - 4);
      *(v386 - 5) = v392;
      v394 = *(v387 - 3);
      *(v386 - 4) = v393;
      v395 = *(v387 - 2);
      *(v386 - 3) = v394;
      v396 = *(v387 - 1);
      *(v386 - 2) = v395;
      *(v386 - 1) = v396;
      --v388;
    }
    while ( v388 );
    *v386 = *v387;
    if ( (int)v382 > 0 )
    {
      v397 = HIDWORD(v1144);
      v398 = v1145;
      do
      {
        ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v387, *(_QWORD *)v398, v397);
        v398 = (__int128 *)((char *)v398 + 8);
        --v382;
      }
      while ( v382 );
      v382 = (unsigned int)v1144;
    }
    if ( *(_QWORD *)(a1 + 72) )
    {
      v399 = v1195;
      v400 = v1143;
      v401 = 0;
      do
      {
        v402 = *(_DWORD *)(v399 + 24);
        v403 = 176 * v401;
        v404 = *(_QWORD *)v399 + 4LL * v402;
        v405 = *(_QWORD *)(a1 + 64) + v402 - (((unsigned __int8)*(_QWORD *)(a1 + 64) + (_BYTE)v402) & 0xF) + 16;
        if ( (((unsigned __int8)*(_QWORD *)(a1 + 64) + (_BYTE)v402) & 0xF) == 0 )
          v405 = *(_QWORD *)(a1 + 64) + v402;
        v406 = *v400;
        *(_DWORD *)(v399 + 24) = v405;
        sub_180860DA0(176 * v401 + a1 + 5560, v404, v406);
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_1800013A0)(v404, *v400, HIDWORD(v1144));
        v407 = *(_DWORD *)(v1195 + 24);
        v408 = *(_QWORD *)v1195 + 4LL * v407;
        v409 = *(_QWORD *)(a1 + 64) + v407 - (((unsigned __int8)*(_QWORD *)(a1 + 64) + (_BYTE)v407) & 0xF) + 16;
        if ( (((unsigned __int8)*(_QWORD *)(a1 + 64) + (_BYTE)v407) & 0xF) == 0 )
          v409 = *(_QWORD *)(a1 + 64) + v407;
        v410 = *v400;
        *(_DWORD *)(v1195 + 24) = v409;
        sub_180860DA0(v403 + a1 + 8376, v408, v410);
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_1800010A0)(v408, *v400, HIDWORD(v1144));
        ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*v400, HIDWORD(v1144), v411, 0);
        v399 = v1195;
        ++v400;
        LODWORD(v35) = v35 + 1;
        v401 = (int)v35;
        *(_DWORD *)(v1195 + 24) = v402;
      }
      while ( (unsigned __int64)(int)v35 < *(_QWORD *)(a1 + 72) );
      v382 = (unsigned int)v1144;
      v35 = 0;
      v75 = v399;
    }
    v412 = *(_DWORD *)(a1 + 984);
    v1137.m128i_i32[1] = *(_DWORD *)(a1 + 992);
    v413 = 0;
    memset(v1136, 0, sizeof(v1136));
    v414 = 0;
    v1137.m128i_i32[0] = v412;
    v1137.m128i_i64[1] = 4LL * v1137.m128i_i32[1];
    if ( v412 > 0 )
    {
      v415 = v1136;
      do
      {
        ++v414;
        *v415 = *(_QWORD *)((char *)v415 + a1 + 856 - (_QWORD)v1136);
        ++v415;
        v412 = v1137.m128i_i32[0];
      }
      while ( v414 < v1137.m128i_i32[0] );
      v413 = *(_QWORD *)&v1136[0];
    }
    v416 = &v1146;
    v417 = (__int128 *)v1143;
    v418 = 8;
    v1120 = (__m128i)v1136[0];
    v1121 = v1136[1];
    v1122 = v1136[2];
    v1123 = v1136[3];
    v1124 = v1136[4];
    v1125 = v1136[5];
    v1126 = v1136[6];
    v1127 = v1136[7];
    v1128 = v1137;
    do
    {
      v416 += 16;
      v419 = *v417;
      v420 = v417[1];
      v417 += 8;
      *((_OWORD *)v416 - 8) = v419;
      v421 = *(v417 - 6);
      *((_OWORD *)v416 - 7) = v420;
      v422 = *(v417 - 5);
      *((_OWORD *)v416 - 6) = v421;
      v423 = *(v417 - 4);
      *((_OWORD *)v416 - 5) = v422;
      v424 = *(v417 - 3);
      *((_OWORD *)v416 - 4) = v423;
      v425 = *(v417 - 2);
      *((_OWORD *)v416 - 3) = v424;
      v426 = *(v417 - 1);
      *((_OWORD *)v416 - 2) = v425;
      *((_OWORD *)v416 - 1) = v426;
      --v418;
    }
    while ( v418 );
    *(_OWORD *)v416 = *v417;
    if ( (_DWORD)v382 == v412 )
    {
      if ( (int)v382 > 0 )
      {
        v427 = HIDWORD(v1144);
        v428 = 0;
        do
        {
          ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(
            v1120.m128i_i64[v428],
            *(_QWORD *)&v1147[v428 * 8 - 8],
            v427);
          ++v428;
          --v382;
        }
        while ( v382 );
      }
    }
    else if ( v412 == 1 && (int)v382 > 0 )
    {
      v429 = HIDWORD(v1144);
      v430 = &v1146;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v413, *v430++, v429);
        --v382;
      }
      while ( v382 );
    }
    v431 = v1145;
    v432 = 8;
    v433 = (__int128 *)v1143;
    do
    {
      v431 += 8;
      v434 = *v433;
      v435 = v433[1];
      v433 += 8;
      *(v431 - 8) = v434;
      v436 = *(v433 - 6);
      *(v431 - 7) = v435;
      v437 = *(v433 - 5);
      *(v431 - 6) = v436;
      v438 = *(v433 - 4);
      *(v431 - 5) = v437;
      v439 = *(v433 - 3);
      *(v431 - 4) = v438;
      v440 = *(v433 - 2);
      *(v431 - 3) = v439;
      v441 = *(v433 - 1);
      *(v431 - 2) = v440;
      *(v431 - 1) = v441;
      --v432;
    }
    while ( v432 );
    v442 = *(__int64 **)(a1 + 16);
    *v431 = *v433;
    sub_1808C0BD0((__int64)v1145, 0, v442, v75);
    sub_1808C1440(a1, (__int64)v1143, (__int64 *)v75);
    v443 = *(_DWORD *)(a1 + 2424);
    v1137.m128i_i32[1] = *(_DWORD *)(a1 + 2432);
    v444 = 0;
    memset(v1136, 0, sizeof(v1136));
    v445 = 0;
    v1137.m128i_i32[0] = v443;
    v1137.m128i_i64[1] = 4LL * v1137.m128i_i32[1];
    if ( v443 > 0 )
    {
      v446 = v1136;
      do
      {
        ++v445;
        *v446 = *(_QWORD *)((char *)v446 + a1 + 2296 - (_QWORD)v1136);
        ++v446;
        v443 = v1137.m128i_i32[0];
      }
      while ( v445 < v1137.m128i_i32[0] );
      v444 = *(_QWORD *)&v1136[0];
    }
    v447 = &v1146;
    v448 = 8;
    v449 = (__int128 *)v1143;
    v1120 = (__m128i)v1136[0];
    v1121 = v1136[1];
    v1122 = v1136[2];
    v1123 = v1136[3];
    v1124 = v1136[4];
    v1125 = v1136[5];
    v1126 = v1136[6];
    v1127 = v1136[7];
    v1128 = v1137;
    do
    {
      v447 += 16;
      v450 = *v449;
      v451 = v449[1];
      v449 += 8;
      *((_OWORD *)v447 - 8) = v450;
      v452 = *(v449 - 6);
      *((_OWORD *)v447 - 7) = v451;
      v453 = *(v449 - 5);
      *((_OWORD *)v447 - 6) = v452;
      v454 = *(v449 - 4);
      *((_OWORD *)v447 - 5) = v453;
      v455 = *(v449 - 3);
      *((_OWORD *)v447 - 4) = v454;
      v456 = *(v449 - 2);
      *((_OWORD *)v447 - 3) = v455;
      v457 = *(v449 - 1);
      *((_OWORD *)v447 - 2) = v456;
      *((_OWORD *)v447 - 1) = v457;
      --v448;
    }
    while ( v448 );
    v458 = (unsigned int)v1144;
    *(_OWORD *)v447 = *v449;
    if ( (_DWORD)v458 == v443 )
    {
      if ( (int)v458 <= 0 )
        goto LABEL_191;
      v459 = HIDWORD(v1144);
      v460 = 0;
      v461 = (unsigned int)v458;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(
          v1120.m128i_i64[v460],
          *(_QWORD *)&v1147[v460 * 8 - 8],
          v459);
        ++v460;
        --v461;
      }
      while ( v461 );
    }
    else
    {
      if ( v443 != 1 || (int)v458 <= 0 )
        goto LABEL_191;
      v462 = HIDWORD(v1144);
      v463 = &v1146;
      v464 = v458;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v444, *v463++, v462);
        --v464;
      }
      while ( v464 );
    }
    LODWORD(v458) = v1144;
LABEL_191:
    v465 = v1165;
    v466 = 8;
    v467 = (__int128 *)v1143;
    do
    {
      v465 += 8;
      v468 = *v467;
      v469 = v467[1];
      v467 += 8;
      *(v465 - 8) = v468;
      v470 = *(v467 - 6);
      *(v465 - 7) = v469;
      v471 = *(v467 - 5);
      *(v465 - 6) = v470;
      v472 = *(v467 - 4);
      *(v465 - 5) = v471;
      v473 = *(v467 - 3);
      *(v465 - 4) = v472;
      v474 = *(v467 - 2);
      *(v465 - 3) = v473;
      v475 = *(v467 - 1);
      *(v465 - 2) = v474;
      *(v465 - 1) = v475;
      --v466;
    }
    while ( v466 );
    v476 = *v467;
    v477 = (__int128 *)v1143;
    v478 = 8;
    *v465 = v476;
    v479 = v1145;
    do
    {
      v479 += 8;
      v480 = *v477;
      v481 = v477[1];
      v477 += 8;
      *(v479 - 8) = v480;
      v482 = *(v477 - 6);
      *(v479 - 7) = v481;
      v483 = *(v477 - 5);
      *(v479 - 6) = v482;
      v484 = *(v477 - 4);
      *(v479 - 5) = v483;
      v485 = *(v477 - 3);
      *(v479 - 4) = v484;
      v486 = *(v477 - 2);
      *(v479 - 3) = v485;
      v487 = *(v477 - 1);
      *(v479 - 2) = v486;
      *(v479 - 1) = v487;
      --v478;
    }
    while ( v478 );
    *v479 = *v477;
    if ( (int)v458 > 0 )
    {
      v488 = HIDWORD(v1144);
      v489 = 0;
      v490 = (unsigned int)v458;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001340)(
          *(_QWORD *)((char *)v1165 + v489),
          *(_QWORD *)((char *)v1145 + v489),
          v488);
        v489 += 8;
        --v490;
      }
      while ( v490 );
      LODWORD(v458) = v1144;
    }
    v491 = &v1146;
    v492 = 8;
    v493 = (__int128 *)v1143;
    do
    {
      v491 += 16;
      v494 = *v493;
      v495 = v493[1];
      v493 += 8;
      *((_OWORD *)v491 - 8) = v494;
      v496 = *(v493 - 6);
      *((_OWORD *)v491 - 7) = v495;
      v497 = *(v493 - 5);
      *((_OWORD *)v491 - 6) = v496;
      v498 = *(v493 - 4);
      *((_OWORD *)v491 - 5) = v497;
      v499 = *(v493 - 3);
      *((_OWORD *)v491 - 4) = v498;
      v500 = *(v493 - 2);
      *((_OWORD *)v491 - 3) = v499;
      v501 = *(v493 - 1);
      *((_OWORD *)v491 - 2) = v500;
      *((_OWORD *)v491 - 1) = v501;
      --v492;
    }
    while ( v492 );
    *(_OWORD *)v491 = *v493;
    if ( (int)v458 > 0 )
    {
      v502 = HIDWORD(v1144);
      v503 = &v1146;
      v504 = (unsigned int)v458;
      do
      {
        ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_1800012E0)(v493, *v503++, v502);
        --v504;
      }
      while ( v504 );
    }
    v505 = a2;
    v506 = (__int128 *)sub_1808AE6F0(a2, v1164, *(_QWORD *)(a1 + 64));
    v507 = (__int128 *)v1143;
    v508 = v1145;
    v509 = 8;
    do
    {
      v508 += 8;
      v510 = *v507;
      v511 = v507[1];
      v507 += 8;
      *(v508 - 8) = v510;
      v512 = *(v507 - 6);
      *(v508 - 7) = v511;
      v513 = *(v507 - 5);
      *(v508 - 6) = v512;
      v514 = *(v507 - 4);
      *(v508 - 5) = v513;
      v515 = *(v507 - 3);
      *(v508 - 4) = v514;
      v516 = *(v507 - 2);
      *(v508 - 3) = v515;
      v517 = *(v507 - 1);
      *(v508 - 2) = v516;
      *(v508 - 1) = v517;
      --v509;
    }
    while ( v509 );
    v518 = *v507;
    v519 = 8;
    *v508 = v518;
    v520 = &v1146;
    do
    {
      v520 += 16;
      v521 = *v506;
      v522 = v506[1];
      v506 += 8;
      *((_OWORD *)v520 - 8) = v521;
      v523 = *(v506 - 6);
      *((_OWORD *)v520 - 7) = v522;
      v524 = *(v506 - 5);
      *((_OWORD *)v520 - 6) = v523;
      v525 = *(v506 - 4);
      *((_OWORD *)v520 - 5) = v524;
      v526 = *(v506 - 3);
      *((_OWORD *)v520 - 4) = v525;
      v527 = *(v506 - 2);
      *((_OWORD *)v520 - 3) = v526;
      v528 = *(v506 - 1);
      *((_OWORD *)v520 - 2) = v527;
      *((_OWORD *)v520 - 1) = v528;
      --v519;
    }
    while ( v519 );
    *(_OWORD *)v520 = *v506;
    if ( v1148 > 0 )
    {
      v529 = v1149;
      v530 = 0;
      v531 = (unsigned int)v1148;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_1801C8500)(
          *(_QWORD *)((char *)v1145 + v530),
          *(_QWORD *)&v1147[v530 - 8],
          v529);
        v530 += 8;
        --v531;
      }
      while ( v531 );
    }
    ((void (*)(void))unk_181C9AA01)();
    v532 = (__int128 *)sub_1808AE6F0(a2, v1164, *(_QWORD *)(a1 + 64));
    v533 = &v1146;
    v534 = 8;
    do
    {
      v533 += 16;
      v535 = *v532;
      v536 = v532[1];
      v532 += 8;
      *((_OWORD *)v533 - 8) = v535;
      v537 = *(v532 - 6);
      *((_OWORD *)v533 - 7) = v536;
      v538 = *(v532 - 5);
      *((_OWORD *)v533 - 6) = v537;
      v539 = *(v532 - 4);
      *((_OWORD *)v533 - 5) = v538;
      v540 = *(v532 - 3);
      *((_OWORD *)v533 - 4) = v539;
      v541 = *(v532 - 2);
      *((_OWORD *)v533 - 3) = v540;
      v542 = *(v532 - 1);
      *((_OWORD *)v533 - 2) = v541;
      *((_OWORD *)v533 - 1) = v542;
      --v534;
    }
    while ( v534 );
    *(_OWORD *)v533 = *v532;
    if ( v1148 > 0 )
    {
      v543 = &v1146;
      v544 = (unsigned int)v1148;
      v545 = v1149;
      do
      {
        ((void (__fastcall *)(__int64 *, _QWORD, _QWORD))unk_180001220)(v533, *v543++, v545);
        --v544;
      }
      while ( v544 );
    }
    goto LABEL_440;
  }
  LODWORD(v1131) = *(_DWORD *)(v75 + 24);
  v1175 = 0;
  ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)(v1176, 0, 1016);
  v1177 = *(_DWORD *)(a1 + 72);
  v1178 = 16;
  v1179 = 64;
  sub_18061A9A0(v75, &v1175);
  v546 = v1145;
  v547 = 8;
  v548 = (__int128 *)v1143;
  do
  {
    v546 += 8;
    v549 = *v548;
    v550 = v548[1];
    v548 += 8;
    *(v546 - 8) = v549;
    v551 = *(v548 - 6);
    *(v546 - 7) = v550;
    v552 = *(v548 - 5);
    *(v546 - 6) = v551;
    v553 = *(v548 - 4);
    *(v546 - 5) = v552;
    v554 = *(v548 - 3);
    *(v546 - 4) = v553;
    v555 = *(v548 - 2);
    *(v546 - 3) = v554;
    v556 = *(v548 - 1);
    *(v546 - 2) = v555;
    *(v546 - 1) = v556;
    --v547;
  }
  while ( v547 );
  v557 = *v548;
  v558 = (__int128 *)&v1175;
  v559 = 8;
  *v546 = v557;
  v560 = v1165;
  do
  {
    v560 += 8;
    v561 = *v558;
    v562 = v558[1];
    v558 += 8;
    *(v560 - 8) = v561;
    v563 = *(v558 - 6);
    *(v560 - 7) = v562;
    v564 = *(v558 - 5);
    *(v560 - 6) = v563;
    v565 = *(v558 - 4);
    *(v560 - 5) = v564;
    v566 = *(v558 - 3);
    *(v560 - 4) = v565;
    v567 = *(v558 - 2);
    *(v560 - 3) = v566;
    v568 = *(v558 - 1);
    *(v560 - 2) = v567;
    *(v560 - 1) = v568;
    --v559;
  }
  while ( v559 );
  *v560 = *v558;
  sub_1808C32C0(a1 + 3880, v1165, v1145);
  v570 = 0;
  v571 = v1178;
  if ( *(_QWORD *)(a1 + 72) )
  {
    v572 = &v1175;
    do
    {
      v573 = *v572;
      v574 = *v572;
      LODWORD(v1193) = 0;
      ((void (__fastcall *)(_DWORD *, __int64, __int64, __int64 *))unk_180001400)(
        &dword_182014360[101672],
        v574,
        16,
        (__int64 *)va1);
      LODWORD(v1193) = 0;
      ((void (__fastcall *)(_DWORD *, __int64, __int64, __int64 *))unk_180001400)(
        &dword_182014360[101624],
        v573,
        16,
        (__int64 *)va1);
      ((void (__fastcall *)(_DWORD *, __int64, __int64, _QWORD))unk_1800011F0)(
        &dword_182014360[101608],
        v575,
        v573,
        (unsigned int)v571);
      ((void (__fastcall *)(_DWORD *, __int64, __int64, _QWORD))unk_1800011F0)(
        &dword_182014360[101688],
        v576,
        v573,
        (unsigned int)v571);
      ++v570;
      ++v572;
    }
    while ( (unsigned __int64)v570 < *(_QWORD *)(a1 + 72) );
  }
  LODWORD(v577) = v1177;
  if ( *(_BYTE *)(a1 + 88) )
  {
    ((void (*)(void))unk_181C9A5AD)();
    v578 = *(_DWORD *)(a1 + 3000);
    v1135.m128i_i32[1] = *(_DWORD *)(a1 + 3008);
    v579 = 0;
    memset(v1134, 0, sizeof(v1134));
    v1135.m128i_i32[0] = v578;
    v1135.m128i_i64[1] = 4LL * v1135.m128i_i32[1];
    if ( v578 > 0 )
    {
      v580 = v1134;
      do
      {
        ++v579;
        *v580 = *(_QWORD *)((char *)v580 + a1 + 2872 - (_QWORD)v1134);
        ++v580;
      }
      while ( v579 < v1135.m128i_i32[0] );
    }
    v581 = v1145;
    v582 = 8;
    v583 = (__int128 *)&v1175;
    do
    {
      v581 += 8;
      v584 = *v583;
      v585 = v583[1];
      v583 += 8;
      *(v581 - 8) = v584;
      v586 = *(v583 - 6);
      *(v581 - 7) = v585;
      v587 = *(v583 - 5);
      *(v581 - 6) = v586;
      v588 = *(v583 - 4);
      *(v581 - 5) = v587;
      v589 = *(v583 - 3);
      *(v581 - 4) = v588;
      v590 = *(v583 - 2);
      *(v581 - 3) = v589;
      v591 = *(v583 - 1);
      *(v581 - 2) = v590;
      *(v581 - 1) = v591;
      --v582;
    }
    while ( v582 );
    HIDWORD(v1116) = HIDWORD(v75);
    v592 = (__m128i)v1134[0];
    *v581 = *v583;
    v1120 = v592;
    v1121 = v1134[1];
    v1122 = v1134[2];
    v1123 = v1134[3];
    v1124 = v1134[4];
    v1125 = v1134[5];
    v1126 = v1134[6];
    v1127 = v1134[7];
    v1128 = v1135;
    sub_1808C33D0(&v1120, v1145);
    v593 = *(_DWORD *)(a1 + 3000);
    v594 = 0;
    v595 = *(_DWORD *)(a1 + 3008);
    v1117 = *(_DWORD *)(v75 + 24);
    v1128.m128i_i64[0] = __PAIR64__(v595, v593);
    if ( v593 > 0 )
    {
      v596 = &v1120;
      do
      {
        ++v594;
        v596->m128i_i64[0] = *(__int64 *)((char *)v596->m128i_i64 + a1 + 2872 - (_QWORD)&v1120);
        v596 = (__m128i *)((char *)v596 + 8);
        v593 = v1128.m128i_i32[0];
      }
      while ( v594 < v1128.m128i_i32[0] );
      v595 = v1128.m128i_i32[1];
    }
    memset(v1136, 0, sizeof(v1136));
    v1137.m128i_i64[0] = __PAIR64__(v595, v593);
    v597 = 0;
    v1137.m128i_i64[1] = 4LL * v595;
    v598 = v593;
    if ( v593 > 0 )
    {
      v599 = *(_DWORD *)(v75 + 24);
      do
      {
        *((_QWORD *)v1136 + v597) = *(_QWORD *)v75 + 4LL * v599;
        v600 = v599 + v595;
        v599 = v599 + v595 - (((_BYTE)v599 + (_BYTE)v595) & 0xF) + 16;
        if ( (v600 & 0xF) == 0 )
          v599 = v600;
        ++v597;
        *(_DWORD *)(v75 + 24) = v599;
      }
      while ( v597 < v593 );
      v595 = v1137.m128i_i32[1];
      v593 = v1137.m128i_i32[0];
    }
    v601 = *(_DWORD *)(a1 + 3000);
    v1135.m128i_i32[1] = *(_DWORD *)(a1 + 3008);
    v602 = 0;
    memset(v1134, 0, sizeof(v1134));
    v1135.m128i_i32[0] = v601;
    v1135.m128i_i64[1] = 4LL * v1135.m128i_i32[1];
    if ( v601 > 0 )
    {
      v603 = v1134;
      do
      {
        ++v602;
        *v603 = *(_QWORD *)((char *)v603 + a1 + 2872 - (_QWORD)v1134);
        ++v603;
      }
      while ( v602 < v1135.m128i_i32[0] );
    }
    v604 = (__m128i)v1136[0];
    v605 = v1136[1];
    v606 = v1136[2];
    v607 = v1136[3];
    v608 = v1136[4];
    v609 = v1136[5];
    v610 = v1136[6];
    v611 = v1136[7];
    v612 = v1137;
    v1120 = (__m128i)v1136[0];
    v1121 = v1136[1];
    v1122 = v1136[2];
    v1123 = v1136[3];
    v1124 = v1136[4];
    v1125 = v1136[5];
    v1126 = v1136[6];
    v1127 = v1136[7];
    v1128 = v1137;
    v1154 = (__m128i)v1134[0];
    v1155 = v1134[1];
    v1156 = v1134[2];
    v1157 = v1134[3];
    v1158 = v1134[4];
    v1159 = v1134[5];
    v1160 = v1134[6];
    v1161 = v1134[7];
    v1162 = v1135;
    if ( v593 > 0 )
    {
      v613 = 0;
      v614 = (unsigned int)v593;
      do
      {
        LODWORD(v1116) = 0;
        ((void (__fastcall *)(__int64, __int64, _QWORD, __int64, __int64))unk_180001250)(
          v1154.m128i_i64[v613],
          v1120.m128i_i64[v613],
          (unsigned int)v595,
          v598,
          v1116);
        ++v613;
        --v614;
      }
      while ( v614 );
      v75 = v1195;
    }
    v1166 = 0;
    ((void (__fastcall *)(char *, _QWORD, __int64, __int64))unk_181798F42)(v1167, 0, 1016, v598);
    v1168 = v1177;
    v1169 = v571;
    v1170 = 4 * v571;
    sub_18061A9A0(v75, &v1166);
    v616 = v1134;
    v1120 = v604;
    v617 = (__int128 *)&v1175;
    v1121 = v605;
    v618 = 8;
    v1122 = v606;
    v1123 = v607;
    v1124 = v608;
    v1125 = v609;
    v1126 = v610;
    v1127 = v611;
    v1128 = v612;
    do
    {
      v616 += 8;
      v619 = *v617;
      v620 = v617[1];
      v617 += 8;
      *(v616 - 8) = v619;
      v621 = *(v617 - 6);
      *(v616 - 7) = v620;
      v622 = *(v617 - 5);
      *(v616 - 6) = v621;
      v623 = *(v617 - 4);
      *(v616 - 5) = v622;
      v624 = *(v617 - 3);
      *(v616 - 4) = v623;
      v625 = *(v617 - 2);
      *(v616 - 3) = v624;
      v626 = *(v617 - 1);
      *(v616 - 2) = v625;
      *(v616 - 1) = v626;
      --v618;
    }
    while ( v618 );
    v627 = *v617;
    v628 = (__m128i *)&v1166;
    v629 = 8;
    *v616 = v627;
    v630 = &v1154;
    do
    {
      v630 += 8;
      v631 = *v628;
      v632 = v628[1];
      v628 += 8;
      v630[-8] = v631;
      v633 = v628[-6];
      v630[-7] = v632;
      v634 = v628[-5];
      v630[-6] = v633;
      v635 = v628[-4];
      v630[-5] = v634;
      v636 = v628[-3];
      v630[-4] = v635;
      v637 = v628[-2];
      v630[-3] = v636;
      v638 = v628[-1];
      v630[-2] = v637;
      v630[-1] = v638;
      --v629;
    }
    while ( v629 );
    v639 = v1168;
    v640 = v1169;
    *v630 = *v628;
    if ( (_DWORD)v639 == v593 )
    {
      if ( (int)v639 > 0 )
      {
        v641 = 0;
        v642 = (unsigned int)v639;
        do
        {
          ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001550)(
            v1120.m128i_i64[v641],
            *(_QWORD *)((char *)v1134 + v641 * 8),
            v1154.m128i_i64[v641],
            (unsigned int)v640);
          ++v641;
          --v642;
        }
        while ( v642 );
      }
    }
    else if ( v593 == 1 && (int)v639 > 0 )
    {
      v643 = v639;
      v644 = 0;
      v645 = *(_QWORD *)&v1136[0];
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001550)(
          v645,
          *(_QWORD *)((char *)v1134 + v644 * 8),
          v1154.m128i_i64[v644],
          (unsigned int)v640);
        ++v644;
        --v643;
      }
      while ( v643 );
      LODWORD(v639) = v1168;
    }
    v646 = (__int128 *)v1181;
    v647 = 8;
    v648 = (__int128 *)&v1166;
    do
    {
      v646 += 8;
      v649 = *v648;
      v650 = v648[1];
      v648 += 8;
      *(v646 - 8) = v649;
      v651 = *(v648 - 6);
      *(v646 - 7) = v650;
      v652 = *(v648 - 5);
      *(v646 - 6) = v651;
      v653 = *(v648 - 4);
      *(v646 - 5) = v652;
      v654 = *(v648 - 3);
      *(v646 - 4) = v653;
      v655 = *(v648 - 2);
      *(v646 - 3) = v654;
      v656 = *(v648 - 1);
      *(v646 - 2) = v655;
      *(v646 - 1) = v656;
      --v647;
    }
    while ( v647 );
    *v646 = *v648;
    if ( (int)v639 > 0 )
    {
      v657 = v1181;
      v658 = (unsigned int)v639;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*v657++, (unsigned int)v640, v615, 0);
        --v658;
      }
      while ( v658 );
    }
    *(_QWORD *)&v1138[0] = 0;
    ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)((char *)v1138 + 8, 0, 1016);
    v1141 = v640;
    v659 = v639;
    v1140 = v639;
    v660 = v640;
    v1142 = 4 * v640;
    v661 = 0;
    v662 = (int)v639;
    if ( (int)v639 > 0 )
    {
      v663 = v1195;
      v664 = *(_DWORD *)(v1195 + 24);
      do
      {
        *((_QWORD *)v1138 + v661) = *(_QWORD *)v663 + 4LL * v664;
        v665 = v664 + v640;
        v664 = v664 + v640 - (((_BYTE)v664 + (_BYTE)v640) & 0xF) + 16;
        if ( (v665 & 0xF) == 0 )
          v664 = v665;
        ++v661;
        *(_DWORD *)(v663 + 24) = v664;
      }
      while ( v661 < (int)v639 );
      v660 = v1141;
      v659 = v1140;
    }
    v666 = v1182;
    v667 = 8;
    v668 = (__int128 *)&v1166;
    do
    {
      v666 += 8;
      v669 = *v668;
      v670 = v668[1];
      v668 += 8;
      *(v666 - 8) = v669;
      v671 = *(v668 - 6);
      *(v666 - 7) = v670;
      v672 = *(v668 - 5);
      *(v666 - 6) = v671;
      v673 = *(v668 - 4);
      *(v666 - 5) = v672;
      v674 = *(v668 - 3);
      *(v666 - 4) = v673;
      v675 = *(v668 - 2);
      *(v666 - 3) = v674;
      v676 = *(v668 - 1);
      *(v666 - 2) = v675;
      *(v666 - 1) = v676;
      --v667;
    }
    while ( v667 );
    v677 = *v668;
    v678 = v1138;
    v679 = 8;
    *v666 = v677;
    v680 = v1136;
    do
    {
      v680 += 8;
      v681 = *v678;
      v682 = v678[1];
      v678 += 8;
      *(v680 - 8) = v681;
      v683 = *(v678 - 6);
      *(v680 - 7) = v682;
      v684 = *(v678 - 5);
      *(v680 - 6) = v683;
      v685 = *(v678 - 4);
      *(v680 - 5) = v684;
      v686 = *(v678 - 3);
      *(v680 - 4) = v685;
      v687 = *(v678 - 2);
      *(v680 - 3) = v686;
      v688 = *(v678 - 1);
      *(v680 - 2) = v687;
      *(v680 - 1) = v688;
      --v679;
    }
    while ( v679 );
    *v680 = *v678;
    if ( v659 == (_DWORD)v639 )
    {
      if ( v659 > 0 )
      {
        v689 = v1140;
        v690 = 0;
        do
        {
          ((void (__fastcall *)(_QWORD, _QWORD, _QWORD, __int64))unk_1800010A0)(
            *(_QWORD *)((char *)v1182 + v690),
            *(_QWORD *)((char *)v1136 + v690),
            v660,
            v662);
          v690 += 8;
          --v689;
        }
        while ( v689 );
LABEL_285:
        v659 = v1140;
        LODWORD(v640) = v1169;
      }
    }
    else if ( (_DWORD)v639 == 1 && v659 > 0 )
    {
      v691 = v1140;
      v692 = v1136;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD, __int64))unk_1800010A0)(v1166, *v692++, v660, v662);
        --v691;
      }
      while ( v691 );
      goto LABEL_285;
    }
    v693 = v1183;
    v694 = 8;
    v695 = v1138;
    do
    {
      v693 += 8;
      v696 = *v695;
      v697 = v695[1];
      v695 += 8;
      *(v693 - 8) = v696;
      v698 = *(v695 - 6);
      *(v693 - 7) = v697;
      v699 = *(v695 - 5);
      *(v693 - 6) = v698;
      v700 = *(v695 - 4);
      *(v693 - 5) = v699;
      v701 = *(v695 - 3);
      *(v693 - 4) = v700;
      v702 = *(v695 - 2);
      *(v693 - 3) = v701;
      v703 = *(v695 - 1);
      *(v693 - 2) = v702;
      *(v693 - 1) = v703;
      --v694;
    }
    while ( v694 );
    *v693 = *v695;
    sub_1808C3C20((__int64)v1183);
    v569 = 8;
    v704 = (__int128 *)v1184;
    v705 = 8;
    v706 = v1138;
    do
    {
      v704 += 8;
      v707 = *v706;
      v708 = v706[1];
      v706 += 8;
      *(v704 - 8) = v707;
      v709 = *(v706 - 6);
      *(v704 - 7) = v708;
      v710 = *(v706 - 5);
      *(v704 - 6) = v709;
      v711 = *(v706 - 4);
      *(v704 - 5) = v710;
      v712 = *(v706 - 3);
      *(v704 - 4) = v711;
      v713 = *(v706 - 2);
      *(v704 - 3) = v712;
      v714 = *(v706 - 1);
      *(v704 - 2) = v713;
      *(v704 - 1) = v714;
      --v705;
    }
    while ( v705 );
    *v704 = *v706;
    if ( v659 > 0 )
    {
      v715 = v1140;
      v716 = v1184;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*v716++, v660, v569, 0);
        --v715;
      }
      while ( v715 );
      LODWORD(v639) = v1168;
      v569 = 8;
      v659 = v1140;
    }
    v717 = v1180;
    v718 = 8;
    v719 = v1138;
    do
    {
      v717 += 8;
      v720 = *v719;
      v721 = v719[1];
      v719 += 8;
      *(v717 - 8) = v720;
      v722 = *(v719 - 6);
      *(v717 - 7) = v721;
      v723 = *(v719 - 5);
      *(v717 - 6) = v722;
      v724 = *(v719 - 4);
      *(v717 - 5) = v723;
      v725 = *(v719 - 3);
      *(v717 - 4) = v724;
      v726 = *(v719 - 2);
      *(v717 - 3) = v725;
      v727 = *(v719 - 1);
      *(v717 - 2) = v726;
      *(v717 - 1) = v727;
      --v718;
    }
    while ( v718 );
    v728 = *v719;
    v729 = (__int128 *)&v1166;
    v730 = 8;
    *v717 = v728;
    v731 = v1165;
    do
    {
      v731 += 8;
      v732 = *v729;
      v733 = v729[1];
      v729 += 8;
      *(v731 - 8) = v732;
      v734 = *(v729 - 6);
      *(v731 - 7) = v733;
      v735 = *(v729 - 5);
      *(v731 - 6) = v734;
      v736 = *(v729 - 4);
      *(v731 - 5) = v735;
      v737 = *(v729 - 3);
      *(v731 - 4) = v736;
      v738 = *(v729 - 2);
      *(v731 - 3) = v737;
      v739 = *(v729 - 1);
      *(v731 - 2) = v738;
      *(v731 - 1) = v739;
      --v730;
    }
    while ( v730 );
    *v731 = *v729;
    if ( (_DWORD)v639 == v659 )
    {
      if ( (int)v639 <= 0 )
        goto LABEL_308;
      v740 = 0;
      v741 = (unsigned int)v639;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001430)(
          v1180[v740],
          *(_QWORD *)((char *)v1165 + v740 * 8),
          (unsigned int)v640);
        ++v740;
        --v741;
      }
      while ( v741 );
    }
    else
    {
      if ( v659 != 1 || (int)v639 <= 0 )
        goto LABEL_308;
      v742 = v1165;
      v743 = (unsigned int)v639;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001430)(
          *(_QWORD *)&v1138[0],
          *(_QWORD *)v742,
          (unsigned int)v640);
        v742 = (__int128 *)((char *)v742 + 8);
        --v743;
      }
      while ( v743 );
    }
    v569 = 8;
LABEL_308:
    v744 = v1164;
    v745 = 8;
    v746 = (__int128 *)&v1166;
    do
    {
      v744 += 8;
      v747 = *v746;
      v748 = v746[1];
      v746 += 8;
      *(v744 - 8) = v747;
      v749 = *(v746 - 6);
      *(v744 - 7) = v748;
      v750 = *(v746 - 5);
      *(v744 - 6) = v749;
      v751 = *(v746 - 4);
      *(v744 - 5) = v750;
      v752 = *(v746 - 3);
      *(v744 - 4) = v751;
      v753 = *(v746 - 2);
      *(v744 - 3) = v752;
      v754 = *(v746 - 1);
      *(v744 - 2) = v753;
      *(v744 - 1) = v754;
      --v745;
    }
    while ( v745 );
    v755 = *v746;
    v756 = (__int128 *)&v1175;
    v757 = 8;
    *v744 = v755;
    v758 = v1145;
    do
    {
      v758 += 8;
      v759 = *v756;
      v760 = v756[1];
      v756 += 8;
      *(v758 - 8) = v759;
      v761 = *(v756 - 6);
      *(v758 - 7) = v760;
      v762 = *(v756 - 5);
      *(v758 - 6) = v761;
      v763 = *(v756 - 4);
      *(v758 - 5) = v762;
      v764 = *(v756 - 3);
      *(v758 - 4) = v763;
      v765 = *(v756 - 2);
      *(v758 - 3) = v764;
      v766 = *(v756 - 1);
      *(v758 - 2) = v765;
      *(v758 - 1) = v766;
      --v757;
    }
    while ( v757 );
    v577 = v1177;
    *v758 = *v756;
    if ( (_DWORD)v577 == (_DWORD)v639 )
    {
      if ( (int)v577 > 0 )
      {
        v767 = 0;
        v768 = (unsigned int)v577;
        do
        {
          ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001340)(
            v1164[v767],
            *(_QWORD *)((char *)v1145 + v767 * 8),
            (unsigned int)v571);
          ++v767;
          --v768;
        }
        while ( v768 );
      }
    }
    else if ( (_DWORD)v639 == 1 && (int)v577 > 0 )
    {
      v769 = v577;
      v770 = v1145;
      v771 = v1166;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v771, *(_QWORD *)v770, (unsigned int)v571);
        v770 = (__int128 *)((char *)v770 + 8);
        --v769;
      }
      while ( v769 );
      LODWORD(v577) = v1177;
    }
    v75 = v1195;
    *(_DWORD *)(v1195 + 24) = v1117;
  }
  v772 = (__int128 *)v1164;
  v773 = 8;
  v774 = (__int128 *)&v1175;
  do
  {
    v772 += 8;
    v775 = *v774;
    v776 = v774[1];
    v774 += 8;
    *(v772 - 8) = v775;
    v777 = *(v774 - 6);
    *(v772 - 7) = v776;
    v778 = *(v774 - 5);
    *(v772 - 6) = v777;
    v779 = *(v774 - 4);
    *(v772 - 5) = v778;
    v780 = *(v774 - 3);
    *(v772 - 4) = v779;
    v781 = *(v774 - 2);
    *(v772 - 3) = v780;
    v782 = *(v774 - 1);
    *(v772 - 2) = v781;
    *(v772 - 1) = v782;
    --v773;
  }
  while ( v773 );
  *v772 = *v774;
  if ( (int)v577 > 0 )
  {
    v783 = v1164;
    v784 = (unsigned int)v577;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*v783++, (unsigned int)v571, v569, 0);
      --v784;
    }
    while ( v784 );
  }
  v1146 = 0;
  ((void (__fastcall *)(char *, _QWORD, __int64))unk_181798F42)(v1147, 0, 1016);
  v1148 = v577;
  v785 = 0;
  v1149 = v571;
  v1150 = 4 * v571;
  v786 = (int)v577;
  if ( (int)v577 > 0 )
  {
    v787 = *(_DWORD *)(v75 + 24);
    do
    {
      *(_QWORD *)&v1147[8 * v785 - 8] = *(_QWORD *)v75 + 4LL * v787;
      v788 = v787 + v571;
      v787 = v787 + v571 - (((_BYTE)v787 + (_BYTE)v571) & 0xF) + 16;
      if ( (v788 & 0xF) == 0 )
        v787 = v788;
      ++v785;
      *(_DWORD *)(v75 + 24) = v787;
    }
    while ( v785 < (int)v577 );
    LODWORD(v571) = v1149;
    LODWORD(v577) = v1148;
  }
  v789 = v1184;
  v790 = 8;
  v791 = (__int128 *)&v1175;
  do
  {
    v789 += 8;
    v792 = *v791;
    v793 = v791[1];
    v791 += 8;
    *(v789 - 8) = v792;
    v794 = *(v791 - 6);
    *(v789 - 7) = v793;
    v795 = *(v791 - 5);
    *(v789 - 6) = v794;
    v796 = *(v791 - 4);
    *(v789 - 5) = v795;
    v797 = *(v791 - 3);
    *(v789 - 4) = v796;
    v798 = *(v791 - 2);
    *(v789 - 3) = v797;
    v799 = *(v791 - 1);
    *(v789 - 2) = v798;
    *(v789 - 1) = v799;
    --v790;
  }
  while ( v790 );
  v800 = *v791;
  v801 = (__int128 *)&v1146;
  v802 = 8;
  *v789 = v800;
  v803 = (__int128 *)v1180;
  do
  {
    v803 += 8;
    v804 = *v801;
    v805 = v801[1];
    v801 += 8;
    *(v803 - 8) = v804;
    v806 = *(v801 - 6);
    *(v803 - 7) = v805;
    v807 = *(v801 - 5);
    *(v803 - 6) = v806;
    v808 = *(v801 - 4);
    *(v803 - 5) = v807;
    v809 = *(v801 - 3);
    *(v803 - 4) = v808;
    v810 = *(v801 - 2);
    *(v803 - 3) = v809;
    v811 = *(v801 - 1);
    *(v803 - 2) = v810;
    *(v803 - 1) = v811;
    --v802;
  }
  while ( v802 );
  *v803 = *v801;
  if ( (int)v577 > 0 )
  {
    v812 = 0;
    v813 = (unsigned int)v577;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, _QWORD, __int64))unk_1801C8500)(
        v1184[v812],
        v1180[v812],
        (unsigned int)v571,
        v786);
      ++v812;
      --v813;
    }
    while ( v813 );
  }
  v1171 = 0;
  ((void (__fastcall *)(char *, _QWORD, __int64, __int64))unk_181798F42)(v1172, 0, 1016, v786);
  v814 = HIDWORD(v1144);
  v815 = 0;
  v816 = (int)v1144;
  v1173 = v1144;
  v1174 = 4LL * SHIDWORD(v1144);
  if ( (int)v1144 > 0 )
  {
    v817 = *(_DWORD *)(v75 + 24);
    do
    {
      *(_QWORD *)&v1172[8 * v815 - 8] = *(_QWORD *)v75 + 4LL * v817;
      v818 = v814 + v817;
      v817 = v814 + v817 - (((_BYTE)v814 + (_BYTE)v817) & 0xF) + 16;
      if ( (v818 & 0xF) == 0 )
        v817 = v818;
      ++v815;
      *(_DWORD *)(v75 + 24) = v817;
    }
    while ( v815 < v816 );
    v814 = HIDWORD(v1173);
    LODWORD(v816) = v1173;
  }
  v819 = v1183;
  v820 = 8;
  v821 = (__int128 *)&v1146;
  do
  {
    v819 += 8;
    v822 = *v821;
    v823 = v821[1];
    v821 += 8;
    *(v819 - 8) = v822;
    v824 = *(v821 - 6);
    *(v819 - 7) = v823;
    v825 = *(v821 - 5);
    *(v819 - 6) = v824;
    v826 = *(v821 - 4);
    *(v819 - 5) = v825;
    v827 = *(v821 - 3);
    *(v819 - 4) = v826;
    v828 = *(v821 - 2);
    *(v819 - 3) = v827;
    v829 = *(v821 - 1);
    *(v819 - 2) = v828;
    *(v819 - 1) = v829;
    --v820;
  }
  while ( v820 );
  v830 = *v821;
  v831 = (__int128 *)&v1171;
  v832 = 8;
  *v819 = v830;
  v833 = v1182;
  do
  {
    v833 += 8;
    v834 = *v831;
    v835 = v831[1];
    v831 += 8;
    *(v833 - 8) = v834;
    v836 = *(v831 - 6);
    *(v833 - 7) = v835;
    v837 = *(v831 - 5);
    *(v833 - 6) = v836;
    v838 = *(v831 - 4);
    *(v833 - 5) = v837;
    v839 = *(v831 - 3);
    *(v833 - 4) = v838;
    v840 = *(v831 - 2);
    *(v833 - 3) = v839;
    v841 = *(v831 - 1);
    *(v833 - 2) = v840;
    *(v833 - 1) = v841;
    --v832;
  }
  while ( v832 );
  *v833 = *v831;
  sub_1808C3E00(a1 + 3880, v1182, v1183);
  v842 = (__int128 *)v1181;
  v843 = 8;
  v844 = (__int128 *)&v1171;
  do
  {
    v842 += 8;
    v845 = *v844;
    v846 = v844[1];
    v844 += 8;
    *(v842 - 8) = v845;
    v847 = *(v844 - 6);
    *(v842 - 7) = v846;
    v848 = *(v844 - 5);
    *(v842 - 6) = v847;
    v849 = *(v844 - 4);
    *(v842 - 5) = v848;
    v850 = *(v844 - 3);
    *(v842 - 4) = v849;
    v851 = *(v844 - 2);
    *(v842 - 3) = v850;
    v852 = *(v844 - 1);
    *(v842 - 2) = v851;
    *(v842 - 1) = v852;
    --v843;
  }
  while ( v843 );
  *v842 = *v844;
  if ( (int)v816 > 0 )
  {
    v853 = v1181;
    v854 = (unsigned int)v816;
    do
    {
      ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v844, *v853++, v814);
      --v854;
    }
    while ( v854 );
  }
  v855 = v1145;
  v856 = 8;
  v857 = (__int128 *)&v1171;
  do
  {
    v855 += 8;
    v858 = *v857;
    v859 = v857[1];
    v857 += 8;
    *(v855 - 8) = v858;
    v860 = *(v857 - 6);
    *(v855 - 7) = v859;
    v861 = *(v857 - 5);
    *(v855 - 6) = v860;
    v862 = *(v857 - 4);
    *(v855 - 5) = v861;
    v863 = *(v857 - 3);
    *(v855 - 4) = v862;
    v864 = *(v857 - 2);
    *(v855 - 3) = v863;
    v865 = *(v857 - 1);
    *(v855 - 2) = v864;
    *(v855 - 1) = v865;
    --v856;
  }
  while ( v856 );
  *v855 = *v857;
  if ( (int)v816 > 0 )
  {
    v866 = v1145;
    v867 = (unsigned int)v816;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_1801C84A0)(*(_QWORD *)v866, *(_QWORD *)v866, v814);
      v866 = (__int128 *)((char *)v866 + 8);
      --v867;
    }
    while ( v867 );
  }
  ((void (*)(void))unk_181C9A9FB)();
  ((void (*)(void))unk_181C9A9D7)();
  v868 = v1165;
  v869 = (__int128 *)&v1171;
  v870 = 8;
  do
  {
    v868 += 8;
    v871 = *v869;
    v872 = v869[3];
    v873 = v869[1];
    v869 += 8;
    *(v868 - 8) = v871;
    v874 = *(v869 - 6);
    *(v868 - 7) = v873;
    *(v868 - 6) = v874;
    v875 = *(v869 - 4);
    *(v868 - 5) = v872;
    v876 = *(v869 - 3);
    *(v868 - 4) = v875;
    v877 = *(v869 - 2);
    *(v868 - 3) = v876;
    v878 = *(v869 - 1);
    *(v868 - 2) = v877;
    *(v868 - 1) = v878;
    --v870;
  }
  while ( v870 );
  *v868 = *v869;
  if ( (int)v816 > 0 )
  {
    v879 = v1165;
    v880 = (unsigned int)v816;
    do
    {
      ((void (__fastcall *)(__int128 *, _QWORD, _QWORD))unk_180001220)(v869, *(_QWORD *)v879, v814);
      v879 = (__int128 *)((char *)v879 + 8);
      --v880;
    }
    while ( v880 );
  }
  v881 = *(_DWORD *)(a1 + 1128);
  v1137.m128i_i32[1] = *(_DWORD *)(a1 + 1136);
  v882 = 0;
  memset(v1136, 0, sizeof(v1136));
  v883 = 0;
  v1137.m128i_i32[0] = v881;
  v1137.m128i_i64[1] = 4LL * v1137.m128i_i32[1];
  if ( v881 > 0 )
  {
    v884 = v1136;
    do
    {
      ++v883;
      *v884 = *(_QWORD *)((char *)v884 + a1 + 1000 - (_QWORD)v1136);
      ++v884;
      v881 = v1137.m128i_i32[0];
    }
    while ( v883 < v1137.m128i_i32[0] );
    v882 = *(_QWORD *)&v1136[0];
  }
  v885 = v1145;
  v886 = 8;
  v887 = (__int128 *)&v1171;
  v1120 = (__m128i)v1136[0];
  v1121 = v1136[1];
  v1122 = v1136[2];
  v1123 = v1136[3];
  v1124 = v1136[4];
  v1125 = v1136[5];
  v1126 = v1136[6];
  v1127 = v1136[7];
  v1128 = v1137;
  do
  {
    v885 += 8;
    v888 = *v887;
    v889 = v887[1];
    v887 += 8;
    *(v885 - 8) = v888;
    v890 = *(v887 - 6);
    *(v885 - 7) = v889;
    v891 = *(v887 - 5);
    *(v885 - 6) = v890;
    v892 = *(v887 - 4);
    *(v885 - 5) = v891;
    v893 = *(v887 - 3);
    *(v885 - 4) = v892;
    v894 = *(v887 - 2);
    *(v885 - 3) = v893;
    v895 = *(v887 - 1);
    *(v885 - 2) = v894;
    *(v885 - 1) = v895;
    --v886;
  }
  while ( v886 );
  *v885 = *v887;
  if ( (_DWORD)v816 == v881 )
  {
    if ( (int)v816 > 0 )
    {
      v896 = 0;
      v897 = (unsigned int)v816;
      do
      {
        ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(
          v1120.m128i_i64[v896],
          *(_QWORD *)((char *)v1145 + v896 * 8),
          v814);
        ++v896;
        --v897;
      }
      while ( v897 );
    }
  }
  else if ( v881 == 1 && (int)v816 > 0 )
  {
    v898 = v1145;
    v899 = (unsigned int)v816;
    do
    {
      ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v882, *(_QWORD *)v898, v814);
      v898 = (__int128 *)((char *)v898 + 8);
      --v899;
    }
    while ( v899 );
  }
  v900 = v1195;
  v1151[0].m128i_i64[0] = 0;
  ((void (__fastcall *)(unsigned __int64 *, _QWORD, __int64))unk_181798F42)(&v1151[0].m128i_u64[1], 0, 1016);
  v901 = HIDWORD(v1144);
  v902 = 0;
  v903 = (int)v1144;
  v1152 = v1144;
  v1153 = 4LL * SHIDWORD(v1144);
  if ( (int)v1144 > 0 )
  {
    v904 = *(_DWORD *)(v900 + 24);
    do
    {
      v1151[0].m128i_i64[v902] = *(_QWORD *)v900 + 4LL * v904;
      v905 = v904 + v901;
      v904 = v904 + v901 - (((_BYTE)v904 + (_BYTE)v901) & 0xF) + 16;
      if ( (v905 & 0xF) == 0 )
        v904 = v905;
      ++v902;
      *(_DWORD *)(v900 + 24) = v904;
    }
    while ( v902 < v903 );
    v901 = HIDWORD(v1152);
    LODWORD(v903) = v1152;
  }
  v906 = v1164;
  v907 = 8;
  v908 = (__int128 *)&v1171;
  do
  {
    v906 += 8;
    v909 = *v908;
    v910 = v908[1];
    v908 += 8;
    *(v906 - 8) = v909;
    v911 = *(v908 - 6);
    *(v906 - 7) = v910;
    v912 = *(v908 - 5);
    *(v906 - 6) = v911;
    v913 = *(v908 - 4);
    *(v906 - 5) = v912;
    v914 = *(v908 - 3);
    *(v906 - 4) = v913;
    v915 = *(v908 - 2);
    *(v906 - 3) = v914;
    v916 = *(v908 - 1);
    *(v906 - 2) = v915;
    *(v906 - 1) = v916;
    --v907;
  }
  while ( v907 );
  v917 = *v908;
  v918 = (__int128 *)v1143;
  v919 = 8;
  *v906 = v917;
  v920 = v1165;
  do
  {
    v920 += 8;
    v921 = *v918;
    v922 = v918[1];
    v918 += 8;
    *(v920 - 8) = v921;
    v923 = *(v918 - 6);
    *(v920 - 7) = v922;
    v924 = *(v918 - 5);
    *(v920 - 6) = v923;
    v925 = *(v918 - 4);
    *(v920 - 5) = v924;
    v926 = *(v918 - 3);
    *(v920 - 4) = v925;
    v927 = *(v918 - 2);
    *(v920 - 3) = v926;
    v928 = *(v918 - 1);
    *(v920 - 2) = v927;
    *(v920 - 1) = v928;
    --v919;
  }
  while ( v919 );
  v929 = *v918;
  v930 = v1151;
  v931 = 8;
  *v920 = v929;
  v932 = v1145;
  do
  {
    v932 += 8;
    v933 = *v930;
    v934 = (__int128)v930[1];
    v930 += 8;
    *(v932 - 8) = (__int128)v933;
    v935 = (__int128)v930[-6];
    *(v932 - 7) = v934;
    v936 = (__int128)v930[-5];
    *(v932 - 6) = v935;
    v937 = (__int128)v930[-4];
    *(v932 - 5) = v936;
    v938 = (__int128)v930[-3];
    *(v932 - 4) = v937;
    v939 = (__int128)v930[-2];
    *(v932 - 3) = v938;
    v940 = (__int128)v930[-1];
    *(v932 - 2) = v939;
    *(v932 - 1) = v940;
    --v931;
  }
  while ( v931 );
  *v932 = (__int128)*v930;
  if ( (_DWORD)v903 == (_DWORD)v816 )
  {
    if ( (int)v903 > 0 )
    {
      v941 = 0;
      v942 = (unsigned int)v903;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD, _QWORD))unk_180001190)(
          *(_QWORD *)((char *)v1165 + v941 * 8),
          v1164[v941],
          *(_QWORD *)((char *)v1145 + v941 * 8),
          v901);
        ++v941;
        --v942;
      }
      while ( v942 );
    }
  }
  else if ( (_DWORD)v816 == 1 && (int)v903 > 0 )
  {
    v943 = v1171;
    v944 = 0;
    v945 = (unsigned int)v903;
    do
    {
      ((void (__fastcall *)(_QWORD, __int64, _QWORD, _QWORD))unk_180001190)(
        *(_QWORD *)((char *)v1165 + v944),
        v943,
        *(_QWORD *)((char *)v1145 + v944),
        v901);
      v944 += 8;
      --v945;
    }
    while ( v945 );
    v900 = v1195;
  }
  v946 = (__m128i *)v1180;
  v947 = 8;
  v948 = v1151;
  do
  {
    v946 += 8;
    v949 = *v948;
    v950 = v948[1];
    v948 += 8;
    v946[-8] = v949;
    v951 = v948[-6];
    v946[-7] = v950;
    v952 = v948[-5];
    v946[-6] = v951;
    v953 = v948[-4];
    v946[-5] = v952;
    v954 = v948[-3];
    v946[-4] = v953;
    v955 = v948[-2];
    v946[-3] = v954;
    v956 = v948[-1];
    v946[-2] = v955;
    v946[-1] = v956;
    --v947;
  }
  while ( v947 );
  v957 = *(__int64 **)(a1 + 16);
  *v946 = *v948;
  sub_1808C0BD0((__int64)v1180, 0, v957, v900);
  sub_1808C1440(a1, (__int64)v1151, (__int64 *)v900);
  v958 = *(_DWORD *)(a1 + 2424);
  v1137.m128i_i32[1] = *(_DWORD *)(a1 + 2432);
  v959 = 0;
  memset(v1136, 0, sizeof(v1136));
  v960 = 0;
  v1137.m128i_i32[0] = v958;
  v1137.m128i_i64[1] = 4LL * v1137.m128i_i32[1];
  if ( v958 > 0 )
  {
    v961 = v1136;
    do
    {
      ++v960;
      *v961 = *(_QWORD *)((char *)v961 + a1 + 2296 - (_QWORD)v1136);
      ++v961;
      v958 = v1137.m128i_i32[0];
    }
    while ( v960 < v1137.m128i_i32[0] );
    v959 = *(_QWORD *)&v1136[0];
  }
  v962 = v1145;
  v963 = 8;
  v964 = v1151;
  v1120 = (__m128i)v1136[0];
  v1121 = v1136[1];
  v1122 = v1136[2];
  v1123 = v1136[3];
  v1124 = v1136[4];
  v1125 = v1136[5];
  v1126 = v1136[6];
  v1127 = v1136[7];
  v1128 = v1137;
  do
  {
    v962 += 8;
    v965 = *v964;
    v966 = (__int128)v964[1];
    v964 += 8;
    *(v962 - 8) = (__int128)v965;
    v967 = (__int128)v964[-6];
    *(v962 - 7) = v966;
    v968 = (__int128)v964[-5];
    *(v962 - 6) = v967;
    v969 = (__int128)v964[-4];
    *(v962 - 5) = v968;
    v970 = (__int128)v964[-3];
    *(v962 - 4) = v969;
    v971 = (__int128)v964[-2];
    *(v962 - 3) = v970;
    v972 = (__int128)v964[-1];
    *(v962 - 2) = v971;
    *(v962 - 1) = v972;
    --v963;
  }
  while ( v963 );
  v973 = (unsigned int)v1152;
  *v962 = (__int128)*v964;
  if ( (_DWORD)v973 == v958 )
  {
    if ( (int)v973 <= 0 )
      goto LABEL_422;
    v974 = HIDWORD(v1152);
    v975 = 0;
    v976 = (unsigned int)v973;
    do
    {
      ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(
        v1120.m128i_i64[v975],
        *(_QWORD *)((char *)v1145 + v975 * 8),
        v974);
      ++v975;
      --v976;
    }
    while ( v976 );
  }
  else
  {
    if ( v958 != 1 || (int)v973 <= 0 )
      goto LABEL_422;
    v977 = HIDWORD(v1152);
    v978 = v1145;
    v979 = v973;
    do
    {
      ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v959, *(_QWORD *)v978, v977);
      v978 = (__int128 *)((char *)v978 + 8);
      --v979;
    }
    while ( v979 );
    v900 = v1195;
  }
  LODWORD(v973) = v1152;
LABEL_422:
  v980 = (__m128i *)v1164;
  v981 = 8;
  v982 = v1151;
  do
  {
    v980 += 8;
    v983 = *v982;
    v984 = v982[1];
    v982 += 8;
    v980[-8] = v983;
    v985 = v982[-6];
    v980[-7] = v984;
    v986 = v982[-5];
    v980[-6] = v985;
    v987 = v982[-4];
    v980[-5] = v986;
    v988 = v982[-3];
    v980[-4] = v987;
    v989 = v982[-2];
    v980[-3] = v988;
    v990 = v982[-1];
    v980[-2] = v989;
    v980[-1] = v990;
    --v981;
  }
  while ( v981 );
  *v980 = *v982;
  if ( (int)v973 > 0 )
  {
    v991 = HIDWORD(v1152);
    v992 = v1164;
    v993 = (unsigned int)v973;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(*v992++, v991, v981, 0);
      --v993;
    }
    while ( v993 );
  }
  v505 = a2;
  v994 = sub_1808AE6F0(a2, v1180, *(_QWORD *)(a1 + 64));
  v995 = v1151;
  v996 = (__int128 *)v994;
  v997 = 8;
  v998 = (__m128i *)v1164;
  do
  {
    v998 += 8;
    v999 = *v995;
    v1000 = v995[1];
    v995 += 8;
    v998[-8] = v999;
    v1001 = v995[-6];
    v998[-7] = v1000;
    v1002 = v995[-5];
    v998[-6] = v1001;
    v1003 = v995[-4];
    v998[-5] = v1002;
    v1004 = v995[-3];
    v998[-4] = v1003;
    v1005 = v995[-2];
    v998[-3] = v1004;
    v1006 = v995[-1];
    v998[-2] = v1005;
    v998[-1] = v1006;
    --v997;
  }
  while ( v997 );
  v1007 = *v995;
  v1008 = 8;
  *v998 = v1007;
  v1009 = &v1146;
  do
  {
    v1009 += 16;
    v1010 = *v996;
    v1011 = v996[1];
    v996 += 8;
    *((_OWORD *)v1009 - 8) = v1010;
    v1012 = *(v996 - 6);
    *((_OWORD *)v1009 - 7) = v1011;
    v1013 = *(v996 - 5);
    *((_OWORD *)v1009 - 6) = v1012;
    v1014 = *(v996 - 4);
    *((_OWORD *)v1009 - 5) = v1013;
    v1015 = *(v996 - 3);
    *((_OWORD *)v1009 - 4) = v1014;
    v1016 = *(v996 - 2);
    *((_OWORD *)v1009 - 3) = v1015;
    v1017 = *(v996 - 1);
    *((_OWORD *)v1009 - 2) = v1016;
    *((_OWORD *)v1009 - 1) = v1017;
    --v1008;
  }
  while ( v1008 );
  *(_OWORD *)v1009 = *v996;
  if ( v1148 > 0 )
  {
    v1018 = v1149;
    v1019 = 0;
    v1020 = (unsigned int)v1148;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_1801C8500)(
        v1164[v1019],
        *(_QWORD *)&v1147[v1019 * 8 - 8],
        v1018);
      ++v1019;
      --v1020;
    }
    while ( v1020 );
  }
  v1021 = (__int128 *)sub_1808AE6F0(a2, v1164, *(_QWORD *)(a1 + 64));
  v1022 = &v1146;
  v1023 = 8;
  do
  {
    v1022 += 16;
    v1024 = *v1021;
    v1025 = v1021[1];
    v1021 += 8;
    *((_OWORD *)v1022 - 8) = v1024;
    v1026 = *(v1021 - 6);
    *((_OWORD *)v1022 - 7) = v1025;
    v1027 = *(v1021 - 5);
    *((_OWORD *)v1022 - 6) = v1026;
    v1028 = *(v1021 - 4);
    *((_OWORD *)v1022 - 5) = v1027;
    v1029 = *(v1021 - 3);
    *((_OWORD *)v1022 - 4) = v1028;
    v1030 = *(v1021 - 2);
    *((_OWORD *)v1022 - 3) = v1029;
    v1031 = *(v1021 - 1);
    *((_OWORD *)v1022 - 2) = v1030;
    *((_OWORD *)v1022 - 1) = v1031;
    --v1023;
  }
  while ( v1023 );
  *(_OWORD *)v1022 = *v1021;
  if ( v1148 > 0 )
  {
    v1032 = v1149;
    v1033 = &v1146;
    v1034 = (unsigned int)v1148;
    do
    {
      ((void (__fastcall *)(__int64 *, _QWORD, _QWORD))unk_180001220)(v1022, *v1033++, v1032);
      --v1034;
    }
    while ( v1034 );
  }
  *(_DWORD *)(v900 + 24) = v1131;
LABEL_440:
  if ( v1185 )
  {
    sub_1808BFCB0(a1, v505);
    sub_1808BFD30(a1, v505);
    v1036 = (__int128 *)v505;
    v1037 = (__int128 *)v1164;
    v1038 = 8;
    do
    {
      v1037 += 8;
      v1039 = *v1036;
      v1040 = v1036[1];
      v1036 += 8;
      *(v1037 - 8) = v1039;
      v1041 = *(v1036 - 6);
      *(v1037 - 7) = v1040;
      v1042 = *(v1036 - 5);
      *(v1037 - 6) = v1041;
      v1043 = *(v1036 - 4);
      *(v1037 - 5) = v1042;
      v1044 = *(v1036 - 3);
      *(v1037 - 4) = v1043;
      v1045 = *(v1036 - 2);
      *(v1037 - 3) = v1044;
      v1046 = *(v1036 - 1);
      *(v1037 - 2) = v1045;
      *(v1037 - 1) = v1046;
      --v1038;
    }
    while ( v1038 );
    v1047 = *(unsigned int ***)(a1 + 16);
    v1048 = *(_QWORD *)(a1 + 11320);
    *v1037 = *v1036;
    sub_1808C3F10((__int64)v1164, v1048, v1035, v1047);
  }
  ((void (*)(void))unk_181C9AA01)();
  ((void (*)(void))unk_181C9A9FB)();
  ((void (*)(void))unk_181C9AA01)();
  ((void (*)(void))unk_181C9A9FB)();
  v1050 = *(_QWORD *)(a1 + 72) == 0;
  LODWORD(v1188) = 0;
  if ( v1050 )
  {
    v1076 = v1195;
  }
  else
  {
    v1051 = 0;
    v1052 = a1 + 2728;
    v1053 = 0;
    do
    {
      ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(
        *(_QWORD *)(v1053 + v505),
        *(unsigned int *)(v505 + 1028),
        v1049,
        0);
      v1054 = *(_QWORD *)(v1053 + v505);
      v1132 = a1 + 176 * v1051 + 8376;
      sub_180860DA0(v1132, v1054, v1054);
      v1055 = *(_DWORD *)(a1 + 3432);
      memset(v1136, 0, sizeof(v1136));
      v1056 = 0;
      v1137.m128i_i32[0] = v1055;
      if ( v1055 > 0 )
      {
        v1057 = v1136;
        do
        {
          ++v1056;
          *v1057 = *(_QWORD *)((char *)v1057 + a1 + 3304 - (_QWORD)v1136);
          ++v1057;
          v1055 = v1137.m128i_i32[0];
        }
        while ( v1056 < v1137.m128i_i32[0] );
      }
      v1058 = *(_DWORD *)(a1 + 3576);
      v1059 = 0;
      *(_QWORD *)&v1138[0] = 0;
      v1060 = 0;
      v1139.m128i_i32[0] = v1058;
      if ( v1058 > 0 )
      {
        v1061 = v1138;
        do
        {
          ++v1060;
          *v1061 = *(_QWORD *)((char *)v1061 + a1 + 3448 - (_QWORD)v1138);
          ++v1061;
          v1058 = v1139.m128i_i32[0];
        }
        while ( v1060 < v1139.m128i_i32[0] );
        v1059 = *(_QWORD *)&v1138[0];
      }
      v1062 = *(_DWORD *)(v1052 + 128);
      v1063 = 0;
      v1064 = *(int *)(v1052 + 136);
      memset(v1134, 0, sizeof(v1134));
      v1065 = *(_DWORD *)(a2 + 1028);
      v1066 = *(_QWORD *)(v1053 + a2);
      LODWORD(v1193) = v1065;
      v1135.m128i_i64[0] = __PAIR64__(v1064, v1062);
      v1135.m128i_i64[1] = 4 * v1064;
      if ( v1062 > 0 )
      {
        v1067 = v1134;
        do
        {
          ++v1063;
          *v1067 = *(_QWORD *)((char *)v1067 + a1 + 2728 - (_QWORD)v1134);
          ++v1067;
        }
        while ( v1063 < v1135.m128i_i32[0] );
        LODWORD(v1064) = v1135.m128i_i32[1];
      }
      v1119 = *(_DWORD *)(v1195 + 24);
      v1068 = *(_QWORD *)v1195 + 4LL * v1119;
      v1131 = v1068;
      v1069 = v1065 + v1119 - (((_BYTE)v1065 + (_BYTE)v1119) & 0xF) + 16;
      if ( (((_BYTE)v1065 + (_BYTE)v1119) & 0xF) == 0 )
        v1069 = v1065 + v1119;
      *(_DWORD *)(v1195 + 24) = v1069;
      ((void (__fastcall *)(_QWORD, __int64, __int64))unk_1800011C0)(*(_QWORD *)((char *)v1134 + v1053), v1066, v1068);
      LODWORD(v1116) = 4;
      v1070 = *(_QWORD *)v1195 + 4LL * *(int *)(v1195 + 24);
      v1071 = v1193 + *(_DWORD *)(v1195 + 24);
      v1118 = v1070;
      v1072 = v1071 - (((_BYTE)v1193 + *(_BYTE *)(v1195 + 24)) & 0xF) + 16;
      if ( (v1071 & 0xF) == 0 )
        v1072 = v1193 + *(_DWORD *)(v1195 + 24);
      v1073 = (unsigned int)v1193;
      *(_DWORD *)(v1195 + 24) = v1072;
      ((void (__fastcall *)(__int64, __int64, __int64))unk_180001250)(v1131, v1070, v1073);
      ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD, __int64))unk_180001100)(
        v1131,
        (unsigned int)v1193,
        v1074,
        0,
        v1116);
      v1050 = v1058 == 1;
      v1075 = *(_QWORD *)((char *)v1134 + v1053);
      if ( v1050 )
        ((void (__fastcall *)(__int64, __int64, _QWORD, _QWORD))unk_180001580)(
          v1131,
          v1059,
          *(_QWORD *)((char *)v1134 + v1053),
          (unsigned int)v1064);
      if ( v1055 == 1 )
        ((void (__fastcall *)(__int64, _QWORD, __int64, _QWORD))unk_180001580)(
          v1118,
          *(_QWORD *)&v1136[0],
          v1075,
          (unsigned int)v1064);
      v1052 = a1 + 2728;
      v1076 = v1195;
      memset(v1134, 0, 24);
      *((_QWORD *)&v1134[7] + 1) = 0;
      v1077 = 0;
      *(_DWORD *)(v1195 + 24) = v1119;
      v1078 = *(_DWORD *)(a1 + 2856);
      v1135.m128i_i32[1] = *(_DWORD *)(a1 + 2864);
      v1135.m128i_i32[0] = v1078;
      v1135.m128i_i64[1] = 4LL * v1135.m128i_i32[1];
      memset((char *)&v1134[1] + 8, 0, 96);
      if ( v1078 > 0 )
      {
        v1079 = v1134;
        do
        {
          ++v1077;
          *v1079 = *(_QWORD *)((char *)v1079 + v1052 - (_QWORD)v1134);
          ++v1079;
        }
        while ( v1077 < v1135.m128i_i32[0] );
      }
      v505 = a2;
      ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_1800010A0)(
        *(_QWORD *)((char *)v1134 + v1053),
        *(_QWORD *)(v1053 + a2),
        *(unsigned int *)(a2 + 1028));
      ((void (__fastcall *)(_QWORD, _QWORD, __int64, _QWORD))unk_180001100)(
        *(_QWORD *)(v1053 + v505),
        *(unsigned int *)(v505 + 1028),
        v1080,
        0);
      sub_180860DA0(v1132, *(_QWORD *)(v1053 + v505), *(_QWORD *)(v1053 + v505));
      v1053 += 8;
      LODWORD(v1188) = (_DWORD)v1188 + 1;
      v1051 = (int)v1188;
    }
    while ( (unsigned __int64)(int)v1188 < *(_QWORD *)(a1 + 72) );
  }
  v1081 = (__int128 *)v1164;
  v1082 = 8;
  v1083 = 8;
  v1084 = (__int128 *)v505;
  do
  {
    v1081 += 8;
    v1085 = *v1084;
    v1086 = v1084[1];
    v1084 += 8;
    *(v1081 - 8) = v1085;
    v1087 = *(v1084 - 6);
    *(v1081 - 7) = v1086;
    v1088 = *(v1084 - 5);
    *(v1081 - 6) = v1087;
    v1089 = *(v1084 - 4);
    *(v1081 - 5) = v1088;
    v1090 = *(v1084 - 3);
    *(v1081 - 4) = v1089;
    v1091 = *(v1084 - 2);
    *(v1081 - 3) = v1090;
    v1092 = *(v1084 - 1);
    *(v1081 - 2) = v1091;
    *(v1081 - 1) = v1092;
    --v1083;
  }
  while ( v1083 );
  v1093 = *(_QWORD *)(a1 + 16);
  *v1081 = *v1084;
  sub_1808C42D0(v1164, 0, v1093, v1187);
  v1094 = *(int *)(a1 + 1280);
  v1095 = *(_DWORD *)(a1 + 1272);
  v1096 = a1 + 1144;
  v1097 = 0;
  memset(v1136, 0, sizeof(v1136));
  v1098 = 0;
  v1137.m128i_i64[0] = __PAIR64__(v1094, v1095);
  v1137.m128i_i64[1] = 4 * v1094;
  if ( v1095 > 0 )
  {
    v1099 = v1096 - (_QWORD)v1136;
    v1100 = v1136;
    do
    {
      ++v1098;
      *v1100 = *(_QWORD *)((char *)v1100 + v1099);
      ++v1100;
      v1095 = v1137.m128i_i32[0];
    }
    while ( v1098 < v1137.m128i_i32[0] );
    v1097 = *(_QWORD *)&v1136[0];
  }
  v1101 = &v1146;
  v1120 = (__m128i)v1136[0];
  v1121 = v1136[1];
  v1122 = v1136[2];
  v1123 = v1136[3];
  v1124 = v1136[4];
  v1125 = v1136[5];
  v1126 = v1136[6];
  v1127 = v1136[7];
  v1128 = v1137;
  do
  {
    v1101 += 16;
    v1102 = *(_OWORD *)v505;
    v1103 = *(_OWORD *)(v505 + 16);
    v505 += 128;
    *((_OWORD *)v1101 - 8) = v1102;
    v1104 = *(_OWORD *)(v505 - 96);
    *((_OWORD *)v1101 - 7) = v1103;
    v1105 = *(_OWORD *)(v505 - 80);
    *((_OWORD *)v1101 - 6) = v1104;
    v1106 = *(_OWORD *)(v505 - 64);
    *((_OWORD *)v1101 - 5) = v1105;
    v1107 = *(_OWORD *)(v505 - 48);
    *((_OWORD *)v1101 - 4) = v1106;
    v1108 = *(_OWORD *)(v505 - 32);
    *((_OWORD *)v1101 - 3) = v1107;
    v1109 = *(_OWORD *)(v505 - 16);
    *((_OWORD *)v1101 - 2) = v1108;
    *((_OWORD *)v1101 - 1) = v1109;
    --v1082;
  }
  while ( v1082 );
  *(_OWORD *)v1101 = *(_OWORD *)v505;
  result = (unsigned int)v1148;
  if ( v1148 == v1095 )
  {
    if ( v1148 > 0 )
    {
      v1111 = v1149;
      v1112 = (unsigned int)v1148;
      do
      {
        ((void (__fastcall *)(_QWORD, _QWORD, _QWORD))unk_180001340)(
          *(__int64 *)((char *)v1120.m128i_i64 + v35),
          *(_QWORD *)&v1147[v35 - 8],
          v1111);
        v35 += 8;
        --v1112;
      }
      while ( v1112 );
      result = v1195;
      *(_DWORD *)(v1195 + 24) = v1192;
      return result;
    }
LABEL_489:
    *(_DWORD *)(v1076 + 24) = v1192;
    return result;
  }
  if ( v1095 != 1 || v1148 <= 0 )
    goto LABEL_489;
  v1113 = v1149;
  v1114 = &v1146;
  v1115 = (unsigned int)v1148;
  do
  {
    ((void (__fastcall *)(__int64, _QWORD, _QWORD))unk_180001340)(v1097, *v1114++, v1113);
    --v1115;
  }
  while ( v1115 );
  result = v1195;
  *(_DWORD *)(v1195 + 24) = v1192;
  return result;
}

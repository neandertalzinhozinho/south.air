OPTION CASEMAP:NONE
R2TEXT SEGMENT ALIGN(1) 'CODE'
PUBLIC Audio_1d2f0c0
PUBLIC dump_1d2f0c0
Audio_1d2f0c0 PROC
dump_1d2f0c0 LABEL NEAR
ins_1d2f0c0:
    push rsi
ins_1d2f0c1:
    push rdi
ins_1d2f0c2:
    DB 048h,08bh,0f9h
ins_1d2f0c5:
    DB 048h,08bh,0f2h
ins_1d2f0c8:
    DB 049h,08bh,0d0h
ins_1d2f0cb:
    pushfq
ins_1d2f0cc:
    movsxd rcx, esi
ins_1d2f0cf:
    xor rax, rax
ins_1d2f0d2:
    mov rdx, qword ptr [rsp]
ins_1d2f0d6:
    test edx, 0400h
ins_1d2f0dc:
    je SHORT ins_1d2f0df
ins_1d2f0de:
    cld
ins_1d2f0df:
    rep stosb byte ptr [rdi], al
ins_1d2f0e1:
    test edx, 0400h
ins_1d2f0e7:
    je SHORT ins_1d2f0ea
ins_1d2f0e9:
    std
ins_1d2f0ea:
    pop rax
ins_1d2f0eb:
    vzeroupper
ins_1d2f0ee:
    pop rdi
ins_1d2f0ef:
    pop rsi
ins_1d2f0f0:
    ret
ins_1d2f0f1:
    DB 0cch
ins_1d2f0f2:
    DB 0cch
ins_1d2f0f3:
    DB 0cch
ins_1d2f0f4:
    DB 0cch
ins_1d2f0f5:
    DB 0cch
ins_1d2f0f6:
    DB 0cch
ins_1d2f0f7:
    DB 0cch
ins_1d2f0f8:
    DB 0cch
ins_1d2f0f9:
    DB 0cch
ins_1d2f0fa:
    DB 0cch
ins_1d2f0fb:
    DB 0cch
ins_1d2f0fc:
    DB 0cch
ins_1d2f0fd:
    DB 0cch
ins_1d2f0fe:
    DB 0cch
ins_1d2f0ff:
    DB 0cch
ins_1d2f100:
    push rsi
ins_1d2f101:
    push rdi
ins_1d2f102:
    DB 048h,08bh,0f9h
ins_1d2f105:
    DB 048h,08bh,0f2h
ins_1d2f108:
    DB 049h,08bh,0d0h
ins_1d2f10b:
    DB 048h,08bh,0c6h
ins_1d2f10e:
    vmovq xmm0, rdi
ins_1d2f113:
    movsxd rdi, edx
ins_1d2f116:
    lea rdi, [rdi*4]
ins_1d2f11e:
    vpunpckldq xmm0, xmm0, xmm0
ins_1d2f122:
    vpunpcklqdq xmm0, xmm0, xmm0
ins_1d2f126:
    vmovq rdx, xmm0
ins_1d2f12b:
    vperm2f128 ymm0, ymm0, ymm0, 0
ins_1d2f131:
    test rsi, 3
ins_1d2f138:
    jne NEAR PTR ins_1d2f2a6
ins_1d2f13e:
    cmp rdi, 0100h
ins_1d2f145:
    jge NEAR PTR ins_1d2f1df
ins_1d2f14b:
    test rdi, 080h
ins_1d2f152:
    je SHORT ins_1d2f177
ins_1d2f154:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f158:
    vmovdqu ymmword ptr [rsi + 020h], ymm0
ins_1d2f15d:
    vmovdqu ymmword ptr [rsi + 040h], ymm0
ins_1d2f162:
    vmovdqu ymmword ptr [rsi + 060h], ymm0
ins_1d2f167:
    add rsi, 080h
ins_1d2f16e:
    sub rdi, 080h
ins_1d2f175:
    je SHORT ins_1d2f1d9
ins_1d2f177:
    test rdi, 040h
ins_1d2f17e:
    je SHORT ins_1d2f193
ins_1d2f180:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f184:
    vmovdqu ymmword ptr [rsi + 020h], ymm0
ins_1d2f189:
    add rsi, 040h
ins_1d2f18d:
    sub rdi, 040h
ins_1d2f191:
    je SHORT ins_1d2f1d9
ins_1d2f193:
    test rdi, 020h
ins_1d2f19a:
    je SHORT ins_1d2f1aa
ins_1d2f19c:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f1a0:
    add rsi, 020h
ins_1d2f1a4:
    sub rdi, 020h
ins_1d2f1a8:
    je SHORT ins_1d2f1d9
ins_1d2f1aa:
    test rdi, 010h
ins_1d2f1b1:
    je SHORT ins_1d2f1c1
ins_1d2f1b3:
    vmovdqu xmmword ptr [rsi], xmm0
ins_1d2f1b7:
    add rsi, 010h
ins_1d2f1bb:
    sub rdi, 010h
ins_1d2f1bf:
    je SHORT ins_1d2f1d9
ins_1d2f1c1:
    test rdi, 8
ins_1d2f1c8:
    je SHORT ins_1d2f1d7
ins_1d2f1ca:
    mov qword ptr [rsi], rdx
ins_1d2f1cd:
    add rsi, 8
ins_1d2f1d1:
    sub rdi, 8
ins_1d2f1d5:
    je SHORT ins_1d2f1d9
ins_1d2f1d7:
    mov dword ptr [rsi], edx
ins_1d2f1d9:
    vzeroupper
ins_1d2f1dc:
    pop rdi
ins_1d2f1dd:
    pop rsi
ins_1d2f1de:
    ret
ins_1d2f1df:
    test rsi, 01fh
ins_1d2f1e6:
    je SHORT ins_1d2f1fd
ins_1d2f1e8:
    DB 048h,08bh,0ceh
ins_1d2f1eb:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f1ef:
    and rcx, 01fh
ins_1d2f1f3:
    sub rcx, 020h
ins_1d2f1f7:
    sub rsi, rcx
ins_1d2f1fa:
    add rdi, rcx
ins_1d2f1fd:
    cmp rdi, 08000h
ins_1d2f204:
    jge SHORT ins_1d2f264
ins_1d2f206:
    sub rdi, 0100h
ins_1d2f20d:
    jl SHORT ins_1d2f252
ins_1d2f20f:
    vmovdqa ymmword ptr [rsi + 0e0h], ymm0
ins_1d2f217:
    vmovdqa ymmword ptr [rsi + 0c0h], ymm0
ins_1d2f21f:
    vmovdqa ymmword ptr [rsi + 0a0h], ymm0
ins_1d2f227:
    vmovdqa ymmword ptr [rsi + 080h], ymm0
ins_1d2f22f:
    vmovdqa ymmword ptr [rsi + 060h], ymm0
ins_1d2f234:
    vmovdqa ymmword ptr [rsi + 040h], ymm0
ins_1d2f239:
    vmovdqa ymmword ptr [rsi + 020h], ymm0
ins_1d2f23e:
    vmovdqa ymmword ptr [rsi], ymm0
ins_1d2f242:
    add rsi, 0100h
ins_1d2f249:
    sub rdi, 0100h
ins_1d2f250:
    jge SHORT ins_1d2f20f
ins_1d2f252:
    add rdi, 0100h
ins_1d2f259:
    jne NEAR PTR ins_1d2f14b
ins_1d2f25f:
    jmp NEAR PTR ins_1d2f1d9
ins_1d2f264:
    test rdi, 03fh
ins_1d2f26b:
    je SHORT ins_1d2f283
ins_1d2f26d:
    DB 048h,08bh,0cfh
ins_1d2f270:
    vmovdqu ymmword ptr [rdi + rsi - 020h], ymm0
ins_1d2f276:
    vmovdqu ymmword ptr [rdi + rsi - 040h], ymm0
ins_1d2f27c:
    and rcx, 03fh
ins_1d2f280:
    sub rdi, rcx
ins_1d2f283:
    vmovdqa xmmword ptr [rdi + rsi - 040h], xmm0
ins_1d2f289:
    vmovdqa xmmword ptr [rdi + rsi - 030h], xmm0
ins_1d2f28f:
    vmovdqa xmmword ptr [rdi + rsi - 020h], xmm0
ins_1d2f295:
    vmovdqa xmmword ptr [rdi + rsi - 010h], xmm0
ins_1d2f29b:
    sub rdi, 040h
ins_1d2f29f:
    jne SHORT ins_1d2f283
ins_1d2f2a1:
    jmp NEAR PTR ins_1d2f1d9
ins_1d2f2a6:
    mov dword ptr [rsi], edx
ins_1d2f2a8:
    add rsi, 4
ins_1d2f2ac:
    sub rdi, 4
ins_1d2f2b0:
    jne SHORT ins_1d2f2a6
ins_1d2f2b2:
    jmp NEAR PTR ins_1d2f1d9
ins_1d2f2b7:
    DB 066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f2c0:
    push rsi
ins_1d2f2c1:
    push rdi
ins_1d2f2c2:
    DB 048h,08bh,0f9h
ins_1d2f2c5:
    DB 048h,08bh,0f2h
ins_1d2f2c8:
    DB 049h,08bh,0d0h
ins_1d2f2cb:
    DB 048h,08bh,0c6h
ins_1d2f2ce:
    vmovq xmm0, rdi
ins_1d2f2d3:
    movsxd rdi, edx
ins_1d2f2d6:
    lea rdi, [rdi*2]
ins_1d2f2de:
    vpunpcklwd xmm0, xmm0, xmm0
ins_1d2f2e2:
    vpunpckldq xmm0, xmm0, xmm0
ins_1d2f2e6:
    vpunpcklqdq xmm0, xmm0, xmm0
ins_1d2f2ea:
    vmovq rdx, xmm0
ins_1d2f2ef:
    vperm2f128 ymm0, ymm0, ymm0, 0
ins_1d2f2f5:
    test rsi, 1
ins_1d2f2fc:
    jne NEAR PTR ins_1d2f480
ins_1d2f302:
    cmp rdi, 0100h
ins_1d2f309:
    jge NEAR PTR ins_1d2f3b9
ins_1d2f30f:
    test rdi, 080h
ins_1d2f316:
    je SHORT ins_1d2f33b
ins_1d2f318:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f31c:
    vmovdqu ymmword ptr [rsi + 020h], ymm0
ins_1d2f321:
    vmovdqu ymmword ptr [rsi + 040h], ymm0
ins_1d2f326:
    vmovdqu ymmword ptr [rsi + 060h], ymm0
ins_1d2f32b:
    add rsi, 080h
ins_1d2f332:
    sub rdi, 080h
ins_1d2f339:
    je SHORT ins_1d2f3b3
ins_1d2f33b:
    test rdi, 040h
ins_1d2f342:
    je SHORT ins_1d2f357
ins_1d2f344:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f348:
    vmovdqu ymmword ptr [rsi + 020h], ymm0
ins_1d2f34d:
    add rsi, 040h
ins_1d2f351:
    sub rdi, 040h
ins_1d2f355:
    je SHORT ins_1d2f3b3
ins_1d2f357:
    test rdi, 020h
ins_1d2f35e:
    je SHORT ins_1d2f36e
ins_1d2f360:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f364:
    add rsi, 020h
ins_1d2f368:
    sub rdi, 020h
ins_1d2f36c:
    je SHORT ins_1d2f3b3
ins_1d2f36e:
    test rdi, 010h
ins_1d2f375:
    je SHORT ins_1d2f385
ins_1d2f377:
    vmovdqu xmmword ptr [rsi], xmm0
ins_1d2f37b:
    add rsi, 010h
ins_1d2f37f:
    sub rdi, 010h
ins_1d2f383:
    je SHORT ins_1d2f3b3
ins_1d2f385:
    test rdi, 8
ins_1d2f38c:
    je SHORT ins_1d2f39b
ins_1d2f38e:
    mov qword ptr [rsi], rdx
ins_1d2f391:
    add rsi, 8
ins_1d2f395:
    sub rdi, 8
ins_1d2f399:
    je SHORT ins_1d2f3b3
ins_1d2f39b:
    test rdi, 4
ins_1d2f3a2:
    je SHORT ins_1d2f3b0
ins_1d2f3a4:
    mov dword ptr [rsi], edx
ins_1d2f3a6:
    add rsi, 4
ins_1d2f3aa:
    sub rdi, 4
ins_1d2f3ae:
    je SHORT ins_1d2f3b3
ins_1d2f3b0:
    mov word ptr [rsi], dx
ins_1d2f3b3:
    vzeroupper
ins_1d2f3b6:
    pop rdi
ins_1d2f3b7:
    pop rsi
ins_1d2f3b8:
    ret
ins_1d2f3b9:
    test rsi, 01fh
ins_1d2f3c0:
    je SHORT ins_1d2f3d7
ins_1d2f3c2:
    DB 048h,08bh,0ceh
ins_1d2f3c5:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f3c9:
    and rcx, 01fh
ins_1d2f3cd:
    sub rcx, 020h
ins_1d2f3d1:
    sub rsi, rcx
ins_1d2f3d4:
    add rdi, rcx
ins_1d2f3d7:
    cmp rdi, 08000h
ins_1d2f3de:
    jge SHORT ins_1d2f43e
ins_1d2f3e0:
    sub rdi, 0100h
ins_1d2f3e7:
    jl SHORT ins_1d2f42c
ins_1d2f3e9:
    vmovdqa ymmword ptr [rsi + 0e0h], ymm0
ins_1d2f3f1:
    vmovdqa ymmword ptr [rsi + 0c0h], ymm0
ins_1d2f3f9:
    vmovdqa ymmword ptr [rsi + 0a0h], ymm0
ins_1d2f401:
    vmovdqa ymmword ptr [rsi + 080h], ymm0
ins_1d2f409:
    vmovdqa ymmword ptr [rsi + 060h], ymm0
ins_1d2f40e:
    vmovdqa ymmword ptr [rsi + 040h], ymm0
ins_1d2f413:
    vmovdqa ymmword ptr [rsi + 020h], ymm0
ins_1d2f418:
    vmovdqa ymmword ptr [rsi], ymm0
ins_1d2f41c:
    add rsi, 0100h
ins_1d2f423:
    sub rdi, 0100h
ins_1d2f42a:
    jge SHORT ins_1d2f3e9
ins_1d2f42c:
    add rdi, 0100h
ins_1d2f433:
    jne NEAR PTR ins_1d2f30f
ins_1d2f439:
    jmp NEAR PTR ins_1d2f3b3
ins_1d2f43e:
    test rdi, 03fh
ins_1d2f445:
    je SHORT ins_1d2f45d
ins_1d2f447:
    DB 048h,08bh,0cfh
ins_1d2f44a:
    vmovdqu ymmword ptr [rdi + rsi - 020h], ymm0
ins_1d2f450:
    vmovdqu ymmword ptr [rdi + rsi - 040h], ymm0
ins_1d2f456:
    and rcx, 03fh
ins_1d2f45a:
    sub rdi, rcx
ins_1d2f45d:
    vmovdqa xmmword ptr [rdi + rsi - 040h], xmm0
ins_1d2f463:
    vmovdqa xmmword ptr [rdi + rsi - 030h], xmm0
ins_1d2f469:
    vmovdqa xmmword ptr [rdi + rsi - 020h], xmm0
ins_1d2f46f:
    vmovdqa xmmword ptr [rdi + rsi - 010h], xmm0
ins_1d2f475:
    sub rdi, 040h
ins_1d2f479:
    jne SHORT ins_1d2f45d
ins_1d2f47b:
    jmp NEAR PTR ins_1d2f3b3
ins_1d2f480:
    mov word ptr [rsi], dx
ins_1d2f483:
    add rsi, 2
ins_1d2f487:
    sub rdi, 2
ins_1d2f48b:
    jne SHORT ins_1d2f480
ins_1d2f48d:
    jmp NEAR PTR ins_1d2f3b3
ins_1d2f492:
    DB 066h,066h,066h,066h,066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f4a1:
    DB 066h,066h,066h,066h,066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f4b0:
    DB 066h,066h,066h,066h,066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f4bf:
    DB 090h
ins_1d2f4c0:
    push rsi
ins_1d2f4c1:
    push rdi
ins_1d2f4c2:
    DB 048h,08bh,0f9h
ins_1d2f4c5:
    DB 048h,08bh,0f2h
ins_1d2f4c8:
    DB 049h,08bh,0d0h
ins_1d2f4cb:
    DB 048h,08bh,0c6h
ins_1d2f4ce:
    vmovq xmm0, rdi
ins_1d2f4d3:
    movsxd rdi, edx
ins_1d2f4d6:
    vpunpcklbw xmm0, xmm0, xmm0
ins_1d2f4da:
    vpunpcklwd xmm0, xmm0, xmm0
ins_1d2f4de:
    vpunpckldq xmm0, xmm0, xmm0
ins_1d2f4e2:
    vpunpcklqdq xmm0, xmm0, xmm0
ins_1d2f4e6:
    vmovq rdx, xmm0
ins_1d2f4eb:
    vperm2f128 ymm0, ymm0, ymm0, 0
ins_1d2f4f1:
    cmp rdi, 0100h
ins_1d2f4f8:
    jge NEAR PTR ins_1d2f5c1
ins_1d2f4fe:
    test rdi, 080h
ins_1d2f505:
    je SHORT ins_1d2f52e
ins_1d2f507:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f50b:
    vmovdqu ymmword ptr [rsi + 020h], ymm0
ins_1d2f510:
    vmovdqu ymmword ptr [rsi + 040h], ymm0
ins_1d2f515:
    vmovdqu ymmword ptr [rsi + 060h], ymm0
ins_1d2f51a:
    add rsi, 080h
ins_1d2f521:
    sub rdi, 080h
ins_1d2f528:
    je NEAR PTR ins_1d2f5bb
ins_1d2f52e:
    test rdi, 040h
ins_1d2f535:
    je SHORT ins_1d2f54a
ins_1d2f537:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f53b:
    vmovdqu ymmword ptr [rsi + 020h], ymm0
ins_1d2f540:
    add rsi, 040h
ins_1d2f544:
    sub rdi, 040h
ins_1d2f548:
    je SHORT ins_1d2f5bb
ins_1d2f54a:
    test rdi, 020h
ins_1d2f551:
    je SHORT ins_1d2f561
ins_1d2f553:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f557:
    add rsi, 020h
ins_1d2f55b:
    sub rdi, 020h
ins_1d2f55f:
    je SHORT ins_1d2f5bb
ins_1d2f561:
    test rdi, 010h
ins_1d2f568:
    je SHORT ins_1d2f578
ins_1d2f56a:
    vmovdqu xmmword ptr [rsi], xmm0
ins_1d2f56e:
    add rsi, 010h
ins_1d2f572:
    sub rdi, 010h
ins_1d2f576:
    je SHORT ins_1d2f5bb
ins_1d2f578:
    test rdi, 8
ins_1d2f57f:
    je SHORT ins_1d2f58e
ins_1d2f581:
    mov qword ptr [rsi], rdx
ins_1d2f584:
    add rsi, 8
ins_1d2f588:
    sub rdi, 8
ins_1d2f58c:
    je SHORT ins_1d2f5bb
ins_1d2f58e:
    test rdi, 4
ins_1d2f595:
    je SHORT ins_1d2f5a3
ins_1d2f597:
    mov dword ptr [rsi], edx
ins_1d2f599:
    add rsi, 4
ins_1d2f59d:
    sub rdi, 4
ins_1d2f5a1:
    je SHORT ins_1d2f5bb
ins_1d2f5a3:
    test rdi, 2
ins_1d2f5aa:
    je SHORT ins_1d2f5b9
ins_1d2f5ac:
    mov word ptr [rsi], dx
ins_1d2f5af:
    add rsi, 2
ins_1d2f5b3:
    sub rdi, 2
ins_1d2f5b7:
    je SHORT ins_1d2f5bb
ins_1d2f5b9:
    mov byte ptr [rsi], dl
ins_1d2f5bb:
    vzeroupper
ins_1d2f5be:
    pop rdi
ins_1d2f5bf:
    pop rsi
ins_1d2f5c0:
    ret
ins_1d2f5c1:
    test rsi, 01fh
ins_1d2f5c8:
    je SHORT ins_1d2f5df
ins_1d2f5ca:
    DB 048h,08bh,0ceh
ins_1d2f5cd:
    vmovdqu ymmword ptr [rsi], ymm0
ins_1d2f5d1:
    and rcx, 01fh
ins_1d2f5d5:
    sub rcx, 020h
ins_1d2f5d9:
    sub rsi, rcx
ins_1d2f5dc:
    add rdi, rcx
ins_1d2f5df:
    cmp rdi, 08000h
ins_1d2f5e6:
    jge SHORT ins_1d2f646
ins_1d2f5e8:
    sub rdi, 0100h
ins_1d2f5ef:
    jl SHORT ins_1d2f634
ins_1d2f5f1:
    vmovdqa ymmword ptr [rsi + 0e0h], ymm0
ins_1d2f5f9:
    vmovdqa ymmword ptr [rsi + 0c0h], ymm0
ins_1d2f601:
    vmovdqa ymmword ptr [rsi + 0a0h], ymm0
ins_1d2f609:
    vmovdqa ymmword ptr [rsi + 080h], ymm0
ins_1d2f611:
    vmovdqa ymmword ptr [rsi + 060h], ymm0
ins_1d2f616:
    vmovdqa ymmword ptr [rsi + 040h], ymm0
ins_1d2f61b:
    vmovdqa ymmword ptr [rsi + 020h], ymm0
ins_1d2f620:
    vmovdqa ymmword ptr [rsi], ymm0
ins_1d2f624:
    add rsi, 0100h
ins_1d2f62b:
    sub rdi, 0100h
ins_1d2f632:
    jge SHORT ins_1d2f5f1
ins_1d2f634:
    add rdi, 0100h
ins_1d2f63b:
    jne NEAR PTR ins_1d2f4fe
ins_1d2f641:
    jmp NEAR PTR ins_1d2f5bb
ins_1d2f646:
    test rdi, 03fh
ins_1d2f64d:
    je SHORT ins_1d2f665
ins_1d2f64f:
    DB 048h,08bh,0cfh
ins_1d2f652:
    vmovdqu ymmword ptr [rdi + rsi - 020h], ymm0
ins_1d2f658:
    vmovdqu ymmword ptr [rdi + rsi - 040h], ymm0
ins_1d2f65e:
    and rcx, 03fh
ins_1d2f662:
    sub rdi, rcx
ins_1d2f665:
    vmovdqa xmmword ptr [rdi + rsi - 040h], xmm0
ins_1d2f66b:
    vmovdqa xmmword ptr [rdi + rsi - 030h], xmm0
ins_1d2f671:
    vmovdqa xmmword ptr [rdi + rsi - 020h], xmm0
ins_1d2f677:
    vmovdqa xmmword ptr [rdi + rsi - 010h], xmm0
ins_1d2f67d:
    sub rdi, 040h
ins_1d2f681:
    jne SHORT ins_1d2f665
ins_1d2f683:
    jmp NEAR PTR ins_1d2f5bb
ins_1d2f688:
    DB 066h,066h,066h,066h,066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f697:
    DB 066h,066h,066h,066h,066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f6a6:
    DB 066h,066h,066h,066h,066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f6b5:
    DB 066h,066h,066h,00fh,01fh,084h,000h,000h,000h,000h,000h
ins_1d2f6c0:
    push rsi
ins_1d2f6c1:
    push rdi
ins_1d2f6c2:
    DB 048h,08bh,0f9h
ins_1d2f6c5:
    DB 048h,08bh,0f2h
ins_1d2f6c8:
    DB 048h,08bh,0c7h
ins_1d2f6cb:
    movsxd rsi, esi
ins_1d2f6ce:
    vxorps ymm0, ymm0, ymm0
ins_1d2f6d2:
    xor rdx, rdx
ins_1d2f6d5:
    cmp rsi, 0100h
ins_1d2f6dc:
    jge NEAR PTR ins_1d2f7a5
ins_1d2f6e2:
    test rsi, 080h
ins_1d2f6e9:
    je SHORT ins_1d2f712
ins_1d2f6eb:
    vmovdqu ymmword ptr [rdi], ymm0
ins_1d2f6ef:
    vmovdqu ymmword ptr [rdi + 020h], ymm0
ins_1d2f6f4:
    vmovdqu ymmword ptr [rdi + 040h], ymm0
ins_1d2f6f9:
    vmovdqu ymmword ptr [rdi + 060h], ymm0
ins_1d2f6fe:
    add rdi, 080h
ins_1d2f705:
    sub rsi, 080h
ins_1d2f70c:
    je NEAR PTR ins_1d2f79f
ins_1d2f712:
    test rsi, 040h
ins_1d2f719:
    je SHORT ins_1d2f72e
ins_1d2f71b:
    vmovdqu ymmword ptr [rdi], ymm0
ins_1d2f71f:
    vmovdqu ymmword ptr [rdi + 020h], ymm0
ins_1d2f724:
    add rdi, 040h
ins_1d2f728:
    sub rsi, 040h
ins_1d2f72c:
    je SHORT ins_1d2f79f
ins_1d2f72e:
    test rsi, 020h
ins_1d2f735:
    je SHORT ins_1d2f745
ins_1d2f737:
    vmovdqu ymmword ptr [rdi], ymm0
ins_1d2f73b:
    add rdi, 020h
ins_1d2f73f:
    sub rsi, 020h
ins_1d2f743:
    je SHORT ins_1d2f79f
ins_1d2f745:
    test rsi, 010h
ins_1d2f74c:
    je SHORT ins_1d2f75c
ins_1d2f74e:
    vmovdqu xmmword ptr [rdi], xmm0
ins_1d2f752:
    add rdi, 010h
ins_1d2f756:
    sub rsi, 010h
ins_1d2f75a:
    je SHORT ins_1d2f79f
ins_1d2f75c:
    test rsi, 8
ins_1d2f763:
    je SHORT ins_1d2f772
ins_1d2f765:
    mov qword ptr [rdi], rdx
ins_1d2f768:
    add rdi, 8
ins_1d2f76c:
    sub rsi, 8
ins_1d2f770:
    je SHORT ins_1d2f79f
ins_1d2f772:
    test rsi, 4
ins_1d2f779:
    je SHORT ins_1d2f787
ins_1d2f77b:
    mov dword ptr [rdi], edx
ins_1d2f77d:
    add rdi, 4
ins_1d2f781:
    sub rsi, 4
ins_1d2f785:
    je SHORT ins_1d2f79f
ins_1d2f787:
    test rsi, 2
ins_1d2f78e:
    je SHORT ins_1d2f79d
ins_1d2f790:
    mov word ptr [rdi], dx
ins_1d2f793:
    add rdi, 2
ins_1d2f797:
    sub rsi, 2
ins_1d2f79b:
    je SHORT ins_1d2f79f
ins_1d2f79d:
    mov byte ptr [rdi], dl
ins_1d2f79f:
    vzeroupper
ins_1d2f7a2:
    pop rdi
ins_1d2f7a3:
    pop rsi
ins_1d2f7a4:
    ret
ins_1d2f7a5:
    test rdi, 01fh
ins_1d2f7ac:
    je SHORT ins_1d2f7c3
ins_1d2f7ae:
    DB 048h,08bh,0cfh
ins_1d2f7b1:
    vmovdqu ymmword ptr [rdi], ymm0
ins_1d2f7b5:
    and rcx, 01fh
ins_1d2f7b9:
    sub rcx, 020h
ins_1d2f7bd:
    sub rdi, rcx
ins_1d2f7c0:
    add rsi, rcx
ins_1d2f7c3:
    sub rsi, 0100h
ins_1d2f7ca:
    jl SHORT ins_1d2f80f
ins_1d2f7cc:
    vmovdqa ymmword ptr [rdi + 0e0h], ymm0
ins_1d2f7d4:
    vmovdqa ymmword ptr [rdi + 0c0h], ymm0
ins_1d2f7dc:
    vmovdqa ymmword ptr [rdi + 0a0h], ymm0
ins_1d2f7e4:
    vmovdqa ymmword ptr [rdi + 080h], ymm0
ins_1d2f7ec:
    vmovdqa ymmword ptr [rdi + 060h], ymm0
ins_1d2f7f1:
    vmovdqa ymmword ptr [rdi + 040h], ymm0
ins_1d2f7f6:
    vmovdqa ymmword ptr [rdi + 020h], ymm0
ins_1d2f7fb:
    vmovdqa ymmword ptr [rdi], ymm0
ins_1d2f7ff:
    add rdi, 0100h
ins_1d2f806:
    sub rsi, 0100h
ins_1d2f80d:
    jge SHORT ins_1d2f7cc
ins_1d2f80f:
    add rsi, 0100h
ins_1d2f816:
    jne NEAR PTR ins_1d2f6e2
ins_1d2f81c:
    jmp SHORT ins_1d2f79f
Audio_1d2f0c0 ENDP
R2TEXT ENDS
END

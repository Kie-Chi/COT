Jarea:
beq $0, $0, JareaEnd
JBackFor16_0:
add $16, $0, $31
jr $16
ori $0, $0, 0x3004
JBackFor16_1:
jr $31
ori $16, $0, 0x3010
JBackFor6_0:
add $6, $0, $31
jr $6
ori $0, $0, 0x3018
JBackFor6_1:
jr $31
ori $6, $0, 0x3024
JBackFor24_0:
add $24, $0, $31
jr $24
ori $0, $0, 0x302c
JBackFor24_1:
jr $31
ori $24, $0, 0x3038
JBackFor15_0:
add $15, $0, $31
jr $15
ori $0, $0, 0x3040
JBackFor15_1:
jr $31
ori $15, $0, 0x304c
JBackFor11_0:
add $11, $0, $31
jr $11
ori $0, $0, 0x3054
JBackFor11_1:
jr $31
ori $11, $0, 0x3060
JBackFor22_0:
add $22, $0, $31
jr $22
ori $0, $0, 0x3068
JBackFor22_1:
jr $31
ori $22, $0, 0x3074
JBackFor9_0:
add $9, $0, $31
jr $9
ori $0, $0, 0x307c
JBackFor9_1:
jr $31
ori $9, $0, 0x3088
JBackFor21_0:
add $21, $0, $31
jr $21
ori $0, $0, 0x3090
JBackFor21_1:
jr $31
ori $21, $0, 0x309c
JBackFor31_0:
jr $31
JareaEnd:
ori $0, $0, 0x96
ori $19, $0, 0xac
ori $25, $0, 0x84
ori $20, $0, 0x49
ori $31, $0, 0x63
ori $16, $0, 0x3010
ori $6, $0, 0x30a4
ori $24, $0, 0x30a4
ori $15, $0, 0x30a4
ori $11, $0, 0x3060
ori $22, $0, 0x30a4
ori $9, $0, 0x3088
ori $21, $0, 0x309c
sw $31, 0($0)
sw $6, 132($0)
sw $24, 80($0)
sw $20, 152($0)
sw $21, 28($0)
sw $20, 168($0)
sw $16, 72($0)
sw $20, 68($0)
sw $9, 116($0)
sw $20, 88($0)
sw $21, 48($0)
sw $20, 144($0)
sw $0, 156($0)
sw $20, 56($0)
sw $21, 108($0)
sw $19, 72($0)
sw $0, 152($0)
sw $21, 64($0)
sw $19, 184($0)
sw $16, 40($0)
Test0Begin:
jal JBackFor31_0
nop
lui $31, 0x0
jr $6
ori $31, $0, 0x3140
jal JBackFor22_0
ori $31, $0, 0x3148
ori $31, $0, 0x3148
Test0End:
ori $22, $0, 0x30a4
ori $31, $0, 0x91
Test1Begin:
lui $0, 0x0
nop
jr $21
ori $31, $0, 0x3164
add $31, $19, $19
ori $31, $0, 0x3168
Test1End:
ori $31, $0, 0x6f
Test2Begin:
sw $20, -160($19)
nop
sw $25, 140($0)
lw $25, 91($20)
ori $31, $0, 0x3180
Test2End:
ori $31, $0, 0x40
Test3Begin:
jal JBackFor31_0
nop
jal JBackFor31_0
nop
jr $22
ori $31, $0, 0x31a0
nop
ori $31, $0, 0x31a4
Test3End:
ori $31, $0, 0x1e
Test4Begin:
lui $31, 0x0
nop
lui $31, 0x0
ori $20, $0, 0x75
ori $31, $0, 0x31bc
Test4End:
ori $31, $0, 0x6b
Test5Begin:
ori $25, $0, 0x85
ori $25, $0, 0x85
beq $25, $25, Test5End
ori $31, $0, 0x31d4
ori $20, $0, 0x4
ori $20, $19, 0x3e
lui $31, 0x0
ori $31, $0, 0x31e0
Test5End:
ori $31, $0, 0xc6
Test6Begin:
lw $31, 31($25)
ori $25, $19, 0x19
jal JBackFor31_0
nop
sub $25, $31, $31
ori $31, $0, 0x31fc
Test6End:
ori $31, $0, 0x7b
Test7Begin:
lw $0, 48($25)
sub $19, $31, $19
ori $31, $19, 0x3c
sw $25, 85($19)
ori $31, $0, 0x3214
Test7End:
ori $31, $0, 0xb1
Test8Begin:
sub $20, $19, $20
ori $20, $20, 0x6
jr $11
ori $31, $0, 0x322c
lui $20, 0x0
ori $31, $0, 0x3230
Test8End:
ori $31, $0, 0x10
Test9Begin:
ori $20, $0, 0xc2
ori $19, $0, 0xc2
beq $20, $19, Test9End
ori $31, $0, 0x3248
nop
jr $11
ori $31, $0, 0x3254
add $20, $20, $25
ori $31, $0, 0x3258
Test9End:
ori $31, $0, 0xc
Test10Begin:
add $20, $20, $19
jal JBackFor11_0
ori $31, $0, 0x326c
jal JBackFor31_0
nop
jr $9
ori $31, $0, 0x327c
ori $31, $0, 0x327c
Test10End:
ori $11, $0, 0x3060
ori $20, $0, 0xc7
ori $31, $0, 0x13
Test11Begin:
jal JBackFor31_0
nop
jal JBackFor22_0
ori $31, $0, 0x329c
lui $31, 0x0
lw $25, 88($25)
ori $31, $0, 0x32a4
Test11End:
ori $22, $0, 0x30a4
ori $31, $0, 0x8f
Test12Begin:
jal JBackFor24_0
ori $31, $0, 0x32b8
sub $20, $19, $31
lui $19, 0x0
sw $0, 12878($20)
ori $31, $0, 0x32c4
Test12End:
ori $24, $0, 0x30a4
ori $20, $0, 0x9f
ori $31, $0, 0x9c
Test13Begin:
ori $25, $0, 0xa1
ori $19, $0, 0xa1
beq $25, $19, Test13End
ori $31, $0, 0x32e4
lui $19, 0x0
lw $0, -12904($31)
jr $9
ori $31, $0, 0x32f4
ori $31, $0, 0x32f4
Test13End:
ori $31, $0, 0x7c
Test14Begin:
add $19, $19, $31
nop
jr $24
ori $31, $0, 0x330c
sw $25, 76($0)
ori $31, $0, 0x3310
Test14End:
ori $19, $0, 0x81
ori $31, $0, 0x24
Test15Begin:
ori $0, $0, 0x1a
ori $0, $0, 0x1a
ori $19, $25, 0x18
beq $0, $0, Test15End
ori $31, $0, 0x3330
nop
jr $15
ori $31, $0, 0x333c
ori $31, $0, 0x333c
Test15End:
ori $31, $0, 0x1
Test16Begin:
sw $31, -61($25)
lw $20, 183($31)
ori $25, $25, 0x23
nop
ori $31, $0, 0x3354
Test16End:
ori $31, $0, 0x47
Test17Begin:
ori $19, $0, 0xc6
ori $0, $0, 0xc6
beq $19, $0, Test17End
ori $31, $0, 0x336c
lui $31, 0x0
jr $24
ori $31, $0, 0x3378
sub $0, $0, $25
ori $31, $0, 0x337c
Test17End:
ori $31, $0, 0xb9
Test18Begin:
ori $19, $0, 0xf
ori $25, $0, 0xf
lui $25, 0x0
ori $19, $19, 0x8f
beq $19, $25, Test18End
ori $31, $0, 0x339c
jal JBackFor21_0
ori $31, $0, 0x33a4
ori $31, $0, 0x33a4
Test18End:
ori $21, $0, 0x30a4
ori $31, $0, 0x6d
Test19Begin:
jal JBackFor24_0
ori $31, $0, 0x33b8
lui $19, 0x0
sub $0, $31, $19
add $19, $0, $19
ori $31, $0, 0x33c4
Test19End:
ori $24, $0, 0x3038
ori $31, $0, 0x3b
Test20Begin:
ori $19, $20, 0x3e
sw $20, -110($19)
lui $0, 0x0
sw $0, -15($31)
ori $31, $0, 0x33e0
Test20End:
ori $31, $0, 0x30
Test21Begin:
add $0, $19, $25
jal JBackFor31_0
nop
nop
ori $19, $0, 0x36
ori $31, $0, 0x33fc
Test21End:
ori $31, $0, 0x62
Test22Begin:
ori $0, $0, 0x50
ori $20, $0, 0x50
sub $0, $20, $19
beq $0, $20, Test22End
ori $31, $0, 0x3418
sub $19, $25, $25
nop
ori $31, $0, 0x3420
Test22End:
ori $31, $0, 0x2a
Test23Begin:
sub $31, $19, $0
jr $24
ori $31, $0, 0x3434
jr $15
ori $31, $0, 0x343c
lw $0, 156($0)
ori $31, $0, 0x3440
Test23End:
ori $31, $0, 0x29
Test24Begin:
ori $25, $0, 0x5d
ori $0, $0, 0x5d
ori $20, $0, 0x60
ori $0, $0, 0x60
beq $25, $0, Test24End
ori $31, $0, 0x3460
sw $31, 80($20)
sw $25, 48($19)
beq $20, $0, Test24End
ori $31, $0, 0x3470
ori $31, $0, 0x3470
Test24End:
ori $31, $0, 0x7e
Test25Begin:
ori $20, $0, 0xbc
ori $31, $0, 0xbc
ori $20, $0, 0xba
ori $25, $0, 0xba
beq $20, $31, Test25End
ori $31, $0, 0x3490
beq $20, $25, Test25End
ori $31, $0, 0x3498
lw $0, -130($20)
sw $31, 152($0)
ori $31, $0, 0x34a0
Test25End:
ori $31, $0, 0x5b
Test26Begin:
jal JBackFor9_0
ori $31, $0, 0x34b0
lui $31, 0x0
nop
sub $19, $31, $19
ori $31, $0, 0x34bc
Test26End:
ori $9, $0, 0x30a4
ori $31, $0, 0x8f
Test27Begin:
ori $19, $0, 0x71
ori $0, $0, 0x71
ori $25, $0, 0x97
ori $19, $0, 0x97
jal JBackFor15_0
ori $31, $0, 0x34e0
jal JBackFor31_0
nop
beq $19, $0, Test27End
ori $31, $0, 0x34f0
beq $25, $19, Test27End
ori $31, $0, 0x34f8
ori $31, $0, 0x34f8
Test27End:
ori $15, $0, 0x304c
ori $31, $0, 0x6c
Test28Begin:
lui $0, 0x0
jal JBackFor31_0
nop
lui $31, 0x0
ori $31, $20, 0x8d
ori $31, $0, 0x3518
Test28End:
ori $31, $0, 0xbd
Test29Begin:
ori $0, $0, 0x12
ori $20, $0, 0x12
lui $0, 0x0
jal JBackFor31_0
nop
ori $20, $19, 0x6e
beq $0, $20, Test29End
ori $31, $0, 0x3540
ori $31, $0, 0x3540
Test29End:
ori $20, $0, 0x70
ori $31, $0, 0xe
Test30Begin:
ori $25, $19, 0x0
jal JBackFor22_0
ori $31, $0, 0x3558
sub $20, $31, $19
jr $11
ori $31, $0, 0x3564
ori $31, $0, 0x3564
Test30End:
ori $22, $0, 0x3074
ori $20, $0, 0x65
ori $31, $0, 0xc0
Test31Begin:
sw $25, -107($25)
ori $20, $31, 0x6b
nop
sub $19, $25, $25
ori $31, $0, 0x3584
Test31End:
ori $20, $0, 0x11
ori $31, $0, 0x1e
Test32Begin:
jal JBackFor11_0
ori $31, $0, 0x3598
ori $19, $19, 0x43
ori $19, $0, 0x34
lw $0, -13716($31)
ori $31, $0, 0x35a4
Test32End:
ori $11, $0, 0x3060
ori $31, $0, 0x66
Test33Begin:
ori $25, $0, 0x1c
ori $0, $0, 0x1c
beq $25, $0, Test33End
ori $31, $0, 0x35c0
add $25, $25, $19
nop
lui $19, 0x0
ori $31, $0, 0x35cc
Test33End:
ori $31, $0, 0x63
Test34Begin:
lui $19, 0x0
jr $11
ori $31, $0, 0x35e0
lw $0, -13692($31)
lui $0, 0x0
ori $31, $0, 0x35e8
Test34End:
ori $31, $0, 0x60
Test35Begin:
nop
jal JBackFor21_0
ori $31, $0, 0x35fc
nop
jr $22
ori $31, $0, 0x3608
ori $31, $0, 0x3608
Test35End:
ori $21, $0, 0x30a4
ori $31, $0, 0x6c
Test36Begin:
ori $19, $0, 0x68
ori $25, $0, 0x68
sw $0, -64($25)
lui $31, 0x0
beq $19, $25, Test36End
ori $31, $0, 0x362c
lw $19, -13868($31)
ori $31, $0, 0x3630
Test36End:
ori $31, $0, 0x80
Test37Begin:
ori $25, $0, 0xc4
ori $25, $0, 0xc4
jal JBackFor31_0
nop
lui $0, 0x0
jr $6
ori $31, $0, 0x3654
beq $25, $25, Test37End
ori $31, $0, 0x365c
ori $31, $0, 0x365c
Test37End:
ori $31, $0, 0x15
Test38Begin:
ori $0, $0, 0x4f
ori $31, $0, 0x4f
lui $25, 0x0
beq $0, $31, Test38End
ori $31, $0, 0x3678
ori $31, $19, 0xad
sub $0, $31, $25
ori $31, $0, 0x3680
Test38End:
ori $31, $0, 0x4f
Test39Begin:
jal JBackFor24_0
ori $31, $0, 0x3690
lui $25, 0x0
lw $19, 172($25)
sw $20, 103($20)
ori $31, $0, 0x369c
Test39End:
ori $24, $0, 0x3038
ori $31, $0, 0xa
Test40Begin:
ori $20, $0, 0x39
ori $31, $0, 0x39
beq $20, $31, Test40End
ori $31, $0, 0x36b8
jr $24
ori $31, $0, 0x36c0
lw $31, 164($19)
lui $25, 0x0
ori $31, $0, 0x36c8
Test40End:
ori $31, $0, 0x37
Test41Begin:
nop
add $20, $19, $20
sub $31, $20, $25
lw $19, 47($31)
ori $31, $0, 0x36e0
Test41End:
ori $31, $0, 0x5e
Test42Begin:
jr $9
ori $31, $0, 0x36f0
nop
nop
jr $24
ori $31, $0, 0x3700
ori $31, $0, 0x3700
Test42End:
ori $31, $0, 0x7c
Test43Begin:
ori $19, $0, 0x30
ori $19, $0, 0x30
add $19, $20, $0
nop
beq $19, $19, Test43End
ori $31, $0, 0x3720
ori $19, $31, 0x9d
ori $31, $0, 0x3724
Test43End:
ori $31, $0, 0x50
Test44Begin:
ori $19, $0, 0x27
ori $25, $0, 0x27
ori $25, $19, 0x7
beq $19, $25, Test44End
ori $31, $0, 0x3740
nop
lui $0, 0x0
ori $31, $0, 0x3748
Test44End:
ori $31, $0, 0xa6
Test45Begin:
ori $20, $0, 0xbc
ori $25, $0, 0xbc
lw $20, -32($20)
lui $0, 0x0
beq $20, $25, Test45End
ori $31, $0, 0x3768
ori $25, $31, 0xbb
ori $31, $0, 0x376c
Test45End:
ori $25, $0, 0x6b
ori $31, $0, 0x4d
Test46Begin:
ori $0, $19, 0x7e
sw $25, 87($31)
sw $19, -1($31)
ori $0, $0, 0x5d
ori $31, $0, 0x3788
Test46End:
ori $31, $0, 0x2f
Test47Begin:
ori $19, $20, 0x79
lui $0, 0x0
sw $20, -35($25)
sub $31, $0, $31
ori $31, $0, 0x37a0
Test47End:
ori $31, $0, 0x99
Test48Begin:
sub $25, $20, $25
nop
sub $19, $25, $20
lw $19, 263($19)
ori $31, $0, 0x37b8
Test48End:
ori $31, $0, 0x1
Test49Begin:
jal JBackFor31_0
nop
lui $19, 0x0
lw $20, 172($0)
sw $20, -14164($31)
ori $31, $0, 0x37d4
Test49End:
ori $31, $0, 0xa9
Test50Begin:
sw $0, 176($20)
sw $19, 88($19)
ori $20, $25, 0x7e
jr $16
ori $31, $0, 0x37f0
ori $31, $0, 0x37f0
Test50End:
ori $31, $0, 0xbd
Test51Begin:
ori $31, $0, 0x13
ori $0, $0, 0x13
lw $31, 137($20)
lw $0, 129($20)
beq $31, $0, Test51End
ori $31, $0, 0x3810
add $0, $19, $0
ori $31, $0, 0x3814
Test51End:
ori $31, $0, 0x34
Test52Begin:
ori $20, $19, 0xc0
add $25, $19, $19
lw $31, 192($25)
sw $0, 124($19)
ori $31, $0, 0x382c
Test52End:
ori $31, $0, 0x2a
Test53Begin:
ori $25, $0, 0x86
ori $31, $0, 0x86
ori $31, $20, 0x5f
sw $31, -31($31)
nop
beq $25, $31, Test53End
ori $31, $0, 0x3850
ori $31, $0, 0x3850
Test53End:
ori $31, $0, 0xb9
Test54Begin:
jr $6
ori $31, $0, 0x3860
nop
lui $19, 0x0
ori $25, $31, 0x32
ori $31, $0, 0x386c
Test54End:
ori $25, $0, 0x13
ori $31, $0, 0x12
Test55Begin:
lui $19, 0x0
sw $31, 25($25)
lw $20, 53($25)
lw $20, 104($20)
ori $31, $0, 0x3888
Test55End:
ori $31, $0, 0xb7
Test56Begin:
lui $20, 0x0
ori $31, $19, 0x37
sw $25, 112($0)
lw $31, 16($0)
ori $31, $0, 0x38a0
Test56End:
ori $31, $0, 0x29
Test57Begin:
ori $25, $0, 0x21
ori $0, $0, 0x21
beq $25, $0, Test57End
ori $31, $0, 0x38b8
jal JBackFor11_0
ori $31, $0, 0x38c0
nop
jal JBackFor31_0
nop
ori $31, $0, 0x38cc
Test57End:
ori $11, $0, 0x30a4
ori $31, $0, 0x22
Test58Begin:
nop
lw $25, 55($25)
sub $0, $31, $19
jr $21
ori $31, $0, 0x38ec
ori $31, $0, 0x38ec
Test58End:
ori $31, $0, 0xb9
Test59Begin:
sw $25, 168($25)
lui $31, 0x0
sw $31, 32($31)
nop
ori $31, $0, 0x3904
Test59End:
ori $31, $0, 0x35
Test60Begin:
ori $19, $0, 0x59
ori $31, $0, 0x59
sw $25, 192($25)
jr $21
ori $31, $0, 0x3920
ori $20, $20, 0x8f
beq $19, $31, Test60End
ori $31, $0, 0x392c
ori $31, $0, 0x392c
Test60End:
ori $31, $0, 0x5
Test61Begin:
jr $16
ori $31, $0, 0x393c
jal JBackFor16_0
ori $31, $0, 0x3944
nop
add $0, $25, $25
ori $31, $0, 0x394c
Test61End:
ori $16, $0, 0x3010
ori $31, $0, 0x17
Test62Begin:
lw $31, 176($25)
sw $20, 184($0)
lui $31, 0x0
jr $16
ori $31, $0, 0x396c
ori $31, $0, 0x396c
Test62End:
ori $31, $0, 0x48
Test63Begin:
nop
nop
ori $19, $31, 0xb4
jal JBackFor11_0
ori $31, $0, 0x3988
ori $31, $0, 0x3988
Test63End:
ori $11, $0, 0x30a4
ori $19, $0, 0x4b
ori $31, $0, 0xb
Test64Begin:
ori $20, $0, 0x77
ori $31, $0, 0x77
beq $20, $31, Test64End
ori $31, $0, 0x39a8
nop
lw $31, 188($25)
ori $19, $31, 0x5b
ori $31, $0, 0x39b4
Test64End:
ori $31, $0, 0x9b
Test65Begin:
lw $25, 61($19)
lw $0, 68($25)
lui $25, 0x0
jal JBackFor31_0
nop
ori $31, $0, 0x39d0
Test65End:
ori $31, $0, 0x31
Test66Begin:
lui $31, 0x0
jal JBackFor24_0
ori $31, $0, 0x39e4
ori $20, $31, 0x71
jr $15
ori $31, $0, 0x39f0
ori $31, $0, 0x39f0
Test66End:
ori $24, $0, 0x3038
ori $20, $0, 0x3f
ori $31, $0, 0xa2
Test67Begin:
jr $24
ori $31, $0, 0x3a08
jal JBackFor6_0
ori $31, $0, 0x3a10
jal JBackFor9_0
ori $31, $0, 0x3a18
ori $31, $19, 0x87
ori $31, $0, 0x3a1c
Test67End:
ori $6, $0, 0x30a4
ori $9, $0, 0x30a4
ori $31, $0, 0x6c
Test68Begin:
ori $20, $0, 0x2f
ori $19, $0, 0x2f
beq $20, $19, Test68End
ori $31, $0, 0x3a3c
lw $25, -14772($31)
add $19, $0, $31
add $0, $19, $19
ori $31, $0, 0x3a48
Test68End:
ori $31, $0, 0xc3
Test69Begin:
ori $20, $0, 0x5
ori $0, $0, 0x5
ori $31, $0, 0x82
ori $0, $0, 0x82
beq $20, $0, Test69End
ori $31, $0, 0x3a68
nop
beq $31, $0, Test69End
ori $31, $0, 0x3a74
ori $19, $0, 0xa4
ori $31, $0, 0x3a78
Test69End:
ori $31, $0, 0x39
Test70Begin:
ori $25, $0, 0x21
ori $19, $0, 0x21
lw $20, 131($25)
jal JBackFor31_0
nop
jr $16
ori $31, $0, 0x3a9c
beq $25, $19, Test70End
ori $31, $0, 0x3aa4
ori $31, $0, 0x3aa4
Test70End:
ori $31, $0, 0x13
Test71Begin:
ori $20, $0, 0x19
ori $31, $0, 0x19
lw $25, -25($25)
sub $20, $25, $31
beq $20, $31, Test71End
ori $31, $0, 0x3ac4
sw $0, -14868($31)
ori $31, $0, 0x3ac8
Test71End:
ori $31, $0, 0x78
Test72Begin:
ori $25, $20, 0xc5
jal JBackFor16_0
ori $31, $0, 0x3adc
sw $25, 65($25)
lw $20, 163($19)
ori $31, $0, 0x3ae4
Test72End:
ori $16, $0, 0x30a4
ori $31, $0, 0xa9
Test73Begin:
ori $20, $0, 0xe
ori $20, $0, 0xe
ori $0, $0, 0xc4
ori $0, $0, 0xc4
beq $20, $20, Test73End
ori $31, $0, 0x3b08
sw $20, -15036($31)
beq $0, $0, Test73End
ori $31, $0, 0x3b14
jal JBackFor31_0
nop
ori $31, $0, 0x3b1c
Test73End:
ori $31, $0, 0x7c
Test74Begin:
sw $20, 169($25)
lw $31, -25($19)
jal JBackFor31_0
nop
sw $25, 29($25)
ori $31, $0, 0x3b38
Test74End:
ori $31, $0, 0x49
Test75Begin:
ori $20, $19, 0x2b
sw $25, 116($0)
sw $0, 99($31)
sw $25, 137($25)
ori $31, $0, 0x3b50
Test75End:
ori $31, $0, 0x28
Test76Begin:
jr $21
ori $31, $0, 0x3b60
nop
jal JBackFor6_0
ori $31, $0, 0x3b6c
sub $0, $19, $20
ori $31, $0, 0x3b70
Test76End:
ori $6, $0, 0x30a4
ori $31, $0, 0x64
Test77Begin:
nop
lui $19, 0x0
jr $24
ori $31, $0, 0x3b8c
lui $20, 0x0
ori $31, $0, 0x3b90
Test77End:
ori $31, $0, 0x72
Test78Begin:
nop
nop
ori $19, $0, 0x20
lw $20, 172($0)
ori $31, $0, 0x3ba8
Test78End:
ori $31, $0, 0xb2
Test79Begin:
ori $19, $0, 0x8a
ori $25, $0, 0x8a
jal JBackFor31_0
nop
beq $19, $25, Test79End
ori $31, $0, 0x3bc8
sw $20, 24($0)
ori $20, $19, 0xb4
ori $31, $0, 0x3bd0
Test79End:
ori $31, $0, 0xd
Test80Begin:
nop
lw $19, 175($31)
ori $19, $19, 0x92
jr $22
ori $31, $0, 0x3bec
ori $31, $0, 0x3bec
Test80End:
ori $31, $0, 0x4e
Test81Begin:
ori $19, $0, 0xa8
ori $19, $0, 0xa8
add $19, $19, $31
beq $19, $19, Test81End
ori $31, $0, 0x3c08
jal JBackFor31_0
nop
sw $25, 112($0)
ori $31, $0, 0x3c14
Test81End:
ori $19, $0, 0x46
ori $31, $0, 0x14
Test82Begin:
lw $31, -98($25)
sub $31, $0, $0
jr $22
ori $31, $0, 0x3c30
jr $16
ori $31, $0, 0x3c38
ori $31, $0, 0x3c38
Test82End:
ori $31, $0, 0x93
Test83Begin:
ori $0, $0, 0xb6
ori $20, $0, 0xb6
sw $31, -110($25)
sw $19, -3($31)
sw $19, 80($0)
beq $0, $20, Test83End
ori $31, $0, 0x3c5c
ori $31, $0, 0x3c5c
Test83End:
ori $31, $0, 0x52
Test84Begin:
nop
nop
lui $19, 0x0
jal JBackFor31_0
nop
ori $31, $0, 0x3c78
Test84End:
ori $31, $0, 0x6
Test85Begin:
jal JBackFor22_0
ori $31, $0, 0x3c88
sub $0, $25, $19
nop
jr $21
ori $31, $0, 0x3c98
ori $31, $0, 0x3c98
Test85End:
ori $22, $0, 0x3074
ori $31, $0, 0x8a
Test86Begin:
jal JBackFor31_0
nop
jr $22
ori $31, $0, 0x3cb4
sub $20, $25, $19
sub $25, $20, $19
ori $31, $0, 0x3cbc
Test86End:
ori $31, $0, 0xbe
Test87Begin:
lw $25, 48($19)
nop
ori $20, $19, 0xaa
nop
ori $31, $0, 0x3cd4
Test87End:
ori $31, $0, 0x8c
Test88Begin:
add $31, $25, $31
lui $0, 0x0
lui $20, 0x0
ori $31, $19, 0x44
ori $31, $0, 0x3cec
Test88End:
ori $31, $0, 0x6e
Test89Begin:
ori $31, $20, 0x64
add $19, $0, $25
ori $19, $19, 0x50
lui $25, 0x0
ori $31, $0, 0x3d04
Test89End:
ori $31, $0, 0x16
Test90Begin:
lui $20, 0x0
nop
sw $31, -69($19)
lw $19, 180($20)
ori $31, $0, 0x3d1c
Test90End:
ori $31, $0, 0x90
Test91Begin:
nop
lw $19, 152($25)
lw $0, 148($20)
nop
ori $31, $0, 0x3d34
Test91End:
ori $31, $0, 0x2d
Test92Begin:
lw $0, 136($20)
lui $31, 0x0
sub $0, $20, $20
jr $9
ori $31, $0, 0x3d50
ori $31, $0, 0x3d50
Test92End:
ori $31, $0, 0x12
Test93Begin:
lui $20, 0x0
jal JBackFor31_0
nop
nop
jr $21
ori $31, $0, 0x3d70
ori $31, $0, 0x3d70
Test93End:
ori $31, $0, 0xc6
Test94Begin:
ori $25, $0, 0x36
ori $31, $0, 0x36
beq $25, $31, Test94End
ori $31, $0, 0x3d88
sub $0, $19, $20
ori $20, $0, 0x49
sub $25, $31, $0
ori $31, $0, 0x3d94
Test94End:
ori $31, $0, 0x89
Test95Begin:
ori $19, $0, 0xc2
ori $0, $0, 0xc2
lw $31, 144($20)
beq $19, $0, Test95End
ori $31, $0, 0x3db0
sw $0, 36($20)
ori $19, $25, 0xb6
ori $31, $0, 0x3db8
Test95End:
ori $31, $0, 0x19
Test96Begin:
sub $20, $19, $19
lw $31, 148($20)
nop
ori $0, $25, 0x96
ori $31, $0, 0x3dd0
Test96End:
ori $31, $0, 0x84
Test97Begin:
jal JBackFor6_0
ori $31, $0, 0x3de0
sw $25, 88($20)
sw $0, 114($25)
lw $19, -15792($31)
ori $31, $0, 0x3dec
Test97End:
ori $6, $0, 0x3024
ori $31, $0, 0x81
Test98Begin:
sw $20, 83($19)
lui $31, 0x0
nop
lw $19, 52($20)
ori $31, $0, 0x3e08
Test98End:
ori $31, $0, 0x20
Test99Begin:
sub $19, $20, $0
ori $31, $19, 0x9b
sw $19, 144($0)
nop
ori $31, $0, 0x3e20
Test99End:
ori $31, $0, 0x85
Test100Begin:
ori $19, $0, 0x4d
ori $31, $0, 0x4d
beq $19, $31, Test100End
ori $31, $0, 0x3e38
add $31, $31, $0
jal JBackFor24_0
ori $31, $0, 0x3e44
jal JBackFor31_0
nop
ori $31, $0, 0x3e4c
Test100End:
ori $24, $0, 0x3038
ori $31, $0, 0xac
Test101Begin:
jal JBackFor21_0
ori $31, $0, 0x3e60
lw $0, 104($0)
lw $31, 84($20)
jal JBackFor24_0
ori $31, $0, 0x3e70
ori $31, $0, 0x3e70
Test101End:
ori $21, $0, 0x30a4
ori $24, $0, 0x30a4
ori $31, $0, 0xc0
Test102Begin:
lui $20, 0x0
jr $11
ori $31, $0, 0x3e8c
sw $19, 32($0)
ori $25, $31, 0x97
ori $31, $0, 0x3e94
Test102End:
ori $25, $0, 0x87
ori $31, $0, 0x4
Test103Begin:
ori $0, $0, 0x83
ori $19, $0, 0x83
sw $0, 168($20)
lw $19, -11($25)
ori $0, $25, 0x9e
beq $0, $19, Test103End
ori $31, $0, 0x3ebc
ori $31, $0, 0x3ebc
Test103End:
ori $31, $0, 0x9
Test104Begin:
jr $22
ori $31, $0, 0x3ecc
jr $16
ori $31, $0, 0x3ed4
nop
sw $20, 140($0)
ori $31, $0, 0x3edc
Test104End:
ori $31, $0, 0xc0
Test105Begin:
ori $25, $0, 0xbc
ori $31, $0, 0xbc
beq $25, $31, Test105End
ori $31, $0, 0x3ef4
sw $31, 44($20)
lw $20, -52($25)
jr $6
ori $31, $0, 0x3f04
ori $31, $0, 0x3f04
Test105End:
ori $31, $0, 0xa9
Test106Begin:
sub $20, $19, $19
sw $31, 176($20)
lui $31, 0x0
add $20, $31, $0
ori $31, $0, 0x3f1c
Test106End:
ori $31, $0, 0x63
Test107Begin:
lw $20, 24($20)
jr $16
ori $31, $0, 0x3f30
jr $21
ori $31, $0, 0x3f38
sub $0, $19, $20
ori $31, $0, 0x3f3c
Test107End:
ori $31, $0, 0x19
Test108Begin:
lw $31, -172($25)
lui $25, 0x0
lui $31, 0x0
lui $0, 0x0
ori $31, $0, 0x3f54
Test108End:
ori $31, $0, 0xab
Test109Begin:
sw $0, 4($25)
jr $15
ori $31, $0, 0x3f68
ori $25, $0, 0x25
sw $25, 196($19)
ori $31, $0, 0x3f70
Test109End:
ori $31, $0, 0x7e
Test110Begin:
nop
lui $19, 0x0
lw $0, 83($25)
sub $31, $19, $0
ori $31, $0, 0x3f88
Test110End:
ori $31, $0, 0x3
Test111Begin:
ori $19, $19, 0x8c
sw $31, -52($19)
sw $20, 173($31)
sw $0, 131($25)
ori $31, $0, 0x3fa0
Test111End:
ori $31, $0, 0x3e
Test112Begin:
ori $25, $0, 0x18
ori $31, $0, 0x18
ori $31, $19, 0x87
lui $20, 0x0
beq $25, $31, Test112End
ori $31, $0, 0x3fc0
jr $22
ori $31, $0, 0x3fc8
ori $31, $0, 0x3fc8
Test112End:
ori $31, $0, 0x5e
Test113Begin:
lw $19, 156($20)
lw $20, 48($20)
sub $25, $0, $25
jr $16
ori $31, $0, 0x3fe4
ori $31, $0, 0x3fe4
Test113End:
ori $31, $0, 0x7b
Test114Begin:
jal JBackFor6_0
ori $31, $0, 0x3ff4
nop
jr $22
ori $31, $0, 0x4000
jal JBackFor16_0
ori $31, $0, 0x4008
ori $31, $0, 0x4008
Test114End:
ori $6, $0, 0x30a4
ori $16, $0, 0x3010
ori $31, $0, 0x1d
Test115Begin:
ori $19, $19, 0x78
sub $25, $25, $19
nop
jal JBackFor9_0
ori $31, $0, 0x402c
ori $31, $0, 0x402c
Test115End:
ori $9, $0, 0x30a4
ori $31, $0, 0x2e
Test116Begin:
ori $20, $0, 0xad
ori $25, $0, 0xad
nop
beq $20, $25, Test116End
ori $31, $0, 0x404c
lw $20, 136($0)
lw $0, -16436($31)
ori $31, $0, 0x4054
Test116End:
ori $31, $0, 0x39
Test117Begin:
add $25, $25, $25
nop
lw $25, 31($31)
ori $31, $25, 0x9a
ori $31, $0, 0x406c
Test117End:
ori $31, $0, 0x51
Test118Begin:
sub $0, $19, $19
ori $31, $0, 0x62
nop
jal JBackFor6_0
ori $31, $0, 0x4088
ori $31, $0, 0x4088
Test118End:
ori $6, $0, 0x3024
ori $31, $0, 0xb6
Test119Begin:
ori $25, $0, 0xb6
ori $20, $0, 0xb6
ori $20, $20, 0xe
lui $20, 0x0
ori $19, $31, 0x79
beq $25, $20, Test119End
ori $31, $0, 0x40b0
ori $31, $0, 0x40b0
Test119End:
ori $19, $0, 0x40
ori $31, $0, 0x77
Test120Begin:
ori $19, $0, 0x3f
ori $20, $0, 0x3f
beq $19, $20, Test120End
ori $31, $0, 0x40cc
nop
jr $9
ori $31, $0, 0x40d8
jr $9
ori $31, $0, 0x40e0
ori $31, $0, 0x40e0
Test120End:
ori $31, $0, 0x2d
Test121Begin:
sw $19, -42($25)
lui $20, 0x0
sw $20, 32($0)
sw $20, -19($19)
ori $31, $0, 0x40f8
Test121End:
ori $31, $0, 0x3
Test122Begin:
ori $31, $0, 0x49
ori $20, $0, 0x49
lui $20, 0x0
lw $0, -90($25)
beq $31, $20, Test122End
ori $31, $0, 0x4118
nop
ori $31, $0, 0x411c
Test122End:
ori $31, $0, 0x25
Test123Begin:
ori $25, $0, 0xa5
ori $25, $0, 0xa5
beq $25, $25, Test123End
ori $31, $0, 0x4134
ori $0, $31, 0x16
sub $20, $19, $25
jal JBackFor24_0
ori $31, $0, 0x4144
ori $31, $0, 0x4144
Test123End:
ori $24, $0, 0x30a4
ori $31, $0, 0x71
Test124Begin:
ori $20, $0, 0x54
ori $31, $0, 0x54
beq $20, $31, Test124End
ori $31, $0, 0x4160
add $31, $19, $19
lui $31, 0x0
ori $0, $20, 0x2b
ori $31, $0, 0x416c
Test124End:
ori $31, $0, 0xc1
Test125Begin:
ori $31, $0, 0x76
ori $20, $0, 0x76
nop
lui $31, 0x0
lw $31, 60($31)
beq $31, $20, Test125End
ori $31, $0, 0x4190
ori $31, $0, 0x4190
Test125End:
ori $31, $0, 0x22
Test126Begin:
sw $31, -98($20)
lui $31, 0x0
nop
jr $21
ori $31, $0, 0x41ac
ori $31, $0, 0x41ac
Test126End:
ori $31, $0, 0x18
Test127Begin:
nop
lw $20, 104($0)
nop
jal JBackFor6_0
ori $31, $0, 0x41c8
ori $31, $0, 0x41c8
Test127End:
ori $6, $0, 0x30a4
ori $31, $0, 0xb1
Test128Begin:
ori $20, $20, 0x4a
lui $20, 0x0
lw $25, 23($25)
nop
ori $31, $0, 0x41e4
Test128End:
ori $31, $0, 0x87
Test129Begin:
ori $31, $0, 0xa1
ori $19, $0, 0xa1
sw $19, 148($25)
beq $31, $19, Test129End
ori $31, $0, 0x4200
lui $19, 0x0
ori $31, $19, 0x38
ori $31, $0, 0x4208
Test129End:
ori $31, $0, 0x8f
Test130Begin:
lw $31, -161($19)
ori $25, $0, 0x32
ori $20, $0, 0x7f
ori $20, $31, 0x4f
ori $31, $0, 0x4220
Test130End:
ori $31, $0, 0x2d
Test131Begin:
ori $20, $0, 0x34
ori $31, $0, 0x34
sw $25, -13($19)
lw $20, 12($0)
lw $19, -8($31)
beq $20, $31, Test131End
ori $31, $0, 0x4244
ori $31, $0, 0x4244
Test131End:
ori $31, $0, 0x6
Test132Begin:
lui $20, 0x0
jal JBackFor31_0
nop
lw $25, 84($20)
ori $20, $0, 0xa
ori $31, $0, 0x4260
Test132End:
ori $31, $0, 0x64
Test133Begin:
lui $0, 0x0
jr $6
ori $31, $0, 0x4274
jr $11
ori $31, $0, 0x427c
sw $25, 132($25)
ori $31, $0, 0x4280
Test133End:
ori $31, $0, 0x56
Test134Begin:
lui $19, 0x0
lw $19, 80($25)
lui $19, 0x0
lui $0, 0x0
ori $31, $0, 0x4298
Test134End:
ori $31, $0, 0x8d
Test135Begin:
jr $24
ori $31, $0, 0x42a8
jr $11
ori $31, $0, 0x42b0
sw $19, 160($0)
lui $0, 0x0
ori $31, $0, 0x42b8
Test135End:
ori $31, $0, 0x10
Test136Begin:
ori $19, $0, 0x4c
ori $25, $0, 0x4c
beq $19, $25, Test136End
ori $31, $0, 0x42d0
add $19, $25, $25
jal JBackFor6_0
ori $31, $0, 0x42dc
nop
ori $31, $0, 0x42e0
Test136End:
ori $6, $0, 0x30a4
ori $31, $0, 0xbf
Test137Begin:
ori $25, $0, 0x4b
ori $19, $0, 0x4b
jr $16
ori $31, $0, 0x42fc
beq $25, $19, Test137End
ori $31, $0, 0x4304
nop
jal JBackFor6_0
ori $31, $0, 0x4310
ori $31, $0, 0x4310
Test137End:
ori $6, $0, 0x3024
ori $31, $0, 0x25
Test138Begin:
sub $25, $20, $31
add $31, $25, $20
jal JBackFor22_0
ori $31, $0, 0x432c
jal JBackFor6_0
ori $31, $0, 0x4334
ori $31, $0, 0x4334
Test138End:
ori $22, $0, 0x30a4
ori $6, $0, 0x3024
ori $31, $0, 0x58
Test139Begin:
ori $25, $0, 0x27
ori $31, $0, 0x27
jr $9
ori $31, $0, 0x4354
jr $16
ori $31, $0, 0x435c
beq $25, $31, Test139End
ori $31, $0, 0x4364
sw $25, -17064($31)
ori $31, $0, 0x4368
Test139End:
ori $31, $0, 0x8a
Test140Begin:
lw $19, 25($25)
lw $20, -12364($19)
jal JBackFor31_0
nop
nop
ori $31, $0, 0x4384
Test140End:
ori $19, $0, 0x56
ori $31, $0, 0x8a
Test141Begin:
sw $19, -14($20)
sw $31, -126($31)
ori $0, $25, 0x3b
add $19, $0, $0
ori $31, $0, 0x43a0
Test141End:
ori $31, $0, 0xa
Test142Begin:
lui $25, 0x0
nop
jr $21
ori $31, $0, 0x43b8
sub $0, $0, $31
ori $31, $0, 0x43bc
Test142End:
ori $31, $0, 0xbd
Test143Begin:
ori $19, $0, 0x41
ori $0, $0, 0x41
beq $19, $0, Test143End
ori $31, $0, 0x43d4
jal JBackFor9_0
ori $31, $0, 0x43dc
jal JBackFor31_0
nop
sub $0, $20, $0
ori $31, $0, 0x43e8
Test143End:
ori $9, $0, 0x30a4
ori $31, $0, 0x3a
Test144Begin:
sw $20, 0($25)
lui $19, 0x0
sw $19, 168($0)
add $20, $19, $0
ori $31, $0, 0x4404
Test144End:
ori $31, $0, 0xa3
Test145Begin:
ori $20, $0, 0xaf
ori $25, $0, 0xaf
lui $31, 0x0
jr $22
ori $31, $0, 0x4420
beq $20, $25, Test145End
ori $31, $0, 0x4428
ori $31, $20, 0xc2
ori $31, $0, 0x442c
Test145End:
ori $31, $0, 0x7e
Test146Begin:
add $25, $19, $20
nop
ori $31, $19, 0x3
sw $0, 16($0)
ori $31, $0, 0x4444
Test146End:
ori $31, $0, 0x12
Test147Begin:
lui $20, 0x0
jal JBackFor31_0
nop
sw $19, -139($25)
jr $24
ori $31, $0, 0x4464
ori $31, $0, 0x4464
Test147End:
ori $31, $0, 0x6a
Test148Begin:
ori $25, $20, 0x4d
ori $0, $31, 0x62
jr $15
ori $31, $0, 0x447c
lui $0, 0x0
ori $31, $0, 0x4480
Test148End:
ori $31, $0, 0x57
Test149Begin:
ori $20, $0, 0x68
ori $0, $0, 0x68
beq $20, $0, Test149End
ori $31, $0, 0x4498
lui $31, 0x0
sub $19, $31, $19
sub $25, $19, $20
ori $31, $0, 0x44a4
Test149End:
ori $31, $0, 0x64
Test150Begin:
ori $25, $0, 0x7f
ori $31, $0, 0x7f
jal JBackFor31_0
nop
lui $0, 0x0
beq $25, $31, Test150End
ori $31, $0, 0x44c8
lw $31, 184($0)
ori $31, $0, 0x44cc
Test150End:
ori $31, $0, 0xba
Test151Begin:
lw $19, -84($20)
lui $19, 0x0
sw $19, 60($0)
nop
ori $31, $0, 0x44e4
Test151End:
ori $31, $0, 0x54
Test152Begin:
nop
nop
jal JBackFor22_0
ori $31, $0, 0x44fc
ori $0, $0, 0x80
ori $31, $0, 0x4500
Test152End:
ori $22, $0, 0x3074
ori $31, $0, 0x30
Test153Begin:
jal JBackFor15_0
ori $31, $0, 0x4514
jal JBackFor24_0
ori $31, $0, 0x451c
jr $6
ori $31, $0, 0x4524
jal JBackFor9_0
ori $31, $0, 0x452c
ori $31, $0, 0x452c
Test153End:
ori $15, $0, 0x304c
ori $24, $0, 0x3038
ori $9, $0, 0x3088
ori $31, $0, 0x10
Test154Begin:
ori $20, $0, 0x37
ori $20, $0, 0x37
lui $20, 0x0
lui $31, 0x0
beq $20, $20, Test154End
ori $31, $0, 0x4558
jr $9
ori $31, $0, 0x4560
ori $31, $0, 0x4560
Test154End:
ori $31, $0, 0x61
Test155Begin:
ori $20, $0, 0x57
ori $25, $0, 0x57
ori $31, $0, 0x9c
ori $19, $0, 0x9c
beq $20, $25, Test155End
ori $31, $0, 0x4580
nop
beq $31, $19, Test155End
ori $31, $0, 0x458c
add $31, $31, $19
ori $31, $0, 0x4590
Test155End:
ori $31, $0, 0x62
Test156Begin:
ori $0, $20, 0x9d
nop
nop
lui $0, 0x0
ori $31, $0, 0x45a8
Test156End:
ori $31, $0, 0x79
Test157Begin:
ori $20, $0, 0x37
ori $31, $0, 0x37
beq $20, $31, Test157End
ori $31, $0, 0x45c0
jr $16
ori $31, $0, 0x45c8
lw $25, -59($25)
lw $25, 97($20)
ori $31, $0, 0x45d0
Test157End:
ori $31, $0, 0x7a
Test158Begin:
add $31, $25, $0
jal JBackFor15_0
ori $31, $0, 0x45e4
nop
sw $19, -136($19)
ori $31, $0, 0x45ec
Test158End:
ori $15, $0, 0x304c
ori $31, $0, 0x5f
Test159Begin:
lui $0, 0x0
nop
jal JBackFor22_0
ori $31, $0, 0x4608
jal JBackFor24_0
ori $31, $0, 0x4610
ori $31, $0, 0x4610
Test159End:
ori $22, $0, 0x3074
ori $24, $0, 0x3038
ori $31, $0, 0xa7
Test160Begin:
sub $31, $25, $19
nop
jr $21
ori $31, $0, 0x4630
lui $20, 0x0
ori $31, $0, 0x4634
Test160End:
ori $31, $0, 0x38
Test161Begin:
ori $31, $0, 0x36
ori $19, $0, 0x36
nop
nop
nop
beq $31, $19, Test161End
ori $31, $0, 0x4658
ori $31, $0, 0x4658
Test161End:
ori $31, $0, 0xc7
Test162Begin:
ori $25, $0, 0x38
ori $0, $0, 0x38
sw $19, -26($19)
jr $11
ori $31, $0, 0x4674
beq $25, $0, Test162End
ori $31, $0, 0x467c
jal JBackFor31_0
nop
ori $31, $0, 0x4684
Test162End:
ori $31, $0, 0x7b
Test163Begin:
nop
ori $0, $31, 0xa0
jr $24
ori $31, $0, 0x469c
lw $20, 134($19)
ori $31, $0, 0x46a0
Test163End:
ori $31, $0, 0x2f
Test164Begin:
ori $31, $0, 0x2a
ori $19, $0, 0x2a
sw $19, 34($19)
lui $20, 0x0
jal JBackFor31_0
nop
beq $31, $19, Test164End
ori $31, $0, 0x46c8
ori $31, $0, 0x46c8
Test164End:
ori $31, $0, 0x99
Test165Begin:
ori $25, $0, 0x54
ori $25, $0, 0x54
sw $31, 16($25)
sw $0, 172($0)
jr $15
ori $31, $0, 0x46e8
beq $25, $25, Test165End
ori $31, $0, 0x46f0
ori $31, $0, 0x46f0
Test165End:
ori $31, $0, 0xe
Test166Begin:
ori $20, $0, 0x48
ori $31, $0, 0x48
beq $20, $31, Test166End
ori $31, $0, 0x4708
jr $16
ori $31, $0, 0x4710
sw $25, 68($25)
lw $0, -18108($31)
ori $31, $0, 0x4718
Test166End:
ori $31, $0, 0x58
Test167Begin:
ori $20, $0, 0x4a
ori $25, $0, 0x4a
lui $20, 0x0
jr $15
ori $31, $0, 0x4734
lui $25, 0x0
beq $20, $25, Test167End
ori $31, $0, 0x4740
ori $31, $0, 0x4740
Test167End:
ori $31, $0, 0x36
Test168Begin:
ori $25, $0, 0x1f
ori $19, $0, 0x1f
lw $0, 128($20)
beq $25, $19, Test168End
ori $31, $0, 0x475c
lw $25, 168($0)
sub $0, $31, $0
ori $31, $0, 0x4764
Test168End:
ori $31, $0, 0x9f
Test169Begin:
ori $25, $0, 0x9e
ori $25, $0, 0x9e
lw $19, 34($25)
ori $25, $20, 0x73
beq $25, $25, Test169End
ori $31, $0, 0x4784
lui $0, 0x0
ori $31, $0, 0x4788
Test169End:
ori $31, $0, 0xa2
Test170Begin:
ori $0, $0, 0xb9
ori $20, $0, 0xb9
lw $25, -77($20)
sub $31, $31, $31
sw $0, 40($31)
beq $0, $20, Test170End
ori $31, $0, 0x47ac
ori $31, $0, 0x47ac
Test170End:
ori $25, $0, 0x6c
ori $31, $0, 0x34
Test171Begin:
nop
sw $19, 68($31)
ori $20, $19, 0xe
jal JBackFor31_0
nop
ori $31, $0, 0x47cc
Test171End:
ori $31, $0, 0xa9
Test172Begin:
lw $25, 54($20)
ori $31, $20, 0x8e
add $25, $25, $0
lw $25, -61($25)
ori $31, $0, 0x47e4
Test172End:
ori $31, $0, 0x5b
Test173Begin:
jr $24
ori $31, $0, 0x47f4
nop
sw $19, -70($25)
jal JBackFor22_0
ori $31, $0, 0x4804
ori $31, $0, 0x4804
Test173End:
ori $22, $0, 0x3074
ori $31, $0, 0x9b
Test174Begin:
ori $31, $25, 0xe
lw $31, 94($20)
add $19, $19, $31
lui $25, 0x0
ori $31, $0, 0x4820
Test174End:
ori $19, $0, 0x13
ori $31, $0, 0x73
Test175Begin:
nop
lw $31, 158($20)
sw $31, 70($20)
sw $0, 66($20)
ori $31, $0, 0x483c
Test175End:
ori $31, $0, 0x57
Test176Begin:
ori $19, $0, 0x7f
ori $25, $0, 0x7f
lui $19, 0x0
beq $19, $25, Test176End
ori $31, $0, 0x4858
jal JBackFor31_0
nop
nop
ori $31, $0, 0x4864
Test176End:
ori $31, $0, 0x74
Test177Begin:
jr $9
ori $31, $0, 0x4874
nop
nop
lui $31, 0x0
ori $31, $0, 0x4880
Test177End:
ori $31, $0, 0x9e
Test178Begin:
nop
lui $0, 0x0
nop
lw $0, 112($19)
ori $31, $0, 0x4898
Test178End:
ori $31, $0, 0x55
Test179Begin:
ori $25, $0, 0x56
ori $19, $0, 0x56
ori $31, $0, 0x66
ori $25, $0, 0x66
beq $25, $19, Test179End
ori $31, $0, 0x48b8
beq $31, $25, Test179End
ori $31, $0, 0x48c0
jr $15
ori $31, $0, 0x48c8
sub $25, $31, $19
ori $31, $0, 0x48cc
Test179End:
ori $25, $0, 0x99
ori $31, $0, 0x36
Test180Begin:
ori $20, $0, 0x55
ori $0, $0, 0x55
jr $16
ori $31, $0, 0x48e8
beq $20, $0, Test180End
ori $31, $0, 0x48f0
sw $19, 79($20)
sw $20, -61($20)
ori $31, $0, 0x48f8
Test180End:
ori $31, $0, 0xa9
Test181Begin:
lw $0, -5($25)
ori $20, $25, 0x9a
lw $0, 128($0)
sw $20, -71($20)
ori $31, $0, 0x4910
Test181End:
ori $31, $0, 0xb2
Test182Begin:
ori $31, $19, 0x25
nop
sw $25, 72($0)
lw $20, 21($31)
ori $31, $0, 0x4928
Test182End:
ori $31, $0, 0x7c
Test183Begin:
ori $0, $0, 0x97
ori $20, $0, 0x97
jal JBackFor31_0
nop
add $0, $19, $0
beq $0, $20, Test183End
ori $31, $0, 0x494c
sw $0, -18636($31)
ori $31, $0, 0x4950
Test183End:
ori $31, $0, 0x5d
Test184Begin:
nop
jal JBackFor31_0
nop
nop
lui $19, 0x0
ori $31, $0, 0x496c
Test184End:
ori $31, $0, 0xad
Test185Begin:
nop
add $25, $19, $19
jr $11
ori $31, $0, 0x4984
nop
ori $31, $0, 0x4988
Test185End:
ori $31, $0, 0x75
Test186Begin:
sub $0, $20, $19
jal JBackFor31_0
nop
nop
ori $25, $31, 0x88
ori $31, $0, 0x49a4
Test186End:
ori $25, $0, 0x3c
ori $31, $0, 0xc1
Test187Begin:
jal JBackFor9_0
ori $31, $0, 0x49b8
lw $25, -44($25)
sub $0, $19, $20
ori $19, $0, 0xb2
ori $31, $0, 0x49c4
Test187End:
ori $9, $0, 0x30a4
ori $31, $0, 0x3b
Test188Begin:
add $0, $19, $25
ori $19, $0, 0xa8
ori $19, $19, 0x7d
nop
ori $31, $0, 0x49e0
Test188End:
ori $19, $0, 0xc7
ori $31, $0, 0x30
Test189Begin:
ori $31, $19, 0x9c
sub $25, $25, $0
jr $22
ori $31, $0, 0x49fc
lw $25, -23($19)
ori $31, $0, 0x4a00
Test189End:
ori $31, $0, 0x2b
Test190Begin:
ori $31, $0, 0x4c
ori $31, $0, 0x4c
ori $19, $20, 0x71
lui $19, 0x0
beq $31, $31, Test190End
ori $31, $0, 0x4a20
lui $0, 0x0
ori $31, $0, 0x4a24
Test190End:
ori $31, $0, 0xc4
Test191Begin:
ori $25, $0, 0x17
ori $25, $0, 0x17
beq $25, $25, Test191End
ori $31, $0, 0x4a3c
nop
lw $20, 140($19)
jr $6
ori $31, $0, 0x4a4c
ori $31, $0, 0x4a4c
Test191End:
ori $31, $0, 0x22
Test192Begin:
jal JBackFor31_0
nop
jr $24
ori $31, $0, 0x4a64
lui $19, 0x0
sw $0, 93($25)
ori $31, $0, 0x4a6c
Test192End:
ori $31, $0, 0xbc
Test193Begin:
nop
jr $24
ori $31, $0, 0x4a80
lui $0, 0x0
jr $21
ori $31, $0, 0x4a8c
ori $31, $0, 0x4a8c
Test193End:
ori $31, $0, 0x2c
Test194Begin:
sw $20, 81($25)
lui $25, 0x0
lui $25, 0x0
ori $0, $0, 0x9d
ori $31, $0, 0x4aa4
Test194End:
ori $31, $0, 0xaa
Test195Begin:
lui $25, 0x0
jal JBackFor11_0
ori $31, $0, 0x4ab8
nop
lw $19, -19092($31)
ori $31, $0, 0x4ac0
Test195End:
ori $11, $0, 0x3060
ori $31, $0, 0x3c
Test196Begin:
jal JBackFor31_0
nop
ori $19, $20, 0x38
add $19, $0, $31
ori $20, $19, 0x4d
ori $31, $0, 0x4ae0
Test196End:
ori $19, $0, 0x6
ori $20, $0, 0x7
ori $31, $0, 0x56
Test197Begin:
ori $0, $0, 0x3b
ori $19, $0, 0x3b
jal JBackFor24_0
ori $31, $0, 0x4b00
nop
beq $0, $19, Test197End
ori $31, $0, 0x4b0c
add $0, $25, $19
ori $31, $0, 0x4b10
Test197End:
ori $24, $0, 0x3038
ori $31, $0, 0x8d
Test198Begin:
sub $0, $19, $20
nop
add $0, $0, $31
jr $22
ori $31, $0, 0x4b30
ori $31, $0, 0x4b30
Test198End:
ori $31, $0, 0x5f
Test199Begin:
lui $19, 0x0
lui $0, 0x0
sw $20, -27($31)
jal JBackFor31_0
nop
ori $31, $0, 0x4b4c
Test199End:
ori $31, $0, 0x14
Test200Begin:
ori $31, $20, 0x20
lui $19, 0x0
ori $31, $19, 0x76
add $19, $25, $19
ori $31, $0, 0x4b64
Test200End:
ori $31, $0, 0x4
Test201Begin:
ori $25, $19, 0xb7
lw $0, 28($19)
lw $31, 64($31)
ori $25, $25, 0x2f
ori $31, $0, 0x4b7c
Test201End:
ori $31, $0, 0x36
Test202Begin:
nop
lw $19, 164($0)
lw $0, -14($19)
lui $19, 0x0
ori $31, $0, 0x4b94
Test202End:
ori $31, $0, 0x1a
Test203Begin:
add $19, $20, $31
sw $0, 127($19)
nop
jal JBackFor31_0
nop
ori $31, $0, 0x4bb0
Test203End:
ori $31, $0, 0xb5
Test204Begin:
nop
nop
jr $9
ori $31, $0, 0x4bc8
lw $20, -23($25)
ori $31, $0, 0x4bcc
Test204End:
ori $31, $0, 0xbd
Test205Begin:
sub $19, $19, $19
jal JBackFor31_0
nop
ori $20, $20, 0x43
lw $31, -67($20)
ori $31, $0, 0x4be8
Test205End:
ori $31, $0, 0xb
Test206Begin:
ori $25, $0, 0x7b
ori $25, $0, 0x7b
ori $31, $0, 0xad
ori $31, $0, 0xad
beq $25, $25, Test206End
ori $31, $0, 0x4c08
nop
lw $31, 152($0)
beq $31, $31, Test206End
ori $31, $0, 0x4c18
ori $31, $0, 0x4c18
Test206End:
ori $31, $0, 0x4d
Test207Begin:
ori $0, $0, 0x40
ori $19, $0, 0x40
jal JBackFor6_0
ori $31, $0, 0x4c30
beq $0, $19, Test207End
ori $31, $0, 0x4c38
ori $25, $31, 0x5
sub $20, $20, $25
ori $31, $0, 0x4c40
Test207End:
ori $6, $0, 0x30a4
ori $25, $0, 0xa4
ori $20, $0, 0x8e
ori $31, $0, 0x82
Test208Begin:
jal JBackFor9_0
ori $31, $0, 0x4c5c
sw $31, -19544($31)
nop
lw $0, -19516($31)
ori $31, $0, 0x4c68
Test208End:
ori $9, $0, 0x3088
ori $31, $0, 0x51
Test209Begin:
lui $19, 0x0
nop
nop
nop
ori $31, $0, 0x4c84
Test209End:
ori $31, $0, 0x36
Test210Begin:
sw $0, -102($20)
jr $24
ori $31, $0, 0x4c98
sw $31, 168($19)
lw $19, -19424($31)
ori $31, $0, 0x4ca0
Test210End:
ori $31, $0, 0x3f
Test211Begin:
ori $19, $0, 0x75
ori $20, $0, 0x75
lw $19, -160($25)
nop
nop
beq $19, $20, Test211End
ori $31, $0, 0x4cc4
ori $31, $0, 0x4cc4
Test211End:
ori $19, $0, 0x40
ori $31, $0, 0x7e
Test212Begin:
ori $25, $0, 0x34
ori $25, $0, 0x34
ori $0, $0, 0x93
ori $0, $0, 0x93
ori $0, $25, 0x46
beq $25, $25, Test212End
ori $31, $0, 0x4cec
beq $0, $0, Test212End
ori $31, $0, 0x4cf4
jal JBackFor15_0
ori $31, $0, 0x4cfc
ori $31, $0, 0x4cfc
Test212End:
ori $15, $0, 0x304c
ori $31, $0, 0xa8
Test213Begin:
lw $25, -117($20)
ori $31, $0, 0x57
jal JBackFor31_0
nop
lui $0, 0x0
ori $31, $0, 0x4d1c
Test213End:
ori $31, $0, 0x1f
Test214Begin:
sub $31, $25, $25
jr $16
ori $31, $0, 0x4d30
lui $19, 0x0
ori $20, $19, 0x70
ori $31, $0, 0x4d38
Test214End:
ori $31, $0, 0x0
Test215Begin:
ori $20, $0, 0x51
ori $19, $0, 0x51
sw $19, 30($25)
jal JBackFor15_0
ori $31, $0, 0x4d54
beq $20, $19, Test215End
ori $31, $0, 0x4d5c
jal JBackFor16_0
ori $31, $0, 0x4d64
ori $31, $0, 0x4d64
Test215End:
ori $15, $0, 0x304c
ori $16, $0, 0x30a4
ori $31, $0, 0x73
Test216Begin:
ori $19, $0, 0x37
ori $20, $0, 0x37
nop
lui $31, 0x0
nop
beq $19, $20, Test216End
ori $31, $0, 0x4d90
ori $31, $0, 0x4d90
Test216End:
ori $31, $0, 0x71
Test217Begin:
ori $31, $0, 0x16
ori $31, $0, 0x16
nop
lw $19, 18($31)
ori $19, $19, 0xa7
beq $31, $31, Test217End
ori $31, $0, 0x4db4
ori $31, $0, 0x4db4
Test217End:
ori $31, $0, 0x95
Test218Begin:
lui $31, 0x0
lui $25, 0x0
lw $0, 57($20)
sw $0, 152($0)
ori $31, $0, 0x4dcc
Test218End:
ori $31, $0, 0x79
Test219Begin:
ori $31, $0, 0x99
ori $20, $0, 0x99
ori $19, $0, 0x57
ori $31, $0, 0x57
add $0, $20, $31
jal JBackFor16_0
ori $31, $0, 0x4df0
beq $31, $20, Test219End
ori $31, $0, 0x4df8
beq $19, $31, Test219End
ori $31, $0, 0x4e00
ori $31, $0, 0x4e00
Test219End:
ori $16, $0, 0x30a4
ori $31, $0, 0x8d
Test220Begin:
lw $0, 176($25)
jr $24
ori $31, $0, 0x4e18
sw $0, 19($20)
add $25, $31, $31
ori $31, $0, 0x4e20
Test220End:
ori $25, $0, 0x84
ori $31, $0, 0x2f
Test221Begin:
ori $31, $0, 0x82
ori $19, $0, 0x82
jal JBackFor16_0
ori $31, $0, 0x4e3c
jal JBackFor31_0
nop
add $31, $19, $20
beq $31, $19, Test221End
ori $31, $0, 0x4e50
ori $31, $0, 0x4e50
Test221End:
ori $16, $0, 0x30a4
ori $31, $0, 0x5e
Test222Begin:
nop
lui $31, 0x0
jal JBackFor31_0
nop
lui $25, 0x0
ori $31, $0, 0x4e70
Test222End:
ori $31, $0, 0x18
Test223Begin:
jr $11
ori $31, $0, 0x4e80
lw $19, 27($20)
jal JBackFor24_0
ori $31, $0, 0x4e8c
jr $11
ori $31, $0, 0x4e94
ori $31, $0, 0x4e94
Test223End:
ori $24, $0, 0x3038
ori $31, $0, 0x4d
Test224Begin:
ori $19, $0, 0x34
ori $19, $0, 0x34
add $20, $25, $19
add $20, $20, $19
lw $31, -52($20)
beq $19, $19, Test224End
ori $31, $0, 0x4ebc
ori $31, $0, 0x4ebc
Test224End:
ori $31, $0, 0xae
Test225Begin:
ori $25, $0, 0xb2
ori $20, $0, 0xb2
lw $0, 32($19)
sub $19, $19, $20
nop
beq $25, $20, Test225End
ori $31, $0, 0x4ee0
ori $31, $0, 0x4ee0
Test225End:
ori $31, $0, 0xa8
Test226Begin:
sub $25, $20, $0
sw $31, -126($25)
jr $24
ori $31, $0, 0x4ef8
sub $0, $31, $31
ori $31, $0, 0x4efc
Test226End:
ori $31, $0, 0xbf
Test227Begin:
sw $20, -30($20)
lw $20, -10($25)
jal JBackFor9_0
ori $31, $0, 0x4f14
ori $31, $0, 0x97
ori $31, $0, 0x4f18
Test227End:
ori $9, $0, 0x30a4
ori $20, $0, 0xa2
ori $31, $0, 0x41
Test228Begin:
ori $20, $0, 0x77
ori $19, $0, 0x77
sw $25, 21($20)
beq $20, $19, Test228End
ori $31, $0, 0x4f3c
jal JBackFor31_0
nop
jr $15
ori $31, $0, 0x4f4c
ori $31, $0, 0x4f4c
Test228End:
ori $31, $0, 0xa4
Test229Begin:
ori $0, $20, 0x2
nop
sw $19, 136($0)
add $25, $31, $31
ori $31, $0, 0x4f64
Test229End:
ori $25, $0, 0x8
ori $31, $0, 0x88
Test230Begin:
ori $0, $20, 0xa8
ori $31, $0, 0xc0
jal JBackFor22_0
ori $31, $0, 0x4f80
lui $0, 0x0
ori $31, $0, 0x4f84
Test230End:
ori $22, $0, 0x3074
ori $31, $0, 0x9b
Test231Begin:
lui $20, 0x0
jr $15
ori $31, $0, 0x4f9c
sw $0, 96($25)
nop
ori $31, $0, 0x4fa4
Test231End:
ori $31, $0, 0xbf
Test232Begin:
ori $31, $20, 0x58
sub $0, $25, $19
ori $20, $0, 0x99
ori $20, $19, 0x97
ori $31, $0, 0x4fbc
Test232End:
ori $20, $0, 0x37
ori $31, $0, 0xc3
Test233Begin:
ori $25, $0, 0x34
ori $19, $0, 0x34
jal JBackFor24_0
ori $31, $0, 0x4fd8
beq $25, $19, Test233End
ori $31, $0, 0x4fe0
jal JBackFor31_0
nop
lui $31, 0x0
ori $31, $0, 0x4fec
Test233End:
ori $24, $0, 0x3038
ori $31, $0, 0x75
Test234Begin:
ori $25, $0, 0x4c
ori $19, $0, 0x4c
jr $16
ori $31, $0, 0x5008
sub $25, $31, $20
beq $25, $19, Test234End
ori $31, $0, 0x5014
nop
ori $31, $0, 0x5018
Test234End:
ori $25, $0, 0xbd
ori $31, $0, 0x3e
Test235Begin:
lui $20, 0x0
lw $20, 36($0)
nop
ori $19, $0, 0x5b
ori $31, $0, 0x5034
Test235End:
ori $31, $0, 0xa4
Test236Begin:
nop
lw $31, 4($20)
jal JBackFor31_0
nop
sw $0, -20444($31)
ori $31, $0, 0x5050
Test236End:
ori $31, $0, 0x20
Test237Begin:
jal JBackFor24_0
ori $31, $0, 0x5060
add $25, $0, $31
jal JBackFor21_0
ori $31, $0, 0x506c
add $31, $31, $25
ori $31, $0, 0x5070
Test237End:
ori $24, $0, 0x30a4
ori $21, $0, 0x309c
ori $25, $0, 0x8c
ori $31, $0, 0xc5
Test238Begin:
ori $20, $0, 0x26
ori $31, $0, 0x26
ori $19, $25, 0x44
add $20, $19, $31
beq $20, $31, Test238End
ori $31, $0, 0x509c
jal JBackFor31_0
nop
ori $31, $0, 0x50a4
Test238End:
ori $19, $0, 0xbb
ori $20, $0, 0x93
ori $31, $0, 0x78
Test239Begin:
jr $22
ori $31, $0, 0x50bc
nop
jal JBackFor15_0
ori $31, $0, 0x50c8
jr $21
ori $31, $0, 0x50d0
ori $31, $0, 0x50d0
Test239End:
ori $15, $0, 0x30a4
ori $31, $0, 0x1b
Test240Begin:
ori $20, $0, 0x28
ori $0, $0, 0x28
nop
beq $20, $0, Test240End
ori $31, $0, 0x50f0
nop
lui $20, 0x0
ori $31, $0, 0x50f8
Test240End:
ori $31, $0, 0x24
Test241Begin:
ori $20, $0, 0x76
ori $20, $0, 0x76
nop
sw $31, -91($19)
lw $31, 2($20)
beq $20, $20, Test241End
ori $31, $0, 0x511c
ori $31, $0, 0x511c
Test241End:
ori $31, $0, 0x69
Test242Begin:
lw $25, -24($25)
jr $9
ori $31, $0, 0x5130
lw $31, -63($19)
jr $16
ori $31, $0, 0x513c
ori $31, $0, 0x513c
Test242End:
ori $31, $0, 0x60
Test243Begin:
sub $31, $20, $20
ori $31, $31, 0x57
lw $0, -23($31)
lui $19, 0x0
ori $31, $0, 0x5154
Test243End:
ori $31, $0, 0x24
Test244Begin:
jr $11
ori $31, $0, 0x5164
nop
jal JBackFor16_0
ori $31, $0, 0x5170
sw $19, 112($25)
ori $31, $0, 0x5174
Test244End:
ori $16, $0, 0x30a4
ori $31, $0, 0xae
Test245Begin:
nop
ori $25, $25, 0xba
sw $31, 16($0)
add $19, $20, $19
ori $31, $0, 0x5190
Test245End:
ori $31, $0, 0x2d
Test246Begin:
ori $19, $0, 0xb0
ori $25, $0, 0xb0
ori $25, $0, 0x17
ori $0, $0, 0x17
ori $0, $25, 0x92
beq $19, $25, Test246End
ori $31, $0, 0x51b4
lw $0, 28($0)
beq $25, $0, Test246End
ori $31, $0, 0x51c0
ori $31, $0, 0x51c0
Test246End:
ori $31, $0, 0xae
Test247Begin:
nop
ori $0, $25, 0x8e
nop
add $0, $0, $20
ori $31, $0, 0x51d8
Test247End:
ori $31, $0, 0x44
Test248Begin:
ori $31, $0, 0x67
ori $0, $0, 0x67
ori $31, $20, 0x6a
sub $31, $19, $19
beq $31, $0, Test248End
ori $31, $0, 0x51f8
jal JBackFor6_0
ori $31, $0, 0x5200
ori $31, $0, 0x5200
Test248End:
ori $6, $0, 0x3024
ori $31, $0, 0x81
Test249Begin:
nop
ori $25, $20, 0x10
sw $25, 30($20)
lui $20, 0x0
ori $31, $0, 0x521c
Test249End:
ori $31, $0, 0x89
Test250Begin:
ori $19, $0, 0xad
ori $20, $0, 0xad
lui $25, 0x0
jr $15
ori $31, $0, 0x5238
sw $19, 168($0)
beq $19, $20, Test250End
ori $31, $0, 0x5244
ori $31, $0, 0x5244
Test250End:
ori $31, $0, 0x65
Test251Begin:
lw $0, -125($20)
lw $31, 60($25)
lui $20, 0x0
lw $31, 28($25)
ori $31, $0, 0x525c
Test251End:
ori $31, $0, 0x78
Test252Begin:
ori $19, $0, 0x9e
ori $31, $0, 0x9e
ori $25, $25, 0x7a
jal JBackFor31_0
nop
lui $19, 0x0
beq $19, $31, Test252End
ori $31, $0, 0x5284
ori $31, $0, 0x5284
Test252End:
ori $31, $0, 0x36
Test253Begin:
lui $19, 0x0
lw $20, 30($31)
jr $16
ori $31, $0, 0x529c
jal JBackFor15_0
ori $31, $0, 0x52a4
ori $31, $0, 0x52a4
Test253End:
ori $15, $0, 0x30a4
ori $31, $0, 0xc7
Test254Begin:
ori $31, $0, 0xac
ori $31, $0, 0xac
lw $25, 104($19)
beq $31, $31, Test254End
ori $31, $0, 0x52c4
sub $31, $0, $19
lui $31, 0x0
ori $31, $0, 0x52cc
Test254End:
ori $31, $0, 0xc3
Test255Begin:
ori $0, $0, 0x29
ori $20, $0, 0x29
jr $11
ori $31, $0, 0x52e4
ori $0, $0, 0xb8
sw $25, 96($19)
beq $0, $20, Test255End
ori $31, $0, 0x52f4
ori $31, $0, 0x52f4
Test255End:
ori $31, $0, 0x33
Test256Begin:
sw $0, 144($19)
ori $25, $19, 0xbe
sub $25, $25, $31
jal JBackFor31_0
nop
ori $31, $0, 0x5310
Test256End:
ori $31, $0, 0x71
Test257Begin:
sub $19, $20, $0
lw $19, 111($19)
lw $25, -37($20)
jr $11
ori $31, $0, 0x532c
ori $31, $0, 0x532c
Test257End:
ori $25, $0, 0x65
ori $31, $0, 0x50
Test258Begin:
ori $25, $0, 0x9d
ori $31, $0, 0x9d
ori $19, $0, 0x4b
ori $0, $0, 0x4b
beq $25, $31, Test258End
ori $31, $0, 0x5350
nop
beq $19, $0, Test258End
ori $31, $0, 0x535c
sub $31, $25, $0
ori $31, $0, 0x5360
Test258End:
ori $31, $0, 0x78
Test259Begin:
jal JBackFor31_0
nop
add $0, $0, $19
nop
sw $20, -21180($31)
ori $31, $0, 0x537c
Test259End:
ori $31, $0, 0x55
Test260Begin:
ori $19, $0, 0x3d
ori $20, $0, 0x3d
jr $11
ori $31, $0, 0x5394
jr $21
ori $31, $0, 0x539c
lw $25, -21304($31)
beq $19, $20, Test260End
ori $31, $0, 0x53a8
ori $31, $0, 0x53a8
Test260End:
ori $31, $0, 0xa4
Test261Begin:
nop
nop
jr $15
ori $31, $0, 0x53c0
jal JBackFor11_0
ori $31, $0, 0x53c8
ori $31, $0, 0x53c8
Test261End:
ori $11, $0, 0x30a4
ori $31, $0, 0xc6
Test262Begin:
sw $19, 119($19)
lui $31, 0x0
sw $25, 16($31)
sw $31, 160($31)
ori $31, $0, 0x53e4
Test262End:
ori $31, $0, 0x87
Test263Begin:
lw $31, -61($20)
lui $20, 0x0
lw $25, 27($19)
lui $20, 0x0
ori $31, $0, 0x53fc
Test263End:
ori $31, $0, 0x8c
Test264Begin:
nop
jal JBackFor24_0
ori $31, $0, 0x5410
jr $15
ori $31, $0, 0x5418
nop
ori $31, $0, 0x541c
Test264End:
ori $24, $0, 0x3038
ori $31, $0, 0x7f
Test265Begin:
sw $31, 75($19)
lui $19, 0x0
nop
sub $31, $19, $0
ori $31, $0, 0x5438
Test265End:
ori $31, $0, 0x54
Test266Begin:
ori $19, $0, 0x87
ori $25, $0, 0x87
lui $31, 0x0
nop
beq $19, $25, Test266End
ori $31, $0, 0x5458
ori $20, $20, 0xa4
ori $31, $0, 0x545c
Test266End:
ori $31, $0, 0x4f
Test267Begin:
sw $25, -127($25)
sw $31, 44($0)
lui $0, 0x0
jal JBackFor9_0
ori $31, $0, 0x5478
ori $31, $0, 0x5478
Test267End:
ori $9, $0, 0x3088
ori $31, $0, 0x3a
Test268Begin:
ori $20, $19, 0x28
lui $31, 0x0
lw $19, 61($25)
sw $31, 20($31)
ori $31, $0, 0x5494
Test268End:
ori $31, $0, 0xc6
Test269Begin:
jal JBackFor15_0
ori $31, $0, 0x54a4
nop
sw $0, -167($20)
ori $31, $0, 0x67
ori $31, $0, 0x54b0
Test269End:
ori $15, $0, 0x304c
ori $31, $0, 0xad
Test270Begin:
nop
nop
lw $20, -23($25)
nop
ori $31, $0, 0x54cc
Test270End:
ori $31, $0, 0xa8
Test271Begin:
ori $20, $0, 0xa1
ori $31, $0, 0xa1
beq $20, $31, Test271End
ori $31, $0, 0x54e4
add $19, $25, $25
lui $20, 0x0
nop
ori $31, $0, 0x54f0
Test271End:
ori $31, $0, 0x5a
Test272Begin:
ori $25, $0, 0x56
ori $25, $0, 0x56
beq $25, $25, Test272End
ori $31, $0, 0x5508
lw $0, -57($20)
sw $25, 20($0)
ori $25, $25, 0x3d
ori $31, $0, 0x5514
Test272End:
ori $31, $0, 0xab
Test273Begin:
ori $19, $19, 0x12
ori $20, $19, 0x6b
sw $31, 10($25)
ori $19, $19, 0x7d
ori $31, $0, 0x552c
Test273End:
ori $31, $0, 0x3c
Test274Begin:
ori $19, $0, 0xa8
ori $19, $0, 0xa8
ori $25, $0, 0x59
ori $31, $0, 0x59
ori $25, $0, 0xb4
ori $25, $0, 0xb4
beq $19, $19, Test274End
ori $31, $0, 0x5554
lw $20, -20($19)
beq $25, $31, Test274End
ori $31, $0, 0x5560
beq $25, $25, Test274End
ori $31, $0, 0x5568
ori $31, $0, 0x5568
Test274End:
ori $31, $0, 0xbf
Test275Begin:
nop
sub $0, $0, $19
nop
jal JBackFor31_0
nop
ori $31, $0, 0x5584
Test275End:
ori $31, $0, 0xa9
Test276Begin:
nop
jr $9
ori $31, $0, 0x5598
lui $0, 0x0
lw $25, -116($19)
ori $31, $0, 0x55a0
Test276End:
ori $31, $0, 0x81
Test277Begin:
ori $31, $0, 0x3f
ori $20, $0, 0x3f
lui $19, 0x0
ori $0, $25, 0xb0
lui $25, 0x0
beq $31, $20, Test277End
ori $31, $0, 0x55c4
ori $31, $0, 0x55c4
Test277End:
ori $31, $0, 0x21
Test278Begin:
add $19, $25, $20
nop
lui $20, 0x0
jr $24
ori $31, $0, 0x55e0
ori $31, $0, 0x55e0
Test278End:
ori $31, $0, 0x96
Test279Begin:
sw $0, 192($25)
nop
lui $19, 0x0
add $19, $31, $20
ori $31, $0, 0x55f8
Test279End:
ori $31, $0, 0x6f
Test280Begin:
sw $19, 2($19)
nop
lw $19, -2($19)
lw $20, 112($25)
ori $31, $0, 0x5610
Test280End:
ori $31, $0, 0xbd
Test281Begin:
ori $19, $0, 0x59
ori $0, $0, 0x59
ori $25, $0, 0x9c
ori $20, $0, 0x9c
beq $19, $0, Test281End
ori $31, $0, 0x5630
beq $25, $20, Test281End
ori $31, $0, 0x5638
lui $20, 0x0
add $31, $31, $19
ori $31, $0, 0x5640
Test281End:
ori $31, $0, 0xa9
Test282Begin:
lw $25, 19($19)
ori $20, $0, 0x5f
jr $9
ori $31, $0, 0x5658
sub $25, $0, $0
ori $31, $0, 0x565c
Test282End:
ori $31, $0, 0x16
Test283Begin:
lui $0, 0x0
sw $0, 118($31)
nop
ori $20, $0, 0x1d
ori $31, $0, 0x5674
Test283End:
ori $31, $0, 0x9c
Test284Begin:
nop
nop
lw $31, 164($0)
lui $31, 0x0
ori $31, $0, 0x568c
Test284End:
ori $31, $0, 0x71
Test285Begin:
jr $16
ori $31, $0, 0x569c
lw $25, -29($19)
lui $0, 0x0
jal JBackFor31_0
nop
ori $31, $0, 0x56ac
Test285End:
ori $31, $0, 0x8e
Test286Begin:
jr $16
ori $31, $0, 0x56bc
sub $25, $31, $31
jr $21
ori $31, $0, 0x56c8
ori $0, $25, 0xb6
ori $31, $0, 0x56cc
Test286End:
ori $31, $0, 0x24
Test287Begin:
lui $0, 0x0
lw $20, 60($0)
lui $20, 0x0
ori $20, $20, 0xf
ori $31, $0, 0x56e4
Test287End:
ori $31, $0, 0xa
Test288Begin:
nop
ori $20, $19, 0x6e
ori $25, $25, 0x18
sw $25, -61($19)
ori $31, $0, 0x56fc
Test288End:
ori $31, $0, 0x86
Test289Begin:
sub $19, $19, $20
sub $0, $19, $0
jr $24
ori $31, $0, 0x5714
lw $20, -22260($31)
ori $31, $0, 0x5718
Test289End:
ori $31, $0, 0xb6
Test290Begin:
ori $0, $0, 0x44
ori $25, $0, 0x44
jal JBackFor31_0
nop
lui $19, 0x0
beq $0, $25, Test290End
ori $31, $0, 0x573c
nop
ori $31, $0, 0x5740
Test290End:
ori $31, $0, 0xae
Test291Begin:
ori $19, $0, 0x54
ori $19, $0, 0x54
lui $25, 0x0
jal JBackFor31_0
nop
beq $19, $19, Test291End
ori $31, $0, 0x5764
sub $19, $31, $19
ori $31, $0, 0x5768
Test291End:
ori $31, $0, 0x29
Test292Begin:
sw $25, 156($25)
add $20, $25, $31
jr $21
ori $31, $0, 0x5780
sw $19, 84($19)
ori $31, $0, 0x5784
Test292End:
ori $31, $0, 0x60
Test293Begin:
ori $25, $0, 0xbf
ori $31, $0, 0xbf
lui $31, 0x0
beq $25, $31, Test293End
ori $31, $0, 0x57a0
lui $20, 0x0
lw $25, -22432($31)
ori $31, $0, 0x57a8
Test293End:
ori $31, $0, 0x6d
Test294Begin:
sw $31, 46($25)
sw $19, 120($20)
lui $31, 0x0
nop
ori $31, $0, 0x57c0
Test294End:
ori $31, $0, 0xc3
Test295Begin:
nop
ori $25, $19, 0xc2
add $31, $20, $31
jr $9
ori $31, $0, 0x57dc
ori $31, $0, 0x57dc
Test295End:
ori $25, $0, 0x7d
ori $31, $0, 0x4e
Test296Begin:
sw $31, 80($20)
jr $21
ori $31, $0, 0x57f4
jal JBackFor31_0
nop
sw $0, 44($0)
ori $31, $0, 0x5800
Test296End:
ori $31, $0, 0x15
Test297Begin:
sub $31, $19, $31
lw $31, 53($31)
nop
ori $31, $0, 0x18
ori $31, $0, 0x5818
Test297End:
ori $31, $0, 0x6b
Test298Begin:
jal JBackFor31_0
nop
ori $0, $31, 0xbd
sw $31, -65($25)
sub $31, $0, $0
ori $31, $0, 0x5834
Test298End:
ori $31, $0, 0x1
Test299Begin:
ori $20, $0, 0x52
ori $25, $0, 0x52
lw $0, -46($20)
beq $20, $25, Test299End
ori $31, $0, 0x5850
jal JBackFor15_0
ori $31, $0, 0x5858
lui $31, 0x0
ori $31, $0, 0x585c
Test299End:
ori $15, $0, 0x304c
ori $31, $0, 0x60
Test300Begin:
ori $19, $0, 0xba
ori $25, $0, 0xba
add $19, $19, $31
beq $19, $25, Test300End
ori $31, $0, 0x587c
add $0, $20, $31
jal JBackFor31_0
nop
ori $31, $0, 0x5888
Test300End:
ori $19, $0, 0x40
ori $31, $0, 0x73
Test301Begin:
jal JBackFor22_0
ori $31, $0, 0x589c
sw $20, 96($19)
lw $25, 106($20)
lui $20, 0x0
ori $31, $0, 0x58a8
Test301End:
ori $22, $0, 0x3074
ori $31, $0, 0x17
Test302Begin:
jr $6
ori $31, $0, 0x58bc
nop
sw $19, 0($19)
jal JBackFor24_0
ori $31, $0, 0x58cc
ori $31, $0, 0x58cc
Test302End:
ori $24, $0, 0x3038
ori $31, $0, 0x36
Test303Begin:
ori $19, $0, 0x61
ori $0, $0, 0x61
ori $0, $0, 0x1f
ori $19, $0, 0x1f
beq $19, $0, Test303End
ori $31, $0, 0x58f0
sw $31, -27($19)
beq $0, $19, Test303End
ori $31, $0, 0x58fc
sub $20, $0, $19
ori $31, $0, 0x5900
Test303End:
ori $31, $0, 0xa5
Test304Begin:
ori $20, $0, 0xb9
ori $20, $0, 0xb9
lw $0, -133($20)
jal JBackFor24_0
ori $31, $0, 0x591c
beq $20, $20, Test304End
ori $31, $0, 0x5924
nop
ori $31, $0, 0x5928
Test304End:
ori $24, $0, 0x30a4
ori $31, $0, 0x1e
Test305Begin:
ori $20, $0, 0x2f
ori $19, $0, 0x2f
beq $20, $19, Test305End
ori $31, $0, 0x5944
lui $25, 0x0
nop
sub $25, $20, $0
ori $31, $0, 0x5950
Test305End:
ori $31, $0, 0xa2
Test306Begin:
ori $19, $0, 0xc2
ori $19, $0, 0xc2
beq $19, $19, Test306End
ori $31, $0, 0x5968
sw $19, 109($25)
lw $20, 76($0)
jr $11
ori $31, $0, 0x5978
ori $31, $0, 0x5978
Test306End:
ori $31, $0, 0xd
Test307Begin:
ori $25, $0, 0x89
ori $25, $0, 0x89
ori $0, $0, 0x61
ori $31, $0, 0x61
beq $25, $25, Test307End
ori $31, $0, 0x5998
beq $0, $31, Test307End
ori $31, $0, 0x59a0
jal JBackFor31_0
nop
nop
ori $31, $0, 0x59ac
Test307End:
ori $31, $0, 0x68
Test308Begin:
ori $31, $0, 0xc4
ori $0, $0, 0xc4
ori $20, $0, 0x7
ori $20, $0, 0x7
ori $25, $0, 0x68
ori $19, $0, 0x68
nop
beq $31, $0, Test308End
ori $31, $0, 0x59d8
beq $20, $20, Test308End
ori $31, $0, 0x59e0
beq $25, $19, Test308End
ori $31, $0, 0x59e8
ori $31, $0, 0x59e8
Test308End:
ori $31, $0, 0xbf
Test309Begin:
ori $31, $0, 0x79
ori $20, $0, 0x79
lw $19, -92($19)
add $31, $19, $20
beq $31, $20, Test309End
ori $31, $0, 0x5a08
lui $0, 0x0
ori $31, $0, 0x5a0c
Test309End:
ori $31, $0, 0x26
Test310Begin:
ori $20, $0, 0x30
ori $20, $0, 0x30
lw $25, 12($25)
beq $20, $20, Test310End
ori $31, $0, 0x5a28
jr $11
ori $31, $0, 0x5a30
nop
ori $31, $0, 0x5a34
Test310End:
ori $31, $0, 0x46
Test311Begin:
ori $19, $0, 0x73
ori $31, $0, 0x73
beq $19, $31, Test311End
ori $31, $0, 0x5a4c
jr $6
ori $31, $0, 0x5a54
jr $16
ori $31, $0, 0x5a5c
sw $31, 100($0)
ori $31, $0, 0x5a60
Test311End:
ori $31, $0, 0x4c
Test312Begin:
ori $25, $0, 0x59
ori $20, $0, 0x59
beq $25, $20, Test312End
ori $31, $0, 0x5a78
nop
sw $19, -22988($31)
jr $21
ori $31, $0, 0x5a88
ori $31, $0, 0x5a88
Test312End:
ori $31, $0, 0x6
Test313Begin:
lui $20, 0x0
lw $0, 81($19)
jr $9
ori $31, $0, 0x5aa0
nop
ori $31, $0, 0x5aa4
Test313End:
ori $31, $0, 0x7d
Test314Begin:
ori $25, $0, 0x3b
ori $31, $0, 0x3b
ori $19, $0, 0x90
ori $25, $0, 0x90
beq $25, $31, Test314End
ori $31, $0, 0x5ac4
beq $19, $25, Test314End
ori $31, $0, 0x5acc
jal JBackFor22_0
ori $31, $0, 0x5ad4
sw $19, 52($19)
ori $31, $0, 0x5ad8
Test314End:
ori $22, $0, 0x3074
ori $31, $0, 0x70
Test315Begin:
sub $20, $19, $0
nop
sw $0, -12($25)
sw $0, -56($19)
ori $31, $0, 0x5af4
Test315End:
ori $31, $0, 0xad
Test316Begin:
ori $31, $20, 0x87
lw $31, 0($20)
jr $11
ori $31, $0, 0x5b0c
jr $11
ori $31, $0, 0x5b14
ori $31, $0, 0x5b14
Test316End:
ori $31, $0, 0xa1
Test317Begin:
jr $21
ori $31, $0, 0x5b24
lui $0, 0x0
sw $19, -23168($31)
jal JBackFor31_0
nop
ori $31, $0, 0x5b34
Test317End:
ori $31, $0, 0xac
Test318Begin:
jal JBackFor31_0
nop
jal JBackFor31_0
nop
sw $19, 48($0)
sub $0, $25, $25
ori $31, $0, 0x5b54
Test318End:
ori $31, $0, 0xa1
Test319Begin:
sw $31, 48($25)
jr $16
ori $31, $0, 0x5b68
jr $11
ori $31, $0, 0x5b70
sub $20, $19, $31
ori $31, $0, 0x5b74
Test319End:
ori $20, $0, 0x39
ori $31, $0, 0xb1
Test320Begin:
jr $16
ori $31, $0, 0x5b88
add $20, $0, $25
sub $25, $20, $0
lui $25, 0x0
ori $31, $0, 0x5b94
Test320End:
ori $31, $0, 0x1
Test321Begin:
lw $20, -80($19)
jr $22
ori $31, $0, 0x5ba8
lw $19, 152($0)
jal JBackFor31_0
nop
ori $31, $0, 0x5bb4
Test321End:
ori $31, $0, 0x6e
Test322Begin:
ori $19, $0, 0x21
ori $0, $0, 0x21
nop
beq $19, $0, Test322End
ori $31, $0, 0x5bd0
sw $0, 188($0)
jr $24
ori $31, $0, 0x5bdc
ori $31, $0, 0x5bdc
Test322End:
ori $31, $0, 0x4b
Test323Begin:
jr $21
ori $31, $0, 0x5bec
sub $19, $0, $19
sw $19, 129($19)
jal JBackFor6_0
ori $31, $0, 0x5bfc
ori $31, $0, 0x5bfc
Test323End:
ori $6, $0, 0x30a4
ori $31, $0, 0x24
Test324Begin:
ori $25, $0, 0x87
ori $31, $0, 0x87
beq $25, $31, Test324End
ori $31, $0, 0x5c18
lw $20, 124($20)
jr $9
ori $31, $0, 0x5c24
lw $0, 57($19)
ori $31, $0, 0x5c28
Test324End:
ori $31, $0, 0x88
Test325Begin:
ori $31, $0, 0xbd
ori $0, $0, 0xbd
jr $16
ori $31, $0, 0x5c40
ori $19, $20, 0x21
lw $0, -55($25)
beq $31, $0, Test325End
ori $31, $0, 0x5c50
ori $31, $0, 0x5c50
Test325End:
ori $31, $0, 0x9e
Test326Begin:
nop
lui $31, 0x0
nop
lui $25, 0x0
ori $31, $0, 0x5c68
Test326End:
ori $31, $0, 0x91
Test327Begin:
ori $0, $0, 0x3e
ori $31, $0, 0x3e
jal JBackFor24_0
ori $31, $0, 0x5c80
lw $20, 116($20)
lw $20, 24($0)
beq $0, $31, Test327End
ori $31, $0, 0x5c90
ori $31, $0, 0x5c90
Test327End:
ori $24, $0, 0x30a4
ori $31, $0, 0x16
Test328Begin:
nop
ori $0, $31, 0xa7
nop
lui $20, 0x0
ori $31, $0, 0x5cac
Test328End:
ori $31, $0, 0x76
Test329Begin:
ori $20, $0, 0x61
ori $25, $0, 0x61
lui $31, 0x0
sw $19, 35($25)
beq $20, $25, Test329End
ori $31, $0, 0x5ccc
lw $31, 47($19)
ori $31, $0, 0x5cd0
Test329End:
ori $31, $0, 0x10
Test330Begin:
lui $25, 0x0
ori $31, $0, 0xbe
jr $6
ori $31, $0, 0x5ce8
sw $20, -23664($31)
ori $31, $0, 0x5cec
Test330End:
ori $31, $0, 0xc7
Test331Begin:
jal JBackFor21_0
ori $31, $0, 0x5cfc
nop
jr $24
ori $31, $0, 0x5d08
lw $25, 7($19)
ori $31, $0, 0x5d0c
Test331End:
ori $21, $0, 0x30a4
ori $31, $0, 0x62
Test332Begin:
ori $31, $0, 0x6f
ori $25, $0, 0x6f
lui $19, 0x0
lui $20, 0x0
lw $25, -107($25)
beq $31, $25, Test332End
ori $31, $0, 0x5d34
ori $31, $0, 0x5d34
Test332End:
ori $25, $0, 0x84
ori $31, $0, 0x7f
Test333Begin:
jal JBackFor24_0
ori $31, $0, 0x5d48
ori $25, $19, 0xb1
lw $0, -23732($31)
sw $25, 160($20)
ori $31, $0, 0x5d54
Test333End:
ori $24, $0, 0x3038
ori $31, $0, 0x21
Test334Begin:
lw $31, 32($19)
jr $22
ori $31, $0, 0x5d6c
sub $19, $0, $19
lui $19, 0x0
ori $31, $0, 0x5d74
Test334End:
ori $31, $0, 0xa3
Test335Begin:
ori $25, $0, 0x4
ori $0, $0, 0x4
jr $15
ori $31, $0, 0x5d8c
sw $20, 60($0)
beq $25, $0, Test335End
ori $31, $0, 0x5d98
sw $19, -23776($31)
ori $31, $0, 0x5d9c
Test335End:
ori $31, $0, 0x90
Test336Begin:
jal JBackFor16_0
ori $31, $0, 0x5dac
jal JBackFor15_0
ori $31, $0, 0x5db4
lw $19, -23988($31)
lw $19, 28($0)
ori $31, $0, 0x5dbc
Test336End:
ori $16, $0, 0x30a4
ori $15, $0, 0x304c
ori $31, $0, 0x53
Test337Begin:
sw $0, 64($20)
nop
jal JBackFor31_0
nop
nop
ori $31, $0, 0x5de0
Test337End:
ori $31, $0, 0x1a
Test338Begin:
sw $0, 76($25)
jal JBackFor24_0
ori $31, $0, 0x5df4
jr $16
ori $31, $0, 0x5dfc
ori $31, $0, 0x36
ori $31, $0, 0x5e00
Test338End:
ori $24, $0, 0x30a4
ori $31, $0, 0x5f
Test339Begin:
sw $0, 164($25)
lw $0, 124($0)
sw $0, 4($19)
lw $31, 148($20)
ori $31, $0, 0x5e1c
Test339End:
ori $31, $0, 0x9c
Test340Begin:
ori $25, $0, 0x2b
ori $0, $0, 0x2b
beq $25, $0, Test340End
ori $31, $0, 0x5e34
lw $31, 44($0)
sub $31, $31, $31
jal JBackFor31_0
nop
ori $31, $0, 0x5e44
Test340End:
ori $31, $0, 0xac
Test341Begin:
lui $20, 0x0
sw $19, 148($19)
lui $0, 0x0
lui $31, 0x0
ori $31, $0, 0x5e5c
Test341End:
ori $31, $0, 0xa6
Test342Begin:
jr $21
ori $31, $0, 0x5e6c
lw $0, -24028($31)
sw $0, 72($0)
lui $20, 0x0
ori $31, $0, 0x5e78
Test342End:
ori $31, $0, 0x9e
Test343Begin:
ori $25, $0, 0x4e
ori $20, $0, 0x4e
ori $25, $20, 0x16
jr $16
ori $31, $0, 0x5e94
beq $25, $20, Test343End
ori $31, $0, 0x5e9c
jal JBackFor11_0
ori $31, $0, 0x5ea4
ori $31, $0, 0x5ea4
Test343End:
ori $11, $0, 0x3060
ori $31, $0, 0xaa
Test344Begin:
jr $11
ori $31, $0, 0x5eb8
jal JBackFor31_0
nop
jr $21
ori $31, $0, 0x5ec8
jr $6
ori $31, $0, 0x5ed0
ori $31, $0, 0x5ed0
Test344End:
ori $31, $0, 0x83
Test345Begin:
ori $31, $20, 0x90
jr $9
ori $31, $0, 0x5ee4
lui $31, 0x0
jal JBackFor24_0
ori $31, $0, 0x5ef0
ori $31, $0, 0x5ef0
Test345End:
ori $24, $0, 0x3038
ori $31, $0, 0x98
Test346Begin:
lw $0, -82($25)
ori $25, $25, 0x66
sw $20, 8($19)
sw $31, -42($25)
ori $31, $0, 0x5f0c
Test346End:
ori $31, $0, 0xc3
Test347Begin:
ori $19, $0, 0x7e
ori $20, $0, 0x7e
ori $19, $0, 0x53
ori $0, $0, 0x53
beq $19, $20, Test347End
ori $31, $0, 0x5f2c
lui $0, 0x0
lui $31, 0x0
beq $19, $0, Test347End
ori $31, $0, 0x5f3c
ori $31, $0, 0x5f3c
Test347End:
ori $31, $0, 0x6f
Test348Begin:
ori $25, $0, 0x1d
ori $0, $0, 0x1d
ori $25, $0, 0x4f
ori $25, $0, 0x4f
beq $25, $0, Test348End
ori $31, $0, 0x5f5c
jr $24
ori $31, $0, 0x5f64
sw $20, -50($20)
beq $25, $25, Test348End
ori $31, $0, 0x5f70
ori $31, $0, 0x5f70
Test348End:
ori $31, $0, 0xc0
Test349Begin:
ori $19, $0, 0xa5
ori $19, $0, 0xa5
lw $19, -27($25)
beq $19, $19, Test349End
ori $31, $0, 0x5f8c
ori $31, $25, 0x20
jal JBackFor31_0
nop
ori $31, $0, 0x5f98
Test349End:
ori $31, $0, 0x1b
Test350Begin:
lw $31, -48($19)
nop
sw $19, -19($25)
add $31, $0, $19
ori $31, $0, 0x5fb0
Test350End:
ori $31, $0, 0x9b
Test351Begin:
add $19, $20, $20
jr $15
ori $31, $0, 0x5fc4
jr $22
ori $31, $0, 0x5fcc
lui $20, 0x0
ori $31, $0, 0x5fd0
Test351End:
ori $19, $0, 0x3f
ori $31, $0, 0x6e
Test352Begin:
add $19, $20, $19
lw $0, 33($19)
ori $25, $20, 0x85
ori $0, $31, 0xc0
ori $31, $0, 0x5fec
Test352End:
ori $31, $0, 0x2a
Test353Begin:
ori $31, $25, 0x36
sw $0, -167($31)
lw $0, -7($31)
sw $31, -25($25)
ori $31, $0, 0x6004
Test353End:
ori $31, $0, 0x42
Test354Begin:
ori $20, $0, 0xad
ori $31, $0, 0xad
ori $31, $0, 0xc7
ori $25, $0, 0xc7
beq $20, $31, Test354End
ori $31, $0, 0x6024
beq $31, $25, Test354End
ori $31, $0, 0x602c
lw $19, -24480($31)
nop
ori $31, $0, 0x6034
Test354End:
ori $31, $0, 0x8f
Test355Begin:
sub $0, $20, $19
lw $0, 44($0)
ori $0, $25, 0x45
nop
ori $31, $0, 0x604c
Test355End:
ori $31, $0, 0x1b
Test356Begin:
jal JBackFor31_0
nop
lui $20, 0x0
nop
ori $20, $31, 0x11
ori $31, $0, 0x6068
Test356End:
ori $20, $0, 0x1d
ori $31, $0, 0x35
Test357Begin:
sw $31, 56($19)
jr $15
ori $31, $0, 0x6080
jr $24
ori $31, $0, 0x6088
add $19, $25, $31
ori $31, $0, 0x608c
Test357End:
ori $19, $0, 0x29
ori $31, $0, 0x4e
Test358Begin:
sw $31, 155($20)
nop
sub $25, $0, $19
lw $25, 233($25)
ori $31, $0, 0x60a8
Test358End:
ori $31, $0, 0x78
Test359Begin:
ori $20, $0, 0x67
ori $25, $0, 0x67
lui $19, 0x0
beq $20, $25, Test359End
ori $31, $0, 0x60c4
jal JBackFor31_0
nop
lw $31, -39($20)
ori $31, $0, 0x60d0
Test359End:
ori $31, $0, 0xac
Test360Begin:
lw $19, 144($19)
jal JBackFor21_0
ori $31, $0, 0x60e4
lw $20, 152($19)
lui $20, 0x0
ori $31, $0, 0x60ec
Test360End:
ori $21, $0, 0x30a4
ori $31, $0, 0xa2
Test361Begin:
ori $31, $0, 0x51
ori $0, $0, 0x51
jal JBackFor9_0
ori $31, $0, 0x6108
nop
beq $31, $0, Test361End
ori $31, $0, 0x6114
nop
ori $31, $0, 0x6118
Test361End:
ori $9, $0, 0x30a4
ori $31, $0, 0xbc
Test362Begin:
jr $11
ori $31, $0, 0x612c
sub $31, $25, $0
lw $20, 73($31)
jr $15
ori $31, $0, 0x613c
ori $31, $0, 0x613c
Test362End:
ori $31, $0, 0x21
Test363Begin:
nop
jr $21
ori $31, $0, 0x6150
lui $31, 0x0
ori $31, $25, 0xbc
ori $31, $0, 0x6158
Test363End:
ori $31, $0, 0x83
Test364Begin:
sub $19, $20, $19
jal JBackFor31_0
nop
lui $19, 0x0
nop
ori $31, $0, 0x6174
Test364End:
ori $31, $0, 0x7b
Test365Begin:
lw $19, 62($20)
sub $31, $25, $25
jr $11
ori $31, $0, 0x618c
lw $20, 134($20)
ori $31, $0, 0x6190
Test365End:
ori $31, $0, 0x29
Test366Begin:
lw $0, -87($25)
nop
sub $20, $31, $31
jr $22
ori $31, $0, 0x61ac
ori $31, $0, 0x61ac
Test366End:
ori $31, $0, 0x29
Test367Begin:
lw $20, 12($19)
sub $19, $0, $31
jal JBackFor31_0
nop
sw $20, 65($25)
ori $31, $0, 0x61c8
Test367End:
ori $31, $0, 0x4f
Test368Begin:
ori $20, $0, 0xa1
ori $31, $0, 0xa1
jal JBackFor31_0
nop
lui $20, 0x0
ori $20, $31, 0x83
beq $20, $31, Test368End
ori $31, $0, 0x61f0
ori $31, $0, 0x61f0
Test368End:
ori $20, $0, 0x98
ori $31, $0, 0x5f
Test369Begin:
ori $25, $0, 0x30
ori $25, $0, 0x30
beq $25, $25, Test369End
ori $31, $0, 0x620c
lui $20, 0x0
lui $25, 0x0
sw $0, -25024($31)
ori $31, $0, 0x6218
Test369End:
ori $31, $0, 0x1b
Test370Begin:
ori $31, $0, 0x71
ori $0, $0, 0x71
jr $6
ori $31, $0, 0x6230
add $0, $20, $19
nop
beq $31, $0, Test370End
ori $31, $0, 0x6240
ori $31, $0, 0x6240
Test370End:
ori $31, $0, 0x5
Test371Begin:
lui $19, 0x0
jal JBackFor22_0
ori $31, $0, 0x6254
add $20, $25, $31
jal JBackFor31_0
nop
ori $31, $0, 0x6260
Test371End:
ori $22, $0, 0x3074
ori $20, $0, 0x58
ori $31, $0, 0xad
Test372Begin:
jal JBackFor11_0
ori $31, $0, 0x6278
ori $31, $19, 0x65
lw $0, 108($20)
add $31, $0, $19
ori $31, $0, 0x6284
Test372End:
ori $11, $0, 0x30a4
ori $31, $0, 0x2a

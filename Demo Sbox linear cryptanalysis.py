import random

SBOX = [9,  11,  12,   4,  10,   1,  2,  6,  13,  7,  3,  8,  15,  14,   0,   5]
REVSBOX = [14,   5,   6,  10,   3,  15,  7,  9,  11,  0,  4,  1,   2,   8,  13,  12]

TableApproximation = []

KEY1 = KEY2 = None
MESSAGE_Plain, MESSAGE_Cipher = [], []
'''执行加密轮函数'''
function_to_round = lambda message, key : SBOX[message ^ key]
'''执行解密轮函数'''
function_to_round_inverse = lambda message_cipher, key : SBOX[message_cipher] ^ key

'''
随机生成两个取值在(0,15)之间的秘钥,从而得到明文和密文
'''
def GenerateData():

    global KEY1, KEY2, MESSAGE_Plain, MESSAGE_Cipher
    KEY1 = random.randint(0,15)
    KEY2 = random.randint(0,15)
    print('Clement :')
    print('   KEY1 : {0} = {0:04b}'.format(KEY1))
    print('   KEY2 : {0} = {0:04b}'.format(KEY2))

    for i in range(0,16):
        MESSAGE_Plain += [i]
        MESSAGE_Cipher += [EncryptedMessage(i, KEY1, KEY2)]
        print('MESSAGE {0}:'.format(i+1))
        print('   Plain   {0} = {0:04b}'.format(MESSAGE_Plain[i]))
        print('   Cipher {0} = {0:04b}'.format(MESSAGE_Cipher[i]))

def EncryptedMessage(message, k1, k2):
    '''
    进行两轮加密
    '''
    # round 1
    message = function_to_round(message, k1)
    # round 2
    message = function_to_round(message, k2)
    return message

def decodingMessage(message, k1, k2):
    # reverse round 2
    message = function_to_round_inverse(message, k2)
    # reverse round 1
    message = function_to_round_inverse(message, k1)
    return message

'''显示线性逼近表,第一行和第一列是无意义的，所以没有显示'''
def ShowTableApproximation(matrix):
    print('     | ', end = '')
    for i in range (1,16):
        print("{0:0=2d}".format(i), '  ', end = '')
    print('|\n', '------------------------------------------------------------------------------------')

    for i in range(1,len(matrix)):
        print('|' , "{0:0=2d}".format(i), ' | ', end = '')
        for j in range(1, len(matrix[i])):
            print("{0:0=2d}".format(matrix[i][j]), '  ', end = '')
        print('| ')
    print('------------------------------------------------------------------------------------')

'''计算线性分布表'''
def AllApproximation():
    global TableApproximation
    ## Approximation table creation
    for i in range(0,16):
        TableApproximation += [[]]
        for j in range(0,16):
            TableApproximation[i] += [0]

    print('Initialize approximation table', '\n--------------------------------')
    ShowTableApproximation(TableApproximation)

    ## Search approximation
    print('\nSearch approximation...')
    for o_mask in range (1,16):
        for i_mask in range (1,16):
            for sbox_input in range (0,16):
                if FindParity(sbox_input, i_mask) == FindParity(SBOX[sbox_input], o_mask):
                    TableApproximation[i_mask][o_mask] += 1               
    
    ## Linear approximation display
    print('\nApproximate value!', '\n-------------------------------')
    ShowTableApproximation(TableApproximation)

#寻找对
def FindParity(x, y):
    maskedValue = x & y
    
    parity = 0
    while maskedValue > 0:
        extractionBinaire =  maskedValue % 2
        maskedValue //= 2
        parity = parity ^ extractionBinaire

    return parity

'''遍历寻找线性逼近表中的最大值'''
def FindABetterApproximation():
    BestAnswer = -1
    for ligne in TableApproximation:
        for approximation in ligne:
            if approximation > BestAnswer:
                BestAnswer = approximation
    return BestAnswer

def FindBetterMaskApproximation(Approx, xor_utilise):
    mask = []
    for i in range(0,16):
        for j in range(0,16):
            if TableApproximation[i][j] == Approx:
                mask += [[i,j]]
    '''这个线性逼近表没有减去8,应该寻找的是距离8最远的数,包括大于8和小于8的，所以才有下面这个判断'''
    if xor_utilise == True:
        for i in range(0,16):
            for j in range(0,16):
                if TableApproximation[i][j] == 16 - Approx:
                    mask += [[i,j]]

    return mask

def LinearAttack(mask):
    Score_Cle = []
    i_mask = mask[0]
    o_mask = mask[1]
    print('Calculate all M for all possible K1...')
    print('Hide and test each "M->Input mask" and "C->Output mask"and each P...')
    print('Give everyone a point K1, if M_mask equal C_mask, let score K1 increase 1')
    for K1_possible in range (0,15):
        Score_Cle += [0]
        for i in range(0,len(MESSAGE_Plain)):
            Message_Semi_Chiffre = function_to_round(MESSAGE_Plain[i] , K1_possible)

            if FindParity(Message_Semi_Chiffre, i_mask) ==  FindParity(MESSAGE_Cipher[i], o_mask):
                Score_Cle[K1_possible] += 1
            else:
                Score_Cle[K1_possible] -= 1
    print('\nEvery K1 score found !')
    print(Score_Cle)

    print('\nSearch for the best K1 (A bigger score)')
    Best_score = -100
    for i in range (0,len(Score_Cle)):
        if Score_Cle[i] > Best_score :
            Best_score  = Score_Cle[i]
    First_class = []
    for i in range (0,len(Score_Cle)):
        if Score_Cle[i] == Best_score :
            First_class += [i]
    print('Best K1 list !')
    print(First_class)

    print('\nK2 search')
    KeyA, KeyB = FindK2(First_class)
    print(KeyA,KeyB)

    return KeyA, KeyB

def FindK2(k1_list):
    for k1 in k1_list:
        k1_mal = False
        k2 = function_to_round(MESSAGE_Plain[0], k1) ^ REVSBOX[MESSAGE_Cipher[0]]
        
        for i in range(0, len (MESSAGE_Cipher)):
            message = EncryptedMessage(MESSAGE_Plain[i], k1, k2)
            if message != MESSAGE_Cipher[i]:
                k1_mal = True
        
        if k1_mal == False:
            return k1, k2
    
    return -1, -1

if __name__ == '__main__':
    print('DataGeneration:')
    GenerateData() 

    print('\nDemo encryption analysis', '\n-------------------------\n')
    AllApproximation()

    print('\nResearch Best approximation')
    '''寻找线性逼近表中最大的值'''
    meilleurApprox = FindABetterApproximation()
    maskMeilleurApprox = FindBetterMaskApproximation(meilleurApprox, True)
    for i_o_masque in maskMeilleurApprox:
        print('Better Approximation Value :','{0} -> {1} : {2} = {1:04b} : {2:04b}'.format(meilleurApprox,i_o_masque[0],i_o_masque[1]))

    print('\nLinear Attack :\n')
    KeyA, KeyB = LinearAttack(random.choice(maskMeilleurApprox))
    if KeyA == -1 or KeyB == -1:
        print('\nFAIL : Can\'t find !')
    else:
        print('\nFind the key !')
        print('KEY 1: {0} = {0:04b}\nKEY 2: {1} = {1:04b}'.format(KeyA, KeyB))
        print('KEY = KEY1KEY2 = {0:04b}{1:04b}'.format(KeyA,KeyB))
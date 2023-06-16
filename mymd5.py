from array import array
from logger import logger
from math import floor, sin

A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476

# 常量表
T = [floor(2**32 * abs(sin(i))) for i in range(1, 65)]

# 循环左移数
S = [
    [7, 12, 17, 22],  # FF
    [5, 9, 14, 20],  # GG
    [4, 11, 16, 23],  # HH
    [6, 10, 15, 21]  # II
]

# 每轮处理顺序
R = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # FF
    [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12],  # GG
    [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2],  # HH
    [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]  # II
]


def toint32(n: int) -> int:
    return n & 0xFFFFFFFF


def circle_shift(x: int, n: int) -> int:
    x = toint32(x)
    return toint32((x << n) | (x >> (32 - n)))


def F(x: int, y: int, z: int) -> int:
    return (x & y) | ((~x) & z)


def G(x: int, y: int, z: int) -> int:
    return (x & z) | (y & (~z))


def H(x: int, y: int, z: int) -> int:
    return x ^ y ^ z


def I(x: int, y: int, z: int) -> int:
    return y ^ (x | (~z))


def DF(a: int, b: int, c: int, d: int, Mj: int, S: int, Ti: int,
       func: callable) -> int:

    a = func(b, c, d) + Mj + Ti + a
    a = circle_shift(a, S)
    a = toint32(a + b)

    return a


def get_pad(data: array) -> array:
    dlen = data.buffer_info()[1] * data.itemsize * 8
    m = dlen % 512
    plen = (512 + (448 - m)) % 512
    if plen == 0:
        plen = 512
    plen = plen // 8
    pad = array('B', [0x80] + [0x00] * (plen - 1))
    len_pad = int.to_bytes(dlen, 8, 'little')
    pad.extend(len_pad)
    pad = array('B', pad.tobytes())

    return pad


def process_blk(block: array, A: int, B: int, C: int, D: int) -> tuple:
    AA, BB, CC, DD = A, B, C, D
    funcs = [F, G, H, I]

    for i in range(0, 4):
        for j in range(0, 16, 4):
            AA = DF(AA, BB, CC, DD, block[R[i][j + 0]], S[i][0],
                    T[i * 16 + j + 0], funcs[i])
            DD = DF(DD, AA, BB, CC, block[R[i][j + 1]], S[i][1],
                    T[i * 16 + j + 1], funcs[i])
            CC = DF(CC, DD, AA, BB, block[R[i][j + 2]], S[i][2],
                    T[i * 16 + j + 2], funcs[i])
            BB = DF(BB, CC, DD, AA, block[R[i][j + 3]], S[i][3],
                    T[i * 16 + j + 3], funcs[i])

    A = toint32(A + AA)
    B = toint32(B + BB)
    C = toint32(C + CC)
    D = toint32(D + DD)

    return A, B, C, D


def get_md5(_data: bytes) -> str:
    data = array('B', b'')
    data.frombytes(_data)
    logger.debug(f"填充前：{' '.join([f'{i:08b}' for i in list(data)])}")

    pad = get_pad(data)
    logger.debug(f"填充值: {' '.join([f'{i:08b}' for i in list(pad)])}")

    data.extend(pad)
    logger.debug(f"填充后: {' '.join([f'{i:08b}' for i in list(data)])}")
    data = array('L', data.tobytes())  # 转换成32bits一组
    logger.debug(f"填充后: {' '.join([f'{i:032b}' for i in list(data)])}")

    n = data.buffer_info()[1] // 16  #计算block的数目，一个block为512 = 16 * 32bits

    AA, BB, CC, DD = A, B, C, D

    for i in range(0, n):
        logger.debug(f"{'='*30}计算第{i+1: ^3}个block{'='*30}")
        block = data[i * 16:(i + 1) * 16]
        logger.debug(
            f"Block{i}: {' '.join([f'{i:032b}' for i in list(block)])}")
        AA, BB, CC, DD = process_blk(block, AA, BB, CC, DD)
        logger.debug(f"A = {AA:08X}, B = {BB:08X}, C = {CC:08X}, D = {DD:08X}")

    return array('L', [AA, BB, CC, DD]).tobytes().hex()

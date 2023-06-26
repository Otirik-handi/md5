from array import array
from logger import logger
from math import floor, sin

# logger.setLevel("DEBUG")

init_A = 0x67452301
init_B = 0xEFCDAB89
init_C = 0x98BADCFE
init_D = 0x10325476

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

def read_file(filepath: str, mode: str = 'rb', size: int = 1024) -> bytes:
    with open(filepath, mode) as f:
        while True:
            chunk = f.read(size)
            if not chunk:
                break
            yield chunk


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


def get_pad(block: array, total_len: int = None) -> array:
    # 最后一个块的长度
    block_len = block.buffer_info()[1] * block.itemsize * 8
    # 计算填充长度
    m = block_len % 512
    plen = (512 + (448 - m)) % 512
    if plen == 0:
        plen = 448
    plen = plen // 8
    # 填充值
    pad = array('B', [0x80] + [0x00] * (plen - 1))
    # 64bits长度填充，计算的是整个数据的长度
    length_pad = int.to_bytes(total_len*8, 8, 'little')
    pad.extend(length_pad)
    logger.debug(f"block_len: {block_len} bits, m: {m} bits, plen: {plen} bytes, total_len: {total_len*8} bits, pad: {pad.tobytes().hex(sep=' ', bytes_per_sep=4)}")

    return pad


def transform(block: array, A: int, B: int, C: int, D: int) -> tuple:
    AA, BB, CC, DD = A, B, C, D
    funcs = [F, G, H, I]
    
    logger.debug(f" [transform]  input: A = 0x{A:X}, B = 0x{B:X}, C = {C}, D = 0x{D:X}")
    
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
    
    logger.debug(f"[transform] output: A = 0x{A:X}, B = 0x{B:X}, C = 0x{C:X}, D = 0x{D:X}\n")

    return A, B, C, D


def get_md5(_data: bytes) -> str:
    data = array('B', _data)
    logger.debug(f"填充前：{' '.join([f'{i:08b}' for i in list(data)])}")

    pad = get_pad(data, len(data))
    logger.debug(f"填充值: {' '.join([f'{i:08b}' for i in list(pad)])}")

    data.extend(pad)
    logger.debug(f"填充后: {' '.join([f'{i:08b}' for i in list(data)])}")
    
    data = array('L', data.tobytes())  # 转换成32bits一组

    n = data.buffer_info()[1] // 16  #计算block的数目，一个block为512 = 16 * 32bits

    AA, BB, CC, DD = init_A, init_B, init_C, init_D

    for i in range(0, n):
        
        block = data[i * 16:(i + 1) * 16]
        
        AA, BB, CC, DD = transform(block, AA, BB, CC, DD)
        
        logger.debug(f"A = {AA:08X}, B = {BB:08X}, C = {CC:08X}, D = {DD:08X}")

    return array('L', [AA, BB, CC, DD]).tobytes().hex()


def get_file_md5(filepath: str) -> str:
    m = MD5()

    for chunk in read_file(filepath, size=4096):
        if chunk is None:
            break   

        m.update(chunk)

    cipher = m.final()
    print(cipher)
    return cipher


class MD5(object):
    
    def __init__(self) -> None:
        self.A = init_A
        self.B = init_B
        self.C = init_C
        self.D = init_D
        self.total_len = 0
        self.buf_index = 0
        self.buffer = None
        
        
    def update(self, data: bytes) -> None:
        self.total_len += len(data)
        
        partlen = (64 - self.buf_index) % 64
        
        if partlen:
            self.buffer.frombytes(data[0:partlen])
            self.A, self.B, self.C, self.D = transform(array('L', self.buffer.tobytes()), self.A, self.B, self.C, self.D)
            logger.debug(f"buffer: {self.buffer.tobytes()}")
        else:
            partlen = 0
        
        n,self.buf_index = divmod(len(data)-partlen, 64)
        
        for i in range(0,n):
            self.buffer = array('L', data[64*i : 64*(i + 1)])
            self.A, self.B, self.C, self.D = transform(self.buffer, self.A, self.B, self.C, self.D)
        
        self.buffer = array('B', data[partlen+n*64:])
        logger.debug(f" input:\n\tdata: {data}, len: {len(data)}\n\tpartlen: {partlen}, buf_index: {self.buf_index}\n\tbuffer: {self.buffer.tobytes()}\n")

    
    
    def final(self) -> str:
        pad = get_pad(array('B', self.buffer.tobytes()), self.total_len)
        self.buffer.frombytes(pad.tobytes())
        logger.debug(f"buffer: {self.buffer.tobytes().hex(sep=' ', bytes_per_sep=4)}, len: {len(self.buffer)}")
        self.A, self.B, self.C, self.D = transform(array('L', self.buffer.tobytes()), self.A, self.B, self.C, self.D)
        return  array('L', [self.A,self.B,self.C,self.D]).tobytes().hex()

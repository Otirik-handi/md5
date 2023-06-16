from mymd5 import get_md5
from hashlib import md5

def test_plain():
    plain = "Hello,I am Otirik~"
    data = plain.encode()
    val1 = get_md5(data)
    val2 = md5(data).hexdigest()
    assert val1 == val2
    print(f"{'get_md5':<12} -> {val1}\n{'hashlib.md5':<12} -> {val2}")

def test_file():
    filename="./logger.py"
    data = b''
    
    with open(filename, 'rb') as f:
        data = f.read(100)
        
    val1 = get_md5(data)
    val2 = md5(data).hexdigest()
    assert val1 == val2
    print(f"{'get_md5':<12} -> {val1}\n{'hashlib.md5':<12} -> {val2}")
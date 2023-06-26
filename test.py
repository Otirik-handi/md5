from mymd5 import *
from hashlib import md5

def test_plain():
    plain = "Hello,I am Otirik~"
    data = plain.encode()
    val1 = get_md5(data)
    val2 = md5(data).hexdigest()
    assert val1 == val2
    print(f"{'get_md5':<12} -> {val1}\n{'hashlib.md5':<12} -> {val2}")

def test_file():
    val = get_file_md5(r"D:\下载\nvm-setup.exe")
    print(val)
    

if __name__ == "__main__":
    test_file()
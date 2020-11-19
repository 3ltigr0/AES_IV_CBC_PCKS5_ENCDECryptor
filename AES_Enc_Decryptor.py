# pycryptodome 라이브러리를 사용하였습니다. (pip install pycryptodome)
from Crypto.Cipher import AES # 암호화 라이브러리 AES 모듈
from Crypto import Random # iv값 random으로 만들기
from Crypto.Util.Padding import pad, unpad # 패딩
from Crypto.Hash import SHA256 # 비밀키 SHA256 사용하여 해쉬
import os # 복호화시 암호화된 파일 삭제

def encrypt(secretkey, filename): # 암호화 함수 / 비밀키, 파일명
    f = open(filename, "rb") # 암호화할 파일 열기
    text = f.read() # 내용 불러오기
    f.close() # 파일 닫기
    text_paded = pad(text, AES.block_size) # pkcs5 패딩
    key = SHA256.new(secretkey.encode("utf-8")).digest() # 비밀키 SHA256으로 해쉬 / AES256
    iv = Random.new().read(AES.block_size) # 임의의 iv 값 생성
    encryptor = AES.new(key, AES.MODE_CBC, iv) # 암호
    text_encrypted = iv + encryptor.encrypt(text_paded) # iv 값 삽입 및 암호화
    f = open(filename+".encrypted", "wb") # 암호화 파일 생성
    f.write(text_encrypted) # 생성된 파일에 내용 쓰기
    f.close() # 파일 닫기

def decrypt(secretkey, filename): # 복호화 함수 / 비밀키, 파일명
    f = open(filename, "rb") # 암호화된 파일 열기
    text = f.read() # 내용 불러오기
    f.close() # 파일 닫기
    iv = text [:AES.block_size] # iv 값 추출
    key = SHA256.new(secretkey.encode("utf-8")).digest() # 비밀키 SHA256으로 해쉬 / AES256
    decryptor = AES.new(key, AES.MODE_CBC, iv) # 복호
    text_decrypted = decryptor.decrypt(text[AES.block_size:]) # iv값 제외하고 복호화
    text_unpaded = unpad(text_decrypted, AES.block_size) # 언패딩
    f = open("decrypted_"+filename[:-10], "wb") # 복호화 파일 생성
    f.write(text_unpaded) # 생성된 파일에 내용 쓰기
    f.close() # 파일 닫기
    os.remove(filename) # 암호화된 파일 지우기

while True:
    a = int(input("1. 파일 암호화\n2. 파일 복호화\n3. 나가기\n숫자를 입력하세요: "))
    if a == 1:
        filename = str(input("\n암호화할 파일명을 입력하세요: "))
        secretkey = str(input("\n암호화에 사용할 비밀키를 입력하세요: "))
        encrypt(secretkey, filename)
        print("\n암호화를 완료했습니다.")

    elif a == 2:
        filename = str(input("\n복호화할 파일명을 입력하세요: "))
        secretkey = str(input("\n복호화에 사용할 비밀키를 입력하세요: "))
        decrypt(secretkey, filename)
        print("\n복호화를 완료했습니다.")
    
    elif a == 3:
        print("\n종료합니다.")
        break
    
    print("")

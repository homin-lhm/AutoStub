from Crypto.Cipher import AES
import base64


class AesHandles:
    def __init__(self, key, iv):
        key = key.encode("utf-8")
        iv = iv.encode("utf-8")
        self.key = key
        self.iv = iv

    def encrypt(self, text):
        encryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 将数据填充到16的倍数
        data = text + ((16 - len(text) % 16) * '*')
        res = encryptor.encrypt(data.encode("utf-8"))
        res = base64.b64encode(res)

        return res.decode("utf-8")

    def decrypt(self, text):
        if isinstance(text, str):
            text = text.encode("utf-8")
        text = base64.b64decode(text)
        decryptor = AES.new(self.key, AES.MODE_CBC, self.iv)

        text = decryptor.decrypt(text)
        text = text.decode("utf-8")
        text = text.strip("*")

        return text


if __name__ == '__main__':
    # 定义秘钥和初始偏移量
    k = "hominhominhominQ"
    i = "uiuiuiuiabababab"
    res = AesHandles(k, i).encrypt("123")
    print(res)

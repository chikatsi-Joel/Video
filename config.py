host = "0.0.0.0"
port = "5000"

from  cryptography.fernet import Fernet

key = b'QqKIMhOXMeUnrlEE61LX9EkRkua7VK_J4-54CTFO1u4='

def encrypt(data : str) :
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

def decrypt(data : bytes) :
    cipher = Fernet(key)
    return cipher.decrypt(data).decode()

def Convert(value : int) :
        if value <= 20 :
            return 'tiny'
        elif value <= 40: 
            return 'base'
        elif value <= 60 : 
            return 'small'
        elif value <= 80: 
            return 'medium'
        elif value <= 100 : 
            return 'large'
        
def get_price(type : str) -> int:
    if type == 'small' :
        return 2
    elif(type == "meduim") :
        return 4
    elif type == 'large' :
        return 6
    else :
        return 0
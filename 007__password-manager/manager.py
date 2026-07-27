# a simple password manager which encrypts passwords
from cryptography.fernet import Fernet

def load_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


master_pwd = input('enter your master password: ')
key = load_key() + master_pwd.encode() # encode() takes a string and turn it into bytes
fer = Fernet(key)
'''
def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as f:
        f.write(key)
'''

def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, pwd = data.split(':')
            print(f'user: {user}\tpassword: {str(fer.decrypt(pwd.encode()))}')

def add():
    name = input('account name: ')
    pwd = input('account password: ')
    with open('passwords.txt', 'a') as f:
        f.write(f'{name}:{str(fer.encrypt(pwd.encode()))}\n')

while True:
    mode = input('enter mode add/view/quit: ').lower()
    if (mode == 'quit') or (mode == 'q'):
        break
    if (mode == 'add') or (mode == 'a'):
        add()
    elif (mode == 'view') or (mode == 'v'):
        view()
    else:
        print('entered choice invalid')
        continue

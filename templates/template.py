import sys
import os

sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.password_1 import FernetHasher

def save_password():
    key = None  # Inicializando a chave
    if len(Password.get()) == 0:
        key, path = FernetHasher.create_key(archive=True)
        print('Sua chave foi criada com sucesso, salve-a com cuidado.')
        print(f'Chave: {key.decode("utf-8")}')
        if path:
            print('Chave salva no arquivo. Lembre-se de remover o arquivo após transferi-lo de local.')
            print(f'Caminho: {path}')
        else:
            key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')
    else:
        key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')
    
    domain = input('Domínio: ')
    password = input('Senha: ')
    fernet_user = FernetHasher(key)

    p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
    p1.save()
    print('Senha salva com sucesso!')

def retrieve_password():
    domain = input('Domínio: ')
    key = input('Key: ')
    fernet_user = FernetHasher(key)
    data = Password.get()

    password_found = False
    for i in data:
        if domain in i['domain']:
            password = fernet_user.decrypt(i['password'])
            password_found = True
            break

    if password_found:
        print(f'Sua senha: {password}')
    else:
        print('Nenhuma senha encontrada para o domínio informado.')

action = input('Digite 1 para salvar uma nova senha ou 2 para ver uma senha salva: ')

if action == '1':
    save_password()
elif action == '2':
    retrieve_password()
else:
    print('Ação inválida! Por favor, digite 1 ou 2.')

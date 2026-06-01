# auth.py - Usuarios e autenticacao

usuarios = []   #usurio normal
admins = [{'usuario': 'admin', 'senha': 'adm123'}]  # admin padrao


def criar_usuario(user: str, senha: str|int):
    for u in usuarios:
        if u['usuario'] == user:
            return False  # ja existe = break
    usuarios.append({'usuario': user, 'senha': senha})
    return True 


def criar_admin(user: str, senha: str|int):
    for a in admins:
        if a['usuario'] == user:
            return False  # ja existe
    admins.append({'usuario': user, 'senha': senha})
    return True


def login_usuario(user: str, senha: str|int):
    for u in usuarios:
        if u['usuario'] == user and u['senha'] == senha:
            return True
    return False


def login_admin(user: str, senha: str|int):
    for a in admins:
        if a['usuario'] == user and a['senha'] == senha:
            return True
    return False

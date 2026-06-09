# auth.py - Usuarios e autenticacao

usuarios = []   #usurio normal
admins = [{'usuario': 'a', 'senha': 'a' }]  # admin teste do code


def criar_usuario(user, senha):
    for u in usuarios:
        if u['usuario'] == user:
            return False  # ja existe = break
    usuarios.append({'usuario': user, 'senha': senha})
    return True 


def criar_admin(user, senha):
    for a in admins:
        if a['usuario'] == user:
            return False  
    admins.append({'usuario': user, 'senha': senha})
    return True


def login_usuario(user, senha):
    for u in usuarios:
        if u['usuario'] == user and u['senha'] == senha:
            return True
    return False


def login_admin(user, senha):
    for a in admins:
        if a['usuario'] == user and a['senha'] == senha:
            return True
    return False

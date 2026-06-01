# fazenda.py - Animais, leite, produtos e historico

from datetime import datetime

animais = []        # [{'tipo':..., 'identificacao':..., 'status':...}, ...]
animais_venda = []  # [{'tipo':..., 'identificacao':..., 'status':..., 'valor':...}, ...]
produtos = []       # [{'nome':..., 'kg':..., 'valor_kg':...}, ...]
historico = []      # [{'data':..., 'acao':..., 'item':..., 'qtd':...}, ...]
leite = 0.0

def _calcular_valor(peso: float, arroba: float):
    """15 kg = 1 arroba."""
    return round((peso / 15) * arroba, 2)

def registrar_historico(acao: str, item: str, qtd: float):
    historico.append({
        'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'acao': acao,
        'item': item,
        'qtd': qtd
    })


# --- Animais ---

def cadastrar_animal(tipo: str, identificacao: str, status: str, 
                     peso: float = 0.0, arroba: float = 0.0):
    animal = {
        'tipo':tipo,
        'identificacao':identificacao,
        'status':status,
        'peso':peso,
        'valor': _calcular_valor(peso, arroba) if status.upper() == 'VENDA' else 0.0,
    }
    if status.upper() == 'VENDA':
        animais_venda.append(animal)
    else:
        animais.append(animal)
    registrar_historico("cadastro_animal", f"{tipo} {identificacao}", status)

def listar_animais():
    return animais, animais_venda

def buscar_animal_por_id(ident: str):
    for a in animais:
        if a["identificacao"].lower() == ident.lower():
            return a, animais
    for a in animais_venda:
        if a["identificacao"].lower() == ident.lower():
            return a, animais_venda
    return None, None
    


def remover_animal(ident: str):
    animal, lista = buscar_animal_por_id(ident)
    if not animal:
        return False
    lista.remove(animal)
    registrar_historico("remocao_animal", f"{animal['tipo']} {ident}", "-")
    return True


def atualizar_animal(ident: str, tipo: str, nova_id: str, status: str,
                     peso: float, arroba: float):
    animal, lista = buscar_animal_por_id(ident)
    if not animal:
        return False
    lista.remove(animal)
    cadastrar_animal(tipo, nova_id, status, peso, arroba)
    return True

def comprar_animal(ident):
    for i in range(len(animais_venda)):
        if animais_venda[i]['identificacao'].lower() == ident.lower():
            animal = animais_venda.pop(i)
            registrar_historico('venda_animal', f"{animal['tipo']} {ident}", f"R${animal['valor']:.2f}")
            return animal
    return None


# --- Leite ---

def adicionar_leite(litros: float):
    global leite
    leite += litros
    registrar_historico('producao_leite', 'Leite', f"{litros}L")

def estoque_leite():
    return leite

# --- Produtos derivados ---

def cadastrar_produto(nome: str, kg: float, valor_kg: float, leite_por_kg: float):
    global leite
    leite_necessario = kg * leite_por_kg
    if leite < leite_necessario:
        return False
    leite -= leite_necessario
    # Verifica se produto já existe para somar
    for p in produtos:
        if p["nome"].lower() == nome.lower():
            p["kg"] += kg
            registrar_historico("cadastro_produto", nome, f"{kg}kg")
            return True
    produtos.append({'nome': nome, 'kg': kg, 'valor_kg': valor_kg})
    registrar_historico('cadastro_produto', nome, f"{kg}kg")
    return True

def listar_produtos():
    return produtos


def comprar_produto(nome: str, quantidade: float):
    for p in produtos:
        if p['nome'].lower() == nome.lower():
            if p['kg'] >= quantidade:
                p['kg'] -= quantidade
                total = round(quantidade * p['valor_kg'], 2)
                registrar_historico('venda_produto', nome, f"{quantidade}kg")
                return {'nome': p['nome'], 'quantidade': quantidade, 'total': total, 'valor_kg': p['valor_kg']}
            else:
                return None
    return None

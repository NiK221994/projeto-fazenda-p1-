# fazenda.py - Animais, leite, produtos, historico e carrinho

from datetime import datetime

animais = []        
animais_venda = []  
produtos = []       
historico = []    
carrinho = []       
leite = 0.0
palavras_a = {}





        

def _calcular_valor(peso, arroba):
    """15 kg = 1 arroba."""
    return round((peso / 15) * arroba, 2)


def registrar_historico(acao, item, qtd):
    historico.append({
        'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'acao': acao,
        'item': item,
        'qtd': qtd,
    })


# ---------------------------------------------------------------------------
# Animais
# ---------------------------------------------------------------------------

def cadastrar_animal(tipo, identificacao, status,
                     peso , arroba ):
    ident_existe, _ = buscar_animal_por_id(identificacao)
    if ident_existe:
        print(f'Erro: já existe um animal com a identificação "{identificacao}".')
        return False   

    else:
        if status.upper() == 'VENDA':
            peso = validacao_geral(peso)
            arroba = validacao_geral(arroba)
        animal = {
            'tipo': tipo,
            'identificacao': identificacao,
            'status': status,
            'peso': peso,
            'valor': _calcular_valor(peso, arroba) if status.upper() == 'VENDA' else 0.0,
        }
        if status.upper() == 'VENDA':
            animais_venda.append(animal)
        else:
            animais.append(animal)
        registrar_historico("cadastro_animal", f"{tipo} {identificacao}", status)
        return True


def listar_animais():
    return animais, animais_venda


def buscar_animal_por_id(ident):
    for a in animais:
        if a['identificacao'].lower() == ident.lower():
            return a, animais
    for a in animais_venda:
        if a['identificacao'].lower() == ident.lower():
            return a, animais_venda

    return None ,None


def remover_animal(ident):
    animal, lista = buscar_animal_por_id(ident)
    if not animal:
        return False
    lista.remove(animal)
    registrar_historico("remocao_animal", f"{animal['tipo']} {ident}", "-")
    return True


def atualizar_animal(ident, tipo, nova_id, status, peso , arroba):
    
    animal, lista = buscar_animal_por_id(ident)
    peso = validacao_geral(peso)
    arroba = validacao_geral(arroba)
    if not animal:
        return False
    lista.remove(animal)
    cadastrar_animal(tipo, nova_id, status, peso, arroba)
    registrar_historico('Atualizar_animal',f'{animal['tipo']}{ident},',1)
    return True
    

def comprar_animal(ident):
    for i, a in enumerate(animais_venda):
        if a['identificacao'].lower() == ident.lower():
            animal = animais_venda.pop(i)
            registrar_historico('venda_animal',
                                f"{animal['tipo']} {ident}",
                                f"R${animal['valor']:.2f}")
            return animal
    return None



# Exibicao de animais


def exibir_animais():
    print("=" * 50)
    print("--- Em producao / engorda ---")
    for a in animais:
        print(f"  {a['tipo']} - {a['identificacao']} - {a['status']}")
    print("--- Para venda ---")
    for a in animais_venda:
        print(f"  {a['tipo']} - {a['identificacao']} - {a['status']} - R$ {a['valor']:.2f}")
    print("=" * 50)


def exibir_animais_venda():
    print("-" * 40)
    for a in animais_venda:
        print(f"  tipo: {a['tipo']} - id: {a['identificacao']} - R$ {a['valor']:.2f}")
    print("-" * 40)



# Leite
def adicionar_leite(litros):
    global leite
    litros = validacao_geral(litros)
    leite += litros
    registrar_historico('producao_leite', 'Leite', f"{litros}L")



        
def estoque_leite():
    return leite



# Produtos derivados

def cadastrar_produto(nome, kg, valor_kg , leite_por_kg):
    global leite
    kg = validacao_geral(kg)
    valor_kg = validacao_geral(valor_kg)
    leite_por_kg = validacao_geral(leite_por_kg)
    leite_necessario = kg * leite_por_kg
    if leite < leite_necessario:
        return False
    leite -= leite_necessario
    for p in produtos:
        if p['nome'].lower() == nome.lower():
            p['kg'] += kg
            registrar_historico("cadastro_produto", nome, f"{kg}kg")
            return True
    produtos.append({'nome': nome, 'kg': kg, 'valor_kg': valor_kg})
    registrar_historico('cadastro_produto', nome, f"{kg}kg")
    return True


def listar_produtos():
    return produtos


def buscar_produto_por_nome(nome):
    for p in produtos:
        if p['nome'].lower() == nome.lower():
            return p
    return None


def comprar_produto(nome, quantidade):
    p = buscar_produto_por_nome(nome)
    if not p:
        return None
    quantidade = validacao_geral(quantidade)
    if p['kg'] < quantidade:
        return None
    p['kg'] -= quantidade
    total = round(quantidade * p['valor_kg'], 2)
    registrar_historico('venda_produto', nome, f"{quantidade}kg")
    return {'nome': p['nome'], 'quantidade': quantidade,
            'total': total, 'valor_kg': p['valor_kg']}


# ---------------------------------------------------------------------------
# Exibicao de produtos
# ---------------------------------------------------------------------------

def exibir_produtos():
    print("-" * 40)
    for p in produtos:
        print(f"  {p['nome']} - {p['kg']:.1f} kg - R$ {p['valor_kg']:.2f}/kg")
    print("-" * 40)


def exibir_catalogo():
    """Mostra produtos derivados E animais para venda (menu cliente)."""
    print("-" * 50)
    for p in produtos:
        print(f"  [PRODUTO] {p['nome']} - {p['kg']:.1f} kg - R$ {p['valor_kg']:.2f}/kg")
    for a in animais_venda:
        print(f"  [ANIMAL]  tipo: {a['tipo']} - id: {a['identificacao']} - R$ {a['valor']:.2f}")
    print("-" * 50)


# ---------------------------------------------------------------------------
# Carrinho
# ---------------------------------------------------------------------------

def adicionar_ao_carrinho(descricao, quantidade, valor):
    carrinho.append({'descricao': descricao, 'quantidade': quantidade, 'valor': valor})


def ver_carrinho():
    """Retorna (itens, total). itens=None se vazio."""
    if not carrinho:
        return None, 0.0
    total = round(sum(item['valor'] for item in carrinho), 2)
    return carrinho, total


def limpar_carrinho():
    carrinho.clear()

def validacao_geral(valor):
    while True:
        try:
            valor = float(valor)
            if valor < 0:
                print('Erro: quantidade não pode ser negativa.')
                valor = input('Digite novamente: ')
            else:
                return valor
        except ValueError:
            print('Erro: digite apenas números.')
            valor = input('Digite novamente: ')




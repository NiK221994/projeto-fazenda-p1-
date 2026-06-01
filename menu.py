# main.py - Sistema Fazenda Sertao (Etapa 2)
#
# Pacotes externos:
#   pip install rich fpdf2 requests
#
#   rich    -> tabelas coloridas no terminal (relatorio do adm)
#   fpdf2   -> gera recibo em PDF ao agendar retirada
#   requests -> consulta clima em tempo real via API Open-Meteo

from rich.console import Console 
from rich.table import Table 

import auth
import fazenda
import agenda
import clima

console = Console()

carrinho = []  


while True:  # MENU PRINCIPAL
    print("[E]   Entrar")
    print("[NEW] Novo cadastro")
    print("[ADM] Administrador")
    print("[S]   Sair")

    opcao = input("Escolha: ").upper()

    if opcao == "S":
        print("Encerrando programa.")
        break


    elif opcao == "NEW":  # NOVO CADASTRO
        user = input("Novo usuario: ")
        senha1 = input("Senha: ")
        senha2 = input("Confirme a senha: ")

        if senha1 != senha2:
            print("As senhas nao coincidem.")
            continue

        tipo_conta = input("Tipo de conta: [U] Usuario  |  [A] Administrador: ").upper()

        if tipo_conta == "U":
            if auth.criar_usuario(user, senha1):
                print("Usuario criado com sucesso!")
            else:
                print("Usuario ja existe.")

        elif tipo_conta == "A":
            if auth.criar_admin(user, senha1):
                print("Administrador criado com sucesso!")
            else:
                print("Administrador já existe.")

        else:
            print("Opção inválida!") 
            print("Cadastro cancelado")


    elif opcao == "ADM":  # ADMINISTRADOR
        user = input("Usuario: ")
        senha = input("Senha: ")

        if not auth.login_admin(user, senha):
            print("Acesso Negado!")

        else:
            print("Acesso Aprovado!")

            while True:  # MENU ADM
                print("===== MENU ADM =====")
                print("[CA]      Cadastrar Animal")
                print("[LISTA]   Lista de Animais")
                print("[LISTA_U] Lista de Usuarios")
                print("[LISTA_A] Lista de Administradores")
                print("[AT]      Atualizar Animal")
                print("[R]       Remover Animal")
                print("[MP]      Menu de Producao")
                print("[REL]     Relatorio Geral")
                print("[HIST]    Historico de Movimentacao")
                print("[V]       Voltar")

                opcao_2 = input("Escolha: ").upper()

                if opcao_2 == "V":
                    break


                elif opcao_2 == "LISTA_U":  # LISTA USUARIOS
                    print("-" * 40)
                    for u in auth.usuarios:
                        print("usuario:", u['usuario'], "-", "senha:", u['senha'])
                    print("-" * 40)


                elif opcao_2 == "LISTA_A":  # LISTA ADMINS
                    print("-" * 40)
                    for a in auth.admins:
                        print("admin:", a['usuario'], "-", "senha:", a['senha'])
                    print("-" * 40)


                elif opcao_2 == "CA":  # CADASTRAR ANIMAL
                    status = input("Status: (em lactacao [LAC], para engorda [GORDA], para venda [VENDA]): ").upper()
                    tipo = input("Tipo do animal (Bovino de Leite, Caprino, Ovino, Suino/Leitao): ")
                    identificacao = input("Identificacao (brinco[A-Z] / numero[0-9]): ")

                    peso = arroba = 0.0
                    if status == "VENDA":
                        peso = float(input("Peso do animal (kg): "))
                        arroba = float(input("Valor da arroba (R$): "))

                    fazenda.cadastrar_animal(tipo, identificacao, status, peso, arroba)
                    print("Animal cadastrado!")


                elif opcao_2 == "LISTA":  # LISTA ANIMAIS
                    print("=" * 50)
                    print("--- Em producao / engorda ---")
                    for a in fazenda.animais:
                        print(a['tipo'], "-", a['identificacao'], "-", a['status'])

                    print("--- Para venda ---")
                    for a in fazenda.animais_venda:
                        print(a['tipo'], "-", a['identificacao'], "-", a['status'], "- R$", a['valor'])
                    print("=" * 50)


                elif opcao_2 == "AT":  # ATUALIZAR ANIMAL
                    ident = input("Identificacao do animal: ")
                    tipo = input("Novo tipo: ")
                    nova_id = input("Nova identificacao: ")
                    status = input("Novo status [LAC / GORDA / VENDA]: ").upper()
                    peso = float(input("Novo peso (kg): "))
                    arroba = float(input("Novo valor da arroba (R$): "))

                    if fazenda.atualizar_animal(ident, tipo, nova_id, status, peso, arroba):
                        print("Atualizado com sucesso!")
                    else:
                        print("Animal nao encontrado.")


                elif opcao_2 == "R":  # REMOVER ANIMAL
                    ident = input("Identificacao do animal: ")
                    if fazenda.remover_animal(ident):
                        print("Removido com sucesso!")
                    else:
                        print("Animal nao encontrado.")


                elif opcao_2 == "MP":  # MENU DE PRODUCAO

                    while True:
                        print("===== MENU DE PRODUCAO =====")
                        print("[1] Cadastrar producao de leite")
                        print("[2] Estoque de leite")
                        print("[3] Cadastrar produto")
                        print("[4] Estoque de produtos")
                        print("[0] Voltar")

                        opcao_3 = input("Escolha: ")

                        if opcao_3 == "0":
                            break

                        elif opcao_3 == "1":  # PRODUCAO LEITE
                            litros = float(input("Litros de leite: "))
                            fazenda.adicionar_leite(litros)
                            print(f"Adicionado! Total no estoque: {fazenda.leite:.1f}L")

                        elif opcao_3 == "2":  # ESTOQUE LEITE
                            print("-" * 40)
                            print(f"{fazenda.leite:.2f} litros de leite")
                            print("-" * 40)

                        elif opcao_3 == "3":  # CADASTRAR PRODUTO
                            nome = input("Nome do produto: ")
                            kg = float(input("Quantidade (kg): "))
                            valor = float(input("Valor por kg (R$): "))
                            leite_por_kg = float(input("Litros de leite necessarios por kg: "))

                            if fazenda.cadastrar_produto(nome, kg, valor, leite_por_kg):
                                print("Produto cadastrado!")
                            else:
                                print("Estoque de leite insuficiente!")

                        elif opcao_3 == "4":  # ESTOQUE PRODUTOS
                            print("-" * 40)
                            for p in fazenda.produtos:
                                print(p['nome'], "-", p['kg'], "kg -", "R$", p['valor_kg'], "/kg")
                            print("-" * 40)

                        else:
                            print("Opcao invalida.")


                elif opcao_2 == "REL":  # RELATORIO GERAL (rich - tabelas coloridas)
                    print("\n===== RELATORIO GERAL DA FAZENDA SERTAO =====")

                    # contagem por tipo
                    contagem = {}
                    for a in fazenda.animais + fazenda.animais_venda:
                        contagem[a['tipo']] = contagem.get(a['tipo'], 0) + 1

                    t1 = Table(title="Animais por Tipo")
                    t1.add_column("Tipo", style="cyan")
                    t1.add_column("Quantidade", justify="right")
                    for tipo, qtd in contagem.items():
                        t1.add_row(tipo, str(qtd))
                    console.print(t1)

                    t2 = Table(title="Estoque")
                    t2.add_column("Item", style="green")
                    t2.add_column("Valor", justify="right")
                    t2.add_row("Leite disponivel", f"{fazenda.leite:.2f} L")
                    t2.add_row("Animais em producao", str(len(fazenda.animais)))
                    t2.add_row("Animais para venda", str(len(fazenda.animais_venda)))
                    console.print(t2)

                    if fazenda.produtos:
                        t3 = Table(title="Produtos Derivados")
                        t3.add_column("Produto", style="yellow")
                        t3.add_column("Estoque (kg)", justify="right")
                        t3.add_column("R$/kg", justify="right")
                        for p in fazenda.produtos:
                            t3.add_row(p['nome'], f"{p['kg']:.2f}", f"R$ {p['valor_kg']:.2f}")
                        console.print(t3)


                elif opcao_2 == "HIST":  # HISTORICO
                    if not fazenda.historico:
                        print("Nenhuma movimentacao registrada.")
                        continue

                    t = Table(title="Historico de Movimentacoes")
                    t.add_column("Data/Hora")
                    t.add_column("Acao")
                    t.add_column("Item")
                    t.add_column("Qtd")
                    for h in fazenda.historico:
                        t.add_row(h['data'], h['acao'], h['item'], str(h['qtd']))
                    console.print(t)


                else:
                    print("Opcao invalida.")


    elif opcao == "E":  # CLIENTE
        user = input("Usuario: ")
        senha = input("Senha: ")

        if not auth.login_usuario(user, senha):
            print("Login invalido.")

        else:
            print(f"Bem-vindo, {user}!")
            carrinho = []

            while True:  # MENU CLIENTE
                print("--- MENU CLIENTE ---")
                print("[1] Ver produtos e animais")
                print("[2] Comprar")
                print("[3] Ver carrinho")
                print("[4] Agendar retirada (gera recibo PDF)")
                print("[5] Lista de agendamentos")
                print("[6] Previsao do tempo")
                print("[0] Sair")

                opcao_4 = input("Escolha: ")

                if opcao_4 == "0":
                    print("VOLTE SEMPRE!!!!")
                    break


                elif opcao_4 == "1":  # VER PRODUTOS
                    print("-" * 50)
                    for p in fazenda.produtos:
                        print(p['nome'], "-", p['kg'], "kg -", "R$", p['valor_kg'], "/kg")
                    for a in fazenda.animais_venda:
                        print("tipo:", a['tipo'], "- id:", a['identificacao'], "- R$", a['valor'])
                    print("-" * 50)


                elif opcao_4 == "2":  # COMPRAR
                    print("[P] Produto derivado  |  [A] Animal")
                    categoria = input("O que deseja comprar? ").upper()

                    if categoria == "P":
                        print("-" * 40)
                        for p in fazenda.produtos:
                            print(p['nome'], "-", p['kg'], "kg -", "R$", p['valor_kg'], "/kg")
                        print("-" * 40)
                        nome = input("Nome do produto: ").lower()
                        quantidade = float(input("Quantos kg: "))

                        resultado = fazenda.comprar_produto(nome, quantidade)
                        if resultado:
                            carrinho.append({
                                'descricao': resultado['nome'],
                                'quantidade': f"{resultado['quantidade']} kg",
                                'valor': resultado['total']
                            })
                            print("Adicionado ao carrinho!")
                            print("=" * 40)
                            print("Produto:", resultado['nome'])
                            print("Quantidade:", resultado['quantidade'], "kg")
                            print("Total: R$", resultado['total'])
                            print("=" * 40)
                        else:
                            print("Produto nao encontrado ou estoque insuficiente.")

                    elif categoria == "A":
                        print("-" * 40)
                        for a in fazenda.animais_venda:
                            print("tipo:", a['tipo'], "- id:", a['identificacao'], "- R$", a['valor'])
                        print("-" * 40)
                        ident = input("Identificacao do animal: ").lower()

                        animal = fazenda.comprar_animal(ident)
                        if animal:
                            carrinho.append({
                                'descricao': f"{animal['tipo']} (ID: {animal['identificacao']})",
                                'quantidade': "1 animal",
                                'valor': animal['valor']
                            })
                            print("Adicionado ao carrinho!")
                            print("=" * 40)
                            print("Animal:", animal['tipo'])
                            print("Total: R$", animal['valor'])
                            print("=" * 40)
                        else:
                            print("Animal nao encontrado.")

                    else:
                        print("Opcao invalida.")


                elif opcao_4 == "3":  # VER CARRINHO
                    if not carrinho:
                        print("Carrinho vazio.")
                        continue
                    print("-" * 50)
                    total_carrinho = 0.0
                    for item in carrinho:
                        print(item['descricao'], "-", item['quantidade'], "- R$", item['valor'])
                        total_carrinho += item['valor']
                    print("TOTAL: R$", round(total_carrinho, 2))
                    print("-" * 50)


                elif opcao_4 == "4":  # AGENDAR RETIRADA + PDF
                    if not carrinho:
                        print("Carrinho vazio. Adicione itens antes de agendar.")
                        continue

                    dia = int(input("Dia da retirada: "))
                    mes = int(input("Mes da retirada (1-12): "))
                    ano = int(input("Ano da retirada: "))
                    nome_cliente = input("Nome para contato: ")

                    erro_data = agenda.validar_data(dia, mes, ano)
                    if erro_data:
                        print(erro_data)
                        continue

                    ag = agenda.agendar(dia, mes, ano, nome_cliente, list(carrinho))
                    print("Agendamento realizado com sucesso!")

                    # Gera o recibo em PDF (fpdf2)
                    caminho = agenda.gerar_recibo_pdf(ag)
                    print(f"Recibo gerado: {caminho}")

                    carrinho = []


                elif opcao_4 == "5":  # LISTA DE AGENDAMENTOS
                    print("-" * 50)
                    for ag in agenda.agendamentos:
                        print(ag['dia'], "/", ag['mes'], "/", ag['ano'], "-", ag['cliente'], "- R$", ag['total'])
                    print("-" * 50)


                elif opcao_4 == "6":  # PREVISAO DO TEMPO (requests + Open-Meteo)
                    print("Consultando clima para a regiao Sertao...")
                    dados = clima.consultar_clima()

                    if not dados:
                        print("Nao foi possivel obter o clima. Verifique a conexao.")
                        continue

                    descricao = clima.descrever_tempo(dados['codigo'])
                    print("-" * 50)
                    print("Clima - Sousa / PB")
                    print("Temperatura atual:", dados['temperatura'], "°C")
                    print("Condicao:", descricao)
                    print("Precipitacao atual:", dados['precipitacao'], "mm")
                    print()
                    print("Previsao proximos 3 dias:")
                    for d in dados['previsao']:
                        print(d['data'], "- Chuva:", d['chuva_mm'], "mm",
                              "- Max:", d['temp_max'], "°C",
                              "- Min:", d['temp_min'], "°C")
                    print("-" * 50)


                else:
                    print("Opcao invalida.")


    else:
        print("Opcao invalida.")

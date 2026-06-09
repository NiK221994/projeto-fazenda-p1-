# main.py - Sistema Fazenda Sertao (Etapa 2)
#
# Pacotes externos:
#   pip install rich fpdf2 requests

#   fpdf2   -> gera recibo em PDF ao agendar retirada
#   requests -> consulta clima em tempo real via API Open-Meteo



import auth
import fazenda
import agenda
import clima



caminho = 'C:/Users/igor/Documents/relatorio-bater-ponto/relatorios.txt'

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
                print("Administrador ja existe.")

        else:
            print("Opcao invalida!")
            print("Cadastro cancelado.")


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
                        print("usuario:", u['usuario'], "- senha:", u['senha'])
                    print("-" * 40)


                elif opcao_2 == "LISTA_A":  # LISTA ADMINS
                    print("-" * 40)
                    for a in auth.admins:
                        print("admin:", a['usuario'], "- senha:", a['senha'])
                    print("-" * 40)


                elif opcao_2 == "CA":  # CADASTRAR ANIMAL
                    status = input("Status: (em lactacao [LAC], para engorda [GORDA], para venda [VENDA]): ").upper()
                    tipo = input("Tipo do animal (Bovino de Leite, Caprino, Ovino, Suino/Leitao): ")
                    identificacao = input("Identificacao (brinco[A-Z] / numero[0-9]): ")
                    

                    peso = arroba = 0.0
                    if status == "VENDA":
                        peso = input("Peso do animal (kg): ")
                        arroba = input("Valor da arroba (R$): ")

                    if fazenda.cadastrar_animal(tipo, identificacao, status, peso, arroba):
                        print("Animal cadastrado!")


                elif opcao_2 == "LISTA":  # LISTA ANIMAIS
                    fazenda.exibir_animais()


                elif opcao_2 == "AT":
                    ident = input("Identificacao do animal: ").upper()

                    animal,lista = fazenda.buscar_animal_por_id(ident) 

                    if not animal:
                        print("Animal nao encontrado.")
                    else:
                        tipo = input("Novo tipo: ")
                        nova_id = input("Nova identificacao: ")
                        status = input("Novo status [LAC / GORDA / VENDA]: ").upper()
                        peso = input("Novo peso (kg): ")
                        arroba = input("Novo valor da arroba (R$): ")

                        if fazenda.atualizar_animal(ident, tipo, nova_id, status, peso, arroba):
                            print("Atualizado com sucesso!")

                    


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
                            valor = input("digite um valor: ")
                            fazenda.adicionar_leite(valor)
                            print(f"Adicionado! Total no estoque: {fazenda.estoque_leite():.1f}L")

                        elif opcao_3 == "2":  # ESTOQUE LEITE
                            print("-" * 40)
                            print(f"{fazenda.estoque_leite():.2f} litros de leite")
                            print("-" * 40)

                        elif opcao_3 == "3":  # CADASTRAR PRODUTO
                            nome = input("Nome do produto: ")
                            kg = input("Quantidade (kg): ")
                            valor = input("Valor por kg (R$): ")
                            leite_por_kg = input("Litros de leite necessarios por kg: ")

                            if fazenda.cadastrar_produto(nome, kg, valor, leite_por_kg):
                                print("Produto cadastrado!")
                            else:
                                print("Estoque de leite insuficiente!")

                        elif opcao_3 == "4":  # ESTOQUE PRODUTOS
                            fazenda.exibir_produtos()

                        else:
                            print("Opcao invalida.")


                elif opcao_2 == "REL":  # RELATORIO GERAL (rich)
                    print("\n===== RELATORIO GERAL DA FAZENDA SERTAO =====")

                    animais, animais_venda = fazenda.listar_animais()

                    contagem = {}
                    for a in animais + animais_venda:
                        contagem[a['tipo']] = contagem.get(a['tipo'], 0) + 1

                    print("\n---Animais por Tipo---")
                    for tipo,qtd in contagem.items():
                        print(f'{tipo}: {qtd}')

                    print('\n---Estoque---')
                    print(f'Leite disponível: {fazenda.leite:.2f}L')
                    print(f'Animais em produção: {len(fazenda.animais)}')
                    print(f'Animais para venda: {len(fazenda.animais_venda)}')

                    produtos = fazenda.listar_produtos()
                    if produtos:
                        print('\n---Produtos Derivados---')
                        for p in produtos:
                            print(
                                f'Produto: {p['nome']}'
                                f'Estoque: {p['kg']:.2f}Kg'
                                f'Preço: R$ {p['valor_kg']:.2f}/Kg'
                            )
                        


                elif opcao_2 == "HIST":  # HISTORICO
                    if not fazenda.historico:
                        print("Nenhuma movimentacao registrada.")
                        continue

                    print('\nHistorico de Movimentacoes')

                    for h in fazenda.historico:
                        print(
                            f"Data: {h['data']} | "
                            f"Ação: {h['acao']} | "
                            f"Item: {h['item']} | "
                            f"Qtd: {h['qtd']}"                  )
                   

                else:
                    print("Opcao invalida.")


    elif opcao == "E":  # CLIENTE
        user = input("Usuario: ")
        senha = input("Senha: ")

        if not auth.login_usuario(user, senha):
            print("Login invalido.")

        else:
            print(f"Bem-vindo, {user}!")
            fazenda.limpar_carrinho()

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


                elif opcao_4 == "1":  # VER PRODUTOS E ANIMAIS
                    fazenda.exibir_catalogo()


                elif opcao_4 == "2":  # COMPRAR
                    print("[P] Produto derivado  |  [A] Animal")
                    categoria = input("O que deseja comprar? ").upper()

                    if categoria == "P":
                        fazenda.exibir_produtos()
                        nome = input("Nome do produto: ").lower()
                        quantidade = input("Quantos kg: ")

                        resultado = fazenda.comprar_produto(nome, quantidade)
                        if resultado:
                            fazenda.adicionar_ao_carrinho(
                                resultado['nome'],
                                f"{resultado['quantidade']} kg",
                                resultado['total']
                            )
                            print("Adicionado ao carrinho!")
                            print("=" * 40)
                            print("Produto:", resultado['nome'])
                            print("Quantidade:", resultado['quantidade'], "kg")
                            print("Total: R$", resultado['total'])
                            print("=" * 40)
                        else:
                            print("Produto nao encontrado ou estoque insuficiente.")

                    elif categoria == "A":
                        fazenda.exibir_animais_venda()
                        ident = input("Identificacao do animal: ").lower()

                        animal = fazenda.comprar_animal(ident)
                        if animal:
                            fazenda.adicionar_ao_carrinho(
                                f"{animal['tipo']} (ID: {animal['identificacao']})",
                                "1 animal",
                                animal['valor']
                            )
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
                    itens, total = fazenda.ver_carrinho()
                    if not itens:
                        print("Carrinho vazio.")
                        continue
                    print("-" * 50)
                    for item in itens:
                        print(item['descricao'], "-", item['quantidade'], "- R$", item['valor'])
                    print("TOTAL: R$", total)
                    print("-" * 50)


                elif opcao_4 == "4":  # AGENDAR RETIRADA + PDF
                    itens, _ = fazenda.ver_carrinho()
                    if not itens:
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

                    ag = agenda.agendar(dia, mes, ano, nome_cliente, list(itens))
                    print("Agendamento realizado com sucesso!")

                    caminho = agenda.gerar_recibo_pdf(ag)
                    print(f"Recibo gerado: {caminho}")

                    fazenda.limpar_carrinho()


                elif opcao_4 == "5":  # LISTA DE AGENDAMENTOS
                    print("-" * 50)
                    for ag in agenda.agendamentos:
                        print(ag['dia'], "/", ag['mes'], "/", ag['ano'],
                              "-", ag['cliente'], "- R$", ag['total'])
                    print("-" * 50)


                elif opcao_4 == "6":  # PREVISAO DO TEMPO
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



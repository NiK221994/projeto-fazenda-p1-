# agenda.py - Agendamento de retirada e recibo PDF

from fpdf import FPDF
from datetime import datetime

agendamentos = []  

DIAS_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def validar_data(dia, mes, ano):
    if mes < 1 or mes > 12:
        return "Mes invalido."
    if ano < datetime.now().year:
        return "Ano invalido."
    if dia < 1 or dia > DIAS_MES[mes - 1]:
        return "Dia invalido para esse mes."
    return None


def agendar(dia, mes, ano, cliente, itens):
    total = sum(i['valor'] for i in itens)
    agendamento = {
        'id': len(agendamentos) + 1,
        'dia': dia,
        'mes': mes,
        'ano': ano,
        'cliente': cliente,
        'itens': itens,
        'total': total,
        'criado_em': datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    agendamentos.append(agendamento)
    return agendamento



def gerar_recibo_pdf(ag):
    pdf = FPDF() #cria documento
    pdf.add_page() #cria pagina

    pdf.set_font("Helvetica", "B", 16) #cabeçalho = fonte:Helvetica,Tamanho 16
    

    pdf.set_fill_color(34, 100, 34) #Cor de fundo | Verde escuro
    pdf.set_text_color(255, 255, 255) #cor do texto | branco 
    pdf.cell(0, 12, "  FAZENDA SERTAO - Ticket de Carga", ln=True, fill=True)#titulo | cria um faixa verde com o titulo

    pdf.set_text_color(0, 0, 0) #cor do texto
    pdf.set_font("Helvetica", "", 10)#cabeçalho
    pdf.cell(0, 6, f"  Emitido em: {ag['criado_em']}", ln=True)# data de emissao
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Dados do Cliente", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"  Cliente: {ag['cliente']}", ln=True)
    pdf.cell(0, 7, f"  Data de Retirada: {ag['dia']:02d}/{ag['mes']:02d}/{ag['ano']}", ln=True)
    pdf.ln(4) #quebra linha(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Itens do Pedido", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(90, 7, "Descricao", border=1)
    pdf.cell(40, 7, "Quantidade", border=1)
    pdf.cell(50, 7, "Valor (R$)", border=1, ln=True)

    pdf.set_font("Helvetica", "", 10)
    for item in ag['itens']:
        pdf.cell(90, 7, str(item['descricao']), border=1)
        pdf.cell(40, 7, str(item['quantidade']), border=1)
        pdf.cell(50, 7, f"R$ {item['valor']:.2f}", border=1, ln=True)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(130, 8, "")
    pdf.cell(50, 8, f"TOTAL: R$ {ag['total']:.2f}", border=1, ln=True)

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Obrigado pela preferencia! Fazenda Sertao.", ln=True, align="C")

    caminho = f"recibo_{ag['id']}.pdf"
    pdf.output(caminho)
    return caminho



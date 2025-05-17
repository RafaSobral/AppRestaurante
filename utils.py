import tkinter as tk
from tkinter import font
from tkinter import messagebox
import serial
from datetime import datetime


hoje = datetime.now().strftime("%d-%m-%Y")

def imprimir_pedido_daruma(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para imprimir.")
        return

    valores = tree.item(selected[0], "values")
    if len(valores) < 14:
        messagebox.showerror("Erro", "Dados do pedido incompletos.")
        return

    pedido = {
        "pedido_id": valores[1],
        "nome_cliente": valores[2],
        "prato": valores[3],
        "acomp1": valores[4],
        "acomp2": valores[5],
        "observacao": valores[6],
        "tamanho": valores[7],
        "bebida": valores[8],
        "pagamento": valores[9],
        "troco": valores[10],
        "taxa": valores[11],
        "total": valores[12],
        "data_hoje": valores[13]
    }

    try:
        porta = serial.Serial('COM3', baudrate=9600, timeout=1)
        texto = f"""
*** Bom Apetite ***
------------------------
Pedido ID: {pedido['pedido_id']}
Nome Cliente: {pedido['nome_cliente']}
Prato: {pedido['prato']}
Acomp1: {pedido['acomp1']}
Acomp2: {pedido['acomp2']}
Obs: {pedido['observacao']}
Tamanho: {pedido['tamanho']}
Bebida: {pedido['bebida']}
Pagamento: {pedido['pagamento']}
Troco: R$ {pedido['troco']}
Taxa: R$ {pedido['taxa']}
Total: R$ {pedido['total']}
Data: {pedido['data_hoje']}
------------------------
"""
        porta.write(texto.encode('utf-8'))
        porta.write(b'\n\n\n')
        porta.close()
        messagebox.showinfo("Sucesso", "Pedido enviado para a impressora.")
    except Exception as e:
        messagebox.showerror("Erro na impressão", f"Erro: {e}")


def editar_pedido(tree, cursor, conn, date_entry, total_vendas_var, total_taxa_var, total_troco_var):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para editar")
        return

    valores = tree.item(selected[0], "values")
    id_real = valores[0]

    _, _, _, prato_antigo, acomp1_antigo, acomp2_antigo, observacao_antiga, tamanho_antigo, bebida_antiga, pagamento_antigo, troco_antigo, taxa_antiga, total_antigo, _ = valores

    janela_editar = tk.Toplevel()
    janela_editar.title('Editar Pedido')
    janela_editar.focus_force()

    campos = {
        "Prato": prato_antigo,
        "Acomp1": acomp1_antigo,
        "Acomp2": acomp2_antigo,
        "Observacao": observacao_antiga,
        "Tamanho": tamanho_antigo,
        "Bebida": bebida_antiga,
        "Pagamento": pagamento_antigo,
        "Troco": troco_antigo,
        "Taxa": taxa_antiga,
        "Total": total_antigo
    }

    entradas = {}

    for label, valor in campos.items():
        tk.Label(janela_editar, text=label).pack()
        entrada = tk.Entry(janela_editar)
        entrada.insert(0, valor)
        entrada.pack()
        entradas[label] = entrada

    def salvar_edicao():
        novos_valores = [entradas[campo].get() for campo in campos]

        cursor.execute("""
            UPDATE pedidos SET prato=?, acompanhamento1=?, acompanhamento2=?, observacao=?,
            tamanho=?,bebida=?, pagamento=?, troco=?, taxa=?, total=? WHERE id=?
        """, (*novos_valores, id_real))
        conn.commit()
        messagebox.showinfo("Sucesso", "Pedido atualizado com sucesso")
        janela_editar.destroy()
        dia, mes, ano = obter_data(date_entry)
        carregar_pedidos(tree, cursor, dia, mes, ano, total_vendas_var, total_taxa_var, total_troco_var)


    botao_salvar = tk.Button(janela_editar, text="Salvar [Enter]", command=salvar_edicao)
    botao_salvar.pack(pady=10)
    janela_editar.bind("<Return>", lambda event=None: botao_salvar.invoke())


def deletar_pedido(tree,cursor,conn):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para deletar")
        return

    id_real = tree.item(selected[0], "values")[0]

    confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse Pedido?")
    if confirm:
        cursor.execute("DELETE FROM pedidos WHERE id=?", (id_real,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Pedido deletado com sucesso")
        


def carregar_pedidos(tree, cursor, dia, mes, ano,
                     total_vendas_var, total_taxa_var, total_troco_var):

    for i in tree.get_children():
        tree.delete(i)

    data_selecionada = f"{dia}-{mes}-{ano}"

    if dia in ['00', '0'] and mes in ['00', '0'] and ano in ['00', '0']:
        cursor.execute("""SELECT * FROM pedidos""")
    elif dia in ['00', '0'] and mes in ['00', '0']:
        cursor.execute("""SELECT * FROM pedidos WHERE data_hoje LIKE ?""", (f"%{ano}%",))
    elif dia in ['00', '0']:
        cursor.execute("""SELECT * FROM pedidos WHERE data_hoje LIKE ?""", (f"%-{mes}-{ano}",))
    else:
        cursor.execute("""SELECT * FROM pedidos WHERE data_hoje LIKE ?""", (data_selecionada,))

    total_vendas = 0.0
    total_taxa = 0.0
    total_troco = 0.0

    tamanho_map = {13: 'P', 15: 'M', 18: 'G'}

    for row in cursor.fetchall():
        row = list(row)

        # Somatórios
        try:
            total_vendas += float(row[12])
            total_taxa += float(row[11])
            total_troco += float(row[10])
        except (ValueError, TypeError):
            pass

        # Converte tamanho numérico para letra
        try:
            row[7] = tamanho_map.get(int(row[7]), row[7])
        except (ValueError, TypeError):
            pass

        tree.insert("", "end", values=row)

    # Atualiza as labels de totais
    total_vendas_var.set(f"Total Vendas: R$ {total_vendas:.2f}")
    total_taxa_var.set(f"Total Taxa: R$ {total_taxa:.2f}")
    total_troco_var.set(f"Total Troco: R$ {total_troco:.2f}")




def obter_data(date_entry):
    data_str = date_entry.get()
    dia, mes, ano = data_str.split('/')
    return  dia, mes, ano


def abrir_info():
    manual_janela = tk.Toplevel()
    manual_janela.title("Manual de Teclas Rápidas")
    manual_janela.geometry("420x520")
    manual_janela.focus_force()
    manual_janela.resizable(False, False)
    manual_janela.iconphoto(False, tk.PhotoImage(file='logo.png'))

    fonte_titulo = font.Font(family="Helvetica", size=10, weight="bold")
    fonte_mono = font.Font(family="Courier", size=10)

    frame_principal = tk.Frame(manual_janela)
    frame_principal.pack(fill="both", expand=True)

    frame_conteudo = tk.Frame(frame_principal)
    frame_conteudo.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_conteudo)
    scrollbar = tk.Scrollbar(frame_conteudo, orient="vertical", command=canvas.yview)
    frame_scroll = tk.Frame(canvas)

    frame_scroll.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def adicionar_secao(titulo, conteudo):
        label_titulo = tk.Label(frame_scroll, text=titulo, font=fonte_titulo, anchor="w", bg="green", fg="white", relief="sunken", borderwidth=3, padx=10, pady=5)
        label_titulo.pack(fill="x", padx=15, pady=(10, 0))

        label_conteudo = tk.Label(frame_scroll, text=conteudo, font=fonte_mono, justify="left", anchor="w")
        label_conteudo.pack(fill="x", padx=30, pady=(0, 5))

 
    adicionar_secao("[Atalhos de Gerenciamento]", """\
F1  → Gerir Clientes
F2  → Gerir Pratos
F3  → Gerir Acompanhamentos
F4  → Gerir Bebidas
ENTER    → Salvar
ESC      → Sair
DELETE   → Apagar
-(Menos) → Editar""")

    adicionar_secao("[Atalhos de Cadastro]", """\
ENTER    → Salvar
ESC      → Sair
F5  → Criar Bebidas
F6  → Criar Pedido
F7  → Criar Cliente
F8  → Criar Pratos
F9  → Criar Acompanhamentos""")

    adicionar_secao("[Ações Rápidas]", """\
Nos Sub-Menus utilize a tecla Enter para
salvar, tecla ESC para sair do menu 
                    
F12         → Editar Pedido Selecionado
F11         → Re-imprimir Pedido
F10         → Abrir Caixa
DELETE      → Apagar Pedido Selecionado
= (Igual)   → Abrir o menu de ajuda""")

    adicionar_secao("[Cadastro de Pedido]", """\
Número 1    → Selecionar Crédito
Número 2    → Selecionar Débito
Número 3    → Selecionar Dinheiro
Número 4    → Selecionar Pix
Número 5    → Selecionar Mumbuca
                    
Letra P     → Selecionar marmita Pequena
Letra M     → Selecionar marmita Média
Letra G     → Selecionar marmita Grande
                    
Navegue pela tela de cadastro de pedido
com a tecla TAB, ao selecionar uma lista
(clientes, pratos, acompanhamentos ou bebidas)
utilize a seta para baixo para abrir a lista, 
após aberta é possível navegar utilizando 
a seta para cima ou para baixo""")

    adicionar_secao("[Menu do Caixa]", """\
Enter       → Confirmar Data
ESC         → Sair do Menu
-(Menos)    → Imprimir fechamento""")

    adicionar_secao("[Outros Comandos]", """\
Enter       → Confirmar a Data no menu inicial
Tab         → Navegar entre campos
Shift + Tab → Navegar para trás""")


    frame_baixo = tk.Frame(frame_principal)
    frame_baixo.pack(side="bottom", fill="x", pady=10)

    botao_sair = tk.Button(
    frame_baixo,
    bg="#FF0000",
    fg="white",
    font=("Helvetica", 8, "normal"),
    activebackground="#45a049",
    activeforeground="white",
    padx=5,
    pady=2,
    text="Sair",
    command=manual_janela.destroy
    )
    botao_sair.pack()


    manual_janela.bind("<Escape>", lambda e: botao_sair.invoke())

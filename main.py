import tkinter as tk
from tkinter import ttk,messagebox
from classes import Cliente, Prato, Pedido, Acompanhamento, Caixa
import sqlite3
import serial


conn = sqlite3.connect("bomapetite.db")
cursor = conn.cursor()

janela = tk.Tk()
janela.title("Bom Apetite")
janela.geometry("1200x500")
janela.iconphoto(False, tk.PhotoImage(file='logo.png'))

app_Cliente = Cliente() 
app_Prato = Prato()
app_Pedido = Pedido()
app_Acompanhamentos = Acompanhamento()
app_Caixa = Caixa()


tree = ttk.Treeview(janela, columns=("N. Pedido:","Nome Cliente:","Prato:","Acompanhamento 1:","Acompanhamento 2:","Observacao:","Tamanho:","Pagamento:","Troco:","Taxa:","Total:","Data:"), show="headings")
tree.heading("N. Pedido:", text="N. Pedido:")
tree.column("N. Pedido:", width=38)

tree.heading("Nome Cliente:", text="Nome Cliente:")
tree.column("Nome Cliente:", width=60)

tree.heading("Prato:", text="Prato:")
tree.column("Prato:", width=100)

tree.heading("Acompanhamento 1:", text="Acompanhamento 1:")
tree.column("Acompanhamento 1:", width=130)

tree.heading("Acompanhamento 2:", text="Acompanhamento 2:")
tree.column("Acompanhamento 2:", width=130)

tree.heading("Observacao:", text="Observacao:")
tree.column("Observacao:", width=150)

tree.heading("Tamanho:", text="Tamanho:")
tree.column("Tamanho:", width=38)

tree.heading("Pagamento:", text="Pagamento:")
tree.column("Pagamento:", width=70)

tree.heading("Troco:", text="Troco:")
tree.column("Troco:", width=38)

tree.heading("Taxa:", text="Taxa:")
tree.column("Taxa:", width=38)

tree.heading("Total:", text="Total:")
tree.column("Total:", width=38)

tree.heading("Data:", text="Data:")
tree.column("Data:", width=60)

tree.pack(fill="both", expand=True, padx=10, pady=10)
cursor.execute("SELECT id, nome_cliente, prato, acompanhamento1, acompanhamento2, observacao, tamanho, pagamento, troco, taxa, total, data_hoje FROM pedidos")
for row in cursor.fetchall():
    tree.insert("", "end", values=row)

def carregar_pedidos():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT pedido_id, nome_cliente, prato, acompanhamento1, acompanhamento2, observacao, tamanho, pagamento, troco, taxa, total, data_hoje FROM pedidos")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def imprimir_pedido_daruma():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para imprimir.")
        return

    valores = tree.item(selected[0], "values")
    if len(valores) < 12:
        messagebox.showerror("Erro", "Dados do pedido incompletos.")
        return

    pedido = {
        "pedido_id": valores[0],
        "nome_cliente": valores[1],
        "prato": valores[2],
        "acomp1": valores[3],
        "acomp2": valores[4],
        "observacao": valores[5],
        "tamanho": valores[6],
        "pagamento": valores[7],
        "troco": valores[8],
        "taxa": valores[9],
        "total": valores[10],
        "data_hoje": valores[11]
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

def editar_pedido():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso","Selecione um pedido para editar")
        return

    id, _, prato_antigo, acomp1_antigo, acomp2_antigo, observacao_antiga, tamanho_antigo, pagamento_antigo, troco_antigo, taxa_antiga, total_antigo, _ = tree.item(selected[0], "values")

    janela_editar = tk.Toplevel()
    janela_editar.focus_force()
    janela_editar.title('Editar Pedido')

    tk.Label(janela_editar, text="Prato").pack()
    prato_entry = tk.Entry(janela_editar)
    prato_entry.insert(0, prato_antigo)
    prato_entry.pack()

    tk.Label(janela_editar, text="Acomp1").pack()
    acomp1_entry = tk.Entry(janela_editar)
    acomp1_entry.insert(0, acomp1_antigo)
    acomp1_entry.pack()

    tk.Label(janela_editar, text="Acomp2").pack()
    acomp2_entry = tk.Entry(janela_editar)
    acomp2_entry.insert(0, acomp2_antigo)
    acomp2_entry.pack()

    tk.Label(janela_editar, text="Observacao").pack()
    observacao_entry = tk.Entry(janela_editar)
    observacao_entry.insert(0,observacao_antiga)
    observacao_entry.pack()

    tk.Label(janela_editar, text="Tamanho").pack()
    tamanho_entry = tk.Entry(janela_editar)
    tamanho_entry.insert(0,tamanho_antigo)
    tamanho_entry.pack()

    tk.Label(janela_editar, text="Pagamento").pack()
    pagamento_entry = tk.Entry(janela_editar)
    pagamento_entry.insert(0,pagamento_antigo)
    pagamento_entry.pack()

    tk.Label(janela_editar, text="Troco").pack()
    troco_entry = tk.Entry(janela_editar)
    troco_entry.insert(0,troco_antigo)
    troco_entry.pack()

    tk.Label(janela_editar, text="Taxa").pack()
    taxa_entry = tk.Entry(janela_editar)
    taxa_entry.insert(0,taxa_antiga)
    taxa_entry.pack()

    tk.Label(janela_editar, text="Total").pack()
    total_entry = tk.Entry(janela_editar)
    total_entry.insert(0,total_antigo)
    total_entry.pack()

    def salvar_edicao():
        novo_prato = prato_entry.get()
        novo_acomp1 = acomp1_entry.get()
        novo_acomp2 = acomp2_entry.get()
        nova_observacao = observacao_entry.get()
        novo_tamanho = tamanho_entry.get()
        novo_pagamento = pagamento_entry.get()
        novo_troco = troco_entry.get()
        nova_taxa = taxa_entry.get()
        novo_total = total_entry.get()

        cursor.execute("UPDATE pedidos SET prato=?, acompanhamento1=?, acompanhamento2=?, observacao=?, tamanho=?, pagamento=?, troco=?, taxa=?, total=? WHERE id=?", (novo_prato, novo_acomp1, novo_acomp2, nova_observacao, novo_tamanho, novo_pagamento, novo_troco, nova_taxa, novo_total, id))
        conn.commit()
        messagebox.showinfo("Sucesso","Pedido atualizado com sucesso")
        janela_editar.destroy()

    botao_salvar = tk.Button(janela_editar, text="Salvar [Enter]", command=salvar_edicao)
    botao_salvar.pack(pady=10)
    def acionar_salvar(event=None):
        botao_salvar.invoke()
    janela_editar.bind("<Return>", acionar_salvar)

def deletar_pedido():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso","Selecione um pedido para deletar")
        return

    pedido_id = tree.item(selected[0],"values")[0]

    confirm = messagebox.askyesno("Confirmar","Tem certeza que deseja excluir esse Pedido?")
    if confirm:
        cursor.execute("DELETE FROM pedidos WHERE id=?", (pedido_id,))
        conn.commit()
        messagebox.showinfo("Sucesso","Pedido deletado com sucesso")        
        tree.delete(selected[0])
            
frame_botoes = tk.Frame(janela)
frame_botoes.pack(fill="x", padx=10, pady=10)


botao_gerenciarClientes = tk.Button(frame_botoes, text="Gerir Clientes [1]", command=app_Cliente.abrir_gerenciarClientes)
botao_gerenciarClientes.pack(side="left", padx=5)
janela.bind("1", lambda e: botao_gerenciarClientes.invoke())

botao_gerenciarPratos = tk.Button(frame_botoes, text="Gerir Pratos [2]", command=app_Prato.abrir_gerenciarPratos)
botao_gerenciarPratos.pack(side="left", padx=5)
janela.bind("2", lambda e: botao_gerenciarPratos.invoke())

botao_gerenciarAcompanhamentos = tk.Button(frame_botoes, text="Gerir Acomp [3]", command=app_Acompanhamentos.abrir_gerenciarAcompanhamentos)
botao_gerenciarAcompanhamentos.pack(side="left", padx=5)
janela.bind("3", lambda e: botao_gerenciarAcompanhamentos.invoke())

botao_cadastrarPedidos = tk.Button(frame_botoes, text="Criar Pedido [4]", command=app_Pedido.abrir_cadastrarPedido)
botao_cadastrarPedidos.pack(side="left", padx=5)
janela.bind("4", lambda e: botao_cadastrarPedidos.invoke())

botao_cadastrarCliente = tk.Button(frame_botoes, text="Criar Cliente [5]", command=app_Cliente.abrir_cadastrarCliente)
botao_cadastrarCliente.pack(side="left", padx=5)
janela.bind("5", lambda e: botao_cadastrarCliente.invoke())

botao_cadastrarPratos = tk.Button(frame_botoes, text="Criar Pratos [6]", command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.pack(side="left", padx=5)
janela.bind("6", lambda e: botao_cadastrarPratos.invoke())

botao_cadastrarAcompanhamentos = tk.Button(frame_botoes, text="Criar Acomp [7]", command=app_Acompanhamentos.abrir_cadastrarAcompanhamentos)
botao_cadastrarAcompanhamentos.pack(side="left", padx=5)
janela.bind("7", lambda e: botao_cadastrarAcompanhamentos.invoke())

botao_atualizar = tk.Button(frame_botoes, text="Atualizar [F5]", command=carregar_pedidos)
botao_atualizar.pack(side="right", pady=10)
def acionar_atualizar(event=None):
        botao_atualizar.invoke()
janela.bind("<F5>", acionar_atualizar)

botao_editar = tk.Button(frame_botoes, text="Editar [E]", command=editar_pedido)
botao_editar.pack(side="right", padx=5, pady=10)
def acionar_editar(event=None):
    botao_editar.invoke()
janela.bind("<Key-e>", acionar_editar)

botao_deletar = tk.Button(frame_botoes, text="Deletar [Del]", command=deletar_pedido)
botao_deletar.pack(side="right", padx=5, pady=10)
def acionar_deletar(event=None):
    botao_deletar.invoke()
janela.bind("<Delete>", acionar_deletar)

btn_imprimir = tk.Button(frame_botoes, text="Re-imprimir [i]", command=imprimir_pedido_daruma)
btn_imprimir.pack(side="right", padx=5, pady=10)
def acionar_imprimir(event=None):
    btn_imprimir.invoke()
janela.bind("<Key-i>", acionar_imprimir)

botao_fecharCaixa = tk.Button(frame_botoes, text="Fechar Caixa [8]", command=app_Caixa.abrir_fecharCaixa)
botao_fecharCaixa.pack(side="right", padx=5)
janela.bind("8", lambda e: botao_fecharCaixa.invoke())

janela.mainloop()

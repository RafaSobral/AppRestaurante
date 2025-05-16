import sqlite3
import tkinter as tk
from estilizacao import *
from tkinter import ttk
from tkcalendar import DateEntry
from classes.Prato import Prato
from classes.Caixa import Caixa
from classes.Pedido import Pedido
from classes.Bebidas import Bebidas
from classes.Cliente import Cliente
from classes.Acompanhamento import Acompanhamento
from utils import carregar_pedidos, deletar_pedido, editar_pedido, imprimir_pedido_daruma, obter_data 

conn = sqlite3.connect("bomapetite.db")
cursor = conn.cursor()

janela = tk.Tk()
janela.title("Bom Apetite")
janela.geometry("1360x500")
janela.iconphoto(False, tk.PhotoImage(file='logo.png'))

app_Cliente = Cliente() 
app_Prato = Prato()
app_Pedido = Pedido()
app_Acompanhamentos = Acompanhamento()
app_Caixa = Caixa()
app_Bebidas = Bebidas()


frame_data = tk.Frame(janela)
frame_data.pack(pady=10, padx=10, anchor="nw")

date_entry = DateEntry(frame_data, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_entry.pack(side='left', padx=(0, 10))  

botao_confirmar = tk.Button(frame_data, text="Confirmar Data [Enter]", **botao_verde, command=lambda: carregar_pedidos(tree, cursor, *obter_data(date_entry)))
botao_confirmar.pack(side='left')
def acionar_confirmar(_):
    botao_confirmar.invoke()
janela.bind("<Return>", acionar_confirmar)

tk.Label(frame_data, text="    Para ver os pedidos:   Do mes: 00/mes/ano,   Do ano: 00/00/ano,   Todos os pedidos: 00/00/00").pack()

tree = ttk.Treeview(
    janela,
    columns=("id", "N. Pedido:", "Nome Cliente:", "Prato:", "Acompanhamento 1:", "Acompanhamento 2:",
             "Observacao:", "Tamanho:", "Bebida:", "Pagamento:", "Troco:", "Taxa:", "Total:", "Data:"),
    show="headings"
)

tree.heading("id", text="id")
tree.column("id", width=0, stretch=False) 

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

tree.heading("Bebida:", text="Bebida:")
tree.column("Bebida:", width=100)

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

carregar_pedidos(tree, cursor, *obter_data(date_entry))
    
frame_botoes = tk.Frame(janela)
frame_botoes.pack(fill="x", padx=10, pady=10)

botao_gerenciarClientes = tk.Button(frame_botoes, text="Gerir Clientes [1]", **botao_azulclaro, command=app_Cliente.abrir_gerenciarClientes)
botao_gerenciarClientes.pack(side="left", padx=5)
janela.bind("1", lambda e: botao_gerenciarClientes.invoke())

botao_gerenciarPratos = tk.Button(frame_botoes, text="Gerir Pratos [2]", **botao_azulclaro, command=app_Prato.abrir_gerenciarPratos)
botao_gerenciarPratos.pack(side="left", padx=5)
janela.bind("2", lambda e: botao_gerenciarPratos.invoke())

botao_gerenciarAcompanhamentos = tk.Button(frame_botoes, text="Gerir Acomp [3]", **botao_azulclaro, command=app_Acompanhamentos.abrir_gerenciarAcompanhamentos)
botao_gerenciarAcompanhamentos.pack(side="left", padx=5)
janela.bind("3", lambda e: botao_gerenciarAcompanhamentos.invoke())

botao_gerenciarBebidas = tk.Button(frame_botoes, text="Gerir Bebidas [4]", **botao_azulclaro, command=app_Bebidas.abrir_gerenciarBebidas)
botao_gerenciarBebidas.pack(side="left", padx=5)
janela.bind("4", lambda e: botao_gerenciarBebidas.invoke())

botao_cadastrarBebidas = tk.Button(frame_botoes, text="Criar Bebidas [5]", **botao_azul, command=app_Bebidas.abrir_cadastrarBebidas)
botao_cadastrarBebidas.pack(side="left", padx=5)
janela.bind("5", lambda e: botao_cadastrarBebidas.invoke())

botao_cadastrarPedidos = tk.Button(frame_botoes, text="Criar Pedido [6]", **botao_azul, command=lambda: app_Pedido.abrir_cadastrarPedido(tree=tree))
botao_cadastrarPedidos.pack(side="left", padx=5)
janela.bind("6", lambda e: botao_cadastrarPedidos.invoke())

botao_cadastrarCliente = tk.Button(frame_botoes, text="Criar Cliente [7]", **botao_azul, command=app_Cliente.abrir_cadastrarCliente)
botao_cadastrarCliente.pack(side="left", padx=5)
janela.bind("7", lambda e: botao_cadastrarCliente.invoke())

botao_cadastrarPratos = tk.Button(frame_botoes, text="Criar Pratos [8]", **botao_azul, command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.pack(side="left", padx=5)
janela.bind("8", lambda e: botao_cadastrarPratos.invoke())

botao_cadastrarAcompanhamentos = tk.Button(frame_botoes, text="Criar Acomp [9]", **botao_azul, command=app_Acompanhamentos.abrir_cadastrarAcompanhamentos)
botao_cadastrarAcompanhamentos.pack(side="left", padx=5)
janela.bind("9", lambda e: botao_cadastrarAcompanhamentos.invoke())

botao_deletar = tk.Button(frame_botoes, text="Deletar [Del]", **botao_vermelho, command=lambda: deletar_pedido(tree, cursor, conn))
botao_deletar.pack(side="right", padx=5, pady=10)
def acionar_deletar(_):
    botao_deletar.invoke()
janela.bind("<Delete>", acionar_deletar)

botao_editar = tk.Button(frame_botoes, text="Editar [E]", **botao_laranja, command=lambda: editar_pedido(tree, cursor, conn, date_entry))
botao_editar.pack(side="right", padx=5, pady=10)
def acionar_editar(_):
    botao_editar.invoke()
janela.bind("<Key-e>", acionar_editar)

btn_imprimir = tk.Button(frame_botoes, text="Re-imprimir [i]", **botao_laranja, command=lambda: imprimir_pedido_daruma(tree))
btn_imprimir.pack(side="right", padx=5, pady=10)
def acionar_imprimir(_):
    btn_imprimir.invoke()
janela.bind("<Key-i>", acionar_imprimir)

botao_fecharCaixa = tk.Button(frame_botoes, text="Caixa [C]", **botao_laranja, command=app_Caixa.abrir_fecharCaixa)
botao_fecharCaixa.pack(side="right", padx=5)
janela.bind("<Key-c>", lambda e: botao_fecharCaixa.invoke())

janela.mainloop()

import sqlite3
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from classes.Prato import Prato
from classes.Caixa import Caixa
from classes.Pedido import Pedido
from classes.Bebidas import Bebidas
from classes.Cliente import Cliente
from classes.Acompanhamento import Acompanhamento
from estilizacao import botao_verde, botao_vermelho, botao_azul, botao_azulclaro, botao_laranja, botao_amarelo
from utils import carregar_pedidos, deletar_pedido, editar_pedido, imprimir_pedido_daruma, obter_data, abrir_info


conn = sqlite3.connect("bomapetite.db")
cursor = conn.cursor()

janela = tk.Tk()
janela.title("Bom Apetite - Clique no botão de ajuda para visualizar as teclas de atalho")
janela.geometry("1360x500")
janela.iconphoto(False, tk.PhotoImage(file='logo.png'))

app_Cliente = Cliente() 
app_Prato = Prato()
app_Pedido = Pedido()
app_Acompanhamentos = Acompanhamento()
app_Caixa = Caixa()
app_Bebidas = Bebidas()

total_vendas_var = tk.StringVar(value="Total Vendas: R$ 0,00")
total_taxa_var = tk.StringVar(value="Total Taxa: R$ 0,00")
total_troco_var = tk.StringVar(value="Total Troco: R$ 0,00")

frame_data = tk.Frame(janela)
frame_data.pack(fill="x", pady=10, padx=10)

frame_esquerda = tk.Frame(frame_data)
frame_esquerda.pack(side="left")

date_entry = DateEntry(frame_esquerda, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_entry.pack(side="left", padx=(0, 10))

botao_confirmar = tk.Button(
    frame_esquerda,
    text="Confirmar Data",
    **botao_verde,
    command=lambda: carregar_pedidos(
        tree, cursor, *obter_data(date_entry),
        total_vendas_var, total_taxa_var, total_troco_var
    )
)

botao_confirmar.pack(side="left")

def acionar_confirmar(event):
    botao_confirmar.invoke()
janela.bind("<FocusIn>", acionar_confirmar)
janela.bind("<Return>", acionar_confirmar)


label_instrucao = tk.Label(frame_esquerda, text="Para ver os pedidos:   Do mês: 00/mês/ano,   Do ano: 00/00/ano,   Todos os pedidos: 00/00/00")
label_instrucao.pack(side="left", padx=(10, 0))

frame_direita = tk.Frame(frame_data)
frame_direita.pack(side="right")

botao_info = tk.Button(frame_direita, **botao_amarelo, text="Ajuda", command=abrir_info)
botao_info.pack(side="left", padx=5)
janela.bind("<equal>", lambda e: botao_info.invoke())

label_total_troco = tk.Label(frame_direita, textvariable=total_troco_var, anchor="e", bg="green", fg="white", relief="sunken", borderwidth=3, padx=10, pady=5)
label_total_troco.pack(side="left", padx=5)

label_total_taxa = tk.Label(frame_direita, textvariable=total_taxa_var, anchor="e", bg="green", fg="white", relief="sunken", borderwidth=3, padx=10, pady=5)
label_total_taxa.pack(side="left", padx=5)

label_total_vendas = tk.Label(frame_direita, textvariable=total_vendas_var, anchor="e", bg="green", fg="white", relief="sunken", borderwidth=3, padx=10, pady=5)
label_total_vendas.pack(side="left", padx=5)




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

carregar_pedidos(tree, cursor, *obter_data(date_entry), total_vendas_var, total_taxa_var, total_troco_var)
    
frame_botoes = tk.Frame(janela)
frame_botoes.pack(fill="x", padx=10, pady=10)

botao_gerenciarClientes = tk.Button(frame_botoes, text="Gerir Clientes", **botao_azul, command=app_Cliente.abrir_gerenciarClientes)
botao_gerenciarClientes.pack(side="left", padx=5)
janela.bind("<F1>", lambda e: botao_gerenciarClientes.invoke())

botao_gerenciarPratos = tk.Button(frame_botoes, text="Gerir Pratos", **botao_azul, command=app_Prato.abrir_gerenciarPratos)
botao_gerenciarPratos.pack(side="left", padx=5)
janela.bind("<F2>", lambda e: botao_gerenciarPratos.invoke())

botao_gerenciarAcompanhamentos = tk.Button(frame_botoes, text="Gerir Acomp", **botao_azul, command=app_Acompanhamentos.abrir_gerenciarAcompanhamentos)
botao_gerenciarAcompanhamentos.pack(side="left", padx=5)
janela.bind("<F3>", lambda e: botao_gerenciarAcompanhamentos.invoke())

botao_gerenciarBebidas = tk.Button(frame_botoes, text="Gerir Bebidas", **botao_azul, command=app_Bebidas.abrir_gerenciarBebidas)
botao_gerenciarBebidas.pack(side="left", padx=5)
janela.bind("<F4>", lambda e: botao_gerenciarBebidas.invoke())

botao_cadastrarBebidas = tk.Button(frame_botoes, text="Criar Bebidas", **botao_azulclaro, command=app_Bebidas.abrir_cadastrarBebidas)
botao_cadastrarBebidas.pack(side="left", padx=5)
janela.bind("<F5>", lambda e: botao_cadastrarBebidas.invoke())

botao_cadastrarPedidos = tk.Button(frame_botoes, text="Criar Pedido", **botao_azulclaro, command=lambda: app_Pedido.abrir_cadastrarPedido(tree=tree))
botao_cadastrarPedidos.pack(side="left", padx=5)
janela.bind("<F6>", lambda e: botao_cadastrarPedidos.invoke())

botao_cadastrarCliente = tk.Button(frame_botoes, text="Criar Cliente", **botao_azulclaro, command=app_Cliente.abrir_cadastrarCliente)
botao_cadastrarCliente.pack(side="left", padx=5)
janela.bind("<F7>", lambda e: botao_cadastrarCliente.invoke())

botao_cadastrarPratos = tk.Button(frame_botoes, text="Criar Pratos", **botao_azulclaro, command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.pack(side="left", padx=5)
janela.bind("<F8>", lambda e: botao_cadastrarPratos.invoke())

botao_cadastrarAcompanhamentos = tk.Button(frame_botoes, text="Criar Acomp", **botao_azulclaro, command=app_Acompanhamentos.abrir_cadastrarAcompanhamentos)
botao_cadastrarAcompanhamentos.pack(side="left", padx=5)
janela.bind("<F9>", lambda e: botao_cadastrarAcompanhamentos.invoke())


botao_deletar = tk.Button(frame_botoes, text="Deletar", **botao_vermelho,  command=lambda: deletar_pedido(tree, cursor, conn))
botao_deletar.pack(side="right", padx=5, pady=10)
def acionar_deletar(_):
    botao_deletar.invoke()
janela.bind("<Delete>", acionar_deletar)

botao_editar = tk.Button(frame_botoes, text="Editar", **botao_laranja, command=lambda: editar_pedido(tree, cursor, conn, date_entry, total_vendas_var, total_taxa_var, total_troco_var))
botao_editar.pack(side="right", padx=5, pady=10)
def acionar_editar(_):
    botao_editar.invoke()
janela.bind("<F12>", acionar_editar)  

btn_imprimir = tk.Button(frame_botoes, text="Re-imprimir", **botao_laranja, command=lambda: imprimir_pedido_daruma(tree))
btn_imprimir.pack(side="right", padx=5, pady=10)
def acionar_imprimir(_):
    btn_imprimir.invoke()
janela.bind("<F11>", acionar_imprimir)  

botao_fecharCaixa = tk.Button(frame_botoes, text="Caixa", **botao_laranja, command=app_Caixa.abrir_fecharCaixa)
botao_fecharCaixa.pack(side="right", padx=5)
janela.bind("<F10>", lambda e: botao_fecharCaixa.invoke())  


janela.mainloop()

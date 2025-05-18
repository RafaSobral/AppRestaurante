import serial
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox,ttk
from utils import carregar_pedidos
from estilizacao import botao_verde, botao_vermelho



class Pedido:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()

        self.cadastrarPedido = None
        self.combo_cliente = None
        self.telefone = None
        self.endereco =  None
        self.referencia = None
        self.combo_prato = None
        self.acomp1 = None
        self.acomp2 = None
        self.observacao = None
        self.tamanho = None
        self.pagamento = None
        self.troco = None
        self.taxa = None
        self.total = None
        self.nome_clientes = None
        self.bebida = None
        self.tree = None
        self.total_vendas_var = tk.StringVar(value="Total Vendas: R$ 0,00")
        self.total_taxa_var = tk.StringVar(value="Total Taxa: R$ 0,00")
        self.total_troco_var = tk.StringVar(value="Total Troco: R$ 0,00")

        

        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER,
                nome_cliente TEXT NOT NULL,
                prato TEXT,
                acompanhamento1 TEXT,
                acompanhamento2 TEXT,
                observacao TEXT,
                tamanho TEXT,
                bebida TEXT,
                pagamento TEXT,
                troco REAL,
                taxa REAL,
                total REAL,
                data_hoje TEXT
            )
        ''')
        self.conexao.commit()

    def abrir_cadastrarPedido(self, tree=None):
        self.tree = tree
        self.cadastrarPedido = tk.Toplevel()
        self.cadastrarPedido.focus_force()
        self.cadastrarPedido.title('Cadastrar Pedido')
        self.cadastrarPedido.geometry('350x480')
        self.cadastrarPedido.iconphoto(False, tk.PhotoImage(file='logo.png'))

        self.cursor.execute("SELECT id, nome FROM clientes")
        clientes = self.cursor.fetchall()
        self.nome_clientes = [f"{id} - {nome}" for id, nome in clientes]

        linha1 = tk.Frame(self.cadastrarPedido)
        linha1.pack(pady=2)  # removido anchor="w"
        tk.Label(linha1, text="Nome:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.combo_cliente = ttk.Combobox(linha1, values=self.nome_clientes)
        self.combo_cliente.pack(side="left")
        self.combo_cliente.bind("<<ComboboxSelected>>", self.preencher_dados_cliente)

        linha2 = tk.Frame(self.cadastrarPedido)
        linha2.pack(pady=2)
        tk.Label(linha2, text="Endereco:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.endereco = tk.Entry(linha2)
        self.endereco.pack(side="left")

        linha3 = tk.Frame(self.cadastrarPedido)
        linha3.pack(pady=2)
        tk.Label(linha3, text="Telefone:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.telefone = tk.Entry(linha3)
        self.telefone.pack(side="left")

        linha4 = tk.Frame(self.cadastrarPedido)
        linha4.pack(pady=2)
        tk.Label(linha4, text="Referencia:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.referencia = tk.Entry(linha4)
        self.referencia.pack(side="left")

        self.cursor.execute("SELECT nome FROM pratos")
        pratos = [p[0] for p in self.cursor.fetchall()]
        linha5 = tk.Frame(self.cadastrarPedido)
        linha5.pack(pady=2)
        tk.Label(linha5, text="Prato:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.combo_prato = ttk.Combobox(linha5, values=pratos)
        self.combo_prato.pack(side="left")

        self.cursor.execute("SELECT nome FROM acompanhamentos")
        acompanhamentos = [a[0] for a in self.cursor.fetchall()]
        linha6 = tk.Frame(self.cadastrarPedido)
        linha6.pack(pady=2)
        tk.Label(linha6, text="Acompanhamento 1:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.acomp1 = ttk.Combobox(linha6, values=acompanhamentos)
        self.acomp1.pack(side="left")

        linha7 = tk.Frame(self.cadastrarPedido)
        linha7.pack(pady=2)
        tk.Label(linha7, text="Acompanhamentos 2:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.acomp2 = ttk.Combobox(linha7, values=acompanhamentos)
        self.acomp2.pack(side="left")

        linha8 = tk.Frame(self.cadastrarPedido)
        linha8.pack(pady=2)
        tk.Label(linha8, text="Observacao:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.observacao = tk.Entry(linha8)
        self.observacao.pack(side="left")

        self.cursor.execute("SELECT nome FROM bebidas")
        bebida = [a[0] for a in self.cursor.fetchall()]
        linha10 = tk.Frame(self.cadastrarPedido)
        linha10.pack(pady=2)
        tk.Label(linha10, text="Bebida:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.bebida = ttk.Combobox(linha10, values=bebida)
        self.bebida.pack(side="left")
        self.bebida.bind("<<ComboboxSelected>>", lambda event: self.calcular_valor())

        tk.Label(self.cadastrarPedido, text="Tamanho:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack()

        linha9 = tk.Frame(self.cadastrarPedido)
        linha9.pack(pady=2)
        self.tamanho = tk.StringVar()
        self.tamanho.set(None)
        frame_tamanho = tk.Frame(linha9)
        frame_tamanho.pack(side="left")
        tamanhos = [("P", "13"), ("M", "15"), ("G", "18")]
        for txt, val in tamanhos:
            tk.Radiobutton(frame_tamanho, text=txt, variable=self.tamanho, value=val, command=self.calcular_valor).pack(side="left", padx=5)
        self.cadastrarPedido.bind("p", lambda e: self.selecionar_tamanho("13"))
        self.cadastrarPedido.bind("m", lambda e: self.selecionar_tamanho("15"))
        self.cadastrarPedido.bind("g", lambda e: self.selecionar_tamanho("18"))

        tk.Label(self.cadastrarPedido, text="Pagamento:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack()

        linha11 = tk.Frame(self.cadastrarPedido)
        linha11.pack(pady=2)
        self.pagamento = tk.StringVar()
        self.pagamento.set(None)
        frame_pagamento = tk.Frame(linha11)
        frame_pagamento.pack(side="left")
        formas = ["Credito", "Debito", "Dinheiro", "Pix", "Mumbuca"]
        for forma in formas:
            tk.Radiobutton(frame_pagamento, text=forma, variable=self.pagamento, value=forma).pack(side="left", padx=2)
        self.cadastrarPedido.bind("1", lambda e: self.selecionar_pagamento("Credito"))
        self.cadastrarPedido.bind("2", lambda e: self.selecionar_pagamento("Debito"))
        self.cadastrarPedido.bind("3", lambda e: self.selecionar_pagamento("Dinheiro"))
        self.cadastrarPedido.bind("4", lambda e: self.selecionar_pagamento("Pix"))
        self.cadastrarPedido.bind("5", lambda e: self.selecionar_pagamento("Mumbuca"))

        linha12 = tk.Frame(self.cadastrarPedido)
        linha12.pack(pady=2)
        tk.Label(linha12, text="Quantidade de troco:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.troco = tk.Entry(linha12)
        self.troco.pack(side="left")

        linha13 = tk.Frame(self.cadastrarPedido)
        linha13.pack(pady=2)
        tk.Label(linha13, text="Taxa de entrega:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.taxa = tk.Entry(linha13)
        self.taxa.pack(side="left")
        self.taxa.bind("<KeyRelease>", lambda e: self.calcular_valor())

        linha14 = tk.Frame(self.cadastrarPedido)
        linha14.pack(pady=2)
        tk.Label(linha14, text="Valor Total:", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack(side="left")
        self.total = tk.StringVar()
        tk.Entry(linha14, textvariable=self.total, state="readonly").pack(side="left")

        linha_botoes = tk.Frame(self.cadastrarPedido)
        linha_botoes.pack(pady=10)
        botao_salvar = tk.Button(linha_botoes, **botao_verde, text="Salvar", command=self.salvar_Pedido)
        botao_salvar.pack(side="left", padx=5)
        def acionar_salvar(_):
            botao_salvar.invoke()
        self.cadastrarPedido.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(linha_botoes, **botao_vermelho, text="Fechar", command=self.cadastrarPedido.destroy)
        botao_voltar.pack(side="left", padx=5)
        def acionar_voltar(_):
            botao_voltar.invoke()
        self.cadastrarPedido.bind("<Escape>", acionar_voltar)


    def selecionar_tamanho(self, valor):
        self.tamanho.set(valor)  
        self.calcular_valor()

    def selecionar_pagamento(self, valor):
        self.pagamento.set(valor)  
        self.calcular_valor()




    def preencher_dados_cliente(self, event):
        cliente_id = self.combo_cliente.get().split(" - ")[0]
        self.cursor.execute("SELECT endereco, telefone, referencia FROM clientes WHERE id = ?", (cliente_id,))
        dados = self.cursor.fetchone()
        if dados:
            self.endereco.delete(0, tk.END)
            self.telefone.delete(0, tk.END)
            self.referencia.delete(0, tk.END)
            self.endereco.insert(0, dados[0])
            self.telefone.insert(0, dados[1])
            self.referencia.insert(0, dados[2])

    def calcular_valor(self):
        try:
            bebida_escolhida = self.bebida.get()
            self.cursor.execute("SELECT preco FROM bebidas WHERE nome=?",(bebida_escolhida,))
            resultado = self.cursor.fetchone()
            valor_bebida = float(resultado[0])if resultado else 0
            valor_marmita = float(self.tamanho.get())
            taxa = float(self.taxa.get()) if self.taxa.get() else 0
            total  = valor_marmita + taxa + valor_bebida
            self.total.set(f"{total:.2f}")
        except:
            self.total.set("")

    def salvar_Pedido(self):
        if not self.combo_cliente.get():
            messagebox.showerror("Erro", "Selecione um cliente.")
            return

        nome_cliente = self.combo_cliente.get().split(" - ")[1]
        prato = self.combo_prato.get()
        acomp1 = self.acomp1.get()
        acomp2 = self.acomp2.get()
        observacao = self.observacao.get()
        tamanho = self.tamanho.get()
        bebida = self.bebida.get()
        pagamento = self.pagamento.get()
        troco = float(self.troco.get() or 0)
        taxa = float(self.taxa.get() or 0)
        total = float(self.total.get() or 0)
        data_hoje = datetime.now().strftime("%d-%m-%Y")

        endereco = self.endereco.get()
        telefone = self.telefone.get()
        referencia = self.referencia.get()

        self.cursor.execute("SELECT MAX(pedido_id) FROM pedidos WHERE data_hoje = ?", (data_hoje,))
        ultimo_id = self.cursor.fetchone()[0]
        pedido_id = (ultimo_id or 0) + 1

        dados = (
            pedido_id, nome_cliente, prato, acomp1, acomp2, observacao,
            tamanho, bebida, pagamento, troco, taxa, total, data_hoje
        )

        self.cursor.execute('''
            INSERT INTO pedidos (pedido_id, nome_cliente, prato, acompanhamento1, acompanhamento2, observacao, tamanho, bebida, pagamento, troco, taxa, total, data_hoje)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)                
        ''', dados)
        self.conexao.commit()

        pedido = {
            "pedido_id": pedido_id,
            "nome_cliente": nome_cliente,
            "endereco": endereco,
            "telefone": telefone,
            "referencia": referencia,
            "prato": prato,
            "acomp1": acomp1,
            "acomp2": acomp2,
            "observacao": observacao,
            "tamanho": tamanho,
            "bebida": bebida,
            "pagamento": pagamento,
            "troco": troco,
            "taxa": taxa,
            "total": total,
            "data_hoje": data_hoje
        }

        self.imprimir_pedido_daruma_por_dados(pedido)

        self.cadastrarPedido.destroy()
        messagebox.showinfo("Sucesso", "Pedido salvo e impresso!")

        agora = datetime.now()
        dia = agora.strftime("%d")
        mes = agora.strftime("%m")
        ano = agora.strftime("%Y")

        carregar_pedidos(self.tree, self.cursor, dia, mes, ano, self.total_vendas_var, self.total_taxa_var, self.total_troco_var)




    def imprimir_pedido_daruma_por_dados(self, pedido):
        try:
            porta = serial.Serial('COM3', baudrate=9600, timeout=1)
            texto = f"""
*** Bom Apetite ***
------------------------
Cliente: {pedido['nome_cliente']}
Endereço: {pedido['endereco']}
Telefone: {pedido['telefone']}
Referência: {pedido['referencia']}
------------------------
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



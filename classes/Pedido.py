import tkinter as tk
import sqlite3
import serial
from tkinter import messagebox,ttk
from datetime import datetime


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
                pagamento TEXT,
                troco REAL,
                taxa REAL,
                total REAL,
                data_hoje TEXT
            )
        ''')
        self.conexao.commit()

    def abrir_cadastrarPedido(self):
        self.cadastrarPedido = tk.Toplevel()
        self.cadastrarPedido.focus_force()
        self.cadastrarPedido.title('Cadastrar Pedido')
        self.cadastrarPedido.geometry('500x310')
        self.cadastrarPedido.iconphoto(False, tk.PhotoImage(file='logo.png'))

        self.cursor.execute("SELECT id, nome FROM clientes")
        clientes = self.cursor.fetchall()
        self.nome_clientes = [f"{id} - {nome}" for id, nome in clientes]

        tk.Label(self.cadastrarPedido, text="Nome:").grid(row=0, column=0)
        self.combo_cliente = ttk.Combobox(self.cadastrarPedido, values=self.nome_clientes)
        self.combo_cliente.grid(row=0, column=1)
        self.combo_cliente.bind("<<ComboboxSelected>>", self.preencher_dados_cliente)

        self.endereco = tk.Entry(self.cadastrarPedido)
        self.endereco.grid(row=1, column=1)
        tk.Label(self.cadastrarPedido, text="Endereco:").grid(row=1,column=0)

        self.telefone = tk.Entry(self.cadastrarPedido)
        self.telefone.grid(row=2, column= 1)
        tk.Label(self.cadastrarPedido, text="Telefone:").grid(row=2,column=0)

        self.referencia = tk.Entry(self.cadastrarPedido)
        self.referencia.grid(row=3,column=1)
        tk.Label(self.cadastrarPedido, text="Referencia:").grid(row=3, column=0)

        self.cursor.execute("SELECT nome FROM pratos")
        pratos = [p[0] for p in self.cursor.fetchall()]
        tk.Label(self.cadastrarPedido, text="Prato:").grid(row=4,column=0)
        self.combo_prato = ttk.Combobox(self.cadastrarPedido, values=pratos)
        self.combo_prato.grid(row=4,column=1)

        self.cursor.execute("SELECT nome FROM acompanhamentos")
        acompanhamentos1 = [a[0] for a in self.cursor.fetchall()]
        tk.Label(self.cadastrarPedido, text="Acompanhamento 1:").grid(row=5,column=0)
        self.acomp1 = ttk.Combobox(self.cadastrarPedido, values=acompanhamentos1)
        self.acomp1.grid(row=5, column=1)

        self.cursor.execute("SELECT nome FROM acompanhamentos")
        acompanhamentos2 = [a[0] for a in self.cursor.fetchall()]
        tk.Label(self.cadastrarPedido, text="Acompanhamentos 2:").grid(row=6,column=0)
        self.acomp2 = ttk.Combobox(self.cadastrarPedido, values=acompanhamentos2)
        self.acomp2.grid(row=6, column=1)

        tk.Label(self.cadastrarPedido, text="Observacao:").grid(row=7, column=0)
        self.observacao = tk.Entry(self.cadastrarPedido)
        self.observacao.grid(row=7,column=1)

        tk.Label(self.cadastrarPedido, text="Tamanho:").grid(row=8, column=0)
        self.tamanho = tk.StringVar()
        self.tamanho.set(None)

        frame_tamanho = tk.Frame(self.cadastrarPedido)
        frame_tamanho.grid(row=8, column=1, columnspan=3, sticky="w")  

        tamanhos = [("P", "13"), ("M", "15"), ("G", "18")]
        for txt, val in tamanhos:
            tk.Radiobutton(frame_tamanho, text=txt, variable=self.tamanho, value=val, command=self.calcular_valor).pack(side="left", padx=12)       
        
        tk.Label(self.cadastrarPedido, text="Forma de Pagamento:").grid(row=9, column=0, sticky="w")
        self.pagamento = tk.StringVar()
        self.pagamento.set(None)

        frame_pagamento = tk.Frame(self.cadastrarPedido)
        frame_pagamento.grid(row=9, column=1, columnspan=5, sticky="w")  

        formas = ["Credito", "Debito", "Dinheiro", "Pix", "Mumbuca"]
        for forma in formas:
            tk.Radiobutton(frame_pagamento, text=forma, variable=self.pagamento, value=forma).pack(side="left", padx=2)
    
        tk.Label(self.cadastrarPedido, text="Quantidade de troco:").grid(row=10, column=0)
        self.troco = tk.Entry(self.cadastrarPedido)
        self.troco.grid(row=10, column=1)

        tk.Label(self.cadastrarPedido, text="Taxa de entrega:").grid(row=11, column=0)
        self.taxa = tk.Entry(self.cadastrarPedido)
        self.taxa.grid(row=11, column=1)
        self.taxa.bind("<KeyRelease>", lambda e: self.calcular_valor())

        tk.Label(self.cadastrarPedido, text="Valor Total:").grid(row=12, column=0)
        self.total = tk.StringVar()
        tk.Entry(self.cadastrarPedido, textvariable=self.total, state="readonly").grid(row=12, column=1)

        botao_salvar = tk.Button(self.cadastrarPedido, text="Salvar [Enter]", command=self.salvar_Pedido)
        botao_salvar.grid(row=13, column=0)
        def acionar_salvar(_):
            botao_salvar.invoke()
        self.cadastrarPedido.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarPedido, text="Fechar [Esc]", command=self.cadastrarPedido.destroy)
        botao_voltar.grid(row = 13, column = 1)
        def acionar_voltar(_):
            botao_voltar.invoke()
        self.cadastrarPedido.bind("<Escape>", acionar_voltar)

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
            valor_marmita = float(self.tamanho.get())
            taxa = float(self.taxa.get()) if self.taxa.get() else 0
            total  = valor_marmita + taxa
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
            tamanho, pagamento, troco, taxa, total, data_hoje
        )

        self.cursor.execute('''
            INSERT INTO pedidos (pedido_id, nome_cliente, prato, acompanhamento1, acompanhamento2, observacao, tamanho, pagamento, troco, taxa, total, data_hoje)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)                
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
            "pagamento": pagamento,
            "troco": troco,
            "taxa": taxa,
            "total": total,
            "data_hoje": data_hoje
        }

        self.imprimir_pedido_daruma_por_dados(pedido)

        self.cadastrarPedido.destroy()
        messagebox.showinfo("Sucesso", "Pedido salvo e impresso!")


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



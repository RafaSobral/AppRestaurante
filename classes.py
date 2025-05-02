import tkinter as tk
from tkinter import messagebox,ttk
from datetime import datetime
import sqlite3

################Classe Cliente################################

class Cliente:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

        self.nome = None
        self.endereco = None
        self.telefone = None
        self.referencia = None



    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT NOT NULL,
                telefone TEXT NOT NULL,
                referencia TEXT NOT NULL
            )
        ''')
        self.conexao.commit()


    def salvar_cliente(self):
        nome = self.nome.get()
        endereco = self.endereco.get()
        telefone = self.telefone.get()
        referencia = self.referencia.get()

        if nome == "" or endereco == "" or telefone == "" or referencia == "":
            messagebox.showerror("Erro", "Nenhum dos campos pode estar vazio!")
            return

        self.cursor.execute('''
            INSERT INTO clientes (nome, endereco, telefone, referencia)
            VALUES (?, ?, ?, ?)
        ''',(nome, endereco, telefone, referencia))
        self.conexao.commit()

        messagebox.showinfo("Sucesso", "Cliente cadastrado!")
        self.cadastrarCliente.destroy()

    def abrir_visualizarClientes(self):
        self.visualizarClientes = tk.Toplevel()
        self.visualizarClientes.title('Visualizar Clientes')
        self.visualizarClientes.geometry("500x300")

        tree = ttk.Treeview(self.visualizarClientes, columns=("id", "nome", "endereco", "telefone", "referencia"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("endereco", text="Endereco")
        tree.heading("telefone", text="Telefone")
        tree.heading("referencia", text="Referencia")
        
        tree.column("id", width=30)
        tree.column("nome", width=100)
        tree.column("endereco", width=100)
        tree.column("telefone", width=90)
        tree.column("referencia", width=100)

        tree.pack(expand=True, fill="both")

        self.cursor.execute("SELECT * FROM clientes")
        dados = self.cursor.fetchall()

        for cliente in dados:
            tree.insert("", "end", values=cliente)



    def abrir_cadastrarCliente(self):
        self.cadastrarCliente = tk.Toplevel()
        self.cadastrarCliente.title('Cadastrar Cliente')

        label_nome = tk.Label(self.cadastrarCliente, text="Nome:")
        label_nome.grid(row = 0, column = 0)
        self.nome = tk.Entry(self.cadastrarCliente)
        self.nome.grid(row = 0, column = 1)

        label_endereco = tk.Label(self.cadastrarCliente, text="Endereco:")
        label_endereco.grid(row = 1, column = 0)
        self.endereco = tk.Entry(self.cadastrarCliente)
        self.endereco.grid(row = 1, column = 1)

        label_telefone = tk.Label(self.cadastrarCliente, text="Telefone:")
        label_telefone.grid(row= 2, column= 0)
        self.telefone = tk.Entry(self.cadastrarCliente)
        self.telefone.grid(row = 2, column = 1)

        label_referencia = tk.Label(self.cadastrarCliente, text="Referencia:")
        label_referencia.grid(row=3 , column= 0)
        self.referencia = tk.Entry(self.cadastrarCliente)
        self.referencia.grid(row=3, column=1)

        botao_salvar = tk.Button(self.cadastrarCliente, text="Salvar", command=self.salvar_cliente)
        botao_salvar.grid(row=6, column=0)

        botao_voltar = tk.Button(self.cadastrarCliente, text="Fechar", command=self.cadastrarCliente.destroy)
        botao_voltar.grid(row = 7, column = 0)



################FIM da Classe Cliente################################


################Classe PRATOS########################################

class Prato:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

        self.nome = None 
        self.descricao = None 
        self.gerenciarPratos = None

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pratos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT
            )
        ''')
        self.conexao.commit()

    def salvar_prato(self):
        nome = self.nome.get()
        descricao = self.descricao.get()

        if nome == "":
            messagebox.showerror("Erro", "O nome nao pode estar vazio")
            return 
        self.cursor.execute('''
            INSERT INTO pratos (nome, descricao)
            VALUES(?,?)
        ''',(nome, descricao))
        self.conexao.commit()

        messagebox.showinfo("Sucesso", "Prato cadastrado!")
        self.cadastrarPratos.destroy()

    def abrir_visualizarPratos(self):
        self.visualizarPratos = tk.Toplevel()
        self.visualizarPratos.title('Visualizar Pratos')
        self.visualizarPratos.geometry('500x300')

        tree = ttk.Treeview(self.visualizarPratos, columns=("id", "nome", "descricao"), show="headings" )
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("descricao", text="Descricao")

        tree.column("id", width=30)
        tree.column("nome", width=100)
        tree.column("descricao", width=100)

        tree.pack(expand=True, fill="both")

        self.cursor.execute("SELECT * FROM pratos")
        dados = self.cursor.fetchall()

        for pratos in dados:
            tree.insert("", "end", values=pratos)



    def abrir_cadastrarPratos(self):
        self.cadastrarPratos = tk.Toplevel()
        self.cadastrarPratos.title('Cadastrar Pratos')
        self.cadastrarPratos.geometry('500x300')

        label_nome = tk.Label(self.cadastrarPratos, text="Nome:")
        label_nome.grid(row=0,column=0)
        self.nome = tk.Entry(self.cadastrarPratos)
        self.nome.grid(row=0,column=1)
        
        label_descricao = tk.Label(self.cadastrarPratos, text="Descricao:")
        label_descricao.grid(row=1,column=0)
        self.descricao = tk.Entry(self.cadastrarPratos)
        self.descricao.grid(row=1,column=1)

        botao_salvar = tk.Button(self.cadastrarPratos, text="Salvar", command=self.salvar_prato)
        botao_salvar.grid(row=6, column=0)

        botao_voltar = tk.Button(self.cadastrarPratos, text="Fechar", command=self.cadastrarPratos.destroy)
        botao_voltar.grid(row=7, column=0)

    def abrir_gerenciarPratos(self):
        self.gerenciarPratos = tk.Toplevel()
        self.gerenciarPratos.title("Gerenciar Pratos:")
        self.gerenciarPratos.geometry('300x500')

        self.tree = ttk.Treeview(self.gerenciarPratos, columns=("id","nome","descricao"), show="headings")
        self.tree.heading("id",text="ID")
        self.tree.heading("nome",text="Nome")
        self.tree.heading("descricao", text="Descricao")

        self.tree.column("id",width=50)
        self.tree.column("nome", width=50)
        self.tree.column("descricao", width=50)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cursor.execute("SELECT * FROM pratos")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

        botao_editar = tk.Button(self.gerenciarPratos, text="Editar", command=self.editar_prato)
        botao_editar.pack(side="left", padx=10, pady=10)

        botao_deletar = tk.Button(self.gerenciarPratos, text="Deletar", command=self.deletar_prato)
        botao_deletar.pack(side="right", padx=10, pady=10)

    def editar_prato(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione um prato para editar")
            return
        
        prato_id, nome_antigo, descricao_antiga = self.tree.item(selected[0], "values")

        janela_editar = tk.Toplevel()
        janela_editar.title("Editar prato")

        tk.Label(janela_editar, text="Nome").pack()
        nome_entry = tk.Entry(janela_editar)
        nome_entry.insert(0, nome_antigo)
        nome_entry.pack()

        tk.Label(janela_editar, text="Descricao").pack()
        descricao_entry = tk.Entry(janela_editar)
        descricao_entry.insert(0, descricao_antiga)
        descricao_entry.pack()

        def salvar_edicao():
            novo_nome = nome_entry.get()
            nova_descricao = descricao_entry.get()
            self.cursor.execute("UPDATE pratos SET nome=?, descricao=? WHERE id=?", (novo_nome, nova_descricao, prato_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Prato atualizado com sucesso")
            janela_editar.destroy()
            self.gerenciarPratos.destroy()
            self.abrir_gerenciarPratos()

        tk.Button(janela_editar, text="Salvar", command=salvar_edicao).pack(pady=10)

    def deletar_prato(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso:","Selecione um prato para deletar")
            return
        
        prato_id = self.tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("confimar", "Tem certeza que deseja excluir esse prato?")
        if confirm:
            self.cursor.execute("DELETE FROM pratos WHERE id=?", (prato_id,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Prato deletado com Sucesso!")
            self.tree.delete(selected[0])


        

################FIM da Classe PRATOS####################################

################Classe Acompanhamentos####################################

class Acompanhamento:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

        self.acomp = None
        self.cadastrarAcomp = None

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS acompanhamentos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL        
            )
        ''')
        self.conexao.commit()

    def salvar_Acompanhamento(self):
        nome = self.acomp.get()

        if nome == "":
            messagebox.showerror("Erro", "O campo esta vazio")
            return
        
        self.cursor.execute('''
            INSERT INTO acompanhamentos (nome)
            VALUES (?)
        ''',(nome,))
        self.conexao.commit()

        messagebox.showinfo("Sucesso", "Acompanhamento Cadastrado!")
        self.cadastrarAcomp.destroy()
            

    def abrir_cadastrarAcompanhamentos(self):
        self.cadastrarAcomp = tk.Toplevel()
        self.cadastrarAcomp.title("Cadastrar Acompanhamentos:")
        self.cadastrarAcomp.geometry("500x600")

        tk.Label(self.cadastrarAcomp, text="Acompanhamento: " ).grid(row=0, column=0)
        self.acomp = tk.Entry(self.cadastrarAcomp)
        self.acomp.grid(row=0, column=1)

        botao_Salvar = tk.Button(self.cadastrarAcomp, text="Salvar", command=self.salvar_Acompanhamento)
        botao_Salvar.grid(row=1, column=1)

    def abrir_visualizarAcompanhamentos(self):
        self.visualizarAcomp = tk.Toplevel()
        self.visualizarAcomp.title("Visualizar Acompanhamentos:")
        self.visualizarAcomp.geometry("500x600")

        tree = ttk.Treeview(self.visualizarAcomp, columns=("id","nome"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")

        tree.column("id", width=30)
        tree.column("nome", width=100)

        tree.pack(expand=True, fill="both")

        self.cursor.execute("SELECT * FROM acompanhamentos")
        dados = self.cursor.fetchall()

        for acompanhamento in dados:
            tree.insert("", "end", values=acompanhamento)


################FIM da Classe Acompanhamentos####################################

################Classe Pedidos####################################

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

        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
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
        self.cadastrarPedido.title('Cadastrar Pedido')
        self.cadastrarPedido.geometry('530x310')

        self.cursor.execute("SELECT id, nome FROM clientes")
        clientes = self.cursor.fetchall()
        nome_clientes = [f"{id} - {nome}" for id, nome in clientes]

        tk.Label(self.cadastrarPedido, text="Nome:").grid(row=0, column=0)
        self.combo_cliente = ttk.Combobox(self.cadastrarPedido, values=nome_clientes)
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
        tamanhos =[("P","13"),("M","15"),("G","18")]
        for i, (txt, val) in enumerate(tamanhos):
            tk.Radiobutton(self.cadastrarPedido, text=txt, variable=self.tamanho, value=val, command=self.calcular_valor).grid(row=8, column=i+1)

        tk.Label(self.cadastrarPedido, text="Forma de Pagamento:").grid(row=9, column=0)
        self.pagamento = tk.StringVar()
        pagamentos =["Credito", "Debito", "Dinheiro", "Pix", "Mumbuca"]
        for i, op in enumerate(pagamentos):
            tk.Radiobutton(self.cadastrarPedido, text=op, variable=self.pagamento, value=op).grid(row=9, column=1 + i)

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

        tk.Button(self.cadastrarPedido, text="Salvar Pedido", command=self.salvar_Pedido).grid(row=13, column=0)

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
        cliente_id = self.combo_cliente.get().split(" - ")[0]
        data_hoje = datetime.now().strftime("%d-%m-%Y")
        dados = (
            cliente_id,
            self.combo_prato.get(),
            self.acomp1.get(),
            self.acomp2.get(),
            self.observacao.get(),
            self.tamanho.get(),
            self.pagamento.get(),
            float(self.troco.get() or 0),
            float(self.taxa.get() or 0),
            float(self.total.get() or 0),
            data_hoje
        )

        self.cursor.execute('''
            INSERT INTO pedidos (cliente_id, prato, acompanhamento1, acompanhamento2, observacao, tamanho, pagamento, troco, taxa, total, data_hoje)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)                
        ''', dados)
        self.conexao.commit()
        messagebox.showinfo("Sucesso", "Pedido salvo!!!")
        self.cadastrarPedido.destroy()

    def abrir_visualizarPedidos(self):
        self.visualizarPedidos = tk.Toplevel()
        self.visualizarPedidos.title('Visualizar Pedidos')
        self.visualizarPedidos.geometry('300x500')

        tree = ttk.Treeview(self.visualizarPedidos, columns=("ID Cliente","Prato","Acomp 1","Acomp 2","Tamanho","Pagamento","Troco","Taxa","Total"), show="headings")
        tree.heading("ID Cliente",text="ID Cliente")
        tree.heading("Prato",text="Prato")
        tree.heading("Acomp 1",text="Acomp 1")
        tree.heading("Acomp 2",text="Acomp 2")
        tree.heading("Tamanho",text="Tamanho")
        tree.heading("Pagamento",text="Pagamento")
        tree.heading("Troco",text="Troco")
        tree.heading("Taxa",text="Taxa")
        tree.heading("Total",text="Total")

        tree.column("ID Cliente", width=30)
        tree.column("Prato", width=30)
        tree.column("Acomp 1", width=30)
        tree.column("Acomp 2", width=30)
        tree.column("Tamanho", width=30)
        tree.column("Pagamento", width=30)
        tree.column("Troco", width=30)
        tree.column("Taxa", width=30)
        tree.column("Total", width=30)
        
        tree.pack(expand=True, fill="both")

        self.cursor.execute("""
            SELECT cliente_id, prato, acompanhamento1, acompanhamento2,
                tamanho, pagamento, troco, taxa, total
            FROM pedidos
        """)

        dados = self.cursor.fetchall()

        for pedidos in dados:
            tree.insert("", "end", values=pedidos)


########FIM da Classe Pedidos####################################

class Caixa:
    def __init__(self):
        self.fecharCaixa = None
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()

    def abrir_fecharCaixa(self):
        hoje = datetime.now().strftime("%d-%m-%Y")

        self.cursor.execute("SELECT pagamento, total FROM pedidos WHERE data_hoje = ?", (hoje,))
        pedidos = self.cursor.fetchall()

        total_geral = 0
        formas_pagamento = {}

        for pagamento, valor in pedidos:
            total_geral += valor
            if pagamento in formas_pagamento:
                formas_pagamento[pagamento] += valor
            else:
                formas_pagamento[pagamento] = valor

        self.fecharCaixa = tk.Toplevel()
        self.fecharCaixa.geometry('500x200')
        self.fecharCaixa.title('Fechar o Caixa - ' + hoje)

        tk.Label(self.fecharCaixa, text=f"Total Geral do Dia: R$ {total_geral:.2f}", font=("Arial", 12, "bold")).pack(pady=5)

        tk.Label(self.fecharCaixa, text="Totais por Forma de Pagamento:", font=("Arial", 10, "underline")).pack()

        for metodo, total in formas_pagamento.items():
            tk.Label(self.fecharCaixa, text=f"{metodo}: R$ {total:.2f}").pack(anchor='w', padx=10)

        



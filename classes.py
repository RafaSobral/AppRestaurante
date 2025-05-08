import tkinter as tk
import sqlite3
import serial
import locale
from tkinter import messagebox,ttk
from datetime import datetime
from tkcalendar import DateEntry


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
        self.gerenciarClientes = None
        self.cadastrarCliente = None
        self.tree = None



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

    
    def abrir_cadastrarCliente(self):
        self.cadastrarCliente = tk.Toplevel()
        self.cadastrarCliente.focus_force()
        self.cadastrarCliente.title('Cadastrar Cliente')
        self.cadastrarCliente.iconphoto(False, tk.PhotoImage(file='logo.png'))

        label_nome = tk.Label(self.cadastrarCliente, text="Nome:")
        label_nome.grid(row = 0, column = 0)
        self.nome = tk.Entry(self.cadastrarCliente)
        self.nome.grid(row = 0, column = 1)
        self.nome.focus_set()

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

        botao_salvar = tk.Button(self.cadastrarCliente, text="Salvar [Return]", command=self.salvar_cliente)
        botao_salvar.grid(row=6, column=0)
        def acionar_salvar(event=None):
            botao_salvar.invoke()
        self.cadastrarCliente.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarCliente, text="Fechar [Esc]", command=self.cadastrarCliente.destroy)
        botao_voltar.grid(row = 7, column = 0)
        def acionar_voltar(event=None):
            botao_voltar.invoke()
        self.cadastrarCliente.bind("<Escape>", acionar_voltar)

    def abrir_gerenciarClientes(self):
        self.gerenciarClientes = tk.Toplevel()
        self.gerenciarClientes.title("Gerenciar Clientes")
        self.gerenciarClientes.focus_force()
        self.gerenciarClientes.geometry('300x500')
        self.gerenciarClientes.iconphoto(False, tk.PhotoImage(file='logo.png'))

        self.tree = ttk.Treeview(self.gerenciarClientes, columns=("id","nome","endereco","telefone","referencia"), show="headings")
        self.tree.heading("id",text="ID")
        self.tree.heading("nome",text="Nome")
        self.tree.heading("endereco",text="Endereco")
        self.tree.heading("telefone",text="Telefone")
        self.tree.heading("referencia",text="Referencia")

        self.tree.column("id", width=30)
        self.tree.column("nome", width=30)
        self.tree.column("endereco", width=30)
        self.tree.column("telefone", width=30)
        self.tree.column("referencia", width=30)

        self.tree.pack(fill="both",expand=True,padx=10,pady=10)

        self.cursor.execute("SELECT * FROM clientes")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

        botao_editar = tk.Button(self.gerenciarClientes, text="Editar [E]", command=self.editar_cliente)
        botao_editar.pack(side="left", padx=10, pady=10)
        self.gerenciarClientes.bind("<Key-e>", lambda e: botao_editar.invoke())

        botao_deletar = tk.Button(self.gerenciarClientes, text="Deletar [DEL]", command=self.deletar_cliente)
        botao_deletar.pack(side="left", padx=10, pady=10)
        self.gerenciarClientes.bind("<Delete>", lambda e: botao_deletar.invoke())

        botao_sair = tk.Button(self.gerenciarClientes, text="Sair [Esc]", command=self.gerenciarClientes.destroy)
        botao_sair.pack(side="left", padx=10, pady=10)
        self.gerenciarClientes.bind("<Escape>", lambda e: botao_sair.invoke())

    def editar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione um cliente para editar")
            return
        
        cliente_id, nome_antigo, endereco_antigo, telefone_antigo, referencia_antiga = self.tree.item(selected[0], "values")

        janela_editar = tk.Toplevel()
        janela_editar.focus_force()
        janela_editar.title("Editar Cliente")
        janela_editar.iconphoto(False, tk.PhotoImage(file='logo.png'))

        tk.Label(janela_editar, text="Nome").pack()
        nome_entry = tk.Entry(janela_editar)
        nome_entry.insert(0, nome_antigo)
        nome_entry.pack()

        tk.Label(janela_editar, text="Endereco").pack()
        endereco_entry = tk.Entry(janela_editar)
        endereco_entry.insert(0, endereco_antigo)
        endereco_entry.pack()

        tk.Label(janela_editar, text="Telefone").pack()
        telefone_entry = tk.Entry(janela_editar)
        telefone_entry.insert(0, telefone_antigo)
        telefone_entry.pack()

        tk.Label(janela_editar, text="Referencia").pack()
        referencia_entry = tk.Entry(janela_editar)
        referencia_entry.insert(0, referencia_antiga)
        referencia_entry.pack()

        def salvar_edicao():
            novo_nome = nome_entry.get()
            novo_endereco = endereco_entry.get()
            novo_telefone = telefone_entry.get()
            nova_referencia = referencia_entry.get()
            self.cursor.execute("UPDATE clientes SET nome=?, endereco=?, telefone=?, referencia=? WHERE ID=?",(novo_nome, novo_endereco, novo_telefone, nova_referencia, cliente_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Cliente atualizado com sucesso")
            janela_editar.destroy()
            self.gerenciarClientes.destroy()
            self.abrir_gerenciarClientes()

        botao_salvar = tk.Button(janela_editar, text="Salvar [Enter]", command=salvar_edicao)
        botao_salvar.pack(pady=10)
        def acionar_salvar(event=None):
            botao_salvar.invoke()
        janela_editar.bind("<Return>", acionar_salvar)


    def deletar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Aviso","Selecione um cliente para deletar")
            return
        
        cliente_id = self.tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar esse cliente?")
        if confirm:
            self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Cliente deletado com Sucesso")
            self.tree.delete(selected[0])

        



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
        self.cadastrarPratos = None
        self.tree = None

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



    def abrir_cadastrarPratos(self):
        self.cadastrarPratos = tk.Toplevel()
        self.cadastrarPratos.title('Cadastrar Pratos')
        self.cadastrarPratos.focus_force()
        self.cadastrarPratos.geometry('190x100')
        self.cadastrarPratos.iconphoto(False, tk.PhotoImage(file='logo.png'))

        label_nome = tk.Label(self.cadastrarPratos, text="Nome:")
        label_nome.grid(row=0,column=0)
        self.nome = tk.Entry(self.cadastrarPratos)
        self.nome.focus_set()
        self.nome.grid(row=0,column=1)
        
        label_descricao = tk.Label(self.cadastrarPratos, text="Descricao:")
        label_descricao.grid(row=1,column=0)
        self.descricao = tk.Entry(self.cadastrarPratos)
        self.descricao.grid(row=1,column=1)

        botao_salvar = tk.Button(self.cadastrarPratos, text="Salvar [Enter]", command=self.salvar_prato)
        botao_salvar.grid(row=6, column=0)
        def acionar_salvar(event=None):
            botao_salvar.invoke()
        self.cadastrarPratos.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarPratos, text="Fechar [Esc]", command=self.cadastrarPratos.destroy)
        botao_voltar.grid(row=7, column=0)
        def acionar_voltar(event=None):
            botao_voltar.invoke()
        self.cadastrarPratos.bind("<Escape>", acionar_voltar)

    def abrir_gerenciarPratos(self):
        self.gerenciarPratos = tk.Toplevel()
        self.gerenciarPratos.title("Gerenciar Pratos:")
        self.gerenciarPratos.focus_force()
        self.gerenciarPratos.geometry('300x500')
        self.gerenciarPratos.iconphoto(False, tk.PhotoImage(file='logo.png'))

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

        botao_editar = tk.Button(self.gerenciarPratos, text="Editar [E]", command=self.editar_prato)
        botao_editar.pack(side="left", padx=10, pady=10)
        self.gerenciarPratos.bind("<Key-e>", lambda e: botao_editar.invoke())

        botao_deletar = tk.Button(self.gerenciarPratos, text="Deletar [DEL]", command=self.deletar_prato)
        botao_deletar.pack(side="left", padx=10, pady=10)
        self.gerenciarPratos.bind("<Delete>", lambda e: botao_deletar.invoke())

        botao_sair = tk.Button(self.gerenciarPratos, text="Sair [Esc]", command=self.gerenciarPratos.destroy)
        botao_sair.pack(side="left", padx=10, pady=10)
        self.gerenciarPratos.bind("<Escape>", lambda e: botao_sair.invoke())

    def editar_prato(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione um prato para editar")
            return
        
        prato_id, nome_antigo, descricao_antiga = self.tree.item(selected[0], "values")

        janela_editar = tk.Toplevel()
        janela_editar.focus_force()
        janela_editar.title("Editar prato")
        janela_editar.iconphoto(False, tk.PhotoImage(file='logo.png'))

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

        botao_salvar = tk.Button(janela_editar, text="Salvar [Enter]", command=salvar_edicao)
        botao_salvar.pack(pady=10)
        def acionar_salvar(event=None):
            botao_salvar.invoke()
        janela_editar.bind("<Return>", acionar_salvar)

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
        self.tree = None
        self.gerenciarAcomp = None

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
        self.cadastrarAcomp.focus_force()
        self.cadastrarAcomp.title("Cadastrar Acompanhamentos:")
        self.cadastrarAcomp.geometry("250x80")
        self.cadastrarAcomp.iconphoto(False, tk.PhotoImage(file='logo.png'))

        tk.Label(self.cadastrarAcomp, text="Acompanhamento: " ).grid(row=0, column=0)
        self.acomp = tk.Entry(self.cadastrarAcomp)
        self.acomp.focus_set()
        self.acomp.grid(row=0, column=1)

        botao_Salvar = tk.Button(self.cadastrarAcomp, text="Salvar [Enter]", command=self.salvar_Acompanhamento)
        botao_Salvar.grid(row=1, column=0)
        def acionar_salvar(event=None):
            botao_Salvar.invoke()
        self.cadastrarAcomp.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarAcomp, text="Fechar [Escape]", command=self.cadastrarAcomp.destroy)
        botao_voltar.grid(row = 2, column = 0)
        def acionar_voltar(event=None):
            botao_voltar.invoke()
        self.cadastrarAcomp.bind("<Escape>", acionar_voltar)
        


    def abrir_gerenciarAcompanhamentos(self):
        self.gerenciarAcomp = tk.Toplevel()
        self.gerenciarAcomp.title('Gerenciar Acompanhamentos')
        self.gerenciarAcomp.focus_force()
        self.gerenciarAcomp.geometry('300x500')
        self.gerenciarAcomp.iconphoto(False, tk.PhotoImage(file='logo.png'))

        self.tree = ttk.Treeview(self.gerenciarAcomp, columns=("id","nome"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")

        self.tree.column("id", width=30)
        self.tree.column("nome", width=30)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cursor.execute("SELECT * FROM acompanhamentos")

        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

        botao_editar = tk.Button(self.gerenciarAcomp, text="Editar [E]", command=self.editar_acompanhamento)
        botao_editar.pack(side="left", padx=10, pady=10)
        self.gerenciarAcomp.bind("<Key-e>", lambda e: botao_editar.invoke())

        botao_deletar = tk.Button(self.gerenciarAcomp, text="Deletar [DEL]", command=self.deletar_acompanhamento)
        botao_deletar.pack(side="left", padx=10, pady=10)
        self.gerenciarAcomp.bind("<Delete>", lambda e: botao_deletar.invoke())

        botao_sair = tk.Button(self.gerenciarAcomp, text="Sair [Esc]", command=self.gerenciarAcomp.destroy)
        botao_sair.pack(side="left", padx=10, pady=10)
        self.gerenciarAcomp.bind("<Escape>", lambda e: botao_sair.invoke())


    def editar_acompanhamento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione um acompanhamento para deletar")
            return
        
        acomp_id, nome_antigo = self.tree.item(selected[0], "values")

        janela_editar = tk.Toplevel()
        janela_editar.focus_force()
        janela_editar.title('Editar prato')
        janela_editar.iconphoto(False, tk.PhotoImage(file='logo.png'))

        tk.Label(janela_editar, text="Nome").pack()
        nome_entry = tk.Entry(janela_editar)
        nome_entry.insert(0, nome_antigo)
        nome_entry.pack()

        def salvar_edicao():
            novo_nome = nome_entry.get()
            self.cursor.execute("UPDATE acompanhamentos SET nome=? WHERE id=?", (novo_nome, acomp_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Acompanhamento atualizado com sucesso")
            janela_editar.destroy()
            self.gerenciarAcomp.destroy()
            self.abrir_gerenciarAcompanhamentos()

        botao_salvar = tk.Button(janela_editar, text="Salvar [Enter]", command=salvar_edicao)
        botao_salvar.pack(pady=10)
        def acionar_salvar(event=None):
            botao_salvar.invoke()
        janela_editar.bind("<Return>", acionar_salvar)

    def deletar_acompanhamento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione um acompanhamento para deletar")
            return

        acomp_id = self.tree.item(selected[0],"values")[0]

        confirm = messagebox.askyesno("Confirmar","Tem certeza que deseja excluir essa acompanhamento?")
        if confirm:
            self.cursor.execute("DELETE FROM acompanhamentos WHERE id=?", (acomp_id,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Acompanhamento deletado com sucesso")
            self.tree.delete(selected[0])


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

        frame_tamanho = tk.Frame(self.cadastrarPedido)
        frame_tamanho.grid(row=8, column=1, columnspan=3, sticky="w")  

        tamanhos = [("P", "13"), ("M", "15"), ("G", "18")]
        for txt, val in tamanhos:
            tk.Radiobutton(frame_tamanho, text=txt, variable=self.tamanho, value=val, command=self.calcular_valor).pack(side="left", padx=12)       
        
        tk.Label(self.cadastrarPedido, text="Forma de Pagamento:").grid(row=9, column=0, sticky="w")
        self.pagamento = tk.StringVar()

        frame_pagamento = tk.Frame(self.cadastrarPedido)
        frame_pagamento.grid(row=9, column=1, columnspan=5, sticky="w")  

        formas = ["Crédito", "Débito", "Dinheiro", "Pix", "Mumbuca"]
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
        def acionar_salvar(event=None):
            botao_salvar.invoke()
        self.cadastrarPedido.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarPedido, text="Fechar [Esc]", command=self.cadastrarPedido.destroy)
        botao_voltar.grid(row = 13, column = 1)
        def acionar_voltar(event=None):
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

        # Gerar pedido_id reiniciando por dia
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



########FIM da Classe Pedidos####################################

class Caixa:
    def __init__(self):
        self.fecharCaixa = None
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.frame_conteudo = None


class Caixa:
    def __init__(self):
        self.fecharCaixa = None
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()

    def abrir_fecharCaixa(self):
        self.fecharCaixa = tk.Toplevel()
        self.fecharCaixa.focus_force()
        self.fecharCaixa.geometry("400x600")
        self.fecharCaixa.title("Fechar o Caixa")
        self.fecharCaixa.iconphoto(False, tk.PhotoImage(file='logo.png'))

        tk.Label(self.fecharCaixa, text="Para gerar o relatorio mensal, Selecione o mes e coloque o dia como 00.").pack(pady=6)
        tk.Label(self.fecharCaixa, text="Selecionar Data:").pack(pady=5)

        date_entry = DateEntry(self.fecharCaixa, width=12, background='darkblue',
                            foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        date_entry.pack(pady=10)

        def obter_data():
            try:
                locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux/macOS
            except:
                locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')  # Windows fallback

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            data_str = date_entry.get()
            dia, mes, ano = data_str.split('/')
            hoje = datetime.now().strftime("%d-%m-%Y")
            data_selecionada = f"{dia}-{mes}-{ano}"

            if dia == '00' or dia == '0':
                data_like = f"-{mes}-{ano}"
                self.cursor.execute("SELECT pagamento, total, tamanho, troco, taxa FROM pedidos WHERE data_hoje LIKE ?", (f"%{data_like}",))
                nome_mes = datetime.strptime(mes, "%m").strftime('%B')
                titulo = f"Fechamento de {nome_mes.capitalize()}/{ano}"
                label_total = f"Total do mês de {nome_mes.capitalize()}:"
            elif data_selecionada == hoje:
                self.cursor.execute("SELECT pagamento, total, tamanho, troco, taxa FROM pedidos WHERE data_hoje = ?", (data_selecionada,))
                titulo = "Fechamento de Hoje"
                label_total = "Total de Hoje:"
            else:
                self.cursor.execute("SELECT pagamento, total, tamanho, troco, taxa FROM pedidos WHERE data_hoje = ?", (data_selecionada,))
                titulo = f"Fechamento do Dia {data_selecionada}"
                label_total = f"Total do Dia {data_selecionada}:"

            pedidos = self.cursor.fetchall()

            total_geral = 0
            total_troco = 0
            total_taxa = 0
            formas_pagamento = {}
            tamanhos_marmita = {}

            for pagamento, valor, tamanho, troco, taxa in pedidos:
                total_geral += valor
                total_troco += troco
                total_taxa += taxa

                formas_pagamento[pagamento] = formas_pagamento.get(pagamento, 0) + valor
                tamanhos_marmita[tamanho] = tamanhos_marmita.get(tamanho, 0) + 1

            self.fecharCaixa.title(titulo)

            tk.Label(self.frame_conteudo, text=f"{label_total} R$ {total_geral:.2f}", font=("Arial", 12, "bold")).pack(pady=5)
            tk.Label(self.frame_conteudo, text="Totais por Forma de Pagamento:", font=("Arial", 10, "underline")).pack()

            for metodo, total in formas_pagamento.items():
                tk.Label(self.frame_conteudo, text=f"{metodo}: R$ {total:.2f}").pack(anchor='w', padx=10)

            mapa_tamanhos = {'13': 'Pequena', '15': 'Média', '18': 'Grande'}
            tk.Label(self.frame_conteudo, text="\nTotal de Marmitas por Tamanho:", font=("Arial", 10, "underline")).pack()

            for tamanho, quantidade in tamanhos_marmita.items():
                descricao = mapa_tamanhos.get(str(tamanho), str(tamanho))
                tk.Label(self.frame_conteudo, text=f"{descricao}: {quantidade}x").pack(anchor='w', padx=10)

            tk.Label(self.frame_conteudo, text=f"\nTotal de Troco: R$ {total_troco:.2f}").pack(anchor='w', padx=10)
            tk.Label(self.frame_conteudo, text=f"Total de Taxa de Entrega: R$ {total_taxa:.2f}").pack(anchor='w', padx=10)

            botao_imprimir = tk.Button(self.frame_conteudo, text="Imprimir Fechamento [i]", command=lambda: self.imprimir_fechamento_caixa(
                total_geral, formas_pagamento, total_troco, total_taxa, tamanhos_marmita, titulo))
            botao_imprimir.pack(pady=10)
            def acionar_imprimir(event=None):
                botao_imprimir.invoke()
            self.fecharCaixa.bind("<Key-i>", acionar_imprimir)

            
        botao_confirmar = tk.Button(self.fecharCaixa, text="Confirmar Data [Enter]", command=obter_data)
        botao_confirmar.pack(pady=5)
        def acionar_confirmar(event=None):
            botao_confirmar.invoke()
        self.fecharCaixa.bind("<Return>", acionar_confirmar)

        botao_sair = tk.Button(self.fecharCaixa, text="Sair [Esc]", command=self.fecharCaixa.destroy)
        botao_sair.pack(pady=10)
        def acionar_sair(event=None):
            botao_sair.invoke()
        self.fecharCaixa.bind("<Escape>", acionar_sair)
        
        self.frame_conteudo = tk.Frame(self.fecharCaixa)
        self.frame_conteudo.pack(fill='both', expand=True)


    def imprimir_fechamento_caixa(self, total_geral, formas_pagamento, total_troco, total_taxa, tamanhos_marmita, hoje):
        mapa_tamanhos = {'13': 'P', '12': 'M', '11': 'G'}  

        try:
            porta = serial.Serial('COM3', baudrate=9600, timeout=1)

            texto = f"""
    *** Bom Apetite ***
    --- Fechamento do Caixa ---
    Data: {hoje}

    Total Geral do Dia: R$ {total_geral:.2f}

    -- Por Forma de Pagamento --
    """
            for metodo, total in formas_pagamento.items():
                texto += f"{metodo}: R$ {total:.2f}\n"

            texto += "\n-- Marmitas por Tamanho --\n"
            for cod, qtd in tamanhos_marmita.items():
                tamanho = mapa_tamanhos.get(str(cod), str(cod))
                texto += f"{tamanho}: {qtd}x\n"

            texto += f"""
    Troco Total: R$ {total_troco:.2f}
    Taxa Total: R$ {total_taxa:.2f}
    ------------------------


    
    """

            porta.write(texto.encode('utf-8'))
            porta.write(b'\n\n\n')  
            porta.close()
            messagebox.showinfo("Sucesso", "Fechamento de caixa enviado para a impressora.")

        except Exception as e:
            messagebox.showerror("Erro na impressão", f"Erro: {e}")




        

        



import tkinter as tk
from tkinter import messagebox,ttk
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
        

################FIM da Classe PRATOS####################################



        #self.quantidade = None
        #self.pagamento = None
        #self.tamanho = None
        #self.prato = None
        #self.complemento = None
        #self.observacao = None 
        #self.valor = None
        #self.troco = None


        #Próximos passos que você pode implementar:
        #Botão de excluir cliente selecionado

        #Edição de cliente (clicar numa linha e abrir para editar)

        #Buscar clientes por nome ou telefone

        #Separar a classe de banco em outro arquivo (DAO)

        #Criar a tabela de pedidos com relação ao cliente

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


################Classe Pedidos####################################

class Pedido:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()

        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                prato TEXT,
                acompanhamento1 TEXT,
                acompanhamento2 TEXT,
                obervacao TEXT,
                tamanho TEXT,
                pagamento TEXT,
                troco REAL,
                taxa_entrega REAL,
                valor_total REAL
            )
        ''')
        self.conexao.commit()

    def abrir_cadastrarPedido(self):
        self.cadastrarPedido = tk.Toplevel()
        self.cadastrarPedido.title('Cadastrar Pedido')
        self.cadastrarPedido.geometry('500x600')

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
        tk.Label(self.cadastrarPedido, text="Prato:").grid(row=4,column=1)
        self.combo_prato = ttk.Combobox(self.cadastrarPedido, values=pratos)
        self.combo_prato.grid(row=4,column=1)

        #Cadastro de acompanhamentos ainda nao foi criado 
        self.cursor.execute("SELECT nome FROM acompanhamentos")
        acompanhamentos1 = [a[0] for a in self.cursor.fetchall()]
        tk.Label(self.cadastrarPedido, text="Acompanhamento 1:").grid(row=5,column=0)
        self.acomp1 = ttk.Combobox(self.cadastrarPedido, values=acompanhamentos1)
        self.acomp1.grid(row=5, column=1)

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
        self.pagamento = tk.Stringvar()
        pagamentos = [("Credito"),("Debito"),("Dinheiro"),("Pix"),("Mumbuca")]
        for i, op in enumerate(pagamentos):
            tk.Radiobutton(self.cadastrarPedido, text=op, variable=self.pagamento, value=op).grid(row=9, column=1)

        tk.Label(self.cadastrarPedido, text="Quantidade de troco:").grid(row=10, column=0)
        self.troco = tk.Entry(self.cadastrarPedido)
        self.troco.grid(row=10, column=1)

        tk.Label(self.cadastrarPedido, text="Taxa de entrega:").grid(row=11, column=0)
        self.taxa = tk.Entry(self.cadastrarPedido)
        self.taxa.grid(row=11, column=1)
        self.taxa.bind("<KeyRealease>", lambda e: self.calcular_valor())

        tk.Label(self.cadastrarPedido, text="Valor Total:").grid(row=12, column=0)
        self.total= tk.StringVar()
        tk.Entry(self.cadastrarPedido, textVariable=self.valor, state="readonly").grid(row=12, column=1)

        tk.Button(self.cadastrarPedido, text="Salvar Pedido", command=self.salvar_Pedido).grid(row=13, column=0)








        

########FIM da Classe Pedidos####################################
     
            
#self.pagamento = None
#self.valor = None
#self.troco = None


#Próximos passos que você pode implementar:
#Botão de excluir cliente selecionado

#Edição de cliente (clicar numa linha e abrir para editar)

#Buscar clientes por nome ou telefone

#Separar a classe de banco em outro arquivo (DAO)

#Criar a tabela de pedidos com relação ao cliente

#Criar funcao para dizer quanto o motoboy tem que me dar no final de cada corrida ou expediente


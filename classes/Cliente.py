import sqlite3
import tkinter as tk
from tkinter import messagebox,ttk
from estilizacao import botao_verde, botao_vermelho, botao_azul


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

        botao_salvar = tk.Button(self.cadastrarCliente, **botao_verde, text="Salvar", command=self.salvar_cliente)
        botao_salvar.grid(row=6, column=0)
        def acionar_salvar(_):
            botao_salvar.invoke()
        self.cadastrarCliente.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarCliente, **botao_vermelho, text="Fechar", command=self.cadastrarCliente.destroy)
        botao_voltar.grid(row = 7, column = 0)
        def acionar_voltar(_):
            botao_voltar.invoke()
        self.cadastrarCliente.bind("<Escape>", acionar_voltar)

    def abrir_gerenciarClientes(self):
        self.gerenciarClientes = tk.Toplevel()
        self.gerenciarClientes.title("Gerenciar Clientes")
        self.gerenciarClientes.focus_force()
        self.gerenciarClientes.geometry('800x500')
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

        botao_editar = tk.Button(self.gerenciarClientes, **botao_verde, text="Editar", command=self.editar_cliente)
        botao_editar.pack(side="left", padx=10, pady=10)
        self.gerenciarClientes.bind("-", lambda e: botao_editar.invoke())

        botao_deletar = tk.Button(self.gerenciarClientes, **botao_vermelho, text="Deletar", command=self.deletar_cliente)
        botao_deletar.pack(side="left", padx=10, pady=10)
        self.gerenciarClientes.bind("<Delete>", lambda e: botao_deletar.invoke())

        botao_sair = tk.Button(self.gerenciarClientes, **botao_azul, text="Sair", command=self.gerenciarClientes.destroy)
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

        botao_salvar = tk.Button(janela_editar, **botao_verde, text="Salvar", command=salvar_edicao)
        botao_salvar.pack(pady=10)
        def acionar_salvar(_):
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

        



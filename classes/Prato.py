import sqlite3
import tkinter as tk
from tkinter import messagebox,ttk
from estilizacao import botao_verde, botao_vermelho, botao_azul

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

        botao_salvar = tk.Button(self.cadastrarPratos, **botao_verde, text="Salvar", command=self.salvar_prato)
        botao_salvar.grid(row=6, column=0)
        def acionar_salvar(_):
            botao_salvar.invoke()
        self.cadastrarPratos.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarPratos, **botao_vermelho, text="Fechar", command=self.cadastrarPratos.destroy)
        botao_voltar.grid(row=7, column=0)
        def acionar_voltar(_):
            botao_voltar.invoke()
        self.cadastrarPratos.bind("<Escape>", acionar_voltar)

    def abrir_gerenciarPratos(self):
        self.gerenciarPratos = tk.Toplevel()
        self.gerenciarPratos.title("Gerenciar Pratos:")
        self.gerenciarPratos.focus_force()
        self.gerenciarPratos.geometry('400x500')
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

        botao_editar = tk.Button(self.gerenciarPratos, **botao_verde, text="Editar", command=self.editar_prato)
        botao_editar.pack(side="left", padx=10, pady=10)
        self.gerenciarPratos.bind("-", lambda e: botao_editar.invoke())

        botao_deletar = tk.Button(self.gerenciarPratos, **botao_vermelho, text="Deletar", command=self.deletar_prato)
        botao_deletar.pack(side="left", padx=10, pady=10)
        self.gerenciarPratos.bind("<Delete>", lambda e: botao_deletar.invoke())

        botao_sair = tk.Button(self.gerenciarPratos, **botao_azul, text="Sair", command=self.gerenciarPratos.destroy)
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

        botao_salvar = tk.Button(janela_editar, **botao_verde, text="Salvar", command=salvar_edicao)
        botao_salvar.pack(pady=10)
        def acionar_salvar(_):
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



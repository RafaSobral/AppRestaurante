import sqlite3
import tkinter as tk
from tkinter import messagebox,ttk
from estilizacao import botao_verde, botao_vermelho, botao_azul

class Bebidas:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

        self.cadastrarBebidas = None
        self.nome = None 
        self.preco = None
        self.gerenciarBebidas = None
        self.tree = None



    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bebidas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                preco REAL
            )
        ''')
        self.conexao.commit()

    def abrir_cadastrarBebidas(self):
        self.cadastrarBebidas = tk.Toplevel()
        self.cadastrarBebidas.title('Cadastrar Bebidas')
        self.cadastrarBebidas.focus_force()
        self.cadastrarBebidas.geometry('190x100')
        self.cadastrarBebidas.iconphoto(False, tk.PhotoImage(file='logo.png'))

        label_nome = tk.Label(self.cadastrarBebidas, text="Nome:")
        label_nome.grid(row=0,column=0)

        self.nome = tk.Entry(self.cadastrarBebidas)
        self.nome.focus_set()
        self.nome.grid(row=0,column=1)

        label_preco = tk.Label(self.cadastrarBebidas, text="Preco:")
        label_preco.grid(row=1,column=0)

        self.preco = tk.Entry(self.cadastrarBebidas)
        self.preco.grid(row=1, column=1)

        botao_salvar = tk.Button(self.cadastrarBebidas, **botao_verde, text="Salvar [Enter]", command=self.salvar_bebida)
        botao_salvar.grid(row=6, column=0)
        def acionar_salvar(_):
            botao_salvar.invoke()
        self.cadastrarBebidas.bind("<Return>", acionar_salvar)
        
        botao_fechar = tk.Button(self.cadastrarBebidas, **botao_vermelho, text="Fechar [Esc]", command=self.cadastrarBebidas.destroy)
        botao_fechar.grid(row=7, column=0)
        def acionar_fechar(_):
            botao_fechar.invoke()
        self.cadastrarBebidas.bind("<Escape>", acionar_fechar)




    def abrir_gerenciarBebidas(self):
        self.gerenciarBebidas = tk.Toplevel()
        self.gerenciarBebidas.title("Gerenciar Bebidas")
        self.gerenciarBebidas.focus_force()
        self.gerenciarBebidas.geometry('400x500')
        self.gerenciarBebidas.iconphoto(False, tk.PhotoImage(file='logo.png'))

        self.tree = ttk.Treeview(self.gerenciarBebidas, columns=("id","nome","preco"), show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", tex="Nome")
        self.tree.heading("preco", text="Preco")

        self.tree.column("id", width=50)
        self.tree.column("nome", width=50)
        self.tree.column("preco", width=50)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cursor.execute("SELECT * FROM bebidas")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

        botao_editar = tk.Button(self.gerenciarBebidas, **botao_verde, text="Editar [E]", command=self.editar_bebida)
        botao_editar.pack(side="left", padx=10, pady=10)
        self.gerenciarBebidas.bind("<Key-e>", lambda e: botao_editar.invoke())

        botao_deletar = tk.Button(self.gerenciarBebidas, **botao_vermelho, text="Deletar [Del]", command=self.deletar_bebida)
        botao_deletar.pack(side="left", padx=10, pady=10)
        self.gerenciarBebidas.bind("<Delete>", lambda e: botao_deletar.invoke())

        botao_fechar = tk.Button(self.gerenciarBebidas, **botao_azul, text="Fechar [Esc]", command=self.gerenciarBebidas.destroy)
        botao_fechar.pack(side="left", padx=10, pady=10)
        self.gerenciarBebidas.bind("<Escape>", lambda e: botao_fechar.invoke())

    def salvar_bebida(self):
        nome = self.nome.get()
        preco = self.preco.get()

        if nome == "":
            messagebox.showerror("Erro", "O nome nao pode estar vazio")
            return

        self.cursor.execute('''
            INSERT INTO bebidas (nome, preco) 
            VALUES(?,?)
        ''',(nome,preco))
        self.conexao.commit()

        messagebox.showinfo("Sucesso", "Bebida cadastrada!")
        self.cadastrarBebidas.destroy()


    def editar_bebida(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione uma bebida para editar")
            return

        bebida_id, nome_antigo, preco_antigo = self.tree.item(selected[0], "values")
        janela_editar = tk.Toplevel()
        janela_editar.focus_force()
        janela_editar.title("Editar Bebidas")
        janela_editar.iconphoto(False, tk.PhotoImage(file='logo.png'))

        tk.Label(janela_editar, text="Nome:").pack()
        nome_entry = tk.Entry(janela_editar)
        nome_entry.insert(0, nome_antigo)
        nome_entry.pack()

        tk.Label(janela_editar, text="Preco").pack()
        preco_entry = tk.Entry(janela_editar)
        preco_entry.insert(0, preco_antigo)
        preco_entry.pack()

        def salvar_edicao():
            novo_nome = nome_entry.get()
            novo_preco = preco_entry.get()

            self.cursor.execute("UPDATE bebidas SET nome=?, preco=? WHERE id=?", (novo_nome, novo_preco, bebida_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Bebida atualizada com sucesso")
            janela_editar.destroy()
            self.gerenciarBebidas.destroy()
            self.abrir_gerenciarBebidas()

        botao_salvar = tk.Button(janela_editar, **botao_verde, text="Salvar [Enter]", command=salvar_edicao)
        botao_salvar.pack(pady=10)
        def acionar_salvar(_):
            botao_salvar.invoke()
        janela_editar.bind("<Return>", acionar_salvar)


    def deletar_bebida(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso","Selecione uma bebida para editar")
            return
        
        bebida_id = self.tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("Confirmar","Tem certeza que deseja deletar essa bebida?")
        if confirm:
            self.cursor.execute("DELETE FROM bebidas WHERE id=?", (bebida_id,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Bebida deletada com sucesso!")
            self.tree.delete(selected[0])
            self.gerenciarBebidas.destroy()
            self.abrir_gerenciarBebidas()

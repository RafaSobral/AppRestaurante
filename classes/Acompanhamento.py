import tkinter as tk
import sqlite3
from tkinter import messagebox,ttk

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
        def acionar_salvar(_):
            botao_Salvar.invoke()
        self.cadastrarAcomp.bind("<Return>", acionar_salvar)

        botao_voltar = tk.Button(self.cadastrarAcomp, text="Fechar [Escape]", command=self.cadastrarAcomp.destroy)
        botao_voltar.grid(row = 2, column = 0)
        def acionar_voltar(_):
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
        def acionar_salvar(_):
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


import sqlite3
import tkinter as tk
from tkinter import messagebox,ttk

class Bebidas:
    def __init__(self):
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

        self.cadastrarBebidas = None
        self.nome = None 
        self.preco = None



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

        label_nome = tk.Label(self.cadastrarBebidas, text="Nome:")
        label_nome.grid(row=0,column=0)

        self.nome = tk.Entry(self.cadastrarBebidas)
        self.nome.focus_set()
        self.nome.grid(row=0,column=1)

        label_preco = tk.Label(self.cadastrarBebidas, text="Preco:")
        label_preco.grid(row=1,column=0)

        self.preco = tk.Entry(self.cadastrarBebidas)
        self.preco.grid(row=1, column=1)

        botao_salvar = tk.Button(self.cadastrarBebidas, text="Salvar [Enter]", command=self.salvar_bebida)
        botao_salvar.grid(row=6, column=0)
        def acionar_salvar(_):
            botao_salvar.invoke()
        self.cadastrarBebidas.bind("<Return>", acionar_salvar)
        
        botao_fechar = tk.Button(self.cadastrarBebidas, text="Fechar [Esc]", command=self.cadastrarBebidas.destroy)
        botao_fechar.grid(row=7, column=0)
        def acionar_fechar(_):
            botao_fechar.invoke()
        self.cadastrarBebidas.bind("<Escape>", acionar_fechar)




    def abrir_gerenciarBebidas(self):
        pass

    
    def salvar_bebida(self):
        pass


    def editar_bebida(self):
        pass


    def deletar_bebida(self):
        pass
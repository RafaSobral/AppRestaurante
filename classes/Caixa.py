import locale
import sqlite3
import serial
import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import messagebox
from estilizacao import botao_verde, botao_vermelho, botao_azul

class Caixa:
    def __init__(self):
        self.fecharCaixa = None
        self.conexao = sqlite3.connect('bomapetite.db')
        self.cursor = self.conexao.cursor()
        self.frame_conteudo = None


    def abrir_fecharCaixa(self):
        self.fecharCaixa = tk.Toplevel()
        self.fecharCaixa.focus_force()
        self.fecharCaixa.geometry("400x700")
        self.fecharCaixa.title("Fechar o Caixa")
        self.fecharCaixa.iconphoto(False, tk.PhotoImage(file='logo.png'))

        tk.Label(self.fecharCaixa, text="Para gerar o relatorio mensal, Selecione o mes e coloque o dia como 00.", bg="green", fg="white", relief="sunken", borderwidth=3, padx=10, pady=5).pack(pady=6)
        
        date_entry = DateEntry(self.fecharCaixa, width=12, background='darkblue',
                            foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        date_entry.pack(pady=10)

        def obter_data():
            try:
                locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  
            except:
                locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')  

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            data_str = date_entry.get()
            dia, mes, ano = data_str.split('/')
            hoje = datetime.now().strftime("%d-%m-%Y")
            data_selecionada = f"{dia}-{mes}-{ano}"

            if dia == '00' or dia == '0':
                data_like = f"-{mes}-{ano}"
                self.cursor.execute("SELECT pagamento, total, tamanho, bebida, troco, taxa FROM pedidos WHERE data_hoje LIKE ?", (f"%{data_like}",))
                nome_mes = datetime.strptime(mes, "%m").strftime('%B')
                titulo = f"Fechamento de {nome_mes.capitalize()}/{ano}"
                label_total = f"Total do mês de {nome_mes.capitalize()}:"
            elif data_selecionada == hoje:
                self.cursor.execute("SELECT pagamento, total, tamanho, bebida, troco, taxa FROM pedidos WHERE data_hoje = ?", (data_selecionada,))
                titulo = "Fechamento de Hoje"
                label_total = "Total de Hoje:"
            else:
                self.cursor.execute("SELECT pagamento, total, tamanho, bebida, troco, taxa FROM pedidos WHERE data_hoje = ?", (data_selecionada,))
                titulo = f"Fechamento do Dia {data_selecionada}"
                label_total = f"Total do Dia {data_selecionada}:"

            pedidos = self.cursor.fetchall()

            total_geral = 0
            total_troco = 0
            total_taxa = 0
            formas_pagamento = {}
            tamanhos_marmita = {}
            bebidas_vendidas = {}

            for pagamento, valor, tamanho, bebida, troco, taxa in pedidos:
                total_geral += valor
                total_troco += troco
                total_taxa += taxa

                formas_pagamento[pagamento] = formas_pagamento.get(pagamento, 0) + valor
                tamanhos_marmita[tamanho] = tamanhos_marmita.get(tamanho, 0) + 1

                if bebida and bebida.strip():
                    bebidas = [b.strip() for b in bebida.split(',')] 
                    for b in bebidas:
                        bebidas_vendidas[b] = bebidas_vendidas.get(b, 0) + 1

            self.fecharCaixa.title(titulo)

            tk.Label(self.frame_conteudo, text=f"{label_total} R$ {total_geral:.2f}", font=("Arial", 12, "bold"), bg="green", fg="white", relief="sunken", borderwidth=3, padx=10, pady=5).pack(pady=5)
            tk.Label(self.frame_conteudo, text="Totais por Forma de Pagamento:", font=("Arial", 10, "bold"), bg="green", fg="white", relief="sunken", borderwidth=3, padx=23).pack()

            for metodo, total in formas_pagamento.items():
                tk.Label(self.frame_conteudo, text=f"{metodo}: R$ {total:.2f}", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=80).pack()

            mapa_tamanhos = {'13': 'Pequena', '15': 'Média', '18': 'Grande'}
            tk.Label(self.frame_conteudo, text="\nTotal de Marmitas por Tamanho:", font=("Arial", 10, "bold"), bg="green", fg="white", relief="sunken", borderwidth=3, padx=23).pack()

            for tamanho, quantidade in tamanhos_marmita.items():
                descricao = mapa_tamanhos.get(str(tamanho), str(tamanho))
                tk.Label(self.frame_conteudo, text=f"{descricao}: {quantidade}x", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=94).pack()

            if bebidas_vendidas:
                tk.Label(self.frame_conteudo, text="\nBebidas Vendidas:", font=("Arial", 10, "bold"), bg="green", fg="white", relief="sunken", borderwidth=3, padx=66).pack()
                for bebida, qtd in bebidas_vendidas.items():
                    tk.Label(self.frame_conteudo, text=f"{bebida}: {qtd}x", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=69).pack()


            tk.Label(self.frame_conteudo, text=f"\nTotal de Troco: R$ {total_troco:.2f}", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack()
            tk.Label(self.frame_conteudo, text=f"Total de Taxa de Entrega: R$ {total_taxa:.2f}", bg="blue", fg="white", relief="sunken", borderwidth=3, padx=10).pack()

            botao_imprimir = tk.Button(self.frame_conteudo, **botao_azul, text="Imprimir Fechamento", command=lambda: self.imprimir_fechamento_caixa(
                total_geral, formas_pagamento, total_troco, total_taxa, tamanhos_marmita, titulo,  bebidas_vendidas))
            botao_imprimir.pack(pady=10)
            def acionar_imprimir(event=None):
                botao_imprimir.invoke()
            self.fecharCaixa.bind("-", acionar_imprimir)


        botao_confirmar = tk.Button(self.fecharCaixa, **botao_verde, text="Confirmar Data", command=obter_data)
        botao_confirmar.pack(pady=5)
        def acionar_confirmar(event=None):
            botao_confirmar.invoke()
        self.fecharCaixa.bind("<Return>", acionar_confirmar)

        botao_sair = tk.Button(self.fecharCaixa, **botao_vermelho, text="Sair", command=self.fecharCaixa.destroy)
        botao_sair.pack(pady=10)
        def acionar_sair(event=None):
            botao_sair.invoke()
        self.fecharCaixa.bind("<Escape>", acionar_sair)
        
        self.frame_conteudo = tk.Frame(self.fecharCaixa)
        self.frame_conteudo.pack(fill='both', expand=True)


    def imprimir_fechamento_caixa(self, total_geral, formas_pagamento, total_troco, total_taxa, tamanhos_marmita, hoje, bebidas_vendidas):
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

            if bebidas_vendidas:
                texto += "\n-- Bebidas Vendidas --\n"
                for bebida, qtd in bebidas_vendidas.items():
                    texto += f"{bebida}: {qtd}x\n"


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




        

        



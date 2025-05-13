import tkinter as tk
from tkinter import messagebox
import serial

def imprimir_pedido_daruma(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para imprimir.")
        return

    valores = tree.item(selected[0], "values")
    if len(valores) < 14:
        messagebox.showerror("Erro", "Dados do pedido incompletos.")
        return

    pedido = {
        "pedido_id": valores[1],
        "nome_cliente": valores[2],
        "prato": valores[3],
        "acomp1": valores[4],
        "acomp2": valores[5],
        "observacao": valores[6],
        "tamanho": valores[7],
        "bebida": valores[8],
        "pagamento": valores[9],
        "troco": valores[10],
        "taxa": valores[11],
        "total": valores[12],
        "data_hoje": valores[13]
    }

    try:
        porta = serial.Serial('COM3', baudrate=9600, timeout=1)
        texto = f"""
*** Bom Apetite ***
------------------------
Pedido ID: {pedido['pedido_id']}
Nome Cliente: {pedido['nome_cliente']}
Prato: {pedido['prato']}
Acomp1: {pedido['acomp1']}
Acomp2: {pedido['acomp2']}
Obs: {pedido['observacao']}
Tamanho: {pedido['tamanho']}
Bebida: {pedido['bebida']}
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


def editar_pedido(tree, cursor, conn):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para editar")
        return

    valores = tree.item(selected[0], "values")
    id_real = valores[0]

    _, _, _, prato_antigo, acomp1_antigo, acomp2_antigo, observacao_antiga, tamanho_antigo, bebida_antiga, pagamento_antigo, troco_antigo, taxa_antiga, total_antigo, _ = valores

    janela_editar = tk.Toplevel()
    janela_editar.title('Editar Pedido')
    janela_editar.focus_force()

    campos = {
        "Prato": prato_antigo,
        "Acomp1": acomp1_antigo,
        "Acomp2": acomp2_antigo,
        "Observacao": observacao_antiga,
        "Tamanho": tamanho_antigo,
        "Bebida": bebida_antiga,
        "Pagamento": pagamento_antigo,
        "Troco": troco_antigo,
        "Taxa": taxa_antiga,
        "Total": total_antigo
    }

    entradas = {}

    for label, valor in campos.items():
        tk.Label(janela_editar, text=label).pack()
        entrada = tk.Entry(janela_editar)
        entrada.insert(0, valor)
        entrada.pack()
        entradas[label] = entrada

    def salvar_edicao():
        novos_valores = [entradas[campo].get() for campo in campos]

        cursor.execute("""
            UPDATE pedidos SET prato=?, acompanhamento1=?, acompanhamento2=?, observacao=?,
            tamanho=?,bebida=? pagamento=?, troco=?, taxa=?, total=? WHERE id=?
        """, (*novos_valores, id_real))
        conn.commit()
        messagebox.showinfo("Sucesso", "Pedido atualizado com sucesso")
        janela_editar.destroy()
        carregar_pedidos(tree, cursor)

    botao_salvar = tk.Button(janela_editar, text="Salvar [Enter]", command=salvar_edicao)
    botao_salvar.pack(pady=10)
    janela_editar.bind("<Return>", lambda event=None: botao_salvar.invoke())


def deletar_pedido(tree,cursor,conn):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um pedido para deletar")
        return

    id_real = tree.item(selected[0], "values")[0]

    confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse Pedido?")
    if confirm:
        cursor.execute("DELETE FROM pedidos WHERE id=?", (id_real,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Pedido deletado com sucesso")
        tree.delete(selected[0])


def carregar_pedidos(tree, cursor):
    for i in tree.get_children():
        tree.delete(i)
    
    cursor.execute("""
        SELECT id, pedido_id, nome_cliente, prato, acompanhamento1, acompanhamento2,
               observacao, tamanho, bebida, pagamento, troco, taxa, total, data_hoje 
        FROM pedidos
    """)
    
    for row in cursor.fetchall():
        row = list(row)
        tamanho_map = {13: 'P', 15: 'M', 18: 'G'}
        try:
            valor = int(row[7])
            row[7] = tamanho_map.get(valor, row[7])
        except (ValueError, TypeError):
            pass
        
        tree.insert("", "end", values=row)
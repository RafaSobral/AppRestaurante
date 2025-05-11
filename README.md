# 📋 Documentação:

## 📌 Visão Geral

Esta é uma aplicação desktop desenvolvida em Python, com uma interface gráfica intuitiva voltada para a gestão de delivery de marmitas.
O principal foco é a *agilidade no cadastro de pedidos*, por isso foi pensada para ser utilizada *apenas com o teclado*.
O sistema permite:
- Cadastro de Clientes, Pratos, Acompanhamentos e Pedidos.
- Gerenciamento (Editar ou Remover) clientes, pratos, acompanhamentos e pedidos.
- Fechamento de caixa com opção de imprimir o fechamento de um dia selecionado ou do mês.
- Impressão automática do pedido após o cadastro.
- Re-impressão de pedidos
Ideal para pequenos estabelecimentos que buscam uma solução simples, rápida e funcional.

## 🧰 Tecnologias Utilizadas

### 🐍 Linguagem:

* **Python 3.x** – Linguagem principal da aplicação.

### 📦 Bibliotecas e Dependências:

| Biblioteca          | Versão       | Descrição                                                                                                                                                   |
| ------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tkinter`           | Embutido     | Biblioteca padrão do Python para criação da interface gráfica (GUI).                                                                                        |
| `Pillow`            | mais recente | Utilizada para carregamento e manipulação de imagens, como logotipos e ícones.                                                                              |
| `tkcalendar==1.6.1` | 1.6.1        | Fornece widgets de calendário no Tkinter, útil para seleção de datas em pedidos ou reservas.                                                                |
| `babel==2.17.0`     | 2.17.0       | Suporte à localização e formatação de datas, números e moedas em diferentes idiomas.                                                                        |                                              |
| `serial==0.0.97`    | 0.0.97       | Apesar do nome genérico, pode se referir ao `pyserial`, utilizado para comunicação com portas seriais (ex: integração com balanças ou impressoras fiscais). |

> **Observação:** a biblioteca `serial` costuma causar confusão; caso seja usada para comunicação com dispositivos externos, verifique se a intenção é realmente `pyserial`.

## 📁 Estrutura do Projeto

```
AppRestaurante/
├── anotacoes.txt        # Notas e ideias de desenvolvimento
├── bomapetite.db        # Banco de dados local SQLite
├── classes.py           # Lógica das classes principais do sistema (pedidos, clientes etc.)
├── logo.ico             # Ícone do app para exibição na janela
├── logo.png             # Imagem do logotipo do restaurante
└── main.py              # Ponto de entrada do sistema
```

## 🚀 Como Executar o Projeto

### 1. Clone o repositório:

```bash
git clone https://github.com/RafaSobral/AppRestaurante.git
cd AppRestaurante
```

### 2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação:

```bash
python main.py
```

## 🧠 Funcionalidades Principais

* Registro de pedidos com cálculo automático de total
* Cadastro de clientes e histórico de compras
* Escolha de pratos, acompanhamentos, tamanhos e observações
* Suporte a taxa de entrega, formas de pagamento e troco
* Interface gráfica simples e intuitiva com widgets personalizados

## 📌 Sugestões de Melhorias Futuras

* Opção de cadastro de bebidas (Em breve)
* Imprimir duas comandas ao cadastrar o pedido (Cozinha e Motoboy)
* Relatórios financeiros e estatísticas em gráfico com matplotlib
* Interface responsiva para diferentes tamanhos de tela
* Modernizar a interface gráfica
* Salvar banco na nuvem

## 🤝 Contribuições

Você pode contribuir com o projeto seguindo os passos abaixo:

1. Faça um fork
2. Crie uma nova branch: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m 'Minha contribuição'`
4. Faça push para o seu fork: `git push origin minha-feature`
5. Crie um Pull Request!


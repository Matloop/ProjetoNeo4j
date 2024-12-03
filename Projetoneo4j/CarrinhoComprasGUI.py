import tkinter as tk
from tkinter import messagebox, ttk
from Main import GerenciadorCarrinhoCompras

class CarrinhoComprasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Carrinho de Compras")
        self.gerenciador = GerenciadorCarrinhoCompras()
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        # Aba Criar Usuário
        self.frame_usuario = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_usuario, text="Criar Usuário")
        self.criar_aba_usuario()
        
        # Aba Criar Produto
        self.frame_produto = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_produto, text="Criar Produto")
        self.criar_aba_produto()
        
        # Aba Adicionar ao Carrinho
        self.frame_carrinho = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_carrinho, text="Adicionar ao Carrinho")
        self.criar_aba_carrinho()

    def criar_aba_usuario(self):
        # Labels e Entries para Usuário
        ttk.Label(self.frame_usuario, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_usuario = ttk.Entry(self.frame_usuario)
        self.nome_usuario.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_usuario, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_usuario = ttk.Entry(self.frame_usuario)
        self.email_usuario.grid(row=1, column=1, padx=5, pady=5)
        
        # Botão Criar Usuário
        ttk.Button(self.frame_usuario, text="Criar Usuário", 
                  command=self.criar_usuario).grid(row=2, column=0, columnspan=2, pady=10)

    def criar_aba_produto(self):
        # Labels e Entries para Produto
        ttk.Label(self.frame_produto, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_produto = ttk.Entry(self.frame_produto)
        self.nome_produto.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_produto, text="Preço:").grid(row=1, column=0, padx=5, pady=5)
        self.preco_produto = ttk.Entry(self.frame_produto)
        self.preco_produto.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_produto, text="Estoque:").grid(row=2, column=0, padx=5, pady=5)
        self.estoque_produto = ttk.Entry(self.frame_produto)
        self.estoque_produto.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão Criar Produto
        ttk.Button(self.frame_produto, text="Criar Produto", 
                  command=self.criar_produto).grid(row=3, column=0, columnspan=2, pady=10)

    def criar_aba_carrinho(self):
        # Labels e Entries para Carrinho
        ttk.Label(self.frame_carrinho, text="Email do Usuário:").grid(row=0, column=0, padx=5, pady=5)
        self.email_carrinho = ttk.Entry(self.frame_carrinho)
        self.email_carrinho.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_carrinho, text="Nome do Produto:").grid(row=1, column=0, padx=5, pady=5)
        self.produto_carrinho = ttk.Entry(self.frame_carrinho)
        self.produto_carrinho.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_carrinho, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5)
        self.quantidade_carrinho = ttk.Entry(self.frame_carrinho)
        self.quantidade_carrinho.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão Adicionar ao Carrinho
        ttk.Button(self.frame_carrinho, text="Adicionar ao Carrinho", 
                  command=self.adicionar_carrinho).grid(row=3, column=0, columnspan=2, pady=10)

    def criar_usuario(self):
        try:
            nome = self.nome_usuario.get()
            email = self.email_usuario.get()
            
            if not nome or not email:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
                return
                
            self.gerenciador.criar_usuario(nome, email)
            messagebox.showinfo("Sucesso", f"Usuário {nome} criado com sucesso!")
            
            # Limpar campos
            self.nome_usuario.delete(0, tk.END)
            self.email_usuario.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {str(e)}")

    def criar_produto(self):
        try:
            nome = self.nome_produto.get()
            preco = float(self.preco_produto.get())
            estoque = int(self.estoque_produto.get())
            
            if not nome or not preco or not estoque:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
                return
                
            self.gerenciador.criar_produto(nome, preco, estoque)
            messagebox.showinfo("Sucesso", f"Produto {nome} criado com sucesso!")
            
            # Limpar campos
            self.nome_produto.delete(0, tk.END)
            self.preco_produto.delete(0, tk.END)
            self.estoque_produto.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar produto: {str(e)}")

    def adicionar_carrinho(self):
        try:
            email = self.email_carrinho.get()
            produto = self.produto_carrinho.get()
            quantidade = int(self.quantidade_carrinho.get())
            
            if not email or not produto or not quantidade:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
                return
                
            total = self.gerenciador.adicionar_ao_carrinho(email, produto, quantidade)
            messagebox.showinfo("Sucesso", 
                              f"Produto adicionado ao carrinho!\nTotal do carrinho: R$ {total:.2f}")
            
            # Limpar campos
            self.email_carrinho.delete(0, tk.END)
            self.produto_carrinho.delete(0, tk.END)
            self.quantidade_carrinho.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar ao carrinho: {str(e)}")

    def __del__(self):
        if hasattr(self, 'gerenciador'):
            self.gerenciador.fechar()

def main():
    root = tk.Tk()
    app = CarrinhoComprasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import logging
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GerenciadorCarrinhoCompras:
    def __init__(self, 
                 uri: str = "neo4j+s://d33ff794.databases.neo4j.io", 
                 usuario: str = "neo4j", 
                 senha: str = "4DgD1IeubygXSagFAh9a5pH_-AgyOgMvo1mIhzx9zBk"):
        """
        Inicializa a conexão com o banco de dados Neo4j
        
        :param uri: URI de conexão com o Neo4j (padrão: URI do Neo4j Aura)
        :param usuario: Nome de usuário para a conexão (padrão: "neo4j")
        :param senha: Senha para a conexão
        """
        self._uri = uri
        self._usuario = usuario
        self._senha = senha

        # Validação dos parâmetros de conexão
        if not all([self._uri, self._usuario, self._senha]):
            raise ValueError(
                "Detalhes da conexão com o Neo4j estão faltando. "
                "Por favor, forneça-os diretamente ou configure variáveis de ambiente."
            )

        try:
            # Inicializa o driver de conexão
            self._driver = GraphDatabase.driver(
                self._uri, 
                auth=(self._usuario, self._senha)
            )

            # Verifica a conectividade
            with self._driver.session() as session:
                session.run("RETURN 1")
            logger.info("Conectado com sucesso ao Neo4j!")

        except (Neo4jError) as e:
            logger.error(f"Erro de conexão: {type(e).__name__} - {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao conectar ao Neo4j: {e}")
            raise

    def fechar(self):
        """
        Fecha a conexão com o banco de dados
        """
        if self._driver:
            self._driver.close()
            logger.info("Conexão com o Neo4j fechada.")

    def criar_usuario(self, nome: str, email: str):
        """
        Cria um novo usuário
        
        :param nome: Nome do usuário
        :param email: Email do usuário
        """
        with self._driver.session() as session:
            try:
                session.run(
                    "MERGE (u:Usuario {email: $email}) "
                    "SET u.nome = $nome "
                    "RETURN u.email AS email, u.nome AS nome",
                    nome=nome, email=email
                )
                logger.info(f"Usuário {nome} criado com sucesso.")
            except Neo4jError as e:
                logger.error(f"Erro ao criar usuário {nome}: {e}")

    def criar_produto(self, nome: str, preco: float, estoque: int):
        """
        Cria um novo produto
        
        :param nome: Nome do produto
        :param preco: Preço do produto
        :param estoque: Quantidade em estoque do produto
        """
        with self._driver.session() as session:
            try:
                session.run(
                    "MERGE (p:Produto {nome: $nome}) "
                    "SET p.preco = $preco, p.estoque = $estoque "
                    "RETURN p.nome AS nome, p.preco AS preco, p.estoque AS estoque",
                    nome=nome, preco=preco, estoque=estoque
                )
                logger.info(f"Produto {nome} criado com sucesso.")
            except Neo4jError as e:
                logger.error(f"Erro ao criar produto {nome}: {e}")

    def criar_carrinho(self, email_usuario: str):
        """
        Cria um novo carrinho de compras para um usuário
        
        :param email_usuario: Email do usuário
        """
        with self._driver.session() as session:
            try:
                session.run(
                    "MERGE (u:Usuario {email: $email_usuario}) "
                    "MERGE (c:Carrinho {usuario_email: $email_usuario}) "
                    "SET c.total = 0 "
                    "RETURN c.usuario_email AS usuario_email, c.total AS total",
                    email_usuario=email_usuario
                )
                logger.info(f"Carrinho de compras criado para {email_usuario}.")
            except Neo4jError as e:
                logger.error(f"Erro ao criar carrinho para {email_usuario}: {e}")

    def adicionar_ao_carrinho(self, email_usuario: str, nome_produto: str, quantidade: int):
        """
        Adiciona um produto ao carrinho de compras do usuário
        
        :param email_usuario: Email do usuário
        :param nome_produto: Nome do produto
        :param quantidade: Quantidade do produto
        """
        with self._driver.session() as session:
            try:
                session.run(
                    "MATCH (u:Usuario {email: $email_usuario}) "
                    "MATCH (p:Produto {nome: $nome_produto}) "
                    "MATCH (c:Carrinho {usuario_email: $email_usuario}) "
                    "MERGE (c)-[r:CONTEM]->(p) "
                    "SET r.quantidade = COALESCE(r.quantidade, 0) + $quantidade "
                    "SET c.total = c.total + (p.preco * $quantidade) "
                    "RETURN p.nome AS nome_produto, r.quantidade AS quantidade, c.total AS total",
                    email_usuario=email_usuario, nome_produto=nome_produto, quantidade=quantidade
                )
                logger.info(f"{quantidade} {nome_produto}(s) adicionados ao carrinho de {email_usuario}.")
            except Neo4jError as e:
                logger.error(f"Erro ao adicionar produto {nome_produto} ao carrinho de {email_usuario}: {e}")

    def obter_conteudo_carrinho(self, email_usuario: str):
        """
        Obtém o conteúdo do carrinho de compras de um usuário
        
        :param email_usuario: Email do usuário
        """
        with self._driver.session() as session:
            try:
                result = session.run(
                    "MATCH (u:Usuario {email: $email_usuario})-[:POSUI]->(c:Carrinho) "
                    "MATCH (c)-[r:CONTEM]->(p:Produto) "
                    "RETURN p.nome AS nome_produto, r.quantidade AS quantidade, p.preco AS preco, "
                    "r.quantidade * p.preco AS total_produto",
                    email_usuario=email_usuario
                )
                return [{"nome_produto": record["nome_produto"], "quantidade": record["quantidade"], 
                         "preco": record["preco"], "total_produto": record["total_produto"]} 
                        for record in result]
            except Neo4jError as e:
                logger.error(f"Erro ao obter conteúdo do carrinho de {email_usuario}: {e}")
                return []

    def obter_total_carrinho(self, email_usuario: str):
        """
        Obtém o total do carrinho de compras de um usuário
        
        :param email_usuario: Email do usuário
        """
        with self._driver.session() as session:
            try:
                result = session.run(
                    "MATCH (u:Usuario {email: $email_usuario})-[:POSUI]->(c:Carrinho) "
                    "RETURN c.total AS total",
                    email_usuario=email_usuario
                )
                return result.single()["total"] if result.single() else 0
            except Neo4jError as e:
                logger.error(f"Erro ao obter total do carrinho de {email_usuario}: {e}")
                return 0

def main():
    """
    Exemplo de uso e demonstração do GerenciadorCarrinhoCompras
    """
    gerenciador_carrinho = None
    try:
        # Inicializa o gerenciador de carrinho com as credenciais definidas
        
        gerenciador_carrinho = GerenciadorCarrinhoCompras()

        

        # Adiciona itens ao carrinho
        gerenciador_carrinho.adicionar_ao_carrinho("joao@exemplo.com", "Laptop", 1)
        gerenciador_carrinho.adicionar_ao_carrinho("maria@exemplo.com", "Fone de Ouvido", 65)

        # Exibe conteúdo do carrinho
        print("Carrinho João:", gerenciador_carrinho.obter_conteudo_carrinho("joao@exemplo.com"))
        print("Carrinho Maria:", gerenciador_carrinho.obter_conteudo_carrinho("maria@exemplo.com"))

        # Exibe total do carrinho
        print("Total João:", gerenciador_carrinho.obter_total_carrinho("joao@exemplo.com"))
        print("Total Maria:", gerenciador_carrinho.obter_total_carrinho("maria@exemplo.com"))

    finally:
        if gerenciador_carrinho:
            gerenciador_carrinho.fechar()

if __name__ == "__main__":
    main()

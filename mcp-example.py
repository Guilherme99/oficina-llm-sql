import json
from langchain_ollama import ChatOllama
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# --- 1. LLM usando Ollama ---
class OllamaSQLGenerator:
    def __init__(self, model="duckdb-nsql:7b", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)

    def generate_sql(self, question: str) -> str:
        prompt = f"""
Você é um especialista gerador de SQL.
Com base no esquema de banco de dados: CREATE TABLE public.queimadas (
	"year" int4 NULL,
	state varchar(50) NULL,
	"month" varchar(50) NULL,
	"number" int4 NULL,
	"date" varchar(50) NULL
);

Gere uma consulta SQL válida baseada na pergunta:

Pergunta: "{question}"

RETORNE APENAS O SQL PURO. SEM TEXTOS ACRESCENTES.
"""
        response = self.llm.invoke(prompt)
        return response.content.strip()


# --- 2. Executor SQL com SQLAlchemy ---
class SQLAlchemyExecutor:
    def __init__(self, database_url: str):
        """
        database_url exemplos:
        - SQLite: "sqlite:///seu_banco.db"
        - PostgreSQL: "postgresql://user:password@localhost:5432/database"
        - MySQL: "mysql+pymysql://user:password@localhost:3306/database"
        """
        self.engine = create_engine(database_url)

    def query(self, sql: str):
        """Executa a query SQL e retorna os resultados"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql))
                
                # Se for SELECT, retorna os dados
                if sql.strip().upper().startswith("SELECT"):
                    # Pega os nomes das colunas
                    columns = list(result.keys())
                    
                    # Converte as linhas para lista de dicionários
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    
                    return {
                        "success": True,
                        "columns": columns,
                        "rows": rows,
                        "count": len(rows)
                    }
                else:
                    # Para INSERT/UPDATE/DELETE
                    connection.commit()
                    return {
                        "success": True,
                        "affected_rows": result.rowcount
                    }
                    
        except SQLAlchemyError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }


# --- 3. Loop interativo ---
def main():
    print("🚀 Sistema NL → SQL iniciado!")
    
    # Configure a URL do seu banco de dados aqui
    DATABASE_URL = "postgresql://postgres:adm123@localhost:5432/oficina-db"  # ← Altere conforme necessário
    
    sql_generator = OllamaSQLGenerator()
    executor = SQLAlchemyExecutor(DATABASE_URL)

    while True:
        try:
            question = input("\nPergunta (EN): ")
            
            # Gera o SQL usando Ollama
            sql = sql_generator.generate_sql(question)
            print("\n📘 SQL gerado:\n", sql)

            # Executa no banco via SQLAlchemy
            result = executor.query(sql)
            print("\n📊 Resultado:\n", json.dumps(result, indent=2, ensure_ascii=False))

        except KeyboardInterrupt:
            print("\n\nSaindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
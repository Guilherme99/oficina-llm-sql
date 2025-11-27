import json
from langchain_ollama import ChatOllama
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

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



class SQLAlchemyExecutor:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)

    def convert_value(self, value):
        if isinstance(value, Decimal):
            return float(value)
        return value

    def query(self, sql: str):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql))

                if sql.strip().upper().startswith("SELECT"):
                    columns = list(result.keys())

                    rows = [
                        {col: self.convert_value(val) for col, val in zip(columns, row)}
                        for row in result.fetchall()
                    ]

                    return {
                        "success": True,
                        "columns": columns,
                        "rows": rows,
                        "count": len(rows)
                    }

                else:
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
            question = input("\nPergunta (EN/PT): ")
            
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
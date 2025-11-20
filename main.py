import json
import requests
from langchain_ollama import ChatOllama

# --- 1. LLM usando Ollama ---
class OllamaSQLGenerator:
    def __init__(self, model="llama2", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)

    def generate_sql(self, question: str) -> str:
        prompt = f"""
Você é um gerador de SQL.
Gere uma consulta SQL válida baseada na pergunta:

Pergunta: "{question}"

Apenas SQL puro.
"""
        response = self.llm.invoke(prompt)
        return response.content.strip()


# --- 2. Cliente HTTP para MCP Server ---
class MCPClientHTTP:
    def __init__(self, base_url="http://localhost:3000/mcp"):
        self.base_url = base_url.rstrip("/")

    def query(self, sql: str):
        payload = {"method": "query", "params": {"query": sql}}
        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

# --- 3. Loop interativo ---
def main():
    print("🚀 Sistema NL → SQL iniciado!")
    sql_generator = OllamaSQLGenerator()
    mcp = MCPClientHTTP()

    while True:
        try:
            question = input("\nPergunta (PT-BR): ")
            sql = sql_generator.generate_sql(question)
            print("\n📘 SQL gerado:\n", sql)

            result = mcp.query(sql)
            print("\n📊 Resultado:\n", json.dumps(result, indent=2))

        except KeyboardInterrupt:
            print("\nSaindo...")
            break
        except Exception as e:
            print("❌ Erro:", e)


if __name__ == "__main__":
    main()

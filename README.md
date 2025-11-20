# 📘 Projeto – Ambiente com Docker, PostgreSQL, Ollama e Python

Este projeto utiliza **Docker**, **PostgreSQL**, **Ollama** e **Python** como base para desenvolvimento e testes.
Siga este guia para instalar tudo o que precisa e iniciar o ambiente rapidamente.

---

## ✅ 1. Pré-requisitos

Antes de rodar o ambiente, instale as ferramentas abaixo.

---

## 🐳 2. Instalar o Docker

### **Windows**

1. Acesse: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Baixe e instale o **Docker Desktop**
3. Após instalado, abra o Docker Desktop e verifique se está rodando.

---

## 🐍 3. Instalar Python

Baixe o Python 3.10+ no site oficial:

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## 🛢️ 4. Instalar o DBeaver

Baixe a versão Community no site oficial:

🔗 [https://dbeaver.io/download/](https://dbeaver.io/download/)

Com isso você poderá se conectar ao banco PostgreSQL criado pelo Docker.

---

## ▶️ 5. Rodando o ambiente

Certifique-se de estar na pasta onde está o arquivo `docker-compose.yml` e execute:

```bash
docker-compose up -d --build
```

Isso irá:

* Baixar e subir o PostgreSQL
* Criar o volume de dados
* Subir o Ollama

Acessar Container:
> docker exec -it ollama bash

Puxar imagem:
> ollama pull duckdb-nsql:7b

* Fazer automaticamente o pull do modelo `duckdb-nsql:7b`
* Disponibilizar o ambiente completo

---

## 📡 6. Acessar o banco PostgreSQL via DBeaver

Use as seguintes informações:

| Parâmetro | Valor      |
| --------- | ---------- |
| Host      | localhost  |
| Porta     | 5432       |
| Usuário   | postgres   |
| Senha     | adm123     |
| Database  | oficina-db |

---

## 🚀 7. Derrubar o ambiente

Para parar os contêineres:

```bash
docker-compose down
```

Para parar e remover volumes:

```bash
docker-compose down -v
```

---

## 🙋 Suporte

Se quiser incluir instruções sobre APIs, scripts Python, endpoints, ou como usar o Ollama no projeto, posso complementar o README.
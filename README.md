# Sistema de Gestão de Revistas

**Um sistema web simples para controle de estoque, vendas e indicadores gerenciais de uma banca de revistas.**


![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

## ✨ Funcionalidades

- **Autenticação** com CPF e senha (bcrypt)
- **Dois perfis**: Administrador e Vendedor
- **CRUD** completo de revistas (cadastrar, editar, excluir com proteção)
- **Registro de vendas** com baixa automática de estoque
- **Painel BI** com faturamento total, estoque geral e ranking por revista
- Banco de dados **SQLite** com chaves estrangeiras

## 🖥️ Tecnologias

- **Backend**: Python + Flask (Blueprints)
- **Banco**: SQLite3
- **Autenticação**: bcrypt + Flask Session
- **Frontend**: HTML + Jinja2 + CSS inline

## 🚀 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/IsaArrakis/banco-de-revistas.git
   cd banco-de-revistas

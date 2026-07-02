import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'sistema_revistas.db')


def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='FUNCIONARIO'")
        if not cursor.fetchone():
            _criar_tabelas(conn)
            _inserir_dados_iniciais(conn)

        return conn
    except Exception as e:
        print(f"Erro de conexão com o banco: {e}")
        return None


def _criar_tabelas(conn):
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS FUNCIONARIO (
            id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            nome_funcionario TEXT NOT NULL,
            cargo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS CLIENTE (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            cpf TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS REVISTA (
            id_revista INTEGER PRIMARY KEY,
            nome_revista TEXT NOT NULL,
            quantidade_em_estoque INTEGER NOT NULL DEFAULT 0,
            preco REAL NOT NULL DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS VENDA (
            id_venda INTEGER PRIMARY KEY,
            data_da_venda TEXT NOT NULL,
            forma_de_pagamento TEXT NOT NULL,
            preco_total REAL NOT NULL,
            id_cliente INTEGER,
            id_funcionario INTEGER,
            id_revista INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
            FOREIGN KEY (id_funcionario) REFERENCES FUNCIONARIO(id_funcionario),
            FOREIGN KEY (id_revista) REFERENCES REVISTA(id_revista)
        );
    ''')
    conn.commit()
    print("✅ Tabelas criadas com sucesso!")


def _inserir_dados_iniciais(conn):
    cursor = conn.cursor()

    senha_admin = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO FUNCIONARIO (cpf, senha, nome_funcionario, cargo) VALUES (?, ?, ?, ?)",
        ('11111111111', senha_admin.decode('utf-8'), 'Ana Administradora', 'Administrador')
    )

    senha_user = bcrypt.hashpw('user123'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO FUNCIONARIO (cpf, senha, nome_funcionario, cargo) VALUES (?, ?, ?, ?)",
        ('22222222222', senha_user.decode('utf-8'), 'Bruno Vendedor', 'Vendedor')
    )

    cursor.execute(
        "INSERT INTO CLIENTE (id_cliente, nome_cliente, cpf) VALUES (?, ?, ?)",
        (1, 'Cliente Balcão', '00000000000')
    )

    revistas = [
        (1, 'Veja', 50, 15.90),
        (2, 'Superinteressante', 30, 12.50),
        (3, 'National Geographic', 20, 18.00),
        (4, 'Mundo Estranho', 40, 9.90),
        (5, 'Época Negócios', 25, 22.00),
    ]
    cursor.executemany(
        "INSERT INTO REVISTA (id_revista, nome_revista, quantidade_em_estoque, preco) VALUES (?, ?, ?, ?)",
        revistas
    )

    conn.commit()
    print("✅ Dados iniciais inseridos com sucesso!")
    print("   👤 Admin  → CPF: 11111111111 | Senha: admin123")
    print("   👤 Usuário → CPF: 22222222222 | Senha: user123")

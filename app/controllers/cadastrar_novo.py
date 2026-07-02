import bcrypt
from app.models.db import get_db_connection 

novo_cpf = "99988877766"
nova_senha = "minhasenhanova"
nome = "Carlos Silva"
cargo = "Vendedor"

senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())

conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    
    sql = "INSERT INTO FUNCIONARIO (cpf, senha, nome_funcionario, cargo) VALUES (%s, %s, %s, %s)"
    
    try:
        cursor.execute(sql, (novo_cpf, senha_hash, nome, cargo))
        conn.commit()
        print(f"Sucesso! Funcionário {nome} foi criado com a senha criptografada.")
    except Exception as e:
        print(f"Ops, deu erro ao salvar: {e}")
    finally:
        cursor.close()
        conn.close()

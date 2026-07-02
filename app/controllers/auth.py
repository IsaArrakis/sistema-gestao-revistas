import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha_digitada = request.form['senha']
        
        conn = get_db_connection()
        
        if conn:
            cursor = conn.cursor()
            
            sql = "SELECT * FROM FUNCIONARIO WHERE cpf = ?"
            cursor.execute(sql, (cpf,)) 
            
            funcionario = cursor.fetchone()
            
            if funcionario:
                hash_do_banco = funcionario['senha']
                
                if isinstance(hash_do_banco, str):
                    hash_do_banco = hash_do_banco.encode('utf-8')
                
                if bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_do_banco):
                    session['id_funcionario'] = funcionario['id_funcionario']
                    session['nome'] = funcionario['nome_funcionario']
                    session['cargo'] = funcionario['cargo']
                    
                    conn.close()
                    
                    return redirect(url_for('revista.listar'))
                else:
                    erro = "CPF ou senha inválidos."
            else:
                erro = "CPF ou senha inválidos."
                
            conn.close()
        else:
            erro = "Falha ao conectar com o banco de dados. Verifique o arquivo db.py."
            
    return render_template('login.html', erro=erro)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

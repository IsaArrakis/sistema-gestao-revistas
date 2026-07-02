from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.db import get_db_connection
from datetime import date
import random

venda_bp = Blueprint('venda', __name__)

@venda_bp.route('/vendas/nova', methods=['GET', 'POST'])
def nova_venda():
    if 'id_funcionario' not in session: return redirect(url_for('auth.login'))
    if session.get('cargo') != 'Administrador': return "Acesso Negado: Esta ação é exclusiva para Administradores.", 403
    conn = get_db_connection()
    
    if request.method == 'POST':
        id_revista = request.form['id_revista']
        quantidade = int(request.form['quantidade'])
        pagamento = request.form['pagamento']
        
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT id_cliente FROM CLIENTE WHERE id_cliente = 1")
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO CLIENTE (id_cliente, nome_cliente, cpf) VALUES (1, 'Cliente Balcão', '00000000000')")
                
                cursor.execute("SELECT preco, quantidade_em_estoque FROM REVISTA WHERE id_revista = ?", (id_revista,))
                revista = cursor.fetchone()
                
                if revista and revista['quantidade_em_estoque'] >= quantidade:
                    preco_total = float(revista['preco']) * quantidade
                    id_venda = random.randint(10000, 99999) 
                    
                    sql_venda = "INSERT INTO VENDA (id_venda, data_da_venda, forma_de_pagamento, preco_total, id_cliente, id_funcionario, id_revista) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    cursor.execute(sql_venda, (id_venda, date.today().isoformat(), pagamento, preco_total, 1, session['id_funcionario'], id_revista))
                    
                    sql_update = "UPDATE REVISTA SET quantidade_em_estoque = quantidade_em_estoque - ? WHERE id_revista = ?"
                    cursor.execute(sql_update, (quantidade, id_revista))
                    
                    conn.commit()
                    return redirect(url_for('revista.listar'))
                else:
                    return "Erro: Estoque insuficiente."
            except Exception as e:
                conn.rollback() 
                return f"Erro no banco: {e}"
            finally:
                conn.close()

    revistas = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM REVISTA WHERE quantidade_em_estoque > 0")
        revistas = cursor.fetchall()
        conn.close()
        
    return render_template('nova_venda.html', revistas=revistas)

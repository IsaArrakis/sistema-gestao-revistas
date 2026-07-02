from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.db import get_db_connection

revista_bp = Blueprint('revista', __name__)

@revista_bp.route('/revistas')
def listar():
    if 'id_funcionario' not in session:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    revistas = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM REVISTA")
        revistas = cursor.fetchall()
        conn.close()
        
    return render_template('revistas.html', revistas=revistas)

@revista_bp.route('/revistas/excluir/<int:id_revista>')
def excluir(id_revista):
    if 'id_funcionario' not in session:
        return redirect(url_for('auth.login'))
        
    if session.get('cargo') != 'Administrador':
        return "Acesso Negado: Esta ação é exclusiva para Administradores.", 403
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM REVISTA WHERE id_revista = ?", (id_revista,))
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            return f"""
            <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f7f6; margin: 0; min-height: 100vh; display: flex; justify-content: center; align-items: center; text-align: center;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <h2 style="color: #e74c3c;">Ação Bloqueada pelo Sistema!</h2>
                    <p style="color: #2c3e50; font-size: 16px;">Você não pode excluir esta revista porque ela já possui <b>vendas registradas no histórico</b>.</p>
                    <p style="color: #7f8c8d; font-size: 14px;">Para manter a integridade dos dados financeiros no Painel BI, o banco de dados impede a exclusão de produtos que geraram faturamento.</p>
                    <br>
                    <a href="/revistas" style="padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">Voltar ao Catálogo</a>
                </div>
            </div>
            """
        finally:
            conn.close()
            
    return redirect(url_for('revista.listar'))

@revista_bp.route('/revistas/nova', methods=['GET', 'POST'])
def nova():
    if 'id_funcionario' not in session:
        return redirect(url_for('auth.login'))
    if session.get('cargo') != 'Administrador':
        return "Acesso Negado: Esta ação é exclusiva para Administradores.", 403

    if request.method == 'POST':
        id_revista = request.form['id_revista']
        nome = request.form['nome_revista']
        estoque = request.form['estoque']
        preco = request.form['preco']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO REVISTA (id_revista, nome_revista, quantidade_em_estoque, preco) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (id_revista, nome, estoque, preco))
            conn.commit()
            conn.close()
            return redirect(url_for('revista.listar'))

    return render_template('nova_revista.html')

@revista_bp.route('/revistas/editar/<int:id_revista>', methods=['GET', 'POST'])
def editar(id_revista):
    if 'id_funcionario' not in session:
        return redirect(url_for('auth.login'))
    if session.get('cargo') != 'Administrador':
        return "Acesso Negado: Esta ação é exclusiva para Administradores.", 403

    conn = get_db_connection()
    
    if request.method == 'POST':
        nome = request.form['nome_revista']
        estoque = request.form['estoque']
        preco = request.form['preco']

        if conn:
            cursor = conn.cursor()
            sql = "UPDATE REVISTA SET nome_revista = ?, quantidade_em_estoque = ?, preco = ? WHERE id_revista = ?"
            cursor.execute(sql, (nome, estoque, preco, id_revista))
            conn.commit()
            conn.close()
            return redirect(url_for('revista.listar'))

    revista = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM REVISTA WHERE id_revista = ?", (id_revista,))
        revista = cursor.fetchone()
        conn.close()

    return render_template('editar_revista.html', revista=revista)

from flask import Blueprint, render_template, session, redirect, url_for
from app.models.db import get_db_connection

bi_bp = Blueprint('bi', __name__)

@bi_bp.route('/bi')
def painel():
    if 'id_funcionario' not in session: return redirect(url_for('auth.login'))
    if session.get('cargo') != 'Administrador': return "Acesso Negado", 403

    conn = get_db_connection()
    dados = {'total_estoque': 0, 'faturamento': 0}
    detalhes = []
    
    if conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(quantidade_em_estoque) as total FROM REVISTA")
        res1 = cursor.fetchone()
        if res1 and res1['total']: dados['total_estoque'] = res1['total']
        
        cursor.execute("SELECT SUM(preco_total) as faturamento FROM VENDA")
        res2 = cursor.fetchone()
        if res2 and res2['faturamento']: dados['faturamento'] = round(float(res2['faturamento']), 2)
        
        cursor.execute("""
            SELECT r.nome_revista, SUM(v.preco_total) as faturamento_revista 
            FROM VENDA v
            JOIN REVISTA r ON v.id_revista = r.id_revista
            GROUP BY r.id_revista, r.nome_revista
            ORDER BY faturamento_revista DESC
        """)
        detalhes = cursor.fetchall()
        
        conn.close()

    return render_template('bi.html', dados=dados, detalhes=detalhes)

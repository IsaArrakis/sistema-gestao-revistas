from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__, template_folder='views')
    app.secret_key = 'chave_secreta_super_segura_lab4' 

    from .controllers.auth import auth_bp
    from .controllers.revista_ctrl import revista_bp
    from .controllers.venda_ctrl import venda_bp
    from .controllers.bi_ctrl import bi_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(revista_bp)
    app.register_blueprint(venda_bp)
    app.register_blueprint(bi_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__, template_folder='../templates')

# Página inicial de login
@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(nome=nome).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['is_admin'] = usuario.is_admin
            return redirect(url_for('usuarios.painel'))

        flash('Nome de usuário ou senha incorretos.')
        return render_template('login.html')

    return render_template('login.html')

# Página de cadastro
@usuarios_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        if not nome or not senha:
            flash('Nome e senha são obrigatórios.')
            return render_template('cadastro.html')

        if Usuario.query.filter_by(nome=nome).first():
            flash('Nome de usuário já existe.')
            return render_template('cadastro.html')

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Conta criada com sucesso. Faça login.')
        return redirect(url_for('usuarios.login'))

    return render_template('cadastro.html')

# Painel após login
@usuarios_bp.route('/painel')
def painel():
    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.erro', mensagem='Acesso negado. Faça login.'))

    return render_template('painel.html')

# Logout
@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('usuarios.login'))

# Página de erro
@usuarios_bp.route('/erro')
def erro():
    mensagem = request.args.get('mensagem', 'Ocorreu um erro.')
    return render_template('erro.html', mensagem=mensagem)

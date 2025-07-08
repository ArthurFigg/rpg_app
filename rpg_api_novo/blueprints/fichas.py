from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from database import db
from models.fichas import Ficha

fichas = Blueprint('fichas', __name__, template_folder='../templates')


@fichas.route('/fichas')
def fichas_index():
    return "This is the Fichas index page."


@fichas.route('/criar-ficha', methods=['GET', 'POST'])
def criar_ficha_html():
    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.erro', mensagem='Acesso negado. Faça login.'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        classe = request.form.get('classe')
        raca = request.form.get('raca')
        subclasse = request.form.get('subclasse')
        nivel = request.form.get('nivel', 1)
        forca = request.form.get('forca', 10)
        destreza = request.form.get('destreza', 10)
        constituicao = request.form.get('constituicao', 10)
        inteligencia = request.form.get('inteligencia', 10)
        sabedoria = request.form.get('sabedoria', 10)
        carisma = request.form.get('carisma', 10)
        pontos_de_vida = request.form.get('pontos_de_vida', 10)

        nova_ficha = Ficha(
            nome=nome,
            classe=classe,
            raca=raca,
            subclasse=subclasse,
            nivel=int(nivel),
            forca=int(forca),
            destreza=int(destreza),
            constituicao=int(constituicao),
            inteligencia=int(inteligencia),
            sabedoria=int(sabedoria),
            carisma=int(carisma),
            pontos_de_vida=int(pontos_de_vida),
            usuario_id=session['usuario_id']
        )
        db.session.add(nova_ficha)
        db.session.commit()
        return redirect(url_for('fichas.pagina_minhas_fichas'))

    return render_template('criar_ficha.html')


@fichas.route('/minhas-fichas')
def pagina_minhas_fichas():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuarios.erro', mensagem='Acesso negado. Faça login.'))

    fichas_usuario = Ficha.query.filter_by(usuario_id=usuario_id).all()
    return render_template('listar_fichas.html', fichas=fichas_usuario)


@fichas.route('/fichas/<int:ficha_id>')
def ver_ficha(ficha_id):
    ficha = Ficha.query.get(ficha_id)
    if not ficha:
        return redirect(url_for('usuarios.erro', mensagem='Ficha não encontrada.'))

    usuario_id = session.get('usuario_id')
    is_admin = session.get('is_admin', False)
    if ficha.usuario_id != usuario_id and not is_admin:
        return redirect(url_for('usuarios.erro', mensagem='Acesso não autorizado.'))

    return render_template('visualizar_ficha.html', ficha=ficha)


@fichas.route('/api/fichas', methods=['POST'])
def criar_ficha_api():
    dados = request.get_json()
    nome = dados.get('nome')
    classe = dados.get('classe')
    raca = dados.get('raca')
    subclasse = dados.get('subclasse', None)
    nivel = dados.get('nivel', 1)
    forca = dados.get('forca', 10)
    destreza = dados.get('destreza', 10)
    constituicao = dados.get('constituicao', 10)
    inteligencia = dados.get('inteligencia', 10)
    sabedoria = dados.get('sabedoria', 10)
    carisma = dados.get('carisma', 10)
    pontos_de_vida = dados.get('pontos_de_vida', 10)
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
    if not nome or not classe or not raca:
        return jsonify({"error": "Nome, classe e raça são obrigatórios"}), 400
    nova_ficha = Ficha(
        nome=nome,
        classe=classe,
        raca=raca,
        subclasse=subclasse,
        nivel=nivel,
        forca=forca,
        destreza=destreza,
        constituicao=constituicao,
        inteligencia=inteligencia,
        sabedoria=sabedoria,
        carisma=carisma,
        pontos_de_vida=pontos_de_vida,
        usuario_id=usuario_id
    )
    db.session.add(nova_ficha)
    db.session.commit()
    return jsonify(nova_ficha.to_dict()), 201


@fichas.route('/api/fichas/me', methods=['GET'])
def listar_fichas_usuario_api():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
    fichas = Ficha.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([ficha.to_dict() for ficha in fichas]), 200


@fichas.route('/api/fichas/<int:ficha_id>', methods=['GET'])
def obter_ficha_api(ficha_id):
    ficha = Ficha.query.get(ficha_id)
    if not ficha:
        return jsonify({"error": "Ficha não encontrada"}), 404

    usuario_id = session.get('usuario_id')
    is_admin = session.get('is_admin', False)

    if ficha.usuario_id != usuario_id and not is_admin:
        return jsonify({"error": "Acesso não autorizado"}), 403

    return jsonify(ficha.to_dict()), 200


@fichas.route('/api/fichas/<int:ficha_id>', methods=['DELETE'])
def deletar_ficha_api(ficha_id):
    ficha = Ficha.query.get(ficha_id)
    if not ficha:
        return jsonify({"error": "Ficha não encontrada"}), 404

    usuario_id = session.get('usuario_id')
    is_admin = session.get('is_admin', False)

    if ficha.usuario_id != usuario_id and not is_admin:
        return jsonify({"error": "Acesso não autorizado"}), 403

    db.session.delete(ficha)
    db.session.commit()
    return jsonify({"message": "Ficha deletada com sucesso"}), 200


@fichas.route('/api/fichas/<int:ficha_id>', methods=['PUT'])
def editar_ficha_api(ficha_id):
    ficha = Ficha.query.get(ficha_id)
    if not ficha:
        return jsonify({"error": "Ficha não encontrada"}), 404

    usuario_id = session.get('usuario_id')
    is_admin = session.get('is_admin', False)

    if ficha.usuario_id != usuario_id and not is_admin:
        return jsonify({"error": "Acesso não autorizado"}), 403

    dados = request.get_json()
    campos_permitidos = [
        'nome', 'classe', 'raca', 'subclasse', 'nivel',
        'forca', 'destreza', 'constituicao', 'inteligencia',
        'sabedoria', 'carisma', 'pontos_de_vida'
    ]

    for campo in campos_permitidos:
        if campo in dados:
            setattr(ficha, campo, dados[campo])

    db.session.commit()
    return jsonify(ficha.to_dict()), 200

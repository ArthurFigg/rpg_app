from flask import Flask
from flask_session import Session
from database import db
from blueprints.usuarios import usuarios_bp
from blueprints.fichas import fichas  

app = Flask(__name__)


app.secret_key = 'sua_chave_secreta_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'


Session(app)
db.init_app(app)


app.register_blueprint(usuarios_bp)
app.register_blueprint(fichas)  


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

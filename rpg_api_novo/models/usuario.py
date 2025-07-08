from database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    fichas = db.relationship('Ficha', backref='usuario', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'is_admin': self.is_admin,
            'fichas': [ficha.to_dict() for ficha in self.fichas]
        }

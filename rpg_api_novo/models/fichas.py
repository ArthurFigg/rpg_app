from database import db
from utils.proficiencia import calcular_bonus_proficiencia

class Ficha(db.Model):
    __tablename__ = "fichas"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.Integer, nullable=False, default=1)
    raca = db.Column(db.String(50), nullable=False)
    classe = db.Column(db.String(50), nullable=False)
    subclasse = db.Column(db.String(50), nullable=True)
    
    forca = db.Column(db.Integer, nullable=False, default=10)
    destreza = db.Column(db.Integer, nullable=False, default=10)
    constituicao = db.Column(db.Integer, nullable=False, default=10)
    inteligencia = db.Column(db.Integer, nullable=False, default=10)
    sabedoria = db.Column(db.Integer, nullable=False, default=10)
    carisma = db.Column(db.Integer, nullable=False, default=10)
    
    pontos_de_vida = db.Column(db.Integer, nullable=False, default=10)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'nivel': self.nivel,
            'raca': self.raca,
            'classe': self.classe,
            'subclasse': self.subclasse,
            'forca': self.forca,
            'destreza': self.destreza,
            'constituicao': self.constituicao,
            'inteligencia': self.inteligencia,
            'sabedoria': self.sabedoria,
            'carisma': self.carisma,
            'pontos_de_vida': self.pontos_de_vida,
            'proficiencia': calcular_bonus_proficiencia(self.nivel),
            'usuario_id': self.usuario_id
        }

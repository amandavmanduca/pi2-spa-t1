from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import date


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/controles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Controle(db.Model):
    __tablename__ = 'controles'
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(15), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    classe = db.Column(db.String(100), nullable=False)
    caixa = db.Column(db.String(20), nullable=False)
    pagto = db.Column(db.String(30), nullable=False)
    acao = db.Column(db.String(30), nullable=False)
    
    def to_json(self):
        json_controles = {
            'id': self.id,
            'dia': self.dia,
            'valor': self.valor,
            'nome': self.nome,
            'descricao': self.descricao,
            'classe': self.classe,
            'caixa': self.caixa,
            'pagto': self.pagto,
            'acao': self.acao
        }
        return json_controles

    @staticmethod
    def from_json(json_controles):
        valor = json_controles.get('valor')
        dia = date.today()
        nome = json_controles.get('nome')
        descricao = json_controles.get('descricao')
        classe = json_controles.get('classe')
        caixa = json_controles.get('caixa')
        pagto = json_controles.get('pagto')
        acao = json_controles.get('acao')
        return Controle(valor=valor, dia=dia, nome=nome, descricao=descricao, classe=classe, caixa=caixa, pagto=pagto, acao=acao)



@app.route('/controles')
@cross_origin()
def cadastro():
    controles = Controle.query.order_by(-Controle.id).all()
    return jsonify([controle.to_json() for controle in controles])


@app.route('/controles/hoje')
@cross_origin()
def busca():
    controles = Controle.query.order_by(-Controle.id).filter(Controle.dia == date.today()).all()
    return jsonify([controle.to_json() for controle in controles])


@app.route('/controles/filtra/<dia>')
@cross_origin()
def buscaDia(dia):
    controles = Controle.query.order_by(-Controle.id).filter(Controle.dia == str(dia)).all()
    return jsonify([controle.to_json() for controle in controles])


@app.route('/controles', methods=['POST'])
@cross_origin()
def inclusao():
    controle = Controle.from_json(request.json)  
    db.session.add(controle)
    db.session.commit()
    return jsonify(controle.to_json()), 201


@app.route('/controles/<int:id>')
@cross_origin()
def consulta(id):
    controle = Controle.query.get_or_404(id)
    return jsonify(controle.to_json()), 200


@app.errorhandler(404)
@cross_origin()
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@app.route('/controles/<int:id>', methods=['PUT'])
@cross_origin()
def alteracao(id):
    controle = Controle.query.get_or_404(id)
    
    controle.valor = request.json['valor']
    #controle.dia = request.json['dia']
    controle.nome = request.json['nome']
    controle.descricao = request.json['descricao']
    controle.classe = request.json['classe']
    controle.caixa = request.json['caixa']
    controle.pagto = request.json['pagto']
    controle.acao = request.json['acao']

    db.session.add(controle)
    db.session.commit()
    return jsonify(controle.to_json()), 204


@app.route('/controles/<int:id>', methods=['DELETE'])
@cross_origin()
def exclui(id):
    Controle.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Filme excluído com sucesso'}), 200


@app.route('/controles/busca/<palavra>')
@cross_origin()
def pesquisa(palavra):
    # obtém todos os registros da tabela filmes em ordem de titulo
    controles = Controle.query.order_by(Controle.nome).filter(
        Controle.nome.like(f'%{palavra}%')).all()
    # converte a lista de filmes para o formato JSON (list comprehensions)
    return jsonify([controle.to_json() for controle in controles])

@app.route('/dados')
@cross_origin()
def dados():
    totalTransicoes = db.session.query(db.func.count(Controle.id)).first()[0]
    totalTransicoesDia = db.session.query(db.func.count(Controle.id)).first()[0]

    entradasM = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-M").filter(Controle.acao=="Entrada").filter(Controle.pagto=="Dinheiro").first()[0]
    saidasM = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-M").filter(Controle.acao=="Saída").filter(Controle.pagto=="Dinheiro").first()[0]

    entradasV = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-V").filter(Controle.acao=="Entrada").filter(Controle.pagto=="Dinheiro").first()[0]
    saidasV = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-V").filter(Controle.acao=="Saída").filter(Controle.pagto=="Dinheiro").first()[0]

    aberturas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Abertura").filter(Controle.pagto=="Dinheiro").first()[0]
    fechamentos = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Fechamento").filter(Controle.pagto=="Dinheiro").first()[0]
    
    entradas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.pagto=="Dinheiro").first()[0]
    saidas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.pagto=="Dinheiro").first()[0]

    entradasBB = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.pagto!="Dinheiro").first()[0]
    saidasBB = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.pagto!="Dinheiro").first()[0]
 
    baixas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Baixa").filter(Controle.pagto=="Dinheiro").first()[0]
    baixasM = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-M").filter(Controle.acao=="Baixa").filter(Controle.pagto=="Dinheiro").first()[0]
    baixasV = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-V").filter(Controle.acao=="Baixa").filter(Controle.pagto=="Dinheiro").first()[0]
    
    ultimoF = (db.session.query((Controle.valor))).order_by(-Controle.id).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Fechamento").filter(Controle.pagto=="Dinheiro").first()[0]
    
    todasEntradas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").first()[0]
    todasEntradasCF = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.classe=="Serviço de CrossFit").first()[0]
    todasEntradasBar = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.classe=="Bar").first()[0]
    todasEntradasRoupa = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.classe=="Roupas").first()[0]
    todasEntradasNutri = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.classe=="Serviço de Nutrição").first()[0]
    

    todasSaidas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").first()[0]
    todasSaidasCF = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.classe=="Serviço de CrossFit").first()[0]
    todasSaidasBar = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.classe=="Bar").first()[0]
    todasSaidasRoupa = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.classe=="Roupas").first()[0]
    todasSaidasNutri = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.classe=="Serviço de Nutrição").first()[0]
   

    return jsonify(totalTransicoes=totalTransicoes,totalTransicoesDias=totalTransicoesDia,
    entradasM=entradasM, saidasM=saidasM, entradasV=entradasV, saidasV=saidasV,

    aberturas=aberturas, fechamentos=fechamentos, entradas=entradas, saidas=saidas,
    baixas=baixas, baixasM=baixasM, baixasV=baixasV,
    entradasBB=entradasBB, saidasBB=saidasBB, ultimoF=ultimoF,
    todasEntradas=todasEntradas, todasEntradasCF=todasEntradasCF, todasEntradasBar=todasEntradasBar,
    todasEntradasRoupa=todasEntradasRoupa, todasEntradasNutri=todasEntradasNutri,
    todasSaidas=todasSaidas, todasSaidasCF=todasSaidasCF, todasSaidasBar=todasSaidasBar, todasSaidasRoupa=todasSaidasRoupa,
    todasSaidasNutri=todasSaidasNutri)


@app.route('/dados/<dia>')
@cross_origin()
def dados2(dia):
  
    totalTransicoes = db.session.query(db.func.count(Controle.id)).first()[0]
    totalTransicoesDia = db.session.query(db.func.count(Controle.id)).filter(Controle.dia == str(dia)).first()[0]

    entradasM = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-M").filter(Controle.acao=="Entrada").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    saidasM = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-M").filter(Controle.acao=="Saída").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]

    entradasV = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-V").filter(Controle.acao=="Entrada").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    saidasV = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-V").filter(Controle.acao=="Saída").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]

    aberturas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Abertura").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    fechamentos = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Fechamento").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    
    entradas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    saidas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]

    entradasBB = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Entrada").filter(Controle.pagto!="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    saidasBB = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Saída").filter(Controle.pagto!="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
 
    baixas = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Baixa").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    baixasM = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-M").filter(Controle.acao=="Baixa").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]
    baixasV = (db.session.query(db.func.sum(Controle.valor))).filter(Controle.caixa=="Caixa-V").filter(Controle.acao=="Baixa").filter(Controle.pagto=="Dinheiro").filter(Controle.dia == str(dia)).first()[0]

    ultimoA = (db.session.query((Controle.valor))).order_by(-Controle.id).filter(Controle.caixa=="Caixa-E").filter(Controle.acao=="Abertura").filter(Controle.pagto=="Dinheiro").first()[0]
  

    return jsonify(totalTransicoes=totalTransicoes,totalTransicoesDias=totalTransicoesDia,
    entradasM=entradasM, saidasM=saidasM, entradasV=entradasV, saidasV=saidasV,

    aberturas=aberturas, fechamentos=fechamentos, entradas=entradas, saidas=saidas,
    baixas=baixas, baixasM=baixasM, baixasV=baixasV,
    entradasBB=entradasBB, saidasBB=saidasBB, ultimoA=ultimoA)






@app.route('/')
def teste():
    return '<h1>Controle</h1>'


if __name__ == '__main__':
    app.run(debug=True)

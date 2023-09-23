from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/tarefas.db"
db = SQLAlchemy(app)

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    # identificador unico de cada tarefa
    id = db.Column(db.Integer, primary_key=True)
    #conteudo da tarefa, um texto de no maximo 200 caracteres
    conteudo = db.Column(db.String(200))
    #booleano que indica se a tarefa foi feita ou nao
    tarefa_feita = db.Column(db.Boolean)

with app.app_context():
    #Criação das tabelas
    db.create_all()
    #Execução das tarefas pendentes da base de dados
    db.session.commit()

@app.route("/", methods=["GET"])
def home():
    #consulta e armazena todas as tarefas da base de dados
    todas_as_tarefas = Tarefa.query.all()
    return render_template("index.html", lista_de_tarefas = todas_as_tarefas)
@app.route("/criar-tarefa", methods=['POST'])
def criar():
    #Tarefa é um objeto da classe tarefa,id não atribui por ser primary key
    tarefa = Tarefa(conteudo=request.form["conteudo_tarefa"], tarefa_feita=False)
    #adiciona o objeto tarefa a base de dados
    db.session.add(tarefa)
    #executa a operação pendente da base de dados
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/eliminar-tarefa/<id>")
def eliminar(id):
    #pesquisa na base de dados o registro que coincide o id e deleta
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarefa-feita/<id>")
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    tarefa.tarefa_feita = not(tarefa.tarefa_feita)
    db.session.commit()
    return  redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

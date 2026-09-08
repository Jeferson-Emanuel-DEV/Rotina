from flask import Flask, render_template, request, jsonify
import database
import notifications

app = Flask(__name__)
database.init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/atividades", methods=["GET"])
def get_atividades():
    return jsonify(database.obter_atividades())

@app.route("/api/atividades", methods=["POST"])
def save_atividade():
    data = request.json
    database.salvar_atividade(data)
    notifications.enviar_notificacao("Rotina Atualizada", f"Atividade '{data.get('nome')}' salva.")
    return jsonify({"success": True})

@app.route("/api/atividades/<string:id_atividade>", methods=["DELETE"])
def delete_atividade(id_atividade):
    database.deletar_atividade(id_atividade)
    return jsonify({"success": True})

@app.route("/api/historico", methods=["GET"])
def get_historico():
    return jsonify(database.obter_historico())

@app.route("/api/historico", methods=["POST"])
def toggle_historico():
    payload = request.json
    data_str = payload.get("data")
    atividade_id = payload.get("atividade_id")
    status = payload.get("status")
    
    database.alternar_historico(data_str, atividade_id, status)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
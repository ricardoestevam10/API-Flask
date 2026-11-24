from flask import Flask, request, jsonify
import data_model

app = Flask(__name__)

@app.route('/itens/<id>', methods=['GET'])
def get_item(id):
    return jsonify(data_model.get_id(id))

@app.route('/itens', methods=['GET'])
def get_all():
    return jsonify(data_model.get_all())

@app.route('/itens/add', methods=['POST'])
def add_item():
    item = request.get_json()
    return jsonify(data_model.insert(item))

@app.route('/itens/delete/<id>', methods=['DELETE'])
def delete_item(id):
    return jsonify(data_model.delete(id))



@app.route("/")
def home():
    return """
     <h1>Bem-vindo à API CRUD com Flask</h1>
    <p>Esta API permite que você execute operações CRUD (Create, Read, Update, Delete) em uma base de dados SQLite.</p>
    <p>Rotas disponíveis:</p>
    <ul>
        <li>POST /dados - Adiciona um novo dado. Envie um JSON com os campos 'nome' e 'idade'.</li>
        <li>GET /dados - Retorna todos os dados na base de dados.</li>
        <li>GET /dados/{id} - Retorna um dado específico por ID.</li>
        <li>PUT /dados/{id} - Atualiza um dado existente por ID. Envie um JSON com os campos 'nome' e 'idade'.</li>
        <li>DELETE /dados/{id} - Deleta um dado existente por ID.</li>
    </ul>
"""

if __name__ == "__main__":
    data_model.create_table()
    app.run(debug=False)

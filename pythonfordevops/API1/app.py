import flask
import pymongo
from bson.objectid import ObjectId

app = flask.Flask(__name__)

# --- FUNÇÕES DE APOIO ---

def get_collection(col_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['test'] 
    return db[col_name]

# --- ROTAS DA API ---

# 1. LISTAR (READ)
@app.route('/users', methods=['GET'])
def get_users():
    user_col = get_collection('users')
    users_list = []
    for u in user_col.find():
        users_list.append({
            'id': str(u.get('_id')),
            'username': u.get('username')
        })
    return flask.jsonify(users_list)

# 2. ADICIONAR (CREATE)
@app.route('/users/add', methods=['POST'])
def add_new_user():
    user_data = flask.request.form.to_dict()
    if not user_data:
        # Se não vier via form, tenta via JSON (útil para testes)
        user_data = flask.request.json

    user_col = get_collection('users')
    result = user_col.insert_one(user_data)
    
    return flask.jsonify({"status": "sucesso", "id_inserido": str(result.inserted_id)})

# 3. REMOVER (DELETE)
@app.route('/users/remove/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    user_col = get_collection('users')
    try:
        # Precisamos converter a string ID para ObjectId do Mongo
        query = {'_id': ObjectId(id)}
        result = user_col.delete_one(query)
        
        if result.deleted_count > 0:
            return flask.jsonify({"mensagem": "usuário removido"})
        else:
            return flask.jsonify({"mensagem": "usuário não encontrado"}), 404
    except:
        return flask.jsonify({"erro": "ID inválido"}), 400

# 4. ATUALIZAR (UPDATE)
@app.route('/users/update/<id>', methods=['PUT'])
def update_user_by_id(id):
    user_col = get_collection('users')
    updated_data = flask.request.form.to_dict()
    if not updated_data:
        updated_data = flask.request.json

    try:
        query = {'_id': ObjectId(id)}
        new_values = {"$set": updated_data}
        result = user_col.update_one(query, new_values)
        
        if result.matched_count > 0:
            return flask.jsonify({"mensagem": "usuário atualizado"})
        else:
            return flask.jsonify({"mensagem": "usuário não encontrado"}), 404
    except:
        return flask.jsonify({"erro": "ID inválido"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Função para carregar o banco de dados JSON
def carregar_dados():
    with open('usuarios.json', 'r') as f:
        return json.load(f)

# Função para salvar os dados no banco de dados JSON
def salvar_dados(dados):
    with open('usuarios.json', 'w') as f:
        json.dump(dados, f, indent=4)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')  #--------------------------------------------

# Rota para o formulário de assinatura
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    senha = request.form['senha']

    # Carregar os dados atuais
    dados = carregar_dados()

    # Verificar se o email já foi cadastrado
    for usuario in dados['usuarios']:
        if usuario['email'] == email:
            return "Usuário já cadastrado! Tente outro email."

    # Adicionar o novo usuário ao banco de dados
    novo_usuario = {
        'email': email,
        'senha': senha
    }
    dados['usuarios'].append(novo_usuario)

    # Salvar os dados atualizados no JSON
    salvar_dados(dados)

    return redirect(url_for('home'))

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)

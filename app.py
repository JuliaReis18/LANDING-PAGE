import json
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'segredo'

# Classe base que lida com leitura e escrita de dados
class BaseData:
    def __init__(self, file_name):
        self.file_name = file_name

    # Carregar dados do arquivo JSON
    def carregar_dados(self):
        with open(self.file_name, 'r') as f:
            return json.load(f)

    # Salvar dados no arquivo JSON
    def salvar_dados(self, dados):
        with open(self.file_name, 'w') as f:
            json.dump(dados, f, indent=4)

# Classe que lida com as operações de usuário, herdando de BaseData
class UserAccount(BaseData):                                              # HERANÇA----------------
    def __init__(self):
        super().__init__('usuarios.json')

    # Carregar usuários do arquivo JSON
    def carregar_usuarios(self):
        return self.carregar_dados()

    # Salvar usuários no arquivo JSON
    def salvar_usuarios(self, usuarios):
        self.salvar_dados(usuarios)

# Instanciar a classe UserAccount
user_account = UserAccount()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuarios = user_account.carregar_usuarios()['usuarios']
        for usuario in usuarios:
            if usuario['email'] == email and usuario['senha'] == senha:
                session['user'] = email
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))
        flash('Email ou senha incorretos.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))

@app.route('/trocar_senha', methods=['GET', 'POST'])
def trocar_senha():
    if 'user' not in session:
        flash('Você precisa estar logado para trocar a senha.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        email_logado = session['user']

        # Carrega os usuários e atualiza a senha do usuário logado
        usuarios = user_account.carregar_usuarios()['usuarios']
        for usuario in usuarios:
            if usuario['email'] == email_logado:
                usuario['senha'] = nova_senha
                user_account.salvar_usuarios({'usuarios': usuarios})
                flash('Senha alterada com sucesso!', 'success')
                return redirect(url_for('index'))
            
    return render_template('trocar_senha.html')

@app.route('/excluir_usuario', methods=['GET', 'POST'])
def excluir_usuario():
    if 'user' not in session:
        flash('Você precisa estar logado para excluir sua conta.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        email_logado = session['user']

        # Carrega os usuários e remove o usuário logado
        usuarios = user_account.carregar_usuarios()['usuarios']
        novos_usuarios = [usuario for usuario in usuarios if usuario['email'] != email_logado]

        # Atualiza o arquivo JSON com a nova lista de usuários
        user_account.salvar_usuarios({'usuarios': novos_usuarios})

        # Remove o usuário da sessão e exibe uma mensagem de confirmação
        session.pop('user', None)
        flash('Sua conta foi excluída com sucesso.', 'success')
        return redirect(url_for('index'))

    return render_template('excluir_usuario.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    senha = request.form['senha']

    # Carregar os dados atuais
    dados = user_account.carregar_usuarios()

    # Verificar se o email já foi cadastrado
    for usuario in dados['usuarios']:
        if usuario['email'] == email:
            return "Usuário já cadastrado! Faça login!"

    # Adicionar o novo usuário ao banco de dados
    novo_usuario = {
        'email': email,
        'senha': senha
    }
    dados['usuarios'].append(novo_usuario)

    # Salvar os dados atualizados no JSON
    user_account.salvar_usuarios(dados)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

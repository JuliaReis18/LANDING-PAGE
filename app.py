import json
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key= 'segredo'

# Carregar usuários do arquivo JSON
def carregar_usuarios():
    with open('usuarios.json', 'r') as f:
        return json.load(f)

# Salvar usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f)

# Função para carregar o banco de dados JSON
def carregar_dados():
    with open('usuarios.json', 'r') as f:
        return json.load(f)

# Função para salvar os dados no banco de dados JSON
def salvar_dados(dados):
    with open('usuarios.json', 'w') as f:
        json.dump(dados, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuarios = carregar_usuarios()['usuarios']
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
        usuarios = carregar_usuarios()['usuarios']
        for usuario in usuarios:
            if usuario['email'] == email_logado:
                usuario['senha'] = nova_senha
                salvar_usuarios({'usuarios': usuarios})
                flash('Senha alterada com sucesso!', 'success')
                return redirect(url_for('index'))
            
    return render_template('trocar_senha.html')

if __name__ == '_main_':
    app.run(debug=True)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/excluir_usuario', methods=['GET', 'POST'])
def excluir_usuario():
    if 'user' not in session:
        flash('Você precisa estar logado para excluir sua conta.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        email_logado = session['user']

        # Carrega os usuários e remove o usuário logado
        usuarios = carregar_usuarios()['usuarios']
        novos_usuarios = [usuario for usuario in usuarios if usuario['email'] != email_logado]

        # Atualiza o arquivo JSON com a nova lista de usuários
        salvar_usuarios({'usuarios': novos_usuarios})

        # Remove o usuário da sessão e exibe uma mensagem de confirmação
        session.pop('user', None)
        flash('Sua conta foi excluída com sucesso.', 'success')
        return redirect(url_for('index'))

    return render_template('excluir_usuario.html')

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
            return "Usuário já cadastrado! Faça login!"
        

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



# EXCLUIR -----------------------

@app.route('/excluir_usuario', methods=['GET', 'POST'])
def excluir_usuario():
    if 'user' not in session:
        flash('Você precisa estar logado para excluir sua conta.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        email_logado = session['user']

        # Carrega os usuários e remove o usuário logado
        usuarios = carregar_usuarios()['usuarios']
        novos_usuarios = [usuario for usuario in usuarios if usuario['email'] != email_logado]

        # Atualiza o arquivo JSON com a nova lista de usuários
        salvar_usuarios({'usuarios': novos_usuarios})

        # Remove o usuário da sessão e exibe uma mensagem de confirmação
        session.pop('user', None)
        flash('Sua conta foi excluída com sucesso.', 'success')
        return redirect(url_for('index'))

    return render_template('excluir_usuario.html')



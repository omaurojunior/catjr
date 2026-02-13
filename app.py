from flask import Flask, render_template, redirect, request, flash, url_for
import requests

ENDPOINT_API = "https://api.thecatapi.com/v1/images/search"

app = Flask(__name__)
app.secret_key = "super_secret_key_123"  # necessário para usar flash

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cat', methods=['POST'])
def gato():
    nome = request.form.get('nome')

    if not nome:
        flash('O nome é obrigatório!')
        return redirect(url_for('index'))

    try:
        response = requests.get(ENDPOINT_API, timeout=5)
        response.raise_for_status()

        data = response.json()

        if not data:
            flash('Não foi possível encontrar um gato.')
            return redirect(url_for('index'))

        cat_image_url = data[0]['url']

        return render_template('cat.html', nome=nome, cat_image_url=cat_image_url)

    except requests.RequestException:
        flash('Erro ao conectar com a API. Tente novamente.')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

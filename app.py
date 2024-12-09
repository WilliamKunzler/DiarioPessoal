from flask import Flask, render_template, request, redirect, url_for, flash
from db import db

app = Flask(__name__)

app.secret_key = "heitor"

@app.route('/')
def index():
    contos = db.query('SELECT * FROM diario;')
    return render_template('index.html', contos=contos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        db.query('INSERT INTO diario (titulo, texto) VALUES (%s, %s);', titulo, texto)
        flash('Conto adicionado com sucesso!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        db.query('UPDATE diario SET titulo = %s, texto = %s WHERE id = %s;', titulo, texto, id )
        flash('Conto atualizado com sucesso!')
        return redirect(url_for('index'))
    conto = db.query('SELECT * FROM diario WHERE id = %s;', id )
    return render_template('edit.html', conto=conto[0])

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    db.query('DELETE FROM diario WHERE id = %s;', id)
    flash('Conto excluído com sucesso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

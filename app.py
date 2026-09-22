from flask import Flask, render_template_string, request, redirect
import sqlite3, os

app = Flask(__name__)
DB_PATH = 'agencia.db'

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute('CREATE TABLE IF NOT EXISTS modelos (id INTEGER PRIMARY KEY, nombre TEXT, seguidores TEXT, ciudad TEXT)')
    con.close()
init_db()

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AGENCIA PRO - Oficial</title>
<style>
body { background:#0d0d0d; color:white; font-family:Arial; padding:20px; margin:0; }
h1 { color:hotpink; text-align:center; font-size:32px; letter-spacing:2px; }
.badge { background:hotpink; color:white; padding:5px 15px; border-radius:20px; font-size:12px; }
.header { text-align:center; margin-bottom:30px; }
.form-box { background:#1e1e1e; padding:25px; border-radius:15px; max-width:500px; margin:20px auto; border:1px solid #333; }
input { width:95%; padding:13px; margin:8px 0; border-radius:10px; border:1px solid #333; background:#111; color:white; }
button { background:hotpink; color:white; padding:14px; width:100%; border:none; border-radius:10px; font-weight:bold; cursor:pointer; font-size:16px; margin-top:10px; }
button:hover { background:#ff1493; }
.card { background:#1e1e1e; padding:15px; margin:12px auto; max-width:500px; border-radius:12px; display:flex; justify-content:space-between; align-items:center; border:1px solid #333; }
.del { color:#ff4444; font-weight:bold; margin-left:15px; text-decoration:none; background:#2a2a2a; padding:5px 10px; border-radius:6px; }
.stats { text-align:center; opacity:0.7; margin:20px; }
</style>
</head>
<body>
<div class="header">
<h1>AGENCIA PRO</h1>
<span class="badge">www.tuagencia.com</span>
</div>

<div class="form-box">
<form method="POST" action="/add">
<input name="nombre" placeholder="Nombre de la modelo" required>
<input name="seguidores" placeholder="Seguidores Ej: 150k" required>
<input name="ciudad" placeholder="Ciudad Ej: Quito" required>
<button>GUARDAR MODELO</button>
</form>
</div>

<div class="stats">Total registradas: {{d|length}}</div>

{% for m in d %}
<div class="card">
<span><b>{{m[1]}}</b> - {{m[2]}} - {{m[3]}}</span>
<a class="del" href="/del/{{m[0]}}">X</a>
</div>
{% endfor %}
</body>
</html>
"""

@app.route('/')
def i():
    con=sqlite3.connect(DB_PATH)
    d=con.execute('SELECT * FROM modelos ORDER BY id DESC').fetchall()
    con.close()
    return render_template_string(html,d=d)

@app.route('/add',methods=['POST'])
def a():
    con=sqlite3.connect(DB_PATH)
    con.execute('INSERT INTO modelos (nombre,seguidores,ciudad) VALUES (?,?,?)',(request.form['nombre'],request.form['seguidores'],request.form['ciudad']))
    con.commit()
    con.close()
    return redirect('/')

@app.route('/del/<int:id>')
def b(id):
    con=sqlite3.connect(DB_PATH)
    con.execute('DELETE FROM modelos WHERE id=?',(id,))
    con.commit()
    con.close()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

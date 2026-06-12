from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# Učitavanje vaše baze podataka
df = pd.read_excel('KPH-AI.xlsx')

# Ovde počinje izgled stranice (HTML i CSS)
HTML_SABLON = """
<!DOCTYPE html>
<html lang="sr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jednostavan Dnevnik Ishrane</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: #f8f9fa; 
            margin: 0; 
            padding: 20px;
            color: #333;
        }
        .glavni-kontejner { 
            max-width: 500px; 
            background: #ffffff; 
            margin: 40px auto;
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 0px 4px 20px rgba(0,0,0,0.08); 
        }
        h2 { text-align: center; margin-bottom: 25px; color: #2c3e50; font-size: 24px; }
        p.uputstvo { color: #6c757d; font-size: 15px; text-align: center; margin-bottom: 20px; }
        .polje-za-unos { 
            width: 100%; 
            padding: 14px; 
            font-size: 16px; 
            border: 2px solid #ced4da; 
            border-radius: 8px; 
            box-sizing: border-box;
            margin-bottom: 15px;
            outline: none;
        }
        .polje-za-unos:focus { border-color: #28a745; }
        .dugme-trazi { 
            width: 100%; 
            padding: 14px; 
            background-color: #28a745; 
            color: white; 
            font-size: 16px; 
            font-weight: bold;
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
        }
        .dugme-trazi:hover { background-color: #218838; }
        .lista-rezultata { list-style-type: none; padding: 0; margin-top: 25px; }
        .stavka-namirnica { 
            padding: 14px; 
            background: #f1f3f5; 
            margin-top: 8px; 
            border-radius: 8px; 
            font-size: 16px;
            border-left: 4px solid #28a745; 
        }
        .nema-rezultata { 
            padding: 14px; 
            background-color: #fff3cd; 
            color: #856404; 
            border-radius: 8px; 
            margin-top: 25px; 
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="glavni-kontejner">
        <h2>🍏 Pronađi namirnicu</h2>
        <p class="uputstvo">Upišite naziv hrane ispod i pritisnite dugme za pretragu.</p>
        
        <form method="POST">
            <input type="text" class="polje-za-unos" name="pojam" placeholder="Upišite ovde..." autocomplete="off" required>
            <button type="submit" class="dugme-trazi">Pokreni pretragu</button>
        </form>

        {% if rezultati %}
            <ul class="lista-rezultata">
                {% for stavka in rezultati %}
                    <li class="stavka-namirnica">{{ stavka }}</li>
                {% endfor %}
            </ul>
        {% elif pokrenuto %}
            <div class="nema-rezultata">
                Nismo pronašli nijednu namirnicu sa tim nazivom.
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Logika programa i pokretanje servera
@app.route('/', methods=['GET', 'POST'])
def indeks():
    rezultati = []
    pokrenuto = False
    if request.method == 'POST':
        pokrenuto = True
        pojam = request.form.get('pojam', '')
        if pojam:
            filtrirano = df[df['Namirnica'].str.contains(pojam, case=False, na=False)]
            rezultati = filtrirano['Namirnica'].tolist()
    return render_template_string(HTML_SABLON, rezultati=rezultati, pokrenuto=pokrenuto)

if __name__ == '__main__':
    app.run(debug=True)
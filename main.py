from flask import Flask, render_template_string, request
from math import pi, log10

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None

    # Code HTML directement dans la fonction Python
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calcul des pertes de charge avec Colebrook</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                padding-right: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                width: 90%;
                max-width: 400px;
                text-align: center;
            }
            label {
                display: block;
                margin-top: 10px;
                font-weight: bold;
                text-align: left;
            }
            input {
                width: calc(100% - 25px);
                padding: 12px;
                margin-top: 5px;
                margin-right: 25px;
                border: none;
                border-radius: 5px;
                outline: none;
                font-size: 16px;
                display: block;
            }
            .btn {
                width: calc(100% - 25px);
                height: 50px;
                margin-top: 20px;
                background: #ff9800;
                border: none;
                color: white;
                font-size: 22px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-left: auto;
                margin-right: auto;
            }
            .btn:hover {
                background: #e68900;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Calcul des pertes de charge</h2>
            <form method="POST">
                <label for="inputD">Diamètre D (mm):</label>
                <input type="number" step="any" name="D" id="inputD" placeholder="Entrez le diamètre" required>
                
                <label for="inputK">Rugosité K (mm):</label>
                <input type="number" step="any" name="K" id="inputK" placeholder="Entrez la rugosité" required>
                
                <label for="inputL">Longueur L (km):</label>
                <input type="number" step="any" name="L" id="inputL" placeholder="Entrez la longueur" required>
                
                <label for="inputQ">Débit Q (m³/h):</label>
                <input type="number" step="any" name="Q" id="inputQ" placeholder="Entrez le débit" required>
                
                <label for="inputN">Viscosité N (m²/s):</label>
                <input type="number" step="any" name="N" id="inputN" placeholder="Entrez la viscosité" required>
                
                <button class="btn" type="submit">Calculer</button>
            </form>
            
            {% if results %}
                <div>
                    <h3>Résultats :</h3>
                    <p>Vitesse V = {{ results.V }} m/s</p>
                    <p>Re = {{ results.Re }}</p>
                    <p>Lambda = {{ results.La }}</p>
                    <p>Perte de charge unitaire en mCE/km = {{ results.J }}</p>
                    <p>Perte de charge linéaire en mCE = {{ results.JJ }}</p>
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    
    # Vérification si la méthode est POST
    if request.method == 'POST':
        # Récupération des données depuis le formulaire HTML
        D = float(request.form['D'])
        K = float(request.form['K'])
        L = float(request.form['L'])
        Q = float(request.form['Q'])
        N = float(request.form['N'])
        
        # Calculs
        V = 4 * (Q / 3600) / (pi * (D/1000) ** 2)
        Re = V * (D / 1000) / (N/1000000)
        A = -2 * log10(K / (3.71 * D))
        B = -2*log10(K/(3.71*D)+2.51*A/Re)
        
        while A - B > 0.00001:
            A = B
            B = -2 * log10(K / (3.71 * D) + 2.51 / Re * A)
        
        La = B**-2
        J = La * V ** 2 / (2 * 9.81 * D / 1000) * 1000
        JJ = L * J
        
        results = {
            'V': round(V, 2),
            'Re': int(Re),
            'La': round(La, 4),
            'J': round(J, 3),
            'JJ': round(JJ, 3)
        }

    # Retourne la page avec ou sans résultats
    return render_template_string(html_code, results=results)

if __name__ == "__main__":
    app.run(debug=True)

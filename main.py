from flask import Flask, render_template, request, jsonify
import pandas as pd
from model import predictPrice

app = Flask(__name__)

data = pd.read_csv('car-price-dataset.csv')

# Route'lar
# Route: ana sayfa
@app.route('/')
def home():
    return render_template('home.html')

# Route: fiyat tahmini sayfası
@app.route('/predict')
def predict():
    return render_template('price.html')

# Route: istatistik sayfası
@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

# API endpointleri

@app.route('/get-brands', methods=['GET'])
def get_brands():
    brands = data['Marka'].dropna().unique().tolist() # boş veriler silinir, unique olarak alınır ve liste haline getirilir.
    brands.sort()
    return jsonify({'brands': brands})

@app.route('/get-series', methods=['GET'])
def get_series():
    brand = request.args.get('brand')
    filtered_series = data[data['Marka'] == brand]['Seri'].dropna().unique().tolist()
    filtered_series.sort()
    return jsonify({'series': filtered_series})

@app.route('/get-models', methods=['GET'])
def get_models():
    series = request.args.get('series')
    filtered_models = data[data['Seri'] == series]['Model'].dropna().unique().tolist()
    filtered_models.sort()
    return jsonify({'models': filtered_models})

@app.route('/get-bodies', methods=['GET'])
def get_bodies():
    model = request.args.get('model')
    filtered_bodies = data[data['Model'] == model]['KasaTipi'].dropna().unique().tolist()
    filtered_bodies.sort()
    return jsonify({'bodies': filtered_bodies})

@app.route('/get-transmissions', methods=['GET'])
def get_transmissions():
    body = request.args.get('body')
    filtered_transmissions = data[data['KasaTipi'] == body]['VitesTipi'].dropna().unique().tolist()
    filtered_transmissions.sort()
    return jsonify({'transmissions': filtered_transmissions})

@app.route('/get-fuels', methods=['GET'])
def get_fuels():
    transmission = request.args.get('transmission')
    filtered_fuels = data[data['VitesTipi'] == transmission]['YakıtTipi'].dropna().unique().tolist()
    filtered_fuels.sort()
    return jsonify({'fuels': filtered_fuels})

@app.route('/get-years')
def get_years():
    years = list(range(2024, 1884, -1))
    return jsonify({"years": years})

@app.route('/predict-price', methods=['POST'])
def predict_price():
    input_data = request.json
    try:
        predicted_price = predictPrice(input_data)
        return jsonify({'price': round(float(predicted_price),2)})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/suggest-cars', methods=['POST'])
def suggest_cars():
    input_data = request.json
    price = input_data.get('price', 0)

    try:
        df = pd.read_csv('car-price-dataset.csv')
        df['difference'] = abs(df['Fiyat'] - price)
        suggestions = df.nsmallest(20, 'difference')[['Marka', 'Seri', 'Model', 'Yıl', 'Kilometre', 'VitesTipi', 'YakıtTipi', 'Fiyat']].to_dict(orient='records') #default öneri adeti (n) 20, değiştirilebilir.

        return jsonify({'suggestions': suggestions})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
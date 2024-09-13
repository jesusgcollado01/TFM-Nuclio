from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('df_stock.csv', sep=';')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock', methods=['POST'])
def get_stock():
    try:
        id_value = str(request.form['id'])
        week_value = int(request.form['week'])
        
        # Filtrar el DataFrame según id y week
        result = df[(df['id'] == id_value) & (df['week'] == week_value)]
        
        if not result.empty:
            stock_preciso = result.iloc[0]['stock_preciso']
            n_pedido = result.iloc[0]['n_productos_pedido']
            stock_extra = result.iloc[0]['stock_extra']
            return jsonify({
                'stock_preciso': str(stock_preciso),
                'n_pedido': str(n_pedido),
                'stock_extra': str(stock_extra)
            })
        else:
            return jsonify({'error': 'No se encontró el stock para los datos proporcionados'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

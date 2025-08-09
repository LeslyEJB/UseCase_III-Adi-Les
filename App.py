
#  Librerías
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os

app = Flask(__name__)
CORS(app)  

# Carga el modelo
MODEL_PATH = 'brain_tumor_classifier_model_2.keras'
try:
    modelo = tf.keras.models.load_model(MODEL_PATH)
    print(f"Modelo cargado correctamente desde: {MODEL_PATH}")
except Exception as e:
    print(f"Error cargando el modelo: {e}")
    modelo = None

CLASES = ['glioma', 'meningioma', 'notumor', 'pituitary']

def preparar_imagen(imagen_bytes):

    # Carga la imagen desde los bytes recibidos
    img = Image.open(io.BytesIO(imagen_bytes)).convert('RGB')
    # Cambia el tamaño de la imagen
    img = img.resize((150, 150))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Ruta para la página principal
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

# Ruta para los archivos
@app.route('/frontend/<path:filename>')
def serve_frontend_files(filename):
    return send_from_directory('frontend', filename)

@app.route('/predict', methods=['POST'])
def predict():

    if modelo is None:
        return jsonify({'error': 'El modelo no está cargado o disponible.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Petición inválida: no se encontró el archivo.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo.'}), 400

    try:
        imagen_bytes = file.read()
        imagen_preparada = preparar_imagen(imagen_bytes)
        
        # Realiza la predicción
        prediccion = modelo.predict(imagen_preparada)
        
        clase_predicha_idx = np.argmax(prediccion[0])
        nombre_clase_predicha = CLASES[clase_predicha_idx]
        confianza = float(np.max(prediccion[0]))

        return jsonify({
            'prediction': nombre_clase_predicha,
            'confidence': f'{confianza:.2%}'
        })

    except Exception as e:
        print(f"Error durante la predicción: {e}")
        return jsonify({'error': f'Error al procesar la imagen: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
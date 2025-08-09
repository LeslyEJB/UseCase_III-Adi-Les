document.addEventListener('DOMContentLoaded', () => {
    const galeriaImagenes = document.querySelectorAll('.imagen-galeria');
    const inputArchivo = document.getElementById('carga-archivo');
    const imagenParaPredecir = document.getElementById('imagen-a-predecir');
    const botonPredecir = document.getElementById('boton-predecir');
    const resultado = document.getElementById('resultado');

    function mostrarImagen(fuente) {
        imagenParaPredecir.src = fuente;
        imagenParaPredecir.style.display = 'block';
        botonPredecir.style.display = 'inline-block';
        resultado.textContent = 'Resultado';
    }

    galeriaImagenes.forEach(imagen => {
        imagen.addEventListener('click', () => {
            mostrarImagen(imagen.src);
        });
    });

    inputArchivo.addEventListener('change', () => {
        const archivo = inputArchivo.files[0];
        if (archivo) {
            const objectURL = URL.createObjectURL(archivo);
            mostrarImagen(objectURL);
        }
    });

    botonPredecir.addEventListener('click', async () => {
        if (!imagenParaPredecir.src || imagenParaPredecir.src.endsWith('#')) {
            alert('Por favor, selecciona o sube una imagen primero.');
            return;
        }

        resultado.textContent = 'Enviando al servidor...';

        // Convierte la imagen a un formato de archivo para enviar
        const response = await fetch(imagenParaPredecir.src);
        const blob = await response.blob();
        const archivoParaEnviar = new File([blob], "imagen_a_predecir.jpg", { type: blob.type });

        // Crea un objeto FormData para enviar el archivo
        const formData = new FormData();
        formData.append('file', archivoParaEnviar);

        try {
            // Envía la imagen al servidor Python
            const respuestaServidor = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: formData,
            });

            if (!respuestaServidor.ok) {
                throw new Error('Error del servidor: ' + respuestaServidor.statusText);
            }

            // Recibe la predicción en formato JSON
            const data = await respuestaServidor.json();
            
            // Muestra el resultado
            resultado.textContent = `Predicción: ${data.prediction}`;

        } catch (error) {
            console.error('Error al conectar con el servidor:', error);
            resultado.textContent = 'Error: No se pudo conectar con el servidor de predicción.';
        }
    });
});
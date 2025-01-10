# Discord Carbon Footprint Bot

Este es un bot de Discord diseñado para calcular la huella de carbono de los usuarios en función de su uso de transporte y consumo energético.

## Características

- Calcula la huella de carbono basada en el tipo de transporte y la distancia recorrida.
- Calcula el consumo energético mensual.
- Genera una imagen con la huella de carbono calculada.
- Proporciona comandos para interactuar con el bot.

## Requisitos

- Python 3.8 o superior
- Discord.py
- Pillow (PIL)

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu_usuario/discord-carbon-footprint-bot.git
    cd discord-carbon-footprint-bot
    ```

2. Crea un entorno virtual y actívalo:

    ```bash
    python -m venv venv
    venv\Scripts\activate  # En Windows
    source venv/bin/activate  # En macOS/Linux
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura tu token de bot de Discord en el archivo [bot.py](http://_vscodecontentref_/1):

    ```python
    bot_token = 'TU_TOKEN_DE_DISCORD'
    ```

## Uso

1. Ejecuta el bot:

    ```bash
    python bot.py
    ```

2. Usa los comandos en tu servidor de Discord:

    - `!comandos`: Muestra una lista de todos los comandos disponibles.
    - `!carbonf`: Calcula tu huella de carbono basada en tu uso de transporte y consumo energético.

## Referencias útiles:
- [Sistema de recolección de información de noticias](https://colab.research.google.com/drive/1P5wa0cugNbA0QnTH9kPWJ-dX4PfPlf8r?usp=sharing) - Un repositorio que recolecta y envia información con pandas.
- [Eco-calculadora](https://github.com/PanduCa/HTML-CO2) - Un ejemplo de cómo implementar tecnologías para calcular el CO2.
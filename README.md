# SpaceX Extractor 

Extractor de datos de videos.

## Descripción

Este extractor de datos de videos de lanzamientos de SpaceX es una herramienta diseñada para recopilar información relevante de los videos de lanzamientos de SpaceX disponibles en plataformas como YouTube. El objetivo principal es facilitar el análisis de los lanzamientos de SpaceX mediante la extracción de detalles de los lanzamientos, directamente desde los videos.

## Getting Started

### Dependencias

Instala las dependencias con:
``` bash
pip install -r requirements.txt
```

### Ejecución del programa

Para ejecutar el programa es necesario tener descargado el video que se quiere analizar y colocarlo en la carpeta `videos`. Entre mejor la resolucón del video mejor.

Dentro de esta carpeta tienes que modificar el archivo `metadata.json`. Este archivo es el que lee `extractor.py` para saber sobre los videos, tiempos y regiones del video que va a analizar. La estructura del objeto JSON es la siguiente:
```JSON
{
    // Identificador del video. puede ser cualquier cosa
    "id":"itf-3", 
    // path del video
    "path": "videos/IFT-3.webm",
    // recolección de datos cada x cantidad de fotogramas 
    "recolection_rate":15, 
    // segundos del video cuando inicia el despegue
    "booster_start": 52, 
    // segundos del video cuando el booster aterriza
    "booster_end": 463,
    // segundos del video cuando la starship incia
    "starship_start": 220, 
    // segundos del video cuando la starchip atteriza
    "starship_end": 568, 
    // región del video en píxeles donde se encuentran los datos del motor de la starship
    "starship_engine_pos": {
        "x": 1742,
        "y": 912,
        "width": 160,
        "heigth": 150
    },
    // región del video en píxeles donde se encuentran la barra de lox de la starship
    "starship_lox_pos": {
        "x": 1456,
        "y": 1004,
        "width": 245,
        "heigth": 15
    },
    // región del video en píxeles donde se encuentran la barra de CH4 de la starship
    "starship_ch4_pos": {
        "x": 1456,
        "y": 1034,
        "width": 245,
        "heigth": 16
    },
    // región del video en píxeles donde se encuentran los datos de altura de la starship
    "starship_altitude_pos": {
        "x": 1573,
        "y": 945,
        "width": 66,
        "heigth": 38
    },
    // región del video en píxeles donde se encuentran los datos de velocidad de la starship
    "starship_speed_pos": {
        "x": 1544,
        "y": 912,
        "width": 95,
        "heigth": 33
    },
    // región del video en píxeles donde se encuentran el temporizador
    "timer_pos": {
        "x": 905,
        "y": 951,
        "width": 157,
        "heigth": 47
    },
    // región del video en píxeles donde se encuentran los datos del motor del booster
    "booster_engine_pos": {
        "x": 28,
        "y": 913,
        "width": 153,
        "heigth": 151
    },
    // región del video en píxeles donde se encuentran los datos de altura del booster
    "booster_altitude_pos": {
        "x": 390,
        "y": 943,
        "width": 60,
        "heigth": 46
    },
    // región del video en píxeles donde se encuentran los datos de velocidad del booster
    "booster_speed_pos": {
        "x": 353,
        "y": 911,
        "width": 94,
        "heigth": 36
    },
    // región del video en píxeles donde se encuentran la barra de lox del booster
    "booster_lox_pos": {
        "x": 268,
        "y": 1004,
        "width": 246,
        "heigth": 15
    },
    // región del video en píxeles donde se encuentran la barra de CH4 del booster
    "booster_ch4_pos": {
        "x": 268,
        "y": 1040,
        "width": 246,
        "heigth": 15
    }
}
```

Una vez descargado el video y configurado el archivo `metadata.json`, solo sería necesario ejecutar el programa con

```
python extractor.py
```

El programa empezará a procesar el video y cuando termine dejará los datos en la carpeta `outputs`.

## Datos

Puede encontrar un historial de datos recolectados en la carpeta `history`. Allí encontrará un archivo `.csv` para el booster y la starship organizado por misión.

## Autores

Daniel Rojas
[@dani0105](https://github.com/dani0105)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

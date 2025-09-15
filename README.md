# YouTube Downloader API

Una API construida con **FastAPI** para descargar videos o audios de YouTube usando `yt-dlp`. Devuelve el archivo descargado como respuesta HTTP.

---

## 🛠 Requisitos

* **Python 3.10+**
* **ffmpeg** instalado en el sistema (para extracción de audio)

### Instalación de ffmpeg

* **Windows:**
  Descarga desde [FFmpeg](https://ffmpeg.org/download.html) y añade la carpeta `bin` a tu PATH.
* **Linux (Ubuntu/Debian):**

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
* **Mac (Homebrew):**

  ```bash
  brew install ffmpeg
  ```

---

## 📦 Instalación de dependencias

Ejecuta en la carpeta del proyecto:

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn yt-dlp
```

---

## 🚀 Levantar el servidor

```bash
python -m uvicorn main:app --reload
```

> `main` es el nombre del archivo Python que contiene tu FastAPI (ajústalo si es diferente).
> `--reload` habilita recarga automática al hacer cambios en el código.

El servidor correrá por defecto en:

```
http://127.0.0.1:8000
```

---

## 🧩 Endpoint

### `/download` (GET)

Descarga un **video** o **audio** de YouTube.

**Query Parameters:**

| Parámetro | Tipo   | Descripción              | Ejemplo                                       |
| --------- | ------ | ------------------------ | --------------------------------------------- |
| `url`     | string | URL del video de YouTube | `https://www.youtube.com/watch?v=7vEovxBqFiY` |
| `type`    | string | `"video"` o `"audio"`    | `"audio"`                                     |

**Ejemplo de URL completa:**

* Audio (MP3):

```
http://127.0.0.1:8000/download?url=https://www.youtube.com/watch?v=7vEovxBqFiY&type=audio
```

* Video (MP4):

```
http://127.0.0.1:8000/download?url=https://www.youtube.com/watch?v=7vEovxBqFiY&type=video
```

> ⚠️ Para URLs de listas de reproducción, se recomienda usar **solo el enlace del video** para descargar un único archivo.

---

## 📌 Probar en Postman

1. Crear nueva request **GET**
2. URL: `http://127.0.0.1:8000/download`
3. Params:

| Key  | Value                                         |
| ---- | --------------------------------------------- |
| url  | `https://www.youtube.com/watch?v=7vEovxBqFiY` |
| type | `audio` o `video`                             |

4. Presiona **Send**
5. Postman descargará el archivo:

* `download.mp3` para audio
* `download.mp4` para video

---

## 📄 Documentación automática

FastAPI genera documentación interactiva:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔹 Notas avanzadas y producción

* Asegúrate de tener **ffmpeg** instalado para poder extraer audio.
* El archivo descargado se guarda temporalmente con un UUID y se devuelve como `download.mp3` o `download.mp4`.
* Para evitar errores 403 de YouTube en algunos videos, se recomienda usar URLs directas de videos (no listas de reproducción o enlaces de radio automática).
* Para listas de reproducción o URLs con múltiples videos, se puede modificar la API para tomar **solo el primer video** o permitir descargar la playlist completa (requiere ajustar `yt-dlp`).
* Considera limpiar archivos temporales después de enviarlos para no llenar el disco.
* Para producción, se recomienda desplegar detrás de un servidor ASGI como **Gunicorn** o **Uvicorn con `--workers`**, y configurar un directorio seguro para archivos temporales.

---

## 🔧 Pruebas adicionales

### Descargar un video de playlist (solo primer video recomendado)

```
GET http://127.0.0.1:8000/download?url=https://www.youtube.com/watch?v=7vEovxBqFiY&list=RD7vEovxBqFiY&type=video
```

### Descargar un audio de playlist (solo primer video recomendado)

```
GET http://127.0.0.1:8000/download?url=https://www.youtube.com/watch?v=7vEovxBqFiY&list=RD7vEovxBqFiY&type=audio
```

> Nota: Para playlists completas se recomienda crear un endpoint adicional que itere sobre los videos de la lista.

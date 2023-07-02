# Faster Whisper

Whisper se utiliza para transcribir de voz a texto.

## Utilizacion de la aplicacion

Para la utilizacion del mismo, se debe completar el campo WHISPER_PORT en el archivo .env creado.
Se debe realizar una peticion POST a la direccion local, con el puerto asignado en WHISPER_PORT (por ejemplo: 5050):

```
http://127.0.0.1:5050/send
```

En este caso debemos utilizar el entorno local, ya que si enviamos un audio/video largo la peticion dara timeout. La aplicacion esta probada en un Intel Core I5 9400 y tarda en promedio 3min 30s en responder a un audio de 11min.

La peticion debe ser enviada con un archivo, ya sea de audio o video y dara una respuesta en formato JSON con los siguientes campos:

```
{
    'nombre del archivo': "nombre",
    'transcripcion': "transcripcion completa"
}
```

# Faster Whisper

Para la utilizacion del Whisper, se debe completar el campo WHISPER_SUBDOMAIN en el archivo .env creado. Esto nos dara una url conformada de la siguiente forma:
```
https://example.loca.lt
```
Siendo "example" el subdominio elegido.

## Utilizacion de la aplicacion

Se debe realizar una peticion POST a la siguiente url:
```
https://example.loca.lt/send
```
La misma debe ser enviada con un archivo, ya sea de audio o video y dara una respuesta en formato JSON con los siguientes campos:
```
{
    'nombre del archivo': "nombre",
    'transcripcion': "transcripcion completa"
}
```
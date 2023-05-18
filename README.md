# TELEGRAM BOT

Para la utilizacion de este bot de Telegram se debe crear un archivo .env con los mismo atributos que el archivo .env.example.

Solo tiene una funcionalidad, la de enviar un mensaje que elijamos. Para esto debemos realizar una peticion a la url que previamente elegimos mediante el campo SENDER_SUBDOMAIN.
La url quedara conformada de la siguiente forma:
```
https://example.loca.lt
```
Siendo "example" el subdominio elegido.

Al bot que creamos debemos pedirle el "chatid" nuestro para posteriormente utilizarlo en las peticiones.

Para enviar un mensaje se debe realizar una peticion POST a la siguiente url:
```
https://example.loca.lt/send
```
Con el siguiente body en formato json:
```
{
    "chatid": 123,
    "msg": "mensaje a enviar"
}
```
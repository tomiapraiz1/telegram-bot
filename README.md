# TELEGRAM BOT

Para la utilizacion de este bot de Telegram se debe crear un archivo .env con los mismos campos que el archivo .env.example.

El campo BOT_TOKEN debe completarse con el token que nos da el bot de Telegram. Para esto debemos enviar el mensaje "/start" al BotFather, luego enviar "/newbot" y seguir los pasos que nos indica, y por ultimo copiar el token para acceder a la api de Telegram.

El campo HELP_TEXT debe completarse con el texto que deseemos, este aparecera cuando mandemos "/help" a nuestro bot.

El bot solo tiene una funcionalidad, la de enviar un mensaje que elijamos. Para esto debemos realizar una peticion a la url que previamente elegimos mediante el campo SENDER_SUBDOMAIN.
La url quedara conformada de la siguiente forma:
```
https://example.loca.lt
```
Siendo "example" el subdominio elegido.

## Utilizacion de la aplicacion

Al bot que creamos debemos pedirle el "chatid" nuestro para posteriormente utilizarlo en las peticiones. Esto se realiza mandando un mensaje "/start".

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
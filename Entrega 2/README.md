# Desafío - Entrega 2

## Dependencias

Las dependencias necesarias para la ejecución del programa son:

- [Python >=3.7](https://www.python.org/downloads/)
- [LibSSL](https://wiki.openssl.org/index.php/Libssl_API)

### Instalación

### LibSSL

LibSSL es una porción de OpenSSL. La forma más sencilla de instalarla es instalando OpenSSL.

##### ArchLinux based distros

```sh
$ sudo pacman -S openssl
```

##### Debian based distros

```sh
$ sudo apt-get install openssl
```

## Ejecución

Para correr el API gateway, ejecutar el siguiente comando

```sh
$ python run.py [smpt-host] [port]
```

Donde `smtp-host` y `port` son opcionales. Valores por defecto:

- `smtp-host`: localhost
- `port`: 1025

### Ejemplo de ejecución

```sh
$ python run.py smtp.gmail.com 465
```

## Envío de mail

Para esto el API gateway recibe en formato JSON, por método POST, los datos necesarios para el envío de mail.
Para esto, en una terminal separada se puede ejecutar el siguiente comando

```sh
$ curl -XPOST \
--data "{\"from\":\"MAIL_FROM\", \"password\":\"TU_PASS\", \"to\":\"MAIL_TO\", \"message\": \"message_text\"}" \
--header "Content-Type: application/json" \
http://localhost:8001
```

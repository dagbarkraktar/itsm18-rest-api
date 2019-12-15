# REST API для ITSM18 (данные мониторинга и сенсоров)

## Screenshot
Dashboard, построенный на данном API
![screenshot here](/screenshots/screenshot_sm.png)

## REST API - Python/Flask в docker контейнере

### Сборка docker image

```sh
$ docker build -t flask-itsm18-rest-api .
```

### Запуск контейнера с volume (папка app)

Необходимо также передать переменные: `NAGIOS_AUTH_KEY`, `MYSQL_ITSM18_USER`, `MYSQL_ITSM18_PASS`

```sh
$ docker run -d --name flask-itsm-rest-api -p 8030:80 -v $(pwd)/app:/app flask-itsm18-rest-api
```

### Можно проверить по URL Docker-контейнера

- `http://server_name:8030/api/v1/sensors/1`
- `http://server_name:8030/api/v1/nagios/0`
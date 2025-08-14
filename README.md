# Simple Web Net Tester

Простое веб-приложение для тестирования скорости интернет-соединения, измеряющее:
- Ping (среднее время и джиттер)
- Скорость загрузки (Download)
- Скорость отдачи (Upload)

## Требования
- Python 3.12
- Flask

## Установка и запуск

1. Установите Flask:
```bash
pip install flask
```

2. Склонируйте репозиторий или скачайте файлы:
```bash
git clone https://github.com/yourusername/simple-web-net-tester.git
cd simple-web-net-tester
```

3. Запустите сервер:
```bash
python app.py
```

4. Откройте в браузере:
```
http://IP_СЕРВЕРА:5080
```

## Важно:
На Линукс рекомендую использовать виртуальное окружение для Python:

```
sudo apt install python3.12-venv

python3 -m venv my-venv

my-venv/bin/pip install flask

my-venv/bin/python3 app.py
```

## Безопасность
- Вы можете изменить список разрешенных сетей в файле `app.py` (переменная `ALLOWED_NETWORKS`).
- Для безопасности используйте reverse-proxy для доступа к сервису

## Пример конфига с минимальными расхождениями в замерах скорости для reverse-proxy на базе nginx
```
server {
    listen 80 reuseport so_keepalive=on; # Стандартный 80 порт для web сервера
    server_name ВАШ_ДОМЕН_ИЛИ_IP;

    allow 127.0.0.1/32;     # теперь не в Python скрипт, а сюда пишем 
    allow 192.168.0.0/16;   # те сети, которые имеют доступ к замерам скорости
    allow 10.0.0.0/8;       # если вам нужно ограничивать доступ к сервису

    # Блокируем ВСЕ подключения по умолчанию
    deny all;               # если ничего ограничивать не надо удалите эту строку и строки выше с разрешенными подсетями


    client_max_body_size 0;       # Выключаем проверку размера (для потоковых данных)
    tcp_nodelay on;               # Отключаем алгоритм Нейгла (иначе можем получить разницу в скорости до 30% от чистой работы скрипта на Flask
    underscores_in_headers on;    # Разрешаем подчёркивания в заголовках (на всякий случай)

    location / {
        proxy_pass http://127.0.0.1:5080;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Полное отключение буферизации
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_cache off;
    }

    # Дополнительные настройки для upload
    location /speedtest/upload {
        # Явно дублируем настройки из location / (для гарантии)
        proxy_pass http://127.0.0.1:5080;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_request_buffering off;
    }
}
```


## Технические детали
- Серверная часть: Flask (Python)
- Клиентская часть: HTML5, CSS3, JavaScript
- Тестирование скорости реализовано через потоковую передачу данных
- Поддерживает высокоскоростные соединения (блоки по 1MB)

<img width="1132" height="699" alt="изображение" src="https://github.com/user-attachments/assets/9f95cb79-023d-43db-88b0-7e0048ad7d3d" />

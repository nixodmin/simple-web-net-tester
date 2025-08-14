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

## Технические детали
- Серверная часть: Flask (Python)
- Клиентская часть: HTML5, CSS3, JavaScript
- Тестирование скорости реализовано через потоковую передачу данных
- Поддерживает высокоскоростные соединения (блоки по 1MB)

<img width="1132" height="699" alt="изображение" src="https://github.com/user-attachments/assets/9f95cb79-023d-43db-88b0-7e0048ad7d3d" />

from flask import Flask, request, jsonify, send_from_directory, Response
import socket
import struct
import time
import os

app = Flask(__name__)

# Разрешенные сети (CIDR)
ALLOWED_NETWORKS = [
    "127.0.0.1/32",  # localhost для тестирования
    "192.168.0.0/16",  # локальная сеть для тестирования
    "10.0.0.0/8"  # локальная сеть для тестирования
]

def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def is_ip_allowed(ip):
    ip_int = ip_to_int(ip)
    for network in ALLOWED_NETWORKS:
        net_ip, net_bits = network.split('/')
        net_ip_int = ip_to_int(net_ip)
        mask = (0xFFFFFFFF << (32 - int(net_bits))) & 0xFFFFFFFF
        if (ip_int & mask) == (net_ip_int & mask):
            return True
    return False

@app.before_request
def limit_remote_addr():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.remote_addr

    if not is_ip_allowed(client_ip):
        return jsonify({"error": "Access denied"}), 403

@app.route('/speedtest/download')
def download_test():
    """Тест скорости загрузки - отправка больших блоков данных"""
    def generate():
        start_time = time.time()
        # Используем блоки по 1MB для высокоскоростных соединений
        chunk_size = 1024 * 1024  # 1 MB
        chunk = b'A' * chunk_size

        while time.time() - start_time < 10:
            yield chunk
            # Без искусственных задержек - пусть сеть работает на максимальной скорости

    return Response(generate(), mimetype='application/octet-stream')

@app.route('/speedtest/upload', methods=['POST'])
def upload_test():
    """Тест скорости отдачи - прием данных с измерением времени"""
    start_time = time.time()
    total_bytes = 0
    buffer_size = 1024 * 1024  # 1MB буфер для быстрого чтения

    try:
        # Читаем все данные из запроса
        while True:
            chunk = request.stream.read(buffer_size)
            if not chunk:
                break
            total_bytes += len(chunk)

            # Проверяем, не превысили ли мы время теста
            if time.time() - start_time > 15:  # немного больше времени на всякий случай
                break

    except Exception as e:
        print(f"Upload test error: {e}")

    duration = time.time() - start_time

    print(f"Upload completed: {total_bytes} bytes in {duration:.2f}s")

    return jsonify({
        "status": "success",
        "total_bytes": total_bytes,
        "duration_sec": duration
    })

@app.route('/speedtest/ping')
def ping_test():
    """Тест пинга"""
    return jsonify({"status": "pong", "timestamp": time.time()})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    print("Starting server on http://0.0.0.0:5080")
    print("Make sure index.html is in the same directory as app.py")
    app.run(host='0.0.0.0', port=5080, threaded=True, debug=True)

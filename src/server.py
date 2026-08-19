#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простое веб-приложение для event-агентства.
Реализует:
- GET-запросы: возвращает HTML-страницы
- POST-запросы: выводит данные в консоль
- Обработку ошибок 404 и 500
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import sys


class EventAgencyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов для сайта event-агентства"""

    # Словарь для маппинга URL -> HTML-файл
    ROUTES = {
        '/': 'index.html',
        '/contacts': 'contacts.html',
        '/about': 'about.html',
    }

    def do_GET(self):
        """
        Обработка GET-запросов.
        Возвращает HTML-страницы с Content-Type: text/html.
        """
        try:
            # Парсим URL, чтобы получить путь без параметров
            parsed_url = urlparse(self.path)
            path = parsed_url.path

            # Определяем, какой файл отдавать
            html_file = self.ROUTES.get(path)

            if html_file and os.path.exists(html_file):
                # ✅ ЧТЕНИЕ ФАЙЛА С ПОМОЩЬЮ КОНТЕКСТНОГО МЕНЕДЖЕРА
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Отправляем успешный ответ
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                # Страница не найдена — отдаём 404
                self.serve_404()

        except Exception as e:
            # Внутренняя ошибка сервера — отдаём 500
            print(f"❌ Ошибка: {e}")
            self.serve_500()

    def do_POST(self):
        """
        Обработка POST-запросов.
        Читает данные формы и выводит их в консоль.
        """
        try:
            # Получаем длину тела запроса
            content_length = int(self.headers.get('Content-Length', 0))

            # Читаем данные
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Парсим данные формы (application/x-www-form-urlencoded)
            params = parse_qs(post_data)

            # ✅ ВЫВОДИМ ДАННЫЕ В КОНСОЛЬ
            print("\n" + "=" * 60)
            print("📨 ПОЛУЧЕН POST-ЗАПРОС")
            print("=" * 60)
            print(f"🌐 Путь: {self.path}")
            print(f"📡 IP-адрес: {self.client_address[0]}")
            print("-" * 60)

            # Выводим все поля формы
            for key, values in params.items():
                value = values[0] if values else ''
                print(f"  {key}: {value}")

            print("=" * 60 + "\n")

            # Отправляем ответ с перенаправлением обратно на страницу
            self.send_response(303)  # See Other
            self.send_header('Location', '/contacts')
            self.end_headers()

        except Exception as e:
            print(f"❌ Ошибка при обработке POST: {e}")
            self.serve_500()

    def serve_404(self):
        """Отдаёт страницу 404 Not Found"""
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        if os.path.exists('404.html'):
            with open('404.html', 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "<h1>404 Not Found</h1><p>Страница не найдена</p>"

        self.wfile.write(content.encode('utf-8'))

    def serve_500(self):
        """Отдаёт страницу 500 Internal Server Error"""
        self.send_response(500)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        if os.path.exists('500.html'):
            with open('500.html', 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "<h1>500 Internal Server Error</h1><p>Ошибка на сервере</p>"

        self.wfile.write(content.encode('utf-8'))

    def log_message(self, format, *args):
        """Переопределяем логирование, чтобы было короче"""
        print(f"📝 {format % args}")


def run_server(port=8000):
    """Запуск HTTP-сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, EventAgencyHandler)

    print("\n" + "=" * 60)
    print("🚀 СЕРВЕР ЗАПУЩЕН")
    print("=" * 60)
    print(f"📍 Адрес: http://localhost:{port}")
    print(f"📄 Страница контактов: http://localhost:{port}/contacts")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("=" * 60 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Сервер остановлен пользователем")
        sys.exit(0)


if __name__ == '__main__':
    run_server()

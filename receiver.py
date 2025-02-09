import pika
import requests

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

# Функция обработки сообщений
def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Получено сообщение: {message}")

    # Отправляем подтверждение в Flask
    try:
        response = requests.post("http://127.0.0.1:5000/confirm", json={"message": message})
        if response.status_code == 200:
            print(" [✓] Подтверждение отправлено")
    except requests.exceptions.RequestException as e:
        print(f" [!] Ошибка при отправке подтверждения: {e}")

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(" [*] Ожидание сообщений. Нажмите CTRL+C для выхода.")
channel.start_consuming()

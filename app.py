from flask import Flask, render_template, request, redirect, jsonify
import pika

app = Flask(__name__)

# Хранилище полученных сообщений
received_messages = []

# Функция отправки сообщения в RabbitMQ
def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    connection.close()

# Главная страница с формой и списком сообщений
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            send_message(message)
        return redirect("/")
    return render_template("index.html", messages=received_messages)

# API для подтверждения получения сообщения
@app.route("/confirm", methods=["POST"])
def confirm():
    data = request.json
    if "message" in data:
        received_messages.append(data["message"])
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(debug=True)

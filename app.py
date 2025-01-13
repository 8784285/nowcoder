from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html', name='caly ')

# MQTT broker configuration
MQTT_BROKER = "120.79.10.51"
MQTT_PORT = 1883
MQTT_TOPIC = "ledctrl"

# 创建MQTT客户端实例
mqtt_client = mqtt.Client()

# 连接到MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/send_mqtt', methods=['POST'])
def send_mqtt():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.json
    print("Received JSON data:",data)
    message = data.get('msg')
    print("messge:",message)
    if not message:
        return jsonify({"error": "No message provided"}), 400

    # 发布消息到MQTT topic
    mqtt_client.publish(MQTT_TOPIC, message)
    print("messge is alredy sended:", message)
    return jsonify({"status": "Message sent", "msg": message}), 200


if __name__ == "__main__":
    app.run()
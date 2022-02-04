import paho.mqtt.client as mqtt

topics = {
    "NEW_HEAT": "new-heat",
    "UPDATE_HEAT": "update-heat",
}


def get_mqtt_client(topic: str):
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(_, userdata, flags, rc):
        print("Connected to MQTT broker with code: " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(topic)

    client = mqtt.Client()
    client.on_connect = on_connect

    return client

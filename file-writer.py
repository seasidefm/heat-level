import json
from common import get_mqtt_client, topics

config_json = open('config.json', 'r')
config = json.loads(config_json.read())
config_json.close()

print("Starting file-writer worker")


def on_message(_, __, msg):
    payload = json.loads(msg.payload)
    heat_level = payload['faveCount']
    print(f"🔥Received new heat level {heat_level}")

    f = open(config['heat_file'], 'w')
    if heat_level == 0:
        f.write(f"🔥HEAT LEVEL RISING")
    else:
        f.write(f"🔥HEAT LEVEL: {heat_level}")

    f.close()
    print("🔥Heat level set")


client = get_mqtt_client(topics["UPDATE_HEAT"])

client.connect(config["mqtt_broker"], 1883, 60)
client.on_message = on_message

client.loop_forever()

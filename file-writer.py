import json
from common import get_mqtt_client, topics

config_json = open('config.json', 'r')
config = json.loads(config_json.read())
config_json.close()

print("🔥 Starting heat level file script")


def on_message(_, __, msg):
    payload = json.loads(msg.payload)
    heat_level = payload['faveCount']
    print(f"🔥 Received new heat level {heat_level}")

    f = open(config['heat_file'], encoding='utf-8', mode='w')
    if heat_level == 0:
        f.write(f"🔥 HEAT LEVEL RISING")
    else:
        f.write(f"🔥 HEAT LEVEL: {heat_level}")

    f.close()
    print("🔥 Heat level set")


client = get_mqtt_client(topics["UPDATE_HEAT"])

client.connect(config["mqtt_broker"], 5555, 60)
client.on_message = on_message

print("🔥 Client configured and connected")
print("🔥 Starting topic subscription loop...")

client.loop_forever()

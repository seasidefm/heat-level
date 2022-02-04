# This file is meant to simulate a message coming in from the bot process

import common

client = common.get_mqtt_client("none")

client.connect("localhost", 1883, 60)

client.publish(common.topics['NEW_HEAT'], "Junko Ohashi - テレフォン・ナンバー (Telephone Number)  \n")

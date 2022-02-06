import json
import os

from pymongo import MongoClient

from common import get_mqtt_client, topics

print("Starting heat level checker")


def on_message(_, userdata, msg):
    new_heat = msg.payload.decode('utf-8').strip()
    print("🔥 Received heat level req for: \n->", new_heat)

    mongo = MongoClient(os.environ['MONGO_URL'])
    result = mongo['devDb']['saved_songs'].aggregate([
        {
            '$match': {
                'user': {
                    '$not': {
                        '$in': [
                            'duke_ferdinand', 'seasidefm'
                        ]
                    }
                }
            }
        }, {
            '$group': {
                '_id': 'songs',
                'songList': {
                    '$push': '$songs.song'
                }
            }
        }, {
            '$unwind': {
                'path': '$songList'
            }
        }, {
            '$unwind': {
                'path': '$songList'
            }
        }, {
            '$group': {
                '_id': {
                    'song': '$_id',
                    'songName': '$songList'
                },
                'songCount': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'songCount': -1,
                '_id.songName': 1
            }
        }, {
            '$group': {
                '_id': '$_id.song',
                'songs': {
                    '$push': {
                        'name': '$_id.songName',
                        'faveCount': '$songCount'
                    }
                }
            }
        }
    ])

    def match_song(song: dict) -> bool:
        if song['name'].strip() == new_heat:
            return True

        return False

    # result    -> Mongo cursor
    # list()    -> array of one doc
    # [0]       -> extract doc
    # ['songs'] -> pull out array of songs
    list_results = list(result)[0]['songs']

    default_heat = {
            "name": new_heat,
            "faveCount": 0
        }

    filtered = list(filter(match_song, list_results))
    match = filtered[0] if len(filtered) > 0 else default_heat
    client.publish(topics['UPDATE_HEAT'], json.dumps(match))

    if len(filtered) > 0:
        print('🔥 Updated heat')
    else:
        print('🔥 Sent data for new heat')


client = get_mqtt_client(topics['NEW_HEAT'])


client.connect("mosquitto", 5555, 60)

client.on_message = on_message

client.loop_forever()

from flask import Flask, request
import urllib3, json, ssl
app = Flask(__name__)

BASE_URL = "https://www.travys.ch/wp-json/travys_tiramisu/v1/iv/lines"
ICON = "i19110"

@app.route("/")
def hello():
    line = request.args.get('line')
    stop = request.args.get('stop')

    if len(line) == 0 or len(stop) == 0:
        return '', 422

    direction = request.args.get('direction') if len(request.args.get('direction')) > 0 else 'forward'
    url = BASE_URL + "/{}/{}".format(line, direction)

    schedule = dict()
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(keep_alive=True, accept_encoding=True, user_agent="LameEtTrique/1.0")
    req = http.request('GET', url, headers=headers)
    json_file = json.loads(req.data.decode('utf-8'))['line']['stops']

    for value in json_file:
        if str(value['name']) == str(stop):
            schedule = value
            break

    texts = []
    if len(schedule) > 0 and len(schedule['next_departures']) > 0:
        texts.append("Ligne {}, arrêt {}".format(line, stop))
        texts.append("Prochain bus dans {} min".format(schedule['next_departures'][0]['calculatedValue'])) 
    else:
        texts.append("Pas de correspondance pour la ligne {}, à l'arrêt {}".format(line, stop))

    payload = { "frames": [] }
    for value in texts:
        frame = { "text": "", "icon": ICON }
        frame['text'] = value
        payload['frames'].append(frame)

    return(str(payload))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
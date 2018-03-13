from flask import Flask, request
import urllib3, json, ssl
app = Flask(__name__)

BASE_URL = "https://www.travys.ch/wp-json/travys_tiramisu/v1/iv/lines"
ICON = "i19110"

def getData(line, direction):
    url = BASE_URL + "/{}/{}".format(line, direction)
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(keep_alive=True, accept_encoding=True, user_agent="LameEtTrique/1.0")
    req = http.request('GET', url, headers=headers)
    
    return json.loads(req.data.decode('utf-8'))['line']['stops']

def getPayload(values):
    payload = { "frames": [] }
    for value in values:
        frame = { "text": "", "icon": ICON }
        frame['text'] = value
        payload['frames'].append(frame)

    return payload

@app.route("/")
@app.route("/schedule")
def lame_et_trique():
    texts = []
    schedule = dict()

    line = request.args.get('line')
    stop = request.args.get('stop')

    if not line or not stop:
        texts.append("Données fournies incorrectes.")
    else:
        direction = request.args.get('direction') if request.args.get('direction') else 'forward'
        json_file = getData(line, direction)

        for value in json_file:
            if str(value['name']) == str(stop):
                schedule = value
                break

        if len(schedule) > 0 and len(schedule['next_departures']) > 0:
            texts.append("Ligne {}, arrêt {}".format(line, stop))
            texts.append("Prochain bus dans {} min".format(schedule['next_departures'][0]['calculatedValue'])) 
        else:
            texts.append("Pas de correspondance pour la ligne {}, à l'arrêt {}".format(line, stop))

    return(json.dumps(getPayload(texts)))

@app.route("/<line>/stops")
def get_stops(line=None):
    stops = ""

    if not line:
        return 'Données manquantes !', 422

    direction = request.args.get('direction') if request.args.get('direction') else 'forward'
    json_file = getData(line, direction)

    for value in json_file:
        stops = stops + str(value['name']) + "<br />"

    if stops == "":
        return "Pas d'arrêt pour la ligne {} dans le sens {}".format(line, direction)

    return(stops)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
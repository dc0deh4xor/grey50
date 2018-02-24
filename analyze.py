from flask import Flask, request
from playground import parse_time
from pymystem3 import Mystem
from json import dumps

app = Flask(__name__)
system = Mystem()


@app.route("/parse", methods=["POST"])
def launch_parse():
    data = request.get_json(force=True)
    print(dumps(data))
    title = data["message"]
    if len(data["message"]) > 255:
        title = data("message")[0:255]

    timestamp,date_data = parse_time(data["message"])

    return dumps({
        "id": data["id"],
        "result": {
            "title": title,
            "when": timestamp,
            "when_data": date_data,
            "place": None
        }
    })


@app.route('/analyze', methods=["GET"])
def index():
    if "q" in request.args:
        text = request.args.get("q")
        return str(system.analyze(text))
    else:
        return 'GET {q} param expected with string'

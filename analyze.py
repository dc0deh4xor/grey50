from flask import Flask, request
from pymystem3 import Mystem

app = Flask(__name__)
system = Mystem()

@app.route('/analyze', methods=["GET"])
def index():
    if "q" in request.args:
        text = request.args.get("q")
        return str(system.analyze(text))
    else:
        return 'GET {q} param expected with string'

import re
from time import sleep

import numpy as np
from flask import Flask, request

app = Flask(__name__)


def network_delay():
    return abs(np.random.lognormal(0.98, 0.5, 1)[0])


@app.route('/')
def home():
    return 'Hello!'


@app.route('/safe/<path:path>', methods=['GET'])
def safe(path: str):
    # get the value of the id (i.e. ?id=some-value)
    item_id = request.args.get('id')
    sleep(network_delay())
    return 'This is item id #%s at %s' % (item_id, path)


@app.route('/vulnerable/<path:path>', methods=['GET'])
def vulnerable(path: str):
    # get the value of the id (i.e. ?id=some-value)
    item_id = request.args.get('id')
    if item_id is not None:
        if re.match(r'^SLEEP\([0-9]*\.?[0-9]+\)$', item_id) is not None:
            injected_sleep = float(item_id.replace("SLEEP(", "").strip(")"))
            sleep(network_delay() + injected_sleep * 5)
            return 'This is page #%s' % path
        else:
            sleep(network_delay())
            return 'This is page #%s' % path
    else:
        sleep(network_delay())
        return 'This is page #%s' % path


if __name__ == '__main__':
    app.run()

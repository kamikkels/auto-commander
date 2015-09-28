"""
Auto Commander

Get a commander for you, because you just can't choose between Phage the Untouchable or Haakon, Stromgald Scourge

@category   Utility
@version    $ID: 1.0.0 $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.0.0"

import json
import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    pass

if __name__ == '__main__':
    app.run()
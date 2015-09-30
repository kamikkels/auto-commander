"""
Auto Commander

Get a commander for you, because you just can't choose between Phage the Untouchable or Haakon, Stromgald Scourge

@category   Utility
@version    $ID: 1.0.0 $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.0.0"

import os
import json
import yaml
import flask
from peewee import *
from dbinterpret import *

#Work out where we are
DIR = os.path.dirname(os.path.realpath(__file__))
#Get the config
conf = yaml.safe_load(open("{}/rnd.cfg".format(DIR)))
#Get the ban list
with open(conf['ban_list'].format(DIR)) as data_file:
    source = json.load(data_file)

app = flask.Flask(__name__)

@app.route('/randommander')
def index():
    try:
        card = cards.select(cards.name, cards.multiverseid).where(cards.name.not_in(source)).\
            where(cards.id << (card_types.select(card_types.card).
                               where(card_types.type << (types.select(types.id).
                                                         where(types.type == 'Legendary'))
                                     )
                               ),
                  cards.id << (card_types.select(card_types.card).
                               where(card_types.type << (types.select(types.id).
                                                         where(types.type == 'Creature'))
                                     )
                               )
                  ).order_by(fn.Random()).limit(1)
        for c in card:
            return flask.render_template('index.html', name=c.name, verse_id=c.multiverseid)
    except:
        pass

    return 'failure'


if __name__ == '__main__':
    app.run()
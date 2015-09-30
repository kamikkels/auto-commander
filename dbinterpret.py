"""
DB Interpret

Initialise the card database with the needed structure

@author:     KMR
@licence:    GNU GPL v.3
"""
__version__ = "1.0.0"

import os
import yaml
from peewee import *

DIR = os.path.dirname(os.path.realpath(__file__))
conf = yaml.safe_load(open("{}/dbi.cfg".format(DIR)))
database = SqliteDatabase(conf['db_location'].format( DIR ), **{})


class unknown_field(object):
    pass


class base_model(Model):
    class Meta:
        database = database


class cards(base_model):
    """
    Cards: for holding card information
    """
    name         = CharField()
    layout       = CharField()
    type         = CharField()
    mana         = CharField(null=True)
    cmc          = CharField(null=True)
    text         = CharField(null=True)
    rarity       = CharField(null=True)
    flavor       = CharField(null=True)
    artist       = CharField(null=True)
    power        = CharField(null=True)
    toughness    = CharField(null=True)
    loyalty      = IntegerField(null=True)
    number       = CharField(null=True)
    multiverseid = IntegerField(null=True)
    sides        = IntegerField(null=True)

    class Meta:
        db_table = 'cards'


class types(base_model):
    """
    Types: for holding both super and subtypes
    """
    type  = CharField()
    super = BooleanField(default=False)
    sub   = BooleanField(default=False)

    class Meta:
        db_table = 'types'


class colors(base_model):
    """
    Colors: for holding colors, even though there should be a maximum of 5 of these
    """
    type = CharField()

    class Meta:
        db_table = 'colors'

class sets(base_model):
    """
    Sets: reference for each set
    """
    name    = CharField()
    size    = IntegerField()
    code    = CharField()
    block   = CharField(null=True)
    type    = CharField()
    release = DateField()
    online  = BooleanField(default=False,null=True)


class card_types(base_model):
    """
    CardTypes linking table between cards and types
    """
    card = ForeignKeyField(cards, related_name='types')
    type = ForeignKeyField(types, related_name='cards')


class card_colors(base_model):
    """
    CardColors: linking table between cards and colors
    """
    card  = ForeignKeyField(cards, related_name='colors')
    color = ForeignKeyField(colors, related_name='cards')

class card_sets(base_model):
    """
    card_sets: linking table between cards and sets
    """
    card  = ForeignKeyField(cards, related_name='sets')
    set = ForeignKeyField(sets, related_name='cards')


class card_sides(base_model):
    """
    card_sides: a simulated sequence for pairing card sides into a nice group
    """
    side = IntegerField(default=1)

if __name__ == "__main__":
    # Drop the existing tables if they do indeed exist, and we want to
    if conf['force_create']:
        database.drop_tables([cards,colors,sets,types,card_types,card_colors,card_sides,card_sets], safe=True)

    # Create new tables if we need to
    database.create_tables( [
        cards,
        colors,
        sets,
        types,
        card_types,
        card_colors,
        card_sides,
        card_sets
    ], safe=True )

    # Setup the kinda sequence if it's not already there
    if card_sides.select().count() == 0:
        card_sides.create()
"""
DB Interpret

Initialised the card database with the needed structure

@category   Utility
@version    $ID: 1.0.0 $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.0.0"

import os
from peewee import *

DIR = os.path.dirname(os.path.realpath(__file__))
database = SqliteDatabase("{}/dbtables/mtg_cards.sqlite".format( DIR ), **{})


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = database


class Cards(BaseModel):
    id     = PrimaryKeyField(db_column='ID')
    name   = CharField(db_column='name')
    layout = CharField(db_column='layout')
    mana   = CharField(db_column='mana')
    cmc    = CharField(db_column='cmc')
    type   = CharField(db_column='type')
    text   = CharField(db_column='text')

    class Meta:
        db_table = 'cards'


class Types(BaseModel):
    id   = PrimaryKeyField(db_column='ID')
    type = CharField(db_column='type')

    class Meta:
        db_table = 'types'


class Colors(BaseModel):
    id   = PrimaryKeyField(db_column='ID')
    type = CharField(db_column='color')

    class Meta:
        db_table = 'colors'


class cardTypes(BaseModel):
    card = ForeignKeyField(Cards, related_name='types')
    type = ForeignKeyField(Types, related_name='cards')


class cardColors(BaseModel):
    card  = ForeignKeyField(Cards, related_name='colors')
    color = ForeignKeyField(Colors, related_name='cards')

Cards.create_table(True)
Colors.create_table(True)
Types.create_table(True)
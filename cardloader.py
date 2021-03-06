#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Card loader

loads cards from a .json file into sqlite databases

will update existing databases if found, unless the 'force_add' field is set to 'True' in the config

@category   Utility
@version    $ID: 1.0.0 $;
@author     KMR
@licence    GNU GPL v.3
"""
import os
import sys
import yaml
import json
from dbinterpret import cards, colors, sets, types, card_types, card_colors, card_sets, card_sides


class CardLoader:
    """
    CardLoader

    for loading card details in from a json, will append details by default
    """
    def __init__(self):
        """
        Initialise a new instance of card loader using the cl.cfg file in the same path
        :return:
        A new instanace of CardLoader
        """
        #Work out where we are
        DIR = os.path.dirname(os.path.realpath(__file__))
        #Get the config
        self.conf = yaml.safe_load(open("{}/cl.cfg".format(DIR)))
        #Load the giant JSON file
        with open(self.conf['card_source'].format(DIR)) as data_file:
            self.source = json.load(data_file)

    def load_cards(self):
        """
        load_cards
        loads cards into the database based on the dbinterpret class
        """
        sets_done   = 1
        total_cards = 0
        print 'CardLoader running:'

        for n in self.source:
            set = self.source[n]
            # Set the values that might be missing
            nullable = ['block', 'onlineOnly']
            for i in nullable:
                if i not in set:
                    set[i] = None

            # Create the set if it doesn't already exist, if it does we'll just get it
            set_ob, created = sets.get_or_create(
                name    = set['name'],
                size    = len(set['cards']),
                code    = set['code'],
                block   = set['block'],
                type    = set['type'],
                release = set['releaseDate'],
                online  = set['onlineOnly']
            )

            cards_done = 0
            for card in set['cards']:
                # Deal with more potentially absent data
                nullable = ['manaCost','cmc','text','rarity','flavor','power','toughness','multiverseid','number']
                for i in nullable:
                    if i not in card:
                        card[i] = None

                # Create the card if it doesn't already exist (some cards are in multiple sets)
                card_ob, created = cards.get_or_create(
                    name         = card['name'],
                    layout       = card['layout'],
                    mana         = card['manaCost'],
                    cmc          = card['cmc'],
                    type         = card['type'],
                    text         = card['text'],
                    rarity       = card['rarity'],
                    flavor       = card['flavor'],
                    artist       = card['artist'],
                    power        = card['power'],
                    toughness    = card['toughness'],
                    number       = card['number'],
                    multiverseid = card['multiverseid']
                )

                # If a card was created we need to link it to some of the details
                if(created):
                    # If it's a multiple sided card get the linking reference for it
                    if 'names' in card:
                        if cards.select().where(cards.name << card['names'], cards.name != card_ob.name ).count() > 0:
                            pair = cards.get(cards.name << card['names'], cards.name != card_ob.name)
                            card_ob.sides = pair.sides
                        else:
                            sides = card_sides.get()
                            card_ob.sides = sides.side
                            sides.side += 1
                            sides.save()
                        card_ob.save()

                    # If the card has supertypes get each one and setup the required references
                    if 'supertypes' in card:
                        for cardtype in card['supertypes']:
                            type_ob, created = types.get_or_create(type=cardtype, super=True)
                            card_types.get_or_create(card=card_ob.id, type=type_ob.id)

                    # Setup the required types references
                    if 'types' in card:
                        for cardtype in card['types']:
                            type_ob, created = types.get_or_create(type=cardtype)
                            card_types.get_or_create(card=card_ob.id, type=type_ob.id)

                    # If the card has subtypes get each one and setup the required references
                    if 'subtypes' in card:
                        for cardtype in card['subtypes']:
                            type_ob, created = types.get_or_create(type=cardtype, sub=True)
                            card_types.get_or_create(card=card_ob.id, type=type_ob.id)

                    # If the card is colored setup the details
                    if 'colors' in card:
                        for color in card['colors']:
                            color_ob, created = colors.get_or_create(type=color)
                            card_colors.get_or_create(card=card_ob.id, color=color_ob.id)

                # Link the card into the appropriate set
                card_sets.get_or_create(card=card_ob.id,set=set_ob.id)

                # And now were done with this card work out some nice cli output
                cards_done += 1
                sys.stdout.write("\rProcessed card {1:<5} in set {0}".format(sets_done, cards_done))
                sys.stdout.flush()
            # Keep a running total of everything
            total_cards += cards_done
            sets_done   += 1
        # Now everything is done output some totals
        print "\r\n{0} sets processed: {1} cards found".format(sets_done, total_cards)

if __name__ == '__main__':
    loader = CardLoader()
    loader.load_cards()
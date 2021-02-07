import sys

from django.core.management.base import BaseCommand

from core.helpers import scryfall_api


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--set")
        parser.add_argument("--lang")

    def handle(self, **options):
        # Mandatory set
        if options['set'] is None:
            print("set argument is missing!")
            sys.exit()

        # set must be valid
        if len(options['set']) != 3:
            print("set is not valid, must be 3 digit")
            sys.exit()

        lang = options['lang'].lower() if len(options['lang']) == 2 else "en"
        set = options['set'].lower()

        print("Fetching " + set + " (" + lang + ")")
        print("-----------------")

        cards = scryfall_api({
            "q": "set:" + set + " lang:" + lang + " unique:prints",
        })
        print(len(cards))

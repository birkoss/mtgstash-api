import json
import sys

from django.core.management.base import BaseCommand

from core.helpers import get_image_descriptions
from cards.models import Card, Face, Type


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

        with open("data/sets/" + lang + "/" + set + ".json") as f:
            cards = json.load(f)

            counter = 1
            for single_card in cards:
                card = Card.objects.filter(
                    scryfall_id=single_card['id']
                ).first()

                if card is None:
                    card = Card(
                        language=lang,
                        set=set,
                        layout=single_card['layout'],
                        rarity=single_card['rarity'],
                        multiverse_id=single_card['multiverse_ids'].pop(0) if len(single_card['multiverse_ids']) > 0 else "",
                        scryfall_id=single_card['id'],
                        collector_number=single_card['collector_number'],
                    )
                    print(str(counter) + "/" + str(len(cards)) + " New card from " + set + " (" + lang + ") : " + single_card['layout'])  # nopep8

                    faces = []
                    types = []
                    if single_card['layout'] == "normal":
                        # NORMAL layout : 1 Face, 1 Type
                        card.name = single_card['printed_name'] if "printed_name" in single_card else single_card['name']

                        face = Face(
                            card=card,
                            illustration_id=single_card['illustration_id']
                        )
                        face.descriptors = get_image_descriptions(single_card['image_uris']['large'])  # nopep8
                        faces.append(face)

                        type = Type(
                            # Only get the card type (ex: Creature — Human Rogue)
                            type=single_card['type_line'].split(" — ").pop(0),
                            face=face,
                        )
                        types.append(type)
                    elif single_card['layout'] == "modal_dfc":
                        # MODAL DOUBLE FACE : 2 Faces, 2 Types
                        for single_face in single_card["card_faces"]:
                            face = Face(
                                card=card,
                                illustration_id=single_face["illustration_id"],
                                name=single_face['printed_name'] if "printed_name" in single_face else single_face['name']
                            )
                            face.descriptors = get_image_descriptions(single_face['image_uris']['large'])  # nopep8
                            faces.append(face)

                            if card.name != "":
                                card.name = card.name + " // "

                            card.name = card.name + face.name

                            type = Type(
                                # Only get the card type (ex: Creature — Human Rogue)
                                type=single_face['type_line'].split(" — ").pop(0),
                                face=face,
                            )
                            types.append(type)

                    if len(faces) > 0 and len(types) > 0:
                        card.save()
                        for face in faces:
                            face.save()
                        for type in types:
                            type.save()


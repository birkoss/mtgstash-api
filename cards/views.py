import json

from django.http import JsonResponse
from django.shortcuts import render

from core.helpers import get_image_descriptions

from .models import Card, Face, Type


def import_set(request):

    language = "en"
    set = "znr"

    with open("data/sets/" + language + "/" + set + ".json") as f:
        cards = json.load(f)

        for single_card in cards:
            card = Card.objects.filter(scryfall_id=single_card['id']).first()

            if card is None:
                card = Card(
                    language=language,
                    set=set,
                    layout=single_card['layout'],
                    rarity=single_card['rarity'],
                    multiverse_id=single_card['multiverse_ids'].pop(0) if len(single_card['multiverse_ids']) > 0 else "",
                    scryfall_id=single_card['id'],
                    collector_number=single_card['collector_number'],
                )
                print("New card from " + set + " (" + language + ") : " + single_card['layout'])  # nopep8

                faces = []
                types = []
                if single_card['layout'] == "normal":
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

                if len(faces) > 0 and len(types) > 0:
                    card.save()
                    for face in faces:
                        face.save()
                    for type in types:
                        type.save()

    return JsonResponse({
        "ok": 1
    })

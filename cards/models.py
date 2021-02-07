from django.db import models

from core.models import TimeStampedModel, UUIDModel


class Card(TimeStampedModel, UUIDModel, models.Model):
    name = models.CharField(max_length=100, blank=False)
    language = models.CharField(max_length=2, blank=False)

    set = models.CharField(max_length=3, blank=False)
    rarity = models.CharField(max_length=40, blank=False)

    layout = models.CharField(max_length=100, blank=False, null=False)

    multiverse_id = models.CharField(max_length=10, blank=False)
    scryfall_id = models.CharField(max_length=48)

    collector_number = models.IntegerField(blank=False, default=0)

    parent = models.ForeignKey('self', blank=True, null=True, related_name='translations', on_delete=models.CASCADE)  # nopep8

    def __str__(self):
        return self.name


class Face(TimeStampedModel, UUIDModel, models.Model):
    card = models.ForeignKey(Card, blank=False, null=False, related_name="faces", on_delete=models.CASCADE)  # nopep8
    name = models.CharField(max_length=100, blank=False, default="")
    descriptors = models.TextField(blank=False, null=False, default="")
    illustration_id = models.CharField(max_length=48, default="")


class Type(TimeStampedModel, UUIDModel, models.Model):
    face = models.ForeignKey(Face, blank=False, null=False, related_name="types", on_delete=models.CASCADE)  # nopep8
    type = models.CharField(max_length=100, blank=False)

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from base.responses import CustomSerializer


class ItemPostRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=False)
    lastStatusId = serializers.CharField(required=True)
    lastStatusAt = serializers.DateField(required=True)
    mainAuthorId = serializers.IntegerField(required=True)
    authorsId = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    subtitle = serializers.CharField(required=False, allow_null=True)
    titleOriginal = serializers.CharField(required=False)
    subtitleOriginal = serializers.CharField(required=False, allow_null=True)
    isbnFormatted = serializers.CharField(required=False)
    isbn10Formatted = serializers.CharField(required=False)
    itemType = serializers.CharField(required=True)
    pages = serializers.IntegerField(required=False)
    volume = serializers.IntegerField(required=False, default=1)
    edition = serializers.IntegerField(required=False, default=1)
    publishedAt = serializers.DateField(required=False)
    publishedOriginalAt = serializers.DateField(required=False)
    serieId = serializers.IntegerField(required=False)
    collectionId = serializers.IntegerField(required=False)
    publisherId = serializers.IntegerField(required=False)
    itemFormatId = serializers.CharField(required=False)
    languageId = serializers.CharField(required=False)
    coverPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    paidPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    dimensions = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    height = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    thickness = serializers.IntegerField(required=False)
    summary = serializers.CharField(required=False)


class ItemGetRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=False)
    itemType = serializers.CharField(required=True)
    isUnique = serializers.BooleanField(required=False, default=False)

    def validate_itemType(self, value):
        choices = ['all', 'book', 'manga']
        if value not in choices or not value:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base.serializers import CustomSerializer


class ItemGetSerializer(CustomSerializer):
    itemId = serializers.IntegerField(required=False)
    itemType = serializers.CharField(required=True)
    isUnique = serializers.BooleanField(required=False, default=False)

    def validate_itemType(self, value):
        choices = ['all', 'book', 'manga']
        if value not in choices or not value:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value


class ItemPostSerializer(CustomSerializer):
    itemId = serializers.IntegerField(required=False)
    lastStatusId = serializers.CharField(required=True)
    lastStatusAt = serializers.DateField(required=True)
    mainAuthorId = serializers.IntegerField(required=True)
    authorsId = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    subtitle = serializers.CharField(required=False)
    titleOriginal = serializers.CharField(required=False)
    subtitleOriginal = serializers.CharField(required=False)
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
    itemFormat = serializers.CharField(required=False)
    languageId = serializers.CharField(required=False)
    coverPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    paidPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    dimensions = serializers.CharField(required=False)
    height = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    thickness = serializers.IntegerField(required=False)
    summary = serializers.CharField(required=False)


class ItemReadingPostSerializer(CustomSerializer):
    itemId = serializers.IntegerField(required=True)
    startAt = serializers.DateField(required=False)
    endAt = serializers.DateField(required=False)
    isDropped = serializers.BooleanField(default=False)


class AuthorGetSerializer(CustomSerializer):
    pass


class AuthorPostSerializer(CustomSerializer):
    pass

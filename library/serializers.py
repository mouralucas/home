from rest_framework import serializers


class ItemGeTSerializer(serializers.Serializer):
    itemId = serializers.IntegerField(required=False)
    itemType = serializers.CharField(required=False)
    isUnique = serializers.BooleanField(required=False, default=False)


class ItemPostSerializer(serializers.Serializer):
    itemId = serializers.IntegerField(required=False)
    lastStatusId = serializers.CharField(required=True)
    lastStatusDate = serializers.DateField(required=True)
    mainAuthorId = serializers.IntegerField(required=True)
    authorsId = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    subtitle = serializers.CharField(required=False)
    title_original = serializers.CharField(required=False)
    subtitle_original = serializers.CharField(required=False)
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
    payedPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    dimensions = serializers.CharField(required=False)
    height = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    thickness = serializers.IntegerField(required=False)
    summary = serializers.CharField(required=False)
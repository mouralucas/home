from rest_framework import serializers

from base.serializers import CustomSerializer


class ItemSerializer(CustomSerializer):
    itemId = serializers.IntegerField(read_only=True)
    mainAuthorId = serializers.IntegerField(read_only=True)
    mainAuthorName = serializers.CharField(required=True)
    title = serializers.CharField(max_length=500)
    subTitle = serializers.CharField(max_length=500, required=False)
    titleOriginal = serializers.CharField(max_length=500, required=False)
    subTitleOriginal = serializers.CharField(max_length=500, required=False)
    isbn = serializers.CharField(max_length=100, required=False)
    isbn10 = serializers.CharField(max_length=100, required=False)
    itemTypeId = serializers.CharField(max_length=30, required=False)
    pages = serializers.IntegerField(required=False)
    volume = serializers.IntegerField(required=False)
    edition = serializers.IntegerField(required=False)
    publishedAt = serializers.DateTimeField(required=False)
    publishedOriginalAt = serializers.DateTimeField(required=False)
    serieId = serializers.IntegerField(required=False)
    serieName = serializers.CharField(max_length=200, required=False)
    collectionId = serializers.IntegerField(required=False)
    collectionName = serializers.CharField(max_length=250, required=False)
    publisherId = serializers.IntegerField(required=False)
    publisherName = serializers.CharField(max_length=250, required=False)
    formatId = serializers.CharField(max_length=30, required=False)
    languageId = serializers.CharField(max_length=200, required=False)
    languageName = serializers.CharField(max_length=200, required=False)
    coverPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    paidPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    


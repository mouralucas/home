from rest_framework import serializers

import core.serializers
import library.models


class AutorSerializer(core.serializers.DynamicFieldsModelSerializer):
    nm_idioma = serializers.SerializerMethodField()
    nm_pais = serializers.SerializerMethodField()

    @staticmethod
    def get_nm_idioma(instance):
        idioma = instance.idioma.nm_descritivo if instance.idioma else '--'
        return idioma

    @staticmethod
    def get_nm_pais(instance):
        return instance.pais.nome if instance.pais else '--'

    class Meta:
        model = library.models.Author
        fields = '__all__'


class SerieSerializer(core.serializers.DynamicFieldsModelSerializer):
    class Meta:
        model = library.models.Serie
        fields = '__all__'


class EditoraSerializer(core.serializers.DynamicFieldsModelSerializer):
    class Meta:
        model = library.models.Publisher
        fields = '__all__'


class LivroSerializer(core.serializers.DynamicFieldsModelSerializer):
    nm_autor_principal = serializers.SerializerMethodField()
    id_autor_principal = serializers.SerializerMethodField()
    nm_serie = serializers.SerializerMethodField()
    nm_editora = serializers.SerializerMethodField()

    @staticmethod
    def get_nm_autor_principal(instance):
        try:
            autor = instance.autor_principal.nm_completo
        except Exception as e:
            print(e)
            autor = None

        return autor

    @staticmethod
    def get_id_autor_principal(instance):
        try:
            autor = instance.autor_principal_id
        except Exception as e:
            print(e)
            autor = None

        return autor

    @staticmethod
    def get_nm_serie(instance):
        try:
            serie = instance.serie.nm_descritivo
        except Exception as e:
            print(e)
            serie = None

        return serie

    @staticmethod
    def get_nm_editora(instance):
        try:
            editora = instance.editora.nome
        except Exception as e:
            print(e)
            editora = None

        return editora

    @staticmethod
    def get_nm_colecao(instance):
        try:
            nm_colecao = instance.colecao.nome
        except Exception as e:
            print(e)
            nm_colecao = None

        return nm_colecao

    class Meta:
        model = library.models.Item
        fields = '__all__'
        # read_only_fields = fields



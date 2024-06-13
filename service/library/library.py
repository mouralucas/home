from django.db.models import F, Case, When, BooleanField
from django.utils.translation import gettext_lazy as _
from rest_framework import status

import core.models
import library.models
import util.Format
import util.datetime
from library.requests.item import ItemPostRequest
from library.responses.item import ItemPostResponse


class Library:
    def __init__(self, item_id=None, item=None, item_type=None, owner=None, request=None):
        self.item_id = item_id
        self.item = item
        self.item_type = item_type
        self.owner = owner
        self.request = request

    def set_item(self, data: ItemPostRequest = None, request=None):
        """
        :Name: set_item
        :description: Atualiza o status do item
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        :param data: The request data, describe in ItemPostRequest
        :param request: Request

        Implicit params (passed in the class instance or set by other functions):
        :param self.item_id: The id of the item
        """
        if self.item_id is None:
            item = library.models.Item()
        else:
            item = library.models.Item.objects.filter(pk=self.item_id).first()
            if not item:
                item = library.models.Item()

        item.main_author_id = data.validated_data.get('mainAuthorId')
        item.title = data.validated_data.get('title')
        item.subtitle = data.validated_data.get('subtitle')
        item.title_original = data.validated_data.get('titleOriginal')
        item.subtitle_original = data.validated_data.get('subtitleOriginal')
        item.isbn = util.Format.clean_numeric(data.validated_data.get('isbnFormatted'))
        item.isbn_formatted = data.validated_data.get('isbnFormatted')
        item.isbn10 = util.Format.clean_numeric(data.validated_data.get('isbn10Formatted'))
        item.isbn10_formatted = data.validated_data.get('isbn10Formatted')
        item.type = data.validated_data.get('itemType')
        item.pages = data.validated_data.get('pages')
        item.volume = data.validated_data.get('volume')
        item.edition = data.validated_data.get('edition')
        item.publication_date = data.validated_data.get('publishedAt')
        item.original_publication_date = data.validated_data.get('publishedOriginalAt')
        item.serie_id = data.validated_data.get('serieId')
        item.collection_id = data.validated_data.get('collectionId')
        item.publisher_id = data.validated_data.get('publisherId')
        item.format = data.validated_data.get('itemFormat')
        item.language_id = data.validated_data.get('languageId')
        item.cover_price = data.validated_data.get('coverPrice')
        item.paid_price = data.validated_data.get('paidPrice')
        item.dimensions = data.validated_data.get('dimensions')
        item.height = data.validated_data.get('height')
        item.width = data.validated_data.get('width')
        item.thickness = data.validated_data.get('thickness')
        item.summary = data.validated_data.get('summary')
        item.last_status_date = data.validated_data.get('lastStatusAt')
        item.owner_id = self.owner
        item.save(request_=request)

        self.__update_status(item=item, status=data.validated_data.get('lastStatusId'), date=data.validated_data.get('lastStatusAt'), is_update=False, request=request)

        self.__set_author(item=item, author_list=data.validated_data.get('mainAuthorId'), is_main=True)
        self.__set_author(item=item, author_list=[])

        response = ItemPostResponse({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'item': {
                'itemId': item.pk
            },
        }).data

        return response

    def get_item(self, is_unique=False):
        """
        :Name: get_item
        :descrição: Atualiza o status do item
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        :param is_unique: Return the object/reference of the model if true, return the queryset if false

        Implicit params (passed in the class instance or set by other functions):
        :param self.item_type: The type of the item (book, manga, etc)
        :param self.item_id: The id of the item
        """
        filters = {
            'owner_id': self.owner
        }

        if self.item_type:
            filters['type'] = self.item_type

        if self.item_id:
            filters['id'] = self.item_id

        item = library.models.Item.objects.values('title', 'subtitle', 'pages', 'volume', 'edition', 'dimensions', 'height', 'width',
                                                  'thickness', 'summary').filter(**filters) \
            .annotate(itemId=F('id'),
                      titleOriginal=F('title_original'),
                      subtitleOriginal=F('subtitle_original'),
                      mainAuthorName=F('main_author__nm_full'),
                      mainAuthorId=F('main_author_id'),
                      isbn=F('isbn'),
                      isbnFormatted=F('isbn_formatted'),
                      isbn10=F('isbn10'),
                      isbnFormatted10=F('isbn10_formatted'),
                      serieName=F('serie__name'),
                      serieId=F('serie_id'),
                      collectionName=F('collection__name'),
                      collectionId=F('collection_id'),
                      publisherName=F('publisher__name'),
                      publisherId=F('publisher_id'),
                      publishedAt=F('published_at'),
                      originalPublishedAt=F('published_original_at'),
                      lastStatusName=F('last_status__name'),
                      lastStatusId=F('last_status_id'),
                      lastStatusAt=F('last_status_at'),
                      itemType=F('type'),
                      itemFormatId=F('format'),
                      languageName=F('language__name'),
                      languageId=F('language_id'),
                      coverPrice=F('cover_price'),
                      paidPrice=F('paid_price'),
                      createdAt=F('created_at'),
                      lastEditedAt=F('edited_at')
                      ).order_by('title', 'volume')

        if is_unique:
            item = item.first()

        response = {
            'success': True,
            'items': list(item) if not is_unique else item
        }

        return response

    def get_item_authors(self, ids=False, is_selected=False, is_translator=False):
        """
        :Nome da classe/função: get_item_authors
        :descrição: Get the authors from a specifc item
        :Criação: Lucas Penha de Moura - 03/09/2021
        :Edições:
            Motivo:
        :param is_selected: When true return all registered authors and set the flag selected for main author and others
        :param is_translator
        :return:
        """
        item_authors = library.models.ItemAuthor.objects.filter(item_id=self.item_id)

        main_author = list(item_authors.values_list('author_id', flat=True).filter(is_main=True))
        other_author = list(item_authors.values_list('author_id', flat=True).filter(is_main=False))

        authors = library.models.Author.objects.values('id').filter(is_translator=is_translator) \
            .annotate(nm_full=F('nm_full'),
                      is_main_author_selected=Case(
                          When(id__in=main_author, then=True),
                          default=False,
                          output_field=BooleanField()
                      ),
                      is_other_author_selected=Case(
                          When(id__in=other_author, then=True),
                          default=False,
                          output_field=BooleanField()
                      ))

        response = {
            'success': True,
            'description': None,
            'authors': list(authors),
        }

        return response

    @staticmethod
    def get_status(selected_id=None):
        """
        :Name: get_status
        :Description: Get all the possible item status
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        :param selected_id: The id of selected status when editing a item

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        campos = ['id', 'name']

        status = core.models.Status.objects.values(*campos) \
            .filter(type='LIBRARY_ITEM').active() \
            .annotate(is_selected=Case(When(id=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField())) \
            .order_by('order')

        if not status:
            response = {
                'success': False,
                'descricao': 'Nenhuma status encontrado'
            }
            return response

        response = {
            'success': True,
            'status_livros': list(status)
        }

        return response

    def get_types(self, selected_id=None):
        item_types = [{'value': i[0], 'text': i[1], 'is_selected': True if i[0] == selected_id else False} for i in library.models.Item.ItemType.choices]

        response = {
            'success': True,
            'qtd': len(item_types),
            'types': item_types
        }

        return response

    def get_formats(self):
        """
        :Name: get_formats
        :Description: Get all the possible formats
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        formats = [{'value': i[0], 'text': i[1]} for i in library.models.Item.FormatType.choices]

        response = {
            'success': True,
            'qtd': len(formats),
            'formats': formats
        }

        return response

    @staticmethod
    def get_collection():
        """
        :Name: get_collection
        :Description: Get all the item collections
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        collections = library.models.Collection.objects.values('id', 'name', 'description').order_by('name')

        if not collections:
            response = {
                'success': False,
                'description': 'Nenhuma coleção encontrado'
            }
            return response

        response = {
            'success': True,
            'collections': list(collections),
        }

        return response

    def set_collection(self):
        pass

    def get_serie(self):
        """
        :Name: get_series
        :Description: Get all the item series
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None
        """

        series = library.models.Serie.objects.values('id', 'name', 'nm_original', 'description').annotate(
            serie_id=F('id'),
            country_id=F('country_id'),
            nm_country=F('country__name')
        ).active().order_by('name')

        if not series:
            response = {
                'success': False,
                'description': _('Nenhuma série encontrada')
            }
            return response

        response = {
            'success': True,
            'series': list(series)
        }

        return response

    def set_serie(self, serie=None, serie_id=None, name=None, nm_original=None, description=None, country_id=None, request=None):
        if serie_id is None:
            serie = library.models.Serie()
        else:
            serie = library.models.Serie.objects.filter(pk=serie_id).first()
            if not serie:
                serie = library.models.Serie()

        serie.name = name.strip() if name else None
        serie.nm_original = nm_original.strip() if nm_original else None
        serie.description = description if description not in ('', None, 'null') else None
        serie.country_id = country_id
        serie.save(request_=request)

        response = {
            'success': True,
            'serie': self.get_serie(),
        }

        return response

    @staticmethod
    def get_publishers(selected_id=None):
        """
        :Name: get_publishers
        :Description: Get all the item publishers
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        :param selected_id: The id of selected status when editing a item

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        publishers = library.models.Publisher.objects.values('id', 'name', 'description').active() \
            .annotate(publisher_id=F('id'),
                      nm_country=F('country__name'),
                      country_id=F('country_id')).order_by('name')

        if not publishers:
            response = {
                'success': False,
                'description': _('Nenhuma editora encontrada')
            }
            return response

        response = {
            'success': True,
            'publishers': list(publishers)
        }

        return response

    def set_publisher(self, name, description=None, country_id=None, parent_id=None, publisher_id=None, request=None):
        publisher = library.models.Publisher.objects.filter(pk=publisher_id).first()

        if not publisher:
            publisher = library.models.Publisher()

        publisher.name = name
        publisher.description = description
        publisher.country_id = country_id if country_id != 'null' else None
        publisher.parent_id = parent_id if parent_id != 'null' else None
        publisher.save(request_=request)

        response = {
            'success': True,
            'publisher_id': publisher.pk
        }

        return response

    @staticmethod
    def __update_status(item, status, date, is_update=True, request=None):
        """
        :Name: __update_status
        :Description: Update item status and add new register in itemStatus
        :Created by: Lucas Penha de Moura - 08/09/2021
        :Edited by:

        Explicit params:
        :param item: Item object
        :param date: The date that occur the new status
        :param status: The new status
        :param is_update: Update the dat_last_edited and last_edited_by in correspondent table
        :param request: Request
        :return: Update status

        Implicit params (passed in the class instance or set by other functions):
        None
        """

        try:
            current_status = library.models.ItemStatus.objects.filter(item=item).order_by('-date').first()
            if not current_status or status != current_status.log_status_id:
                new_status = library.models.ItemStatus(
                    log_status_id=status,
                    item=item,
                    date=date
                )
                new_status.save(request_=request, is_update=False)

                if item:
                    item.last_status_id = status
                    item.save(request_=request, is_update=is_update)

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def __set_author(item=None, author_list=None, is_main=False):
        """
        :Name: __set_author
        :Description: Create the relation between item and author
        :Created by: Lucas Penha de Moura - 10/09/2021
        :Edited by:

        Explicit params:
        :param item: Item object
        :param author_list: List of authors
        :param is_main: Indicates if is the main author of the item

        Implicit params (passed in the class instance or set by other functions):
        None

        :return: True if all operation succeeds, False otherwise
        """
        if not isinstance(author_list, list):
            author_list = [author_list]

        item_author = []
        library.models.ItemAuthor.objects.filter(item=item, is_main=is_main).delete()
        for index, i in enumerate(author_list):
            if i != 0 and i != '0':
                aux = library.models.ItemAuthor(
                    item=item,
                    author_id=i,
                    is_main=is_main
                )
                item_author.append(aux)
        library.models.ItemAuthor.objects.bulk_create(item_author)

        return True

from django.db.models import F
from django.utils.translation import gettext_lazy as _

import BO.person.person
import library.models


class Author(BO.person.person.Person):
    def __init__(self, author_id=None):
        super(Author, self).__init__()
        self.author_id = author_id

    def set_author(self, nm_full=None, dat_birth=None, language_id=None, country_id=None, is_translator=False, description=None, request=None):
        if not self.author_id:
            author = library.models.Author()
        else:
            author = library.models.Author.objects.filter(pk=self.author_id).first()

        self.nm_full = nm_full
        self._name_handler()

        author.nm_full = self.nm_full
        author.nm_first = self.nm_first
        author.nm_last = self.nm_last
        author.language_id = language_id
        author.country_id = None
        author.description = description
        author.dat_birth = dat_birth
        author.is_translator = is_translator
        author.save(request_=request)

        response = {
            'status': True,
            'description': _('Autor cadastrado com sucesso.'),
            'authors': self.get_author().get('authors'),
        }

        return response

    def get_author(self, is_translator=False):
        authors = library.models.Author.objects.filter(is_translator=is_translator) \
            .values('id').annotate(nm_full=F('nm_full'),
                                   dat_birth=F('dat_birth'),
                                   nm_language=F('language__name'),
                                   nm_country=F('country__name')).order_by('nm_full')

        if not authors:
            response = {
                'status': False,
                'description': _('Nenhum autor encontrado')
            }
            return response

        response = {
            'status': True,
            'authors': list(authors)
        }

        return response

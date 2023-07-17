import warnings

from django.db.models import Case, When, BooleanField, F
from django.utils.translation import gettext_lazy as _

import core.models
import core.serializers
from decouple import config

class Misc:
    def __init__(self):
        pass

    @staticmethod
    def get_language(campos=None, selected_id=None):
        if campos is None:
            campos = ['id', 'name']

        languages = core.models.Language.objects.values(*campos).order_by('name')

        if not languages:
            response = {
                'status': False,
                'descricao': 'Nenhum idioma encontrado'
            }
            return response

        response = {
            'status': True,
            'languages': list(languages)
        }

        return response

    def get_country(self, campos=None):
        if campos is None:
            campos = ['id', 'name']

        contries = core.models.Country.objects.order_by('id')

        if not contries:
            response = {
                'status': False,
                'description': _('Nenhum país encontrado')
            }
            return response

        response = {
            'status': True,
            'countries': core.serializers.PaisSerializer(contries, many=True, fields=campos).data
        }

        return response

    def get_currency(self):
        warnings.warn("Use new function getCurrency in finance service", DeprecationWarning, stacklevel=2)
        currency = [{'value': i[0], 'text': i[1]} for i in core.models.CurrencyTypes.choices]

        response = {
            'status': True,
            'qtd': len(currency),
            'currency': currency
        }

        return response

    def get_category(self, show_mode, module_id):
        """
        :Name: get_category
        :Description: Save the information about a category
        :Created by: Lucas Penha de Moura - 14/08/2022
        :Edited by:

        Explicit params:
        :param show_mode: Indicate the requested return, father, children or all
                            -- father - return only the father categories
                            -- children - return only the children categories
                            -- all - return all categories
        :param module_id: The module of the categories
        :param selected_id: The id of selected category, returned as True in the json

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        if show_mode not in ['all', 'father', 'child']:
            return {
                'status': False,
                'description': _('Show mode dever ser uma das três opções: all, father ou child')
            }

        filters = {
            'module_id': module_id
        }

        if show_mode != 'all':
            filters['father_id__isnull'] = True if show_mode == 'father' else False

        categories = core.models.Category.objects.values('id', 'name', 'description', 'comments').active() \
            .filter(parent__status=True)\
            .annotate(id_father=F('parent_id'),
                      nm_father=F('parent__name')).filter(**filters).order_by('order')

        response = {
            'status': True,
            'categories': list(categories)
        }

        return response

    def set_category(self, id_category, name=None, module_id=None, description=None, comments=None, request=None):
        """
        :Name: set_category
        :Description: Save the information about a category
        :Created by: Lucas Penha de Moura - 13/08/2022
        :Edited by:

        Explicit params:
        :param id_category: The id of the category
        :param name: The name of the category
        :param module_id: The id of the module of the category
        :param description: The description of the category
        :param comments: The comments about the category
        :param request: The request

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        if not id_category:
            return {
                'status': False,
                'description': 'É necessário informar um id'
            }

        category = core.models.Category.objects.filter(pk=id_category).first()
        if not category:
            category = core.models.Category()
            category.id = id_category

        category.name = name
        category.description = description
        category.comments = comments
        category.module_id = module_id
        category.save(request_=request)

        response = self.get_category(module_id=module_id, show_mode='all')

        return response

    def get_module(self, id_selected='', is_father=None):
        modules = core.models.Module.objects.values('id', 'name') \
            .annotate(is_selected=Case(When(id=id_selected, then=True),
                                       default=False,
                                       output_field=BooleanField()),
                      id_father=F('father_id'),
                      nm_father=F('father__name'))

        response = {
            'status': True,
            'modules': list(modules)
        }

        return response

    def get_states(self, id_selected=''):
        states = core.models.State.objects.values('id', 'name', 'code') \
            .annotate(country=F('country__name'))

        response = {
            'status': True,
            'states': list(states)
        }

        return response

    def get_status(self, status_type):
        """
        :Name: get_status
        :Description: Get all the possible item status
        :Created by: Lucas Penha de Moura - 23/07/2022
        :Edited by:

        Explicit params:
        :param status_type: the type of status one of: []

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        status = core.models.Status.objects.values('id', 'name', 'description', 'order', 'image', 'type') \
            .filter(type=status_type).order_by('order')

        if not status:
            response = {
                'status': False,
                'descricao': _('Nenhum status encontrado')
            }
            return response

        response = {
            'success': True,
            'status': list(status)
        }

        return response

    def get_version(self):
        return {
            'status': True,
            'version': '0.0.1',
            'environment': config('ENV_NAME')
        }

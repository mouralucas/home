from django.utils.translation import gettext_lazy as _


class Person:
    """
        :Name: Trainer
        :Created by: Lucas Penha de Moura - 16/06/2022
        :Edited by:

            service to handle information about a Person
        """

    def __init__(self, nm_full=None, person_id_formatted=None, id_type=None):
        self.nm_full = nm_full
        self.nm_first = ''
        self.nm_last = ''
        self.person_id_formatted = person_id_formatted
        self.person_id = None
        self.id_type = id_type

    def _id_handler(self):
        """
        :Name: _process_id_type
        :Created by: Lucas Penha de Moura - 16/06/2022
        :Edited by:

            Handles the id thas was passed to register, if it is not valid returns and show a error message
        """
        response = {
            'status': False,
            'description': None,
            'type': None,
            'id': None
        }
        if self.id_type == 'cpf':
            try:
                # TODO validate the len of the id CPF = 11
                self.person_id = self.person_id_formatted.replace('.', '').replace('-', '').replace('/', '')
                self.person_id = int(self.person_id)

            except Exception as e:
                self.person_id = None

        elif self.id_type == 'passport':
            try:
                passport = self.person_id_formatted.replace('.', '').replace('-', '').replace('/', '')

                response['status'] = True
                response['type'] = self.id_type
                response['id'] = passport
            except Exception as e:
                self.person_id = None

        else:
            self.person_id = None

        return response

    def _name_handler(self):
        try:
            self.nm_full = self.nm_full[:200].strip()
            aux = self.nm_full.split()
            if len(aux) > 1:
                self.nm_first = aux[0]
                self.nm_last = aux[len(aux) - 1]
            elif len(aux) == 1:
                self.nm_first = aux[0]

        except Exception as e:
            # TODO: raise exception?
            return False

    def _cell_handler(self):
        pass
        # try:
        #     numero_completo = numero.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        #
        #     # pega o ddd por uma expressão regular
        #     numero_ddd = re.search(r'^.*?\([^\d]*(\d+)[^\d]*\).*$', numero)
        #
        #     # Pga apenar o primeiro grupo, caso tenha algo na expressão regular
        #     if numero_ddd is not None and len(numero_ddd.groups()) > 0:
        #         numero_ddd = numero_ddd.groups()[0]
        #
        #     # numero sem o ddd
        #     numero_numero = numero_completo.replace(numero_ddd, '', 1) if numero_ddd is not None else numero_completo
        #     return True, '', numero_completo, numero_ddd, numero_numero
        # except:
        #     return False, 'telefone_invalido', None, None, None
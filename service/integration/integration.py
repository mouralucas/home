import requests
import json
import unicodedata

import core.models
import core.log.models


class Integration:
    """
    :Name: Integration
    :Description: Implements the "requests" library
    :Created by: Lucas Penha de Moura - 24/08/2022
    :Edited by:
    """

    def __init__(self, service, body=None, params=None, headers=None, request=None):
        self.url = None
        self.user = None
        self.password = None

        self.service = service

        self.status_code = None
        self.body = body
        self.params = params
        self.headers = headers
        self.response = None

        self.request = request
        self.response_text = None

    def save_log(self):
        try:
            new_log = core.log.models.ApiIntegration(
                service=self.service,
                url=self.url,
                body=self.body,
                params=self.params,
                headers=self.headers,
                status_code=self.status_code,
                response=self.response,
            )
            new_log.save(request_=self.request)
        except Exception as e:
            print(e)
        pass

    # def tratar_campo(self, campo=None):
    #     """
    #     :Nome da classe/função: tratar_campo
    #     :descrição: Função para tratar o campos para enviar para integração
    #     :Criação: Nícolas Marinoni Grande - 17/08/2020
    #     :Edições:
    #     :param campo: Valor a ser tratado
    #     :return: Valor tratado
    #     """
    #     if isinstance(campo, str) and campo is not None:
    #         campo = unicodedata.normalize('NFD', campo)
    #
    #     if isinstance(campo, Decimal):
    #         campo = float(campo)
    #
    #     return campo if campo is not None else ''

    def post(self, dumps=True, unicode=True, auth=None, json_content=False, parametros=None, ensure_ascii=False, timeout=15, verify=True):
        data = self.body
        if dumps:
            data = json.dumps(data, ensure_ascii=ensure_ascii)
        if unicode and isinstance(data, str):
            data = unicodedata.normalize('NFD', data).encode('ASCII', 'ignore')

        if not json_content:
            resposta = requests.post(self.url, data=data, headers=self.headers, params=parametros, auth=auth, timeout=timeout, verify=verify)
        else:
            resposta = requests.post(self.url, json=data, headers=self.headers, params=parametros, auth=auth, timeout=timeout, verify=verify)
        self.response = resposta.content
        self.status_code = resposta.status_code
        self.save_log()

    def get(self, dumps=False, auth=None):
        data = self.body
        if dumps:
            data = json.dumps(data)

        resposta = requests.get(self.url, headers=self.headers, data=data, auth=auth, params=self.params)
        self.response = resposta.content
        self.response_text = resposta.text
        self.status_code = resposta.status_code
        self.save_log()

    def delete(self):
        resposta = requests.delete(self.url, headers=self.headers, data=self.body)
        self.response = resposta.content
        self.status_code = resposta.status_code
        self.save_log()

    def put(self):
        resposta = requests.put(self.url, headers=self.headers, data=self.body)
        self.response = resposta.content
        self.status_code = resposta.status_code
        self.save_log()

    def patch(self, dumps=True, unicode=True, ensure_ascii=False):
        data = self.body
        if dumps:
            data = json.dumps(data, ensure_ascii=ensure_ascii)
        if unicode and isinstance(data, str):
            data = unicodedata.normalize('NFD', data).encode('ASCII', 'ignore')

        resposta = requests.patch(url=self.url, headers=self.headers, data=data)

        self.response = resposta.content
        self.status_code = resposta.status_code
        self.save_log()

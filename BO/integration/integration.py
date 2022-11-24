import requests


class Integration:
    """
    :Name: Integration
    :Description: Implements the "requests" library
    :Created by: Lucas Penha de Moura - 24/08/2022
    :Edited by:
    """
    def __init__(self):
        self.url = None
        self.user = None
        self.password = None

    def get(self):
        requests.get(url=self.url)

    def post(self):
        pass
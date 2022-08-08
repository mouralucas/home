import core.user.models


class Account:
    def __init__(self, username=None, raw_password=None):
        self.user = None
        self.username = username
        self.raw_password = raw_password

    def create(self):
        if not self.username:
            return {'status': False, 'description': ''}

        self.user = core.user.models.Account.objects.filter(pk=self.username)
        if self.user:
            return {'status': False, 'description': 'User already exists'}

        self.user = core.user.models.Account()
        self.user.username = self.username
        self.user.set_password(self.raw_password)
        self.user.save()

        print('')

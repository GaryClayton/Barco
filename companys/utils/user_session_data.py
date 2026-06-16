# defins a class to hold user session specific data

class UserState:
    def __init__(self, request):
        self.request = request

    #  -------- User Status ----------
    @property
    def name(self):
        return self.request.session.get('name')

    @name.setter
    def name(self, value):
        self.request.session['name'] = value

    @property
    def user_id(self):
        return self.request.session.get('user_id')

    @user_id.setter
    def user_id(self, value):
        self.request.session['user_id'] = value

    #  -------- Company Viewing Status ----------
    @property
    def last_company_viewed(self):
        return self.request.session.get('last_company_viewed')

    @last_company_viewed.setter
    def last_company_viewed(self, value):
        self.request.session['last_company_viewed'] = value

    #  -------- Charity Viewing Status ----------
    @property
    def last_charity_viewed(self):
        return self.request.session.get('last_charity_viewed')

    @last_charity_viewed.setter
    def last_charity_viewed(self, value):
        self.request.session['last_charity_viewed'] = value


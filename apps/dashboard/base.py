# test file for mako template:  libs/base_rander.py

from django.views import View
from libs.base_rander import render_to_resoponse
from django.contrib.auth import authenticate


class Index(View):
    def get(self, request):
        data = {'error': ''}
        if not authenticate(request.user):
            return render_to_resoponse(request, 'dashboard/auth/login.html', data=data)
        return render_to_resoponse(request, 'dashboard/index.html', data=data)

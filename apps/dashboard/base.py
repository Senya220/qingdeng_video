# test file for mako template:  libs/base_rander.py

from django.views import View
from libs.base_rander import render_to_resoponse


class Base(View):
    def get(self, request):
        return render_to_resoponse(request, 'dashboard/base.html')

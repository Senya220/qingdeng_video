from django.shortcuts import redirect, reverse
from django.views.generic import View
from django.contrib.auth import login, authenticate
from .base import render_to_resoponse
from django.contrib.auth.models import User


class Login(View):
    """
    get
    1. whether user has login
        1.login -> redirect to index
        2.redirect to login page

    post
    1.get username and password
    2.whether username is exists
    3.whether username and password is match
    4.whether user is superuser
    5.validate success then redirect to index

    username: administrator01,admin
    password: test@1234
    """

    def get(self, request):
        # html page show error info
        data = {'error': ''}
        if authenticate(request.user):
            return render_to_resoponse(request, 'dashboard/index.html', data=data)
        return render_to_resoponse(request, 'dashboard/auth/login.html', data=data)

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        exists = User.objects.filter(username=username)
        data = {}

        # validate user is exists in db
        if not exists:
            data['error'] = '用户名不存在'
            return render_to_resoponse(request, 'dashboard/auth/login.html', data=data)
        # verify username and password is match
        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码不正确'
            return render_to_resoponse(request, 'dashboard/auth/login.html', data=data)
        #
        if not user.is_superuser:
            data['error'] = '不是超级管理员'
            return render_to_resoponse(request, 'dashboard/auth/login.html', data=data)

        login(request, user)
        # 跳转到新路径，再由服务端匹配这个路由进入视图函数，再返回这个页面
        #奇怪的问题？ ： 路径跳转了，但还是显示登录页面
        return redirect(reverse('dashboard_index'))

        # # #路径不变 页面刷新到指定页面
        # return render_to_resoponse(request, 'dashboard/index.html', data=data)

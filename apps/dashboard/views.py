from django.shortcuts import redirect, reverse
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from .base import render_to_resoponse
from django.contrib.auth.models import User

#分页
from django.core.paginator import Paginator


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
        # 奇怪的问题？ ： 路径跳转了，但还是显示登录页面
        return redirect(reverse('dashboard_index'))

        # # #路径不变 页面刷新到指定页面
        # return render_to_resoponse(request, 'dashboard/index.html', data=data)

class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('dashboard_login'))

    def post(self, request):
        pass

class AdminManager(View):
    def get(self, request):
        if authenticate(request.user):
            users = User.objects.all()
            #获取当前页面的页数，默认是第一页
            page = request.GET.get('page', 1)
            #设置页面显示的数据量
            p = Paginator(users, 2)
            #获取总页数
            total_page = p.num_pages
            #防止用户输入负数页
            if int(page) <= 1:
                page = 1
            #获取当前页面对应的数据
            current_page = p.get_page(int(page)).object_list
            print(current_page)

            data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
            return render_to_resoponse(request, 'dashboard/auth/admin.html', data=data)
        else:
            return redirect(reverse('dashboard_login'))

    def post(self, request):
        pass

class UpdateAdminStatus(View):
    def get(self, request):
        status = request.GET.get('status', 'on')
        _status = True if status == 'on' else False
        user_id = request.GET.get('id', None)
        if user_id != None:
            user = User.objects.filter(pk=user_id).first()
            # #request.user判断，存在bug, 登录成功后只能对当前登录账号的权限进行修改，而不能对其他账号进行修改
            # request.user.is_superuser = _status
            #解决上面的bug
            user.is_superuser = _status
            user.save()
        return redirect(reverse('admin_manager'))


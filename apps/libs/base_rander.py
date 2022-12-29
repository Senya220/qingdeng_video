from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse


def render_to_resoponse(request, template,data=None):
    #context实例
    context_instance = RequestContext(request)
    #获取模板路径
    path = settings.TEMPLATES[0]['DIRS'][0]
    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8',
    )
    mako_template = lookup.get_template(template)

    if not data:
        data = {}

    #如果上下文实例存在则更新data，如果不存在则创建
    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)

    result = {}
    for d in context_instance:
        result.update(d)

    #设置csrf_token
    result['csrf_token'] = '<input type="hidden" name="csrfmiddlewaretoken", value="{}" />'.format(request.META.get('CSRF_COOKIE'))
    return HttpResponse(mako_template.render(**result))

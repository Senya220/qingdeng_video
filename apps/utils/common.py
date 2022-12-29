
def chekcAndGetVideoType(type_obj, type_value, message):
    """

    :param type_obj: type对象(用户传的对象)
    :param type_value: 数据库中存储的视频类型
    :param message:
    :return:
    """
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}
    return {'code': 0, 'msg': 'success'}
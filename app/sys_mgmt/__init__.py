"""
默认提供的基于角色的用户权限管理模块(RBAC)，
可以根据需要改写/替换
请参考 -http://zhangyiheng.com/blog/articles/py_flaskz_api.html#toc-mgmt
"""

import json

from flask import Blueprint
from flask_login import current_user

from .model import License
from ..main.errors import return_error

sys_mgmt_bp = Blueprint('sys_mgmt', __name__)


def log_operation(module, action, result, req_data=None, res_data=None, description=None):
    """
    Add operation logs to the database.
    :param module: The module of the operation.
    :param action: The action of the operation, add/delete/update.
    :param result: The result of the operation, success/fail.
    :param req_data: The request data of the operation.
    :param res_data: The result data of the operation.
    :param description: The description of the operation.
    :return:
    """
    if result is True:
        result = "success"
    elif result is False:
        result = "fail"

    if not is_str(req_data):
        req_data = json.dumps(req_data)

    if not is_str(res_data):
        res_data = json.dumps(res_data)

    log_data = _get_user_info()
    log_data.update({
        'module': _get_module_name(module),
        'action': action,
        'req_data': req_data,
        'res_data': res_data,
        'result': result,
        'description': description,
    })
    model.OPLog.add(log_data)


def request_check_by_license(current_license, req):
    """
    请求license校验
    """
    path = req.path
    # 页面静态资源不拦截
    if path == '/' or path.startswith('/libs') or path.endswith(('.js', '.css', '.html', '.png', '.svg', '.jpg', '.ico')):
        return
    if 'api' in path:
        # 根据具体项目进行定制
        if current_license is None:
            return return_error(('no_license', 'No License, Please Contact Cisco'), 555)
        # modules = license.get('Modules', "")
        # if 'template' in path:
        #     if "template" not in modules:
        #         return return_error(('no_license', 'No License, Please contact Cisco'), 555)


def load_license():
    """license加载函数"""
    license_result = License.query_all()
    license_list = []
    if license_result[0] is True:
        for item in license_result[1]:
            license_list.append(item.license)
    return license_list


def _get_user_info():
    if current_user.is_anonymous:
        return {
            'user_ip': get_remote_addr(),
        }
    return {
        'username': current_user.username,
        'user_name': current_user.name,
        'user_ip': get_remote_addr()
    }


def _get_module_name(module):
    module_name_mapping = get_app_cache('op_module_name_mapping')
    if module_name_mapping is None:
        module_name_mapping = {}
        menu_list = model.Menu.query_all()
        if menu_list[0] is True:
            for item in menu_list[1]:
                path = item.path
                if path:
                    module_name_mapping[path] = item.name
            set_app_cache('op_module_name_mapping', module_name_mapping)

    return module_name_mapping.get(module)


from flaskz.utils import get_remote_addr, get_app_cache, set_app_cache, is_str

# from . import errors
from . import _private
from . import router
from . import model
from ._init_db import init_db_data
from ._init_db import recover_admin

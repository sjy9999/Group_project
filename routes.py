# routes.py

from flask import Blueprint, render_template

class UserViews:
    # define 定义 Blueprint
    bp = Blueprint('user_views', __name__)

    @staticmethod
    @bp.route('/user')
    def user():
        # return student.html    这里可能会有一些逻辑来准备渲染页面所需的数据
        return render_template('student.html')

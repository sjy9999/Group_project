# routes.py

from flask import Blueprint, render_template

class UserViews:
    # define  Blueprint
    bp = Blueprint('user_views', __name__)

    @staticmethod
    @bp.route('/user')
    def user():
        # return student.html
        return render_template('student.html')

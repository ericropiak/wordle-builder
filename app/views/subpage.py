from flask import Blueprint, render_template

subpage = Blueprint('subpage', __name__)


@subpage.route('/', methods=['GET'])
def home():
    return render_template('subpage/home.html', context_var='Hey there good job!')

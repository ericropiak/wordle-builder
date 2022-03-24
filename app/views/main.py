from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route('/generic-modal/', methods=['GET', 'POST'])
def generic_modal():
    text = request.args.get('text')
    title = request.args.get('title')

    return render_template('generic_modal.html', text=text, title=title)

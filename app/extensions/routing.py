from flask import jsonify


def next_url(url):
    return jsonify({'next_url': url})

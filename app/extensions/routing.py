from flask import jsonify, request


def next_url(url):
    if request.args.get('next_url'):
        return jsonify({'next_url': request.args['next_url']})
    return jsonify({'next_url': url})

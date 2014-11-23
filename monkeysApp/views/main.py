from flask import Blueprint, make_response

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='../templates')


@main_blueprint.route('/', methods=['GET'])
def index():
    return "Hello world!"

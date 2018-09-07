import sys, os
from flask import jsonify, request, Blueprint

from . import app
from .git_profile import GitProfile
from .github import GithubApiError
from .bitbucket import BitbucketApiError

profiles = Blueprint('profiles', __name__)


@app.route('/profiles', methods=['GET'])
def get_profile():
    gh_username = request.args.get('gh')
    bb_username = request.args.get('bb')

    if not gh_username or not bb_username:
        return error('Please provide a Github and Bitbucket username', 400)

    try:
        profile = GitProfile(gh_username, bb_username).merged()
        return jsonify({
            'status': 'ok',
            'profile': profile,
        }), 200

    except Exception as e:
        if app.config['DEBUG']:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        if type(e) == GithubApiError:
            return error('Error occured trying to connect to Github API', 502)
        elif type(e) == BitbucketApiError:
            return error('Error occured trying to connect to Bitbucket API', 502)

        return error('An internal error occured', 500)


def error(message, status_code):
    return jsonify({
        'status': 'error',
        'message': message
    }), status_code

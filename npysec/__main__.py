from . import create_app

if __name__ == '__main__':
    # To run on werkzeug. Generally used for debug purpose.
    create_app().run(ssl_context='adhoc')

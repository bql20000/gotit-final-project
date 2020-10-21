from flask import Flask


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "development":
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.TestingConfig')
    print(f'ENV is set to: {app.config["ENV"]}')




    return app

import logging

from flask import Flask

from pets.controllers.auth import AuthController
from pets.controllers.report import ReportController
from pets.config import cfg_item, Config

class Webserver():

    @property
    def app(self) -> Flask:
        return self.__app
  
    @app.setter
    def app(self, app: Flask):
        self.__app = app
    
    def __init__(self) -> None:
        self.__app = Flask(__name__)
        self.__auth = AuthController()
        self.__report = ReportController()
        self.__register_blueprints()
        

    def __register_blueprints(self):
        with self.__app.app_context():
            self.__app.register_blueprint(self.__auth.authentication_blueprint,url_prefix="/auth2")
            self.__app.register_blueprint(self.__report.report_blueprint,url_prefix="/report")
       
    def run(self,host,port,debug=False):
        self.app.run(host=host,port=port,debug=debug)
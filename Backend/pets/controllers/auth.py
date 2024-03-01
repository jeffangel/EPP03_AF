import logging

from flask import Blueprint, request 
from flask import jsonify

from pets.models.auth import AuthModel

class AuthController():

    def __init__(self) -> None:
        self.__auth_blueprint = Blueprint("auth_blueprint", __name__)
        self.__auth_model = AuthModel()
        self.__register_blueprints()

    @property
    def authentication_blueprint(self) -> Blueprint:
        return self.__auth_blueprint

    def __register_blueprints(self):
        @self.__auth_blueprint.route("/login", methods=["POST","GET"])
        def __login():
            data = request.get_json()
            response = self.__auth_model.login_user(data)
            return response

        @self.__auth_blueprint.route("/register", methods=["POST"])
        def __register():
            data = request.get_json()
            response = self.__auth_model.register_user(data)
            return response
        
        @self.__auth_blueprint.route("/session", methods=["POST"])
        def __session():
            data = request.cookies.get('token','')
            response = self.__auth_model.check_user_session(data)
            return response
        
        @self.__auth_blueprint.route("/logout", methods=["POST"])
        def __logout():
            response = jsonify({"msg":"destroying_cookie"})
            response.set_cookie('token', expires=0)
            return response


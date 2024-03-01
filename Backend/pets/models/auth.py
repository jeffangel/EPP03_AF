import bcrypt
import jwt
import logging

from flask import jsonify

from pets.helpers.database import Database
from pets.config import cfg_item

class AuthModel():

    def __init__(self) -> None:
        self.__database = Database()
        self.__encoded_format = cfg_item("hash", "encoded_format")
        self.__encoded_algorithm = cfg_item("hash", "encoded_algorithm")
        self.__salt = cfg_item("hash", "salt")
        self.__secret = cfg_item("hash", "secret")
        self.__cookie_httponly = cfg_item("cookie", "httponly")
        self.__message : str
        self.__message_code: int
        self.__token = False
        logging.basicConfig(level=logging.DEBUG)

    def register_user(self, data: dict):
        try:
            self.__user_values = {"DNI", "NOMBRES", "APELLIDOPATERNO", "APELLIDOMATERNO", "CORREO", "CELULAR"}
            self.__user_info = tuple(value for key, value in data.items() if key in self.__user_values)
            self.__correo, self.__dni, self.__password = data.get('CORREO'), data.get('DNI'), data.get('CLAVE')
            self.__message, self.__message_code = self.__database.read_user(self.__correo, self.__dni)
            if not self.__database.user_exists:
                self.__hash_password()
                self.__user_info = self.__user_info + (self.__hashed_password,)
                self.__message, self.__message_code = self.__database.create_user(self.__user_info)
        except Exception as error:
            logging.error(error)
        finally:
            return jsonify({"msg": self.__message}), self.__message_code


    def login_user(self, data: dict):
        try:
            self.__correo, self.__password = data.get('CORREO'), data.get('CLAVE')
            self.__message, self.__message_code = self.__database.read_user_password(self.__correo)
            if self.__database.user_password_db:
                self.__hash_password()
                self.__compare_password()
                if self.__validation_password:
                    self.__generate_token()
                else:
                    self.__token = False
        except Exception as error:
            logging.error(error)
        finally:
            if self.__token:
                self.__create_cookie()
                return self.__response, self.__message_code 
            else:
                return jsonify({"msg": self.__message}), self.__message_code
    
    def __compare_password(self) -> None:
        try:
            self.__validation_password = self.__hashed_password == self.__database.user_password_db[0][0]
            if not self.__validation_password:
                self.__message, self.__message_code = "incorrect_password", 243
        except Exception as error:
            logging.error(error)
        
    def __hash_password(self) -> None:
        try:
            self.__byte_password = self.__password.encode(self.__encoded_format)
            self.__byte_salt = self.__salt.encode(self.__encoded_format) #bcrypt.gensalt()
            self.__hashed_password = bcrypt.hashpw(self.__byte_password, self.__byte_salt)
            self.__message = "password_hashed"
            self.__message_code = 200
        except Exception as error:
            logging.error(error)
    
    def __generate_token(self) -> None:
        try:
            self.__token = jwt.encode({'email': self.__correo}, self.__secret, algorithm=self.__encoded_algorithm)
        except Exception as error:
            logging.error(error)

    def __create_cookie(self) -> None:
        try:
            self.__message = "login_successfully"
            self.__message_code = 200
            self.__response = jsonify({"msg": self.__message})
            self.__response.set_cookie("token", self.__token, httponly=self.__cookie_httponly)
        except Exception as error:
            logging.error(error)

    def check_user_session(self,token):
        try:
            #self.__enconded_token = (token[6::])
            self.__enconded_token = token
            self.__user_email = jwt.decode(self.__enconded_token, self.__secret, algorithms=[self.__encoded_algorithm])
            self.__message = self.__user_email.get('email')
            self.__message_code = 200
        except Exception as error:
            self.__message = "invalid_token"
            self.__message_code = 200
            logging.error(error)
        finally:
            return jsonify({"msg": self.__message}), self.__message_code
        
    def __error(self):
        self.__message = "general_error"
        self.__message_code = 500
import logging

from flask import jsonify

from pets.helpers.database import Database
from pets.helpers.external import Imgbb

class ReportModel():

    def __init__(self) -> None:
        self.__database = Database()
        self.__imgbb = Imgbb()
        self.__message : str
        self.__message_code: int
        logging.basicConfig(level=logging.DEBUG)
    
    def register_case(self, case_data: dict):
        try:
            self.__data = case_data
            self.__case_values = {"FECHACASO", "FECHAEXTRAVIO", "CIUDAD", "CALLE", "DISTRITO", "REFERENCIA"}
            self.__report_info = tuple(value for key, value in self.__data.items() if key in self.__case_values)
            user_email = self.__data["EMAIL"]
            self.__message, self.__message_code = self.__database.create_case(self.__report_info, user_email)
            self.__register_pet()
            self.__register_features()
            self.__upload_image()
        except Exception as error:
            logging.error(error)
            return self.__error()
        finally:
            return jsonify({"msg": self.__message}), self.__message_code
    
    def __register_pet(self):
        try:
            self.__pet_values = {"NOMBRE", "RAZA", "COLOR", "SEXO", "OPERADO"}
            self.__pet_info = tuple(value for key, value in self.__data.items() if key in self.__pet_values)
            self.__message, self.__message_code = self.__database.add_pet(self.__pet_info)
        except Exception as error:
            logging.error(error)
            return self.__error()
    
    def __register_features(self):
        try:
            self.__features_info = self.__data.get("ESPECIFICACIONES")
            self.__message, self.__message_code = self.__database.add_feature(self.__features_info)
        except Exception as error:
            logging.error(error)
            return self.__error()

    def __upload_image(self):
        try:
            self.__images_info = self.__data.get("IMAGENES")
            self.__imgbb.upload_image(self.__images_info)
            if self.__imgbb.status_upload:
                self.__message, self.__message_code = self.__database.add_image(self.__imgbb.images_url)
        except Exception as error:
            logging.error(error)
            return self.__error()
        
    def get_case(self, case_num: int):
        try:
            if case_num:
                self.__message, self.__message_code = self.__database.read_case(case_num)
            else:
                self.__message, self.__message_code = self.__database.read_cases()
        except Exception as error:
            logging.error(error)
            return self.__error()
        finally:
            return jsonify({"cases": self.__message}), self.__message_code
            
    def __error(self):
        self.__message = "general_error"
        self.__message_code = 500
import logging

from flask import Blueprint, request 
from flask import jsonify

from pets.models.report import ReportModel

class ReportController():

    def __init__(self) -> None:
        self.__report_blueprint = Blueprint("report_blueprint", __name__)
        self.__report_model = ReportModel()
        self.__register_blueprints()

    @property
    def report_blueprint(self) -> Blueprint:
        return self.__report_blueprint

    def __register_blueprints(self):
        @self.__report_blueprint.route("/new", methods=["POST","GET"])
        def __new():
            case_data = request.get_json()
            response = self.__report_model.register_case(case_data)
            return response

        @self.__report_blueprint.route("/retrieve", methods=["GET"])
        def __retrieve():
            try:
                case_num = request.args.get('case_num',default=0, type =int)
                response = self.__report_model.get_case(case_num)
                return response
            except:
                return jsonify({"msg": "reports_retrieve"})    
    
                    


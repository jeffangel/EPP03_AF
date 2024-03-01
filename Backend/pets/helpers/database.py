from importlib import resources
import logging
from os.path import exists

import sqlite3

from pets.config import cfg_item

class Database():
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.__user_exists = False
        self.__user_password_db = ""
        with resources.path(cfg_item("database", "file","path"),cfg_item("database", "file","name")) as self.__database_path:
            if not exists(self.__database_path):
                self.__create_tables()

    def read_user(self, correo: str, dni: str):
        try:
            self.__create_cursor()
            self.__cursor.execute('SELECT CORREO FROM PERSONA WHERE CORREO=? OR DNI=?', (correo, dni,))
            if len(self.__cursor.fetchall()) > 0:
                self.__user_exists = True
                self.__close_cursor()
                return "user_exists", 200
            else:
                self.__user_exists = False
                self.__close_cursor()
                return "user_not_exists", 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243

    def read_user_password(self, correo: str):
        try:
            self.__create_cursor()
            self.__cursor.execute('SELECT CLAVE FROM PERSONA WHERE CORREO=?', (correo,))
            self.__user_password_db = self.__cursor.fetchall()
            if len(self.__user_password_db) > 0:
                self.__close_cursor()
                return "user_exists", 200
            else:
                self.__close_cursor()
                return "user_not_exists", 200

        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
    
    def create_user(self, user_info: tuple):
        try:
            self.__create_cursor()
            self.__cursor.execute('INSERT INTO PERSONA (DNI, NOMBRES, APELLIDOPATERNO, APELLIDOMATERNO, CORREO, CELULAR, CLAVE) VALUES (?,?,?,?,?,?,?)', user_info)
            self.__connection.commit()
            self.__close_cursor()
            return "user_created", 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
        
    def read_case(self, case_num: int):
        try:
            self.__cases_data = ()
            self.__create_cursor()
            self.__cursor.execute('SELECT * FROM CASO WHERE NUMCASO = ?', (case_num,))
            self.__cases = self.__cursor.fetchall()
            self.__connection.commit()
            self.__close_cursor()
            self.__read_pet()
            self.__read_contact()
            return self.__cases_data, 200
        
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
        
    def read_cases(self):
        try:
            self.__cases_data = ()
            self.__create_cursor()
            self.__cursor.execute('SELECT * FROM CASO')
            self.__cases = self.__cursor.fetchall()
            self.__connection.commit()
            self.__close_cursor()
            self.__read_pet()
            self.__read_contact()
            return self.__cases_data, 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
    
    def __read_contact(self) -> None:
        try:
            for i in range(len(self.__cases)):
                self.__contact_id = self.__cases[i][8]
                self.__create_cursor()
                self.__cursor.execute('SELECT CORREO, CELULAR FROM PERSONA WHERE DNI = ?', (self.__contact_id,))
                self.__contact_info = self.__cursor.fetchall()
                self.__cases_data[i][9]["contacto"] = self.__contact_info[0]
                self.__connection.commit()
                self.__close_cursor()
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
    
    def __read_pet(self) -> None:
        try:
            for i in range(len(self.__cases)):
                self.__cases_data += (self.__cases[i] + ({"contacto":(), "mascotas":()},),)
                num_caso = self.__cases[i][0]
                self.__create_cursor()
                self.__cursor.execute('SELECT * FROM MASCOTA WHERE NUMCASO = ?', (num_caso,))
                self.__mascotas = self.__cursor.fetchall()
                for mascota in self.__mascotas:
                    self.__cases_data[i][9]["mascotas"] += (mascota + ({"imagenes":(), "rasgos":()},),)
                self.__connection.commit()
                self.__close_cursor()
            self.__read_pet_images()
            self.__read_pet_features()
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
        
    def __read_pet_images(self) -> None:
        try:
            for i in range(len(self.__cases_data)):
                for j in range(len(self.__cases_data[i][9]["mascotas"])):
                    id_mascota = self.__cases_data[i][9]["mascotas"][j][0]
                    self.__create_cursor()
                    self.__cursor.execute('SELECT * FROM IMAGENES WHERE IDMASCOTA = ?', (id_mascota,))
                    self.__imagenes_mascotas = self.__cursor.fetchall()
                    self.__cases_data[i][9]["mascotas"][j][7]["imagenes"] = self.__imagenes_mascotas
                    self.__connection.commit()
                    self.__close_cursor()
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
        
    def __read_pet_features(self) -> None:
        try:
            for i in range(len(self.__cases_data)):
                for j in range(len(self.__cases_data[i][9]["mascotas"])):
                    id_mascota = self.__cases_data[i][9]["mascotas"][j][0]
                    self.__create_cursor()
                    self.__cursor.execute('SELECT * FROM RASGOS WHERE IDMASCOTA = ?', (id_mascota,))
                    self.__rasgos_mascotas = self.__cursor.fetchall()
                    self.__cases_data[i][9]["mascotas"][j][7]["rasgos"] = self.__rasgos_mascotas
                    self.__connection.commit()
                    self.__close_cursor()
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
        
    def create_case(self, case_info: tuple, user_email: str):
        try:
            self.__read_user_dni(user_email)
            case_info = case_info + self.__user_dni_db[0]
            self.__create_cursor()
            self.__cursor.execute('INSERT INTO CASO (FECHACASO, FECHAEXTRAVIO, CIUDAD, CALLE, DISTRITO, REFERENCIA, DNI) VALUES (?,?,?,?,?,?,?)', case_info)
            self.__connection.commit()
            self.__case_id = self.__cursor.lastrowid
            self.__close_cursor()
            return "case_created", 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
    
    def __read_user_dni(self, correo: str):
        try:
            self.__create_cursor()
            self.__cursor.execute('SELECT DNI FROM PERSONA WHERE CORREO=?', (correo,))
            self.__user_dni_db = self.__cursor.fetchall()

        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
            
    def add_pet(self, pet_info: tuple):
        try:
            pet_info = pet_info + (self.__case_id,)
            print(pet_info)
            self.__create_cursor()
            self.__cursor.execute('INSERT INTO MASCOTA (NOMBRE, RAZA, COLOR, SEXO, OPERADO, NUMCASO) VALUES (?,?,?,?,?,?)', pet_info)
            self.__connection.commit()
            self.__pet_id = self.__cursor.lastrowid
            self.__close_cursor()
            return "pet_added", 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243

    def add_image(self, images_info: tuple):
        try:
            self.__create_cursor()
            for image_info in images_info:
                image_info = (image_info, self.__pet_id,)
                self.__cursor.execute('INSERT INTO IMAGENES (ARCHIVO, IDMASCOTA) VALUES (?,?)', image_info)
                self.__connection.commit()
            self.__close_cursor()
            return "image_added", 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243
                
    def add_feature(self, features_info: tuple):
        try:
            self.__create_cursor()
            for feature_info in features_info:
                feature_info = (feature_info, self.__pet_id,)
                self.__cursor.execute('INSERT INTO RASGOS (ESPECIFICACIONES, IDMASCOTA) VALUES (?,?)', feature_info)
                self.__connection.commit()
            self.__close_cursor()
            return "features_added", 200
        except Exception as error:
            logging.error(error)
            self.__close_cursor()
            return type(error).__name__, 243

    def __create_cursor(self) -> None:
        self.__connection = sqlite3.connect(self.__database_path)
        self.__connection.execute("PRAGMA foreign_keys = 1")
        self.__cursor = self.__connection.cursor()

    def __close_cursor(self) -> None:
        self.__connection.close()

    @property
    def user_exists(self) -> bool:
        return self.__user_exists
    
    @property
    def user_password_db(self):
        return self.__user_password_db

    def __create_tables(self) -> None:
        self.__create_cursor()
        self.__cursor.execute("""
            CREATE TABLE "PERSONA" (
                "DNI"	TEXT,
                "NOMBRES"	TEXT NOT NULL,
                "APELLIDOPATERNO"	TEXT NOT NULL,
                "APELLIDOMATERNO"	TEXT NOT NULL,
                "CORREO"	TEXT NOT NULL,
                "CELULAR"	TEXT NOT NULL,
                "CLAVE"	TEXT NOT NULL,
                PRIMARY KEY("DNI")
            );
        """)

        self.__cursor.execute("""
            CREATE TABLE "CASO" (
                "NUMCASO"	INTEGER,
                "FECHACASO"	TEXT NOT NULL,
                "ESTADO"	TEXT NOT NULL DEFAULT 0,
                "FECHAEXTRAVIO"	TEXT NOT NULL,
                "CIUDAD"	TEXT NOT NULL,
                "CALLE"	TEXT NOT NULL,
                "DISTRITO"	TEXT NOT NULL,
                "REFERENCIA"	TEXT,
                "DNI"	TEXT NOT NULL,
                FOREIGN KEY("DNI") REFERENCES "PERSONA"("DNI"),
                PRIMARY KEY("NUMCASO" AUTOINCREMENT)
            );
        """)

        self.__cursor.execute("""
            CREATE TABLE "MASCOTA" (
                "IDMASCOTA"	INTEGER,
                "NOMBRE"	TEXT NOT NULL,
                "RAZA"	TEXT NOT NULL,
                "COLOR"	TEXT NOT NULL,
                "SEXO"	TEXT NOT NULL,
                "OPERADO"	TEXT NOT NULL,
                "NUMCASO"	INTEGER NOT NULL,
                PRIMARY KEY("IDMASCOTA" AUTOINCREMENT),
                FOREIGN KEY("NUMCASO") REFERENCES "CASO"("NUMCASO")
            );
        """)

        self.__cursor.execute("""
            CREATE TABLE "IMAGENES" (
                "IDIMAGEN"	INTEGER,
                "IDMASCOTA"	INTEGER NOT NULL,
                "ARCHIVO"	TEXT NOT NULL,
                FOREIGN KEY("IDMASCOTA") REFERENCES "MASCOTA"("IDMASCOTA"),
                PRIMARY KEY("IDIMAGEN" AUTOINCREMENT)
            );
        """)

        self.__cursor.execute("""
            CREATE TABLE "RASGOS" (
                "IDRASGO"	INTEGER,
                "IDMASCOTA"	INTEGER NOT NULL,
                "ESPECIFICACIONES"	TEXT NOT NULL,
                FOREIGN KEY("IDMASCOTA") REFERENCES "MASCOTA"("IDMASCOTA"),
                PRIMARY KEY("IDRASGO" AUTOINCREMENT)
            );
        """)

        self.__connection.commit()
        self.__close_cursor()

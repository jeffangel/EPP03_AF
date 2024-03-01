import logging

import requests

from pets.config import cfg_item

class Imgbb():

    def __init__(self) -> None:
        self.__imgbb_api_key = cfg_item("imgbb", "apikey")
        self.__imgbb_endpoint = "https://api.imgbb.com/1/upload"
        self.__status_upload = False
    
    def upload_image(self, images: list):
        self.__images_url = []
        try:
            for image in images:
                payload = {
                    "key": self.__imgbb_api_key,
                    "image": image
                }
                response = requests.post(self.__imgbb_endpoint, payload)
                response_json = response.json()
                print(response_json)
                self.__images_url.append(response_json.get("data").get("url"))
                self.__status_upload = True
                
        except Exception as error:
            self.__status_upload = False
            logging.error(type(error).__name__)
    
    @property
    def status_upload(self) -> bool:
        return self.__status_upload
    
    @property
    def images_url(self) -> list:
        return self.__images_url
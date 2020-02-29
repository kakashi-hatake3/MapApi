import requests


class MapAPI():
    def __init__(self):
        self.cords = ['135.232', '45.214']
        self.zoom = '15'
        self.mod = 0  # вид карты
        self.point = ['2003', '0828']  # метки нет

    def draw(self):  # обновляет файл с картой
        api_server = "http://static-maps.yandex.ru/1.x/"
        if self.mod % 3 == 0:
            map_kind = 'sat'
        elif self.mod % 3 == 1:
            map_kind = 'map'
        else:
            map_kind = 'skl'
        if self.point != ['2003', '0828']:
            params = {
                "ll": ",".join([self.cords[0], self.cords[1]]),
                "z": self.zoom,
                "l": map_kind,
                "pt": ','.join(self.point) + ',pm2dbl'
            }
        else:
            params = {
                "ll": ",".join([self.cords[0], self.cords[1]]),
                "z": self.zoom,
                "l": map_kind,
            }
        response = requests.get(api_server, params=params)
        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

    def find(self, find_object, postal_code):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                   "geocode=" + find_object + "&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            self.cords = toponym["Point"]["pos"].split()
            self.point = toponym["Point"]["pos"].split()
            self.draw()
            if postal_code:
                try:
                    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                        'metaDataProperty']["GeocoderMetaData"]["Address"]["formatted"] + ', ' + json_response[
                        "response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['metaDataProperty'][
                        "GeocoderMetaData"]["Address"]["postal_code"]
                except Exception as e:
                    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                        'metaDataProperty']["GeocoderMetaData"]["Address"]["formatted"]
            else:
                return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                    'metaDataProperty']["GeocoderMetaData"]["Address"]["formatted"]

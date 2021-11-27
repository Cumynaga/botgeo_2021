import requests

def get_cord(location):
    # Получаем координаты нужного места
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode="+location+"&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        found_ = (json_response["response"]['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])
        if not found_:
            print(12112)
            return None
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coodrinates = toponym["Point"]["pos"]
        #print(toponym_address, "имеет координаты:", toponym_coodrinates)
    else:
        return None

    coords = toponym_coodrinates.split()
    coodrs_url = toponym_coodrinates.replace(" ", ",")
    #print(coords, coodrs_url)
    return coodrs_url

def get_map(coodrs_url):
    # Получаем карту найденой местности
    map_request = "http://static-maps.yandex.ru/1.x/?ll="+coodrs_url+"&spn=0.0052,0.0052&l=sat"
    response = requests.get(map_request)
    if not response:
        return None

    return response.content



if __name__ == '__main__':
    location = input("Введите название места => ")
    coords = get_cord(location)
    print(coords)
    content = get_map(coords)
    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(content)

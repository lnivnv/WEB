import os
import pygame as pg
import requests

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = "37.588392,55.734036"

search_params = {
    "apikey": api_key,
    "text": 'яндекс',
    "lang": "ru_RU",
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass


# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2blywl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pg.init()
screen = pg.display.set_mode((600, 450))
screen.blit(pg.image.load(map_file), (0, 0))
pg.display.flip()


def main():
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        search_api_server = "https://search-maps.yandex.ru/v1/"
                        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

                        address_ll = "37.588392,55.734036"

                        search_params = {
                            "apikey": api_key,
                            "text": text,
                            "lang": "ru_RU",
                            "type": "biz"
                        }

                        response = requests.get(search_api_server, params=search_params)
                        if not response:
                            # ...
                            pass

                        # Преобразуем ответ в json-объект
                        json_response = response.json()

                        # Получаем первую найденную организацию.
                        organization = json_response["features"][0]
                        # Название организации.
                        org_name = organization["properties"]["CompanyMetaData"]["name"]
                        # Адрес организации.
                        org_address = organization["properties"]["CompanyMetaData"]["address"]

                        # Получаем координаты ответа.
                        point = organization["geometry"]["coordinates"]
                        org_point = "{0},{1}".format(point[0], point[1])
                        delta = "0.005"

                        # Собираем параметры для запроса к StaticMapsAPI:
                        map_params = {
                            # позиционируем карту центром на наш исходный адрес
                            "spn": ",".join([delta, delta]),
                            "l": "map",
                            # добавим точку, чтобы указать найденную аптеку
                            "pt": "{0},pm2dgl".format(org_point)
                        }

                        map_api_server = "http://static-maps.yandex.ru/1.x/"
                        # ... и выполняем запрос
                        response = requests.get(map_api_server, params=map_params)

                        map_file = "map.png"
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pg.image.load(map_file), (0, 0))
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                        screen.blit(pg.image.load(map_file), (0, 0))
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)
        pg.display.flip()
        clock.tick(30)


# Рисуем картинку, загружаемую из только что созданного файла.
while pg.event.wait().type != pg.QUIT:
    main()
    pg.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)

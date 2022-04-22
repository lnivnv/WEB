import os
import sys
import pygame as pg
import requests


def photo(text):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_server = "http://static-maps.yandex.ru/1.x/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    if text != '':
        print(1)
        search_params = {
            "apikey": api_key,
            "text": text,
            "lang": "ru_RU",
            "type": "biz"
        }
        response = requests.get(search_api_server, params=search_params)
        json_response = response.json()
        organization = json_response["features"][0]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        delta = "0.005"
        map_params = {
            "spn": ",".join([delta, delta]),
            "l": "map",
            "pt": "{0},pm2dgl".format(org_point)
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
    else:
        print(-1)
        delta = "0.002"
        lon = "37.123456"
        lat = "55.703118"
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response


map_file = "map.png"
r = photo('')
with open(map_file, "wb") as file:
    file.write(r.content)
pg.init()
screen = pg.display.set_mode((600, 450))
screen.blit(pg.image.load("map.png"), (0, 0))
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
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        map_file = "map.png"
                        r = photo(text)
                        with open(map_file, "wb") as file:
                            file.write(r.content)
                        screen.blit(pg.image.load("map.png"), (0, 0))
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                        map_file = "map.png"
                        r = photo('')
                        with open(map_file, "wb") as file:
                            file.write(r.content)
                        screen.blit(pg.image.load("map.png"), (0, 0))
                    else:
                        text += event.unicode
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)
        pg.display.flip()
        clock.tick(30)


while pg.event.wait().type != pg.QUIT:
    main()
    pg.quit()
os.remove(map_file)

import os
import sys
import pygame
import requests


def photo(text, s):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_server = "http://static-maps.yandex.ru/1.x/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    print(s)
    print(len(s))
    if text != '' or len(s) > 0:
        if len(s) > 0:
            if s.count('') == len(s):
                return photo('', [])
            if s[-1] == '':
                print(s)
                for elem in s:
                    if elem != '':
                        text = elem
                        continue
            else:
                text = s[-1]
                print(text)
        search_params = {
            "apikey": api_key,
            "text": text,
            "lang": "ru_RU",
            "type": "biz"
        }
        response = requests.get(search_api_server, params=search_params)
        try:
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
        except Exception as e:
            print("Ошибка выполнения запроса:")
            print(api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    else:
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
s = []
r = photo('', s)
with open(map_file, "wb") as file:
    file.write(r.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load("map.png"), (0, 0))
pygame.display.flip()
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
input_box = pygame.Rect(10, 10, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    map_file = "map.png"
                    s.append(text)
                    r = photo(text, s)
                    with open(map_file, "wb") as file:
                        file.write(r.content)
                    screen.blit(pygame.image.load("map.png"), (0, 0))
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    map_file = "map.png"
                    r = photo('', s)
                    with open(map_file, "wb") as file:
                        file.write(r.content)
                    screen.blit(pygame.image.load("map.png"), (0, 0))
                else:
                    text += event.unicode
    txt_surface = font.render(text, True, color)
    width = max(250, txt_surface.get_width() + 15)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.display.flip()
    clock.tick(30)

os.remove(map_file)

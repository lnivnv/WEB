import os
import sys
import pygame as pg
import requests

api_server = "http://static-maps.yandex.ru/1.x/"
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = "37.588392,55.734036"
delta = "0.002"

params = {
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map"
}
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(api_server)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pg.init()
screen = pg.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pg.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pg.display.flip()
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
                    search_params = {
                        "apikey": api_key,
                        "text": "ИИ глазных болезней",
                        "lang": "ru_RU",
                        "ll": address_ll,
                        "type": "biz"
                    }
                    response = requests.get(search_api_server, params=search_params)
                    if not response:
                        print("Ошибка выполнения запроса:")
                        print(api_server)
                        print("Http статус:", response.status_code, "(", response.reason, ")")
                        sys.exit(1)
                    map_file2 = "map.png"
                    pg.display.flip()
                    with open(map_file2, "wb") as file:
                        file.write(response.content)
                    map_file = map_file2
                    pg.display.flip()
                    text = ''
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pg.draw.rect(screen, color, input_box, 2)

    pg.display.flip()
    clock.tick(30)
os.remove(map_file)

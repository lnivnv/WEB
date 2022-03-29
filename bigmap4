import sys
import os
import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.02"
mapview = "map"


def api(delta, mapview):
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": mapview
    }
    return params


response = requests.get(api_server, params=api(delta, mapview))
if not response:
    print("Ошибка выполнения запроса:")
    print(api_server)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
sat = Button(10, 10, load_image('sat.jpg'), 0.8)
hyb = Button(30, 100, load_image('hyb.jpg'), 0.8)
map = Button(50, 170, load_image('map.jpg'), 0.8)
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        keys = pygame.key.get_pressed()
        if sat.draw(screen):
            mapview = "sat"
            response = requests.get(api_server, params=api(delta, mapview))
            if not response:
                print("Ошибка выполнения запроса:")
                print(api_server)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            with open(map_file, "wb") as file:
                file.write(response.content)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        if map.draw(screen):
            mapview = "map"
            response = requests.get(api_server, params=api(delta, mapview))
            if not response:
                print("Ошибка выполнения запроса:")
                print(api_server)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            with open(map_file, "wb") as file:
                file.write(response.content)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        if hyb.draw(screen):
            mapview = "skl"
            response = requests.get(api_server, params=api(delta, mapview))
            if not response:
                print("Ошибка выполнения запроса:")
                print(api_server)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            with open(map_file, "wb") as file:
                file.write(response.content)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        pygame.display.update()
        if keys[pygame.K_PAGEUP]:
            a = float(delta) + 0.01
            delta = str(a)
            if a < 90:
                response = requests.get(api_server, params=api(delta, mapview))
                if not response:
                    print("Ошибка выполнения запроса:")
                    print(api_server)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
        if keys[pygame.K_PAGEDOWN]:
            a = float(delta) - 0.01
            delta = str(a)
            if a > 0:
                response = requests.get(api_server, params=api(delta, mapview))
                if not response:
                    print("Ошибка выполнения запроса:")
                    print(api_server)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)

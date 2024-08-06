import pygame, sys, os


def load_image(name, colorkey=None):
    """
    A function for translating an image into the library's game format
    :param name: file path
    :param color_key: background color value
    :return:
    """
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image
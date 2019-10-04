# encoding: utf-8

import numpy, sys
import random

try:
    import pygame
except ImportError:
    print("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")


def make_array(rgb_array_: numpy.ndarray, alpha_: numpy.ndarray) -> numpy.ndarray:
    """
    This function is used for 24-32 bit pygame surface with pixel alphas transparency layer
    make_array(RGB array, alpha array) -> RGBA array
    Return a 3D numpy (numpy.uint8) array representing (R, G, B, A)
    values of all pixels in a pygame surface.
    :param rgb_array_: 3D array that directly references the pixel values in a Surface.
                       Only work on Surfaces that have 24-bit or 32-bit formats.
    :param alpha_:     2D array that directly references the alpha values (degree of transparency) in a Surface.
                       alpha_ is created from a 32-bit Surfaces with a per-pixel alpha value.
    :return:           Return a numpy 3D array (numpy.uint8) storing a transparency value for every pixel
                       This allow the most precise transparency effects, but it is also the slowest.
                       Per pixel alphas cannot be mixed with pygame method set_colorkey (this will have
                       no effect).
    """
    return numpy.dstack((rgb_array_, alpha_))


def make_surface(rgba_array: numpy.ndarray) -> pygame.Surface:
    """
    This function is used for 24-32 bit pygame surface with pixel alphas transparency layer
    make_surface(RGBA array) -> Surface
    Argument rgba_array is a 3d numpy array like (width, height, RGBA)
    This method create a 32 bit pygame surface that combines RGB values and alpha layer.
    :param rgba_array: 3D numpy array created with the method surface.make_array.
                       Combine RGB values and alpha values.
    :return:           Return a pixels alpha surface.This surface contains a transparency value
                       for each pixels.
    """
    return pygame.image.frombuffer((rgba_array.transpose([1, 0, 2])).copy(order='C').astype(numpy.uint8),
                                   (rgba_array.shape[:2][0], rgba_array.shape[:2][1]), 'RGBA').convert_alpha()



def rgb_split_channels_alpha(surface_ : pygame.Surface) -> pygame.Surface:
    """
        Extract channels RGBA of a pygame.Surface 32-24 bit and return
        Red channel, green channel and blue channel (all pygame surfaces)
        All channels will contains per-pixels information if the original image
        has been encoded with alpha transparency.
        Pygame surface converted to fast blit (method convert), will raise an exception.

        :param surface_: pygame.Surface, 32 - 24 bit image/texture to process,
        must be converted with the method convert_alpha())
        :return: pygame.Surface: Returns all channels (red, greenn, blue) as pygame surfaces with
        per-pixels information.
    
    """
    assert isinstance(surface_, pygame.Surface), \
           'Positional argument surface_ must be a pygame.Surface, got %s ' % type(surface_)
    rgb_array = pygame.surfarray.pixels3d(surface_)
    
    try:
        alpha_array = pygame.surfarray.pixels_alpha(surface_)
    except ValueError as e:
        # unsupported colormasks for alpha reference array
        print('Unsupported colormasks for alpha reference array.')
        raise ValueError('\nMake sure the surface_ contains per-pixel alpha transparency values.')
        
    
    # RED CHANNEL
    R = rgb_array[:, :, :].copy()
    R[:, :, 1:3] = 0
    R = numpy.dstack((R, alpha_array))
    # GREEN CHANNEL 
    G = rgb_array[:, :, :].copy()
    G[:, :, 0] = 0
    G[:, :, 2] = 0
    G = numpy.dstack((G, alpha_array))
    # BLUE CHANNEL 
    B = rgb_array[:, :, :].copy()
    B[:, :, 0:2] = 0
    B = numpy.dstack((B, alpha_array))
    # RETURN RGB, NO ALPHA VALUES
    return  make_surface(R),\
        make_surface(G),\
        make_surface(B)


def rgb_split_channels(surface_ : pygame.Surface) -> pygame.Surface:
    """
        Extract channels RGB of a pygame.Surface 32-24 bits and return
        Red channel, green channel and blue channel as pygame surfaces

        :param surface_: pygame.Surface (image/texture to process)
        :return: pygame.Surface: Returns all channels (red, greenn, blue) as pygame surfaces
        
        Note: only RGB channels are returns.
        If the pygame surface contains per-pixels data, it will be ignored in the
        resulting product.
    
    """
    assert isinstance(surface_, pygame.Surface), \
           'Positional argument surface_ must be a pygame.Surface, got %s ' % type(surface_)
    rgb_array = pygame.surfarray.pixels3d(surface_)
    # RED CHANNEL
    R = rgb_array[:, :, :].copy()
    R[:, :, 1:3] = 0
    # GREEN CHANNEL 
    G = rgb_array[:, :, :].copy()
    G[:, :, 0] = 0
    G[:, :, 2] = 0
    # BLUE CHANNEL 
    B = rgb_array[:, :, :].copy()
    B[:, :, 0:2] = 0
    # RETURN RGB, NO ALPHA VALUES
    return  pygame.surfarray.make_surface(R),\
        pygame.surfarray.make_surface(G),\
        pygame.surfarray.make_surface(B)

    
def red_channel(surface_: pygame.Surface) -> pygame.Surface:
    """
      Return the red channel (surface) from a pygame surface containing RGB(A) channels 34-24 bit,
      :param surface_: pygame.Surface, (image/texture containing RGB(A) channels
      :return pygame.Surface: return a pygame surface (red channel)
    """
    assert isinstance(surface_, pygame.Surface),\
           'Positional argument surface_ must be a pygame.Surface, got %s ' % type(surface_)
    rgba_array = pygame.surfarray.pixels3d(surface_)
    rgba_array[:, :, 1:3] = 0
    return pygame.surfarray.make_surface(rgba_array)


def green_channel(surface_: pygame.Surface) -> pygame.Surface:
    """
      Return the green channel (surface) from a pygame surface containing RGB(A) channels 32-24 bit,
      :param surface_: pygame.Surface, (image/texture containing RGB(A) channels
      :return pygame.Surface: return a pygame surface (green channel)
    """
    assert isinstance(surface_, pygame.Surface), \
           'Positional argument surface_ must be a pygame.Surface, got %s ' % type(surface_) 
    rgba_array = pygame.surfarray.pixels3d(surface_)
    rgba_array[:, :, 0] = 0
    rgba_array[:, :, 2] = 0
    return pygame.surfarray.make_surface(rgba_array)


def blue_channel(surface_: pygame.Surface) -> pygame.Surface:
    """
      Return the blue channel (surface) from a pygame surface containing RGB(A) channels 32-24 bit,
      :param surface_: pygame.Surface, (image/texture containing RGB(A) channels
      :return pygame.Surface: return a pygame surface (blue channel)
    """
    assert isinstance(surface_, pygame.Surface), \
           'Positional argument surface_ must be a pygame.Surface, got %s ' % type(surface_)
    rgba_array = pygame.surfarray.pixels3d(surface_)
    rgba_array[:, :, 0:2] = 0
    return pygame.surfarray.make_surface(rgba_array)


if __name__ == '__main__':
    numpy.set_printoptions(threshold=sys.maxsize)
    pygame.init()
    SCREENRECT = pygame.Rect(0, 0, 800, 800)
    screen = pygame.display.set_mode(SCREENRECT.size, pygame.HWSURFACE, 32)
    BACKGROUND = pygame.image.load('Assets\\Background.jpg').convert()
    BACKGROUND = pygame.transform.smoothscale(BACKGROUND, SCREENRECT.size)

    IMAGE = pygame.image.load('Assets\\Namiko1.png').convert_alpha()

    #red_surface = red_channel(IMAGE.copy())
    #green_surface = green_channel(IMAGE.copy())
    #blue_surface = blue_channel(IMAGE.copy())

    red_surface, green_surface, blue_surface = rgb_split_channels_alpha(IMAGE)

    All = pygame.sprite.Group()
    clock = pygame.time.Clock()

    TIME_PASSED_SECONDS = 0

    STOP_GAME = False

    FRAME = 0

    org = pygame.math.Vector2(SCREENRECT.w // 2 - IMAGE.get_width() // 2,
                              SCREENRECT.h // 2 - IMAGE.get_height() // 2)

    # pygame.key.set_repeat(1000, 10)

    while not STOP_GAME:
        pygame.event.pump()
        #screen.fill((0, 0, 0, 0))
        screen.blit(BACKGROUND, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Quitting')
                STOP_GAME = True
            if event.type == pygame.MOUSEMOTION:
                MOUSE_POS = event.pos

        keys = pygame.key.get_pressed()

        screen.blit(red_surface, org + pygame.math.Vector2(random.randint(0, 9),
                                                           random.randint(0, 15)), special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(green_surface, org + pygame.math.Vector2(random.randint(10, 15),
                                                             random.randint(0, 15)), special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(blue_surface, org + pygame.math.Vector2(random.randint(15, 25),
                                                            random.randint(0, 25)), special_flags=pygame.BLEND_RGB_ADD)

        TIME_PASSED_SECONDS = clock.tick(300)

        pygame.display.flip()
        FRAME += 1
        # life_ += 1
    pygame.quit()

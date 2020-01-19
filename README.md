# RGB-split
RGB split effect 

![alt text](https://github.com/yoyoberenguer/RGB-split/blob/master/im160x360.png)
![alt text](https://github.com/yoyoberenguer/RGB-split/blob/master/splitRGB.png)

```
Split R, G, B channels from a PNG file (loaded with pygame)

## BELOW CYTHON CODE 

# Returns separate channels R, G, B with per-pixel information
# Use pygame special_flags pygame.BLEND_RGB_ADD
# when bliting channels to your display (additive mode)
def rgb_split_channels_alpha(surface_: pygame.Surface):
    return rgb_split_channels_alpha_c(surface_)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef rgb_split_channels_alpha_c(surface_: pygame.Surface):

    assert isinstance(surface_, pygame.Surface), \
        '\nPositional argument surface_ must be a pygame.Surface, got %s ' % type(surface_)
    if surface_.get_width() == 0 or surface_.get_height() == 0:
        raise ValueError('\nIncorrect pixel size or wrong format.'
                         '\nsurface_ dimensions (width, height) cannot be null.')
    try:
        alpha_array = pygame.surfarray.pixels_alpha(surface_)
    except ValueError:
        # unsupported colormasks for alpha reference array
        print('\nUnsupported colormasks for alpha reference array.')
        raise ValueError('\nMake sure the surface_ contains per-pixel alpha transparency values.')

    width, height = surface_.get_size()
    zeros = numpy.zeros((height, width, 4), dtype=numpy.uint8)
    cdef:
        int w = width
        int h = height
        unsigned char [:, :, :] red_s = zeros
        unsigned char [:, :, :] green_s  = zeros.copy()
        unsigned char [:, :, :] blue_s = zeros.copy()
        unsigned char [:, :] red = pygame.surfarray.pixels_red(surface_)
        unsigned char [:, :] green = pygame.surfarray.pixels_green(surface_)
        unsigned char [:, :] blue = pygame.surfarray.pixels_blue(surface_)
        unsigned char [:, :] alpha = alpha_array
        unsigned char a
    # RED CHANNEL
    for i in range(w):
        for j in range(h):
          a = alpha[i, j]
          red_s[j, i, 0], red_s[j, i, 1], red_s[j, i, 2], red_s[j, i, 3] = red[i, j], 0, 0, a
          green_s[j, i, 0], green_s[j, i, 1], green_s[j, i, 2], green_s[j, i, 3] = 0, green[i, j], 0, a
          blue_s[j, i, 0], blue_s[j, i, 1], blue_s[j, i, 2], blue_s[j, i, 3] = 0, 0, blue[i, j], a
          
    return pygame.image.frombuffer(red_s, (w, h), 'RGBA'),\
           pygame.image.frombuffer(green_s, (w, h), 'RGBA'),\
           pygame.image.frombuffer(blue_s, (w, h), 'RGBA')
```

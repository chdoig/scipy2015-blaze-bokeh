import numpy as np

def hex_to_rgb(value):
    """Given a color in hex format, return it in RGB."""

    values = value.lstrip('#')
    lv = len(values)
    rgb = list(int(values[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return rgb 
 

class RGBAColorMapper(object):
    """Maps floating point values to rgb values over a palette"""
 
    def __init__(self, low, high, palette):
        self.range = np.linspace(low, high, len(palette))
        # self.r, self.g, self.b = np.array(zip(*[hex_to_rgb(i) for i in palette])) #python 2.7
        self.r, self.g, self.b = np.array(list(zip(*[hex_to_rgb(i) for i in palette])))
    
    def color(self, data):
        """Maps your data values to the pallette with linear interpolation"""

        red = np.interp(data, self.range, self.r)
        blue = np.interp(data, self.range, self.b)
        green = np.interp(data, self.range, self.g)
        # Style plot to return a grey color when value is 'nan'
        red[np.isnan(red)] = 240
        blue[np.isnan(blue)] = 240
        green[np.isnan(green)] = 240
        colors = np.dstack([red.astype(np.uint8),
                          green.astype(np.uint8),
                          blue.astype(np.uint8),
                          np.full_like(data, 255, dtype=np.uint8)])
        return colors.view(dtype=np.uint32).reshape(data.shape)
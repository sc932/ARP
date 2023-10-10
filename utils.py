import numpy

def polar_from_x_y(x_orig, y_orig, x_offset=0, y_offset=0):
    x = x_orig - x_offset # optionally subtract off mean, median, etc
    y = y_orig - y_offset
    r = numpy.sqrt(x**2 + y**2)
    theta = 0
    if r > 1e-8:
        if x > 0 and y > 0:
            theta = numpy.arctan(y / x)
        if x < 0 and y > 0:
            theta = numpy.pi - numpy.arctan(y / -x)
        if x > 0 and y < 0:
            theta = 2*numpy.pi - numpy.arctan(-y / x)
        if x < 0 and y < 0:
            theta = numpy.pi + numpy.arctan(-y / -x)
    else:
        r = 0
        theta = 0
    return r, theta
from basis_function import BasisFunction
import utils

import numpy
import matplotlib.pyplot as plt

import statsmodels.api as sm

class UpDownBasisFunction(BasisFunction):
    def __init__(self, basis_type="UpDownBasisFunction", function_shape=None):
        self.basis_type = basis_type # str, ie sawtooth 2 level
        if function_shape == None:
           raise(Exception)
        else:
            basis_vec = function_shape
        if len(basis_vec) != 4:
            raise Exception
        for basis in basis_vec:
            if basis not in [-1, 0, 1]:
                raise Exception
        self.function_shape = function_shape

    def csv_safe_shape(self):
       txt = "["
       for shape_param in self.function_shape:
          txt += str(shape_param)
          txt += ";"
       txt += "]"
       return txt

    def eval_from_x_y(self, x_orig, y_orig, x_offset=0, y_offset=0):
        _, theta = utils.polar_from_x_y(x_orig, y_orig, x_offset, y_offset)
        return self.eval(theta)
    
    def get_function_area(self):
        area = 0
        quadrant_areas = [0,0,0,0]
        for i in range(8):
            f0 = self.eval(0 + numpy.pi/4*i) + 1
            f1 = self.eval(0 + numpy.pi/4*(i+1)) + 1
            area += numpy.pi/4*0.5*(f0 + f1)
            quadrant_areas[int(numpy.floor(i/2))] += numpy.pi/4*0.5*(f0 + f1)
        return [area, quadrant_areas]

    def get_function_mass_angles(self):
        area, quadrant_areas = self.get_function_area()
        heavy_quads = []
        light_quads = []
        for i in range(4):
            if quadrant_areas[i] == max(quadrant_areas):
                heavy_quads.append(i)
            else:
                light_quads.append(i)
        
        if len(heavy_quads) == 1:
            return [numpy.pi/2.0*heavy_quads[0] + numpy.pi/4]
        elif len(heavy_quads) == 2:
            if abs(heavy_quads[0] - heavy_quads[1]) == 2: # symetric
                return [numpy.pi/2.0*heavy_quads[0] + numpy.pi/4, numpy.pi/2.0*heavy_quads[1] + numpy.pi/4]
                """
                if quadrant_areas[light_quads[0]] == quadrant_areas[light_quads[0]]:
                    return []
                    return None # perfectly symetric
                    # TODO, this has angular inertia
                elif quadrant_areas[light_quads[0]] > quadrant_areas[light_quads[0]]:
                    return [numpy.pi/2.0*light_quads[0] + numpy.pi/4]
                else:
                    return [numpy.pi/2.0*light_quads[1] + numpy.pi/4]
                """
            else:
                if 0 in heavy_quads and 3 in heavy_quads:
                    return [0]
                else:
                    return [numpy.pi/2.0*((heavy_quads[1] + heavy_quads[0])/2.0 + 0.5)]
        elif len(heavy_quads) == 3:
            return [numpy.pi/2.0*((light_quads[0] - 2)%3)  + numpy.pi/4] # reflect the light one
        else:
            return None # perfectly symmetric

    def eval(self, x):
        """A function defined on 0 to 2pi that linearly interpolates between -1 and 1 at [pi/4, 3pi/4, 5pi/4, 7pi/4]"""
        basis_vec = self.function_shape
        if x < 0 or x > 2*numpy.pi:
            raise Exception
        if x < numpy.pi/4:
            y = basis_vec[3] + (x + numpy.pi/4)*2*(basis_vec[0] - basis_vec[3])/numpy.pi
        elif x < 3*numpy.pi/4:
            y = basis_vec[0] + (x - numpy.pi/4)*2*(basis_vec[1] - basis_vec[0])/numpy.pi
        elif x < 5*numpy.pi/4:
            y = basis_vec[1] + (x - 3*numpy.pi/4)*2*(basis_vec[2] - basis_vec[1])/numpy.pi
        elif x < 7*numpy.pi/4:
            y = basis_vec[2] + (x - 5*numpy.pi/4)*2*(basis_vec[3] - basis_vec[2])/numpy.pi
        else:
            y = basis_vec[3] + (x - 7*numpy.pi/4)*2*(basis_vec[0] - basis_vec[3])/numpy.pi
        return y
    
    def plot(self, ax1, ax2, ax3, attribute_pair=None, attribute_pair_thetas=None, attribute_pair_rs=None, scores=None, goals=None):
        [x1, x2, x3, x4] = self.function_shape
        x = numpy.arange(start=0, stop=numpy.pi*2, step=2*numpy.pi/100)
        y = [self.eval(xi) for xi in x]

        if attribute_pair is not None:
           a1_text = attribute_pair[0]
           a2_text = attribute_pair[1]
        else:
           a1_text = 'A1'
           a2_text = 'A2'

        ax1.plot(x, y, '--k')
        area, _ = self.get_function_area()

        
        ax2.plot(x, y)
        mass_vecs = self.get_function_mass_angles()
        if mass_vecs is not None:
            for vec in mass_vecs:
                ax2.plot([vec, vec], [-1, 1], '--k')
        ax2.set_rmin(-1.1)
        ax2.set_rmax(1.1)
        ax2.set_rticks([-1, -0.5, 0, 0.5, 1])  # Less radial ticks
        ax2.set_yticklabels([])
        ax2.grid(True)
        
        

        ax3.text(0, .9, "Best Basis Function: " + str([x1, x2, x3, x4]))

        for i in range(0, 4):
          if i == 0:
            xi = x1
          elif i == 1:
            xi = x2
          elif i == 2:
            xi = x3
          elif i == 3:
            xi = x4

          if xi == 1:
            sent_str = "Positive"
          elif xi == 0:
            sent_str = "Neutral"
          elif xi == -1:
            sent_str = "Negative"

          if i == 0:
            ax3.text(0, .8-i*0.1, "(" + a1_text + "+, " + a2_text + "+): " + sent_str)
          elif i == 1:
            ax3.text(0, .8-i*0.1, "(" + a1_text + "-, " + a2_text + "+): " + sent_str)
          elif i == 2:
            ax3.text(0, .8-i*0.1, "(" + a1_text + "-, " + a2_text + "-): " + sent_str)
          elif i == 3:
            ax3.text(0, .8-i*0.1, "(" + a1_text + "+, " + a2_text + "-): " + sent_str)
          

        ax3.grid(False)
        ax3.axis("off")

        

        #return fig
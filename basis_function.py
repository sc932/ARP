class BasisFunction(object):
    def __init__(self, basis_type, function_shape):
        self.basis_type = basis_type # str, ie sawtooth 2 level
        self.function_shape = function_shape

    def plot(self):
        pass #implemented in subclass

    def eval(self):
        pass #implemented in subclass
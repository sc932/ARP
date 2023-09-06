class BasisSpace(object):
    def __init__(self):
        self.basis_functions = None # implemented in subclass

from updown_basis_function import UpDownBasisFunction

class UpDownBasisSpace(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        for x1 in [-1, 1]:
            for x2 in [-1, 1]:
                for x3 in [-1, 1]:
                    for x4 in [-1, 1]:
                        self.basis_functions.append(UpDownBasisFunction(function_shape=[x1, x2, x3, x4]))

class UpMidDownBasisSpace(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        for x1 in [-1, 0, 1]:
            for x2 in [-1, 0, 1]:
                for x3 in [-1, 0, 1]:
                    for x4 in [-1, 0, 1]:
                        if [x1, x2, x3, x4] is not [0, 0, 0, 0]:
                            self.basis_functions.append(UpDownBasisFunction(function_shape=[x1, x2, x3, x4]))

class SymetricUpDownTwo(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1]))
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1]))
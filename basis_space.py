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
                        if not (x1 == 0 and x2 == 0 and x3 == 0 and x4 == 0):
                            self.basis_functions.append(UpDownBasisFunction(function_shape=[x1, x2, x3, x4]))

class SymetricUpDownTwo(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1])) # Q1 & Q3
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1])) # Q2 & Q4

class SymetricUpDownFour(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1])) # Q1 & Q3
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1])) # Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, -1, -1])) # Q1 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, -1, 1, -1])) # Q3 only

class SymetricUpDownSix(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1])) # Q1 & Q3
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1])) # Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, -1, -1])) # Q1 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, -1, 1, -1])) # Q3 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, -1, 0])) # Q1 only, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 0, 1, 0])) # Q3 only, tapered

class SymetricUpDownEight(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1])) # Q1 & Q3
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1])) # Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, 1, 0])) # Q1 & Q3, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[0, 1, 0, 1])) # Q2 & Q4, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, -1, -1])) # Q1 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, -1, 1, -1])) # Q3 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, -1, 0])) # Q1 only, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 0, 1, 0])) # Q3 only, tapered

class SymetricUpDownTen(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1])) # Q1 & Q3
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1])) # Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, 1, 0])) # Q1 & Q3, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[0, 1, 0, 1])) # Q2 & Q4, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, -1, -1])) # Q1 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, -1, 1, -1])) # Q3 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, -1, 0])) # Q1 only, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 0, 1, 0])) # Q3 only, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 1, -1, 1])) # Q1 & Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, 1, 1])) # Q2 & Q3 & Q4

class SymetricUpDownTwelve(BasisSpace):
    def __init__(self):
        self.basis_functions = []
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, 1, -1])) # Q1 & Q3
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, -1, 1])) # Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, 1, 0])) # Q1 & Q3, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[0, 1, 0, 1])) # Q2 & Q4, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, -1, -1, -1])) # Q1 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, -1, 1, -1])) # Q3 only
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 0, -1, 0])) # Q1 only, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 0, 1, 0])) # Q3 only, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 1, -1, 1])) # Q1 & Q2 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[-1, 1, 1, 1])) # Q2 & Q3 & Q4
        self.basis_functions.append(UpDownBasisFunction(function_shape=[1, 1, 0, 1])) # Q1 & Q2 & Q4, tapered
        self.basis_functions.append(UpDownBasisFunction(function_shape=[0, 1, 1, 1])) # Q2 & Q3 & Q4, tapered
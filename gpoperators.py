"""
Genetic Programing Operators Module

Contains functionality and structures pertaining to operators allowed within the stack GP

"""

import random


class EncapsulatedData:
    """
    wrapper for a reference to any primitive or any variable
    """

    def __init__(self, data):
        self.data = data


class EncapsulatedDataUpdater:
    """
    functor wrapper that updates the data
    """

    def __init__(self, encapsulated_data):
        self.encapsulated = encapsulated_data

    def __call__(self, updated_value):
        self.encapsulated.data = updated_value


class TerminalSetOperator:
    """
    represents a terminal set member that can operate on a stack
    """

    def __init__(self, encapsulated_data, **kwargs):
        """

        :param encapsulated_data: EncapsulatedData object meant to be modified outside scope of function
        :param kwargs: name : string identifier of the operator
        """
        self.encapsulated = encapsulated_data
        if 'name' in kwargs:
            self.name = kwargs['name']

    def __call__(self, var_stack):
        """
        pushes the encapsulated data onto the var_stack
        :param var_stack: variable stack
        :return:
        """
        var_stack.append(self.encapsulated.data)

    def clone(self):
        return self


class FunctionalSetOperator:
    """
    represents a member of the functional set.
    """

    def __init__(self, function, num_args, **kwargs):
        """

        :param function: function used
        :param num_args: number of arguments required for operator
        :param kwargs: name : string identifier of the operator
        """
        self.function = function
        self.num_args = num_args
        if 'name' in kwargs:
            self.name = kwargs['name']

    def __call__(self, var_stack):
        """
        given stack, pops off members of the stack as parameters, and returns the resulting operation
        :param var_stack: variable stack to push and pop from
        :return:
        """
        if len(var_stack) >= self.num_args:
            arguments = [var_stack.pop() for _ in range(self.num_args)]
            var_stack.append(self.function(*arguments))

    def clone(self):
        return self


class ERConstantSetOperator:
    """
    Ephermeral Random Constant, generates a unique random constant per member.
    """

    min_range = None
    max_range = None
    _name = "ERK"

    def __init__(self):
        """ initializes self.data to none
        """
        self.data = None

    def __call__(self, var_stack):
        """
        checks if self.data is none, and if it is, initializes it to a perminant variable
        :param var_stack:
        :return:
        """
        if self.data is None:
            self.data = random.uniform(self.min_range, self.max_range)
        var_stack.append(self.data)

    def clone(self):
        return ERConstantSetOperator()

    @classmethod
    def set_range(cls, min_range, max_range):
        """
        sets the range attached to the class
        :param min_range: min range for random variable
        :param max_range: max range for random variable
        :return:
        """
        cls.min_range = min_range
        cls.max_range = max_range

    @property
    def name(self):
        """
        retrieves name of variable along with constant value associated with it
        :return:
        """
        return self._name + " " + str(self.data)

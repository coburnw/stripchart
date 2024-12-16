

class SI():
    def __init__(self, quantity, precision=0):
        """
        Build a printable representation of a Quantity object in SI format
        :param quantity: (Quantity) a quantity object
        :param precision: (int) number of digits to display
        """
        self.quantity = quantity
        self.precision = precision

        self._suffixes = {'p': -12, 'n': -9, 'u': -6, 'm': -3, '': 0}
        self._suffix_zero_offset = len(self._suffixes) - 1
        self._suffixes |= {'K': 3, 'M': 6, 'G': 9, 'T': 12}
        self._suffix_list = list(self._suffixes)

        return

    def __repr__(self):
        return '{} {}{}'.format(self.coefficient, self.exponent, self.units)

    @property
    def name(self):
        return self.quantity.name

    @property
    def value(self):
        """

        :return: (str) full value with SI suffix as required
        """

        return '{}{}'.format(self.coefficient, self.exponent)

    @value.setter
    def value(self, value_str):
        self.quantity.value = self.to_float(value_str)
        return

    @property
    def coefficient(self):
        """
        The coefficient is the decimal adjusted quantity without its exponent
        :return: (str) the precision adjusted coefficient
        """
        coef, exp = self.to_si(self.quantity)
        printable = self.adjust_precision(coef)

        return printable

    @property
    def exponent(self):
        """

        :return: (string) the SI abbreviated exponent ie u,m,K,M etc
        """
        coef, exp = self.to_si(self.quantity)

        index = int(exp / 3) + self._suffix_zero_offset
        suffix = self._suffix_list[index]

        return suffix

    @property
    def units(self):
        return self.quantity.units

    def to_float(self, value_str) -> float:
        """

        :param value_str: (str)  decimal value string with optional SI suffix
        :return: (float) true float value
        """
        value_str = value_str.strip()

        if value_str[-1].isdecimal():
            value = float(value_str)
        else:
            suffix = value_str[-1]
            exponent = self._suffixes[suffix]

            value_str = value_str[:-1]
            value = float(value_str) * 10 ** exponent

        return value

    def to_si(self, quantity):
        """
        convert a quantity to coefficient and SI exponent
        :param quantity: (Quantity) a Value object
        :return: (float, int) the coefficient and exponent in orders of 3's
        """
        coef, exp = self.split(quantity.value)

        if exp < 0:
            exp -= 2

        order = int(exp / 3)

        return self.split(quantity.value, order * 3)

    def adjust_precision(self, value):
        printable = '{:f}'.format(value)
        if self.precision > 0:
            left, right = printable.split('.')
            if len(left.strip('-')) >= self.precision:
                printable = '{}'.format(left)
            else:
                end = (self.precision - len(left.strip('-')))
                if int(left) == 0:
                    end += 1

                right = right[:end]
                printable = '{}.{}'.format(left, right)

        return printable

    def split(self, f_value, exponent=None):
        """
        Splits a float into its coefficient and exponent: 123.7 > 1.237,3
        :param f_value: (float) a quantity
        :param exponent: (integer) the target exponent or None
        :return: (float, int) the coefficient and exponent of the original quantity
        """
        if exponent is None:
            id = 'e'
            str = '{:e}'.format(f_value)
            coef, sep, exp = str.partition(id)

        else:
            exp = exponent
            coef = float(f_value) / 10 ** exp

        return float(coef), int(exp)


class Quantity():
    def __init__(self, value, name='', units=''):
        """
        maintains a quantity as name/value/units properties.
        :param value: (float) a numerical quantity
        :param name: (string) short name of quantity
        :param units: (string) the base units of quantity.
        """
        self._value = 0
        self._name = name
        self._units = units

        self.value = value

        return

    def __repr__(self):
        """
        A printable formatted quantity string
        :return: (string) a formatted string containing the quantity, si exponent and units
        """
        si = SI(self)
        return '{} {}{}'.format(si.coefficient, si.exponent, si.units)

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        """

        :return: (float) the numerical quantity
        """
        return self._value

    @value.setter
    def value(self, value):
        """

        :param value: (float) the numerical quantity
        """
        self._value = value
        return

    @property
    def units(self):
        """

        :return:  (string) the units of the quantity
        """
        return self._units

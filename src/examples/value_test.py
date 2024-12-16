import stripchart

if __name__ == '__main__':
    for i in range(0,9):
        quantity= stripchart.Quantity(12323.4567 * 10 ** -i, units='Hz')
        si = stripchart.SI(quantity, precision=3)
        print(quantity.value, quantity, si)

    print(si.to_float('12.30u'))
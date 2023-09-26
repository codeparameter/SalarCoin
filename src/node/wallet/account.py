# key
def __str__(self):
    return '*' * 20 + \
           f'\nbite: {self._b}\nhex: {self._h}\nbase58: {self._58}\n' + \
           '*' * 20 + '\n'
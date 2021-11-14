from data import Values


class CashBin:

    @classmethod
    def get_reserve(cls):
        return cls.__get_reserve()

    @classmethod
    def __get_reserve(cls):
        reserve = Values.cash_bin.get('reserve', None)
        if not reserve:
            reserve = 0
            Values.cash_bin['reserve'] = reserve

        return reserve

    @classmethod
    def extract(cls, amount):
        if amount <= 0:
            raise ValueError('extract amount should be bigger than zero')

        reserve = cls.__get_reserve()
        new_reserve = reserve - amount
        if new_reserve < 0:
            raise ValueError('insufficient reserve in cash bin')

        Values.cash_bin['reserve'] = new_reserve

    @classmethod
    def insert(cls, amount):
        if amount <= 0:
            raise ValueError('insert amount should be bigger than zero')

        reserve = cls.__get_reserve()
        new_reserve = reserve + amount

        Values.cash_bin['reserve'] = new_reserve

    @classmethod
    def give_back_bill(cls):
        pass  # Todo: give back inserted bill in bill counter


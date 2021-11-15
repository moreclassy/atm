class Values:

    accounts = [
        {'account_number': '123456789', 'balance': 100000000, 'card_number': '111111', 'pin': '1111', },
        {'account_number': '987654321', 'balance': 10000000, 'card_number': '222222', 'pin': '2222', },
        {'account_number': '12341234', 'balance': 1000000, 'card_number': '333333', 'pin': '3333', },
        {'account_number': '98769876', 'balance': 10, 'card_number': '333333', 'pin': '4444', },
    ]

    transactions = [
        {'key': 0, 'type': 'initial transaction', 'account_number': '', 'amount': 0}
    ]

    cash_bin = {
        'reserve': 1000000,
    }

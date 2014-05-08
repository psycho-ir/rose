from django.db import connections


def find_deposit(customer_id, deposit_number):
    cursor = connections['core'].cursor()
    result = cursor.execute('SELECT * FROM DBX1_TX18 WHERE F4=%s AND F5=%s', [deposit_number, customer_id])
    desc = result.description
    r = [
        dict(zip([col[0] for col in desc], row))
        for row in result.fetchall()
    ]

    cursor.close()

    return r


#3564227635.12

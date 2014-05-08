from django.db import connections


def find_customer(customer_id):
    cursor = connections['core'].cursor()
    result = cursor.execute('SELECT * FROM DBX1_TX11 WHERE F1=%s', [customer_id])
    desc = result.description
    r = [
        dict(zip([col[0] for col in desc], row))
        for row in result.fetchall()
    ]

    cursor.close()

    return r

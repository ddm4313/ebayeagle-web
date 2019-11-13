from ebaysdk.trading import Connection
from ebaysdk.exception import ConnectionError
from datetime import date
import datetime
import json, time

api = Connection(config_file="ebay.yaml")

def user_info():
    try:
        response = api.execute('GetUser', {})
        response = json.loads(json.dumps(response.dict()))
        email = response['User']['Email']
        feedback_score = response['User']['FeedbackScore']
        registration_date = response['User']['RegistrationDate']
        year = int(registration_date.split("-")[0])
        month = int(registration_date.split("-")[1])
        day = int(registration_date.split("-")[2].split("T")[0])
        today = datetime.date.today()
        register_date = datetime.date(year, month, day)
        registered = today - register_date
        registered = str(registered).split(",")[0]
        return {"Email": email, "Feedback": feedback_score, "Registered": registered}
    except ConnectionError as e:
        print(e)

def get_orders():
    try:
        response = api.execute('GetOrders', {'NumberOfDays': '7'})
        response = json.loads(json.dumps(response.dict()))
        sold = []
        orders = {}
        total_orders = response['ReturnedOrderCountActual']
        for key, value in enumerate(response['OrderArray']['Order']):
            sold.append(float(response['OrderArray']['Order'][key]['AmountPaid']['value']))
            email = response['OrderArray']['Order'][key]['TransactionArray']['Transaction'][0]['Buyer']['Email']
            transaction_amount = response['OrderArray']['Order'][key]['TransactionArray']['Transaction'][0]['TransactionPrice']['value']
            item = response['OrderArray']['Order'][key]['TransactionArray']['Transaction'][0]['Item']['Title']
            orders.update({key: {"Email": email, "Item": item, "Transaction_Amount": transaction_amount}})
        print(int(sum(sold)))
        return {"TotalSales": int(sum(sold)), "Orders": orders, 'TotalOrders': total_orders}
    except ConnectionError as e:
        print(e)


if __name__ == '__main__':
    get_orders()

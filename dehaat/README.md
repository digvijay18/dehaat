# Mini Backend #
Assignment Project

## Steps To Create New Installation

1. Clone: git clone https://github.com/digvijay18/dehaat

2. Download Pip: sudo easy_install pip

3. Install virtualenv: pip install virtualenv

4. Make a virtual environment: virtualenv venv

5. Initialize: source venv/bin/activate

6. Setup Project: python setup.py install

7. Install and start RabbitMQ: brew install rabbitmq && brew services start rabbitmq

8. Install and start Redis: brew install redis && brew services start redis

9. Install and start Postgres App

10. Install Celery and start celery using:  celery -A dehaat worker -l info

10. Run Django Migrations: python manage.py migrate

11. Run Django Server: python manage.py runserver


## How To Run Project:

1. A superuser with username:password - admin:admin is already set up.

2. To test APIs via Postman, DO NOT forget to add csrf token header -> X-CSRFToken: <token>

3. For convenience of testing, API request for OTP also returns an otp in response (and a header - X-Request-Id).

4. To input OTP, DO NOT forget to add a one time header -> X-Request-Id: <uuid token>

## API Contract:

#### Accounts-

http://127.0.0.1:8000/account/login/ POST `{"username": "admin”,”password": "admin"}`

http://127.0.0.1:8000/account/ POST `{"username": 1234567890,"groups": "customer"}`

http://127.0.0.1:8000/account/logout/ GET

http://127.0.0.1:8000/account/customer?mobile=<10-digits>       POST     `{"username": 9868310218, "groups": "customer”}` / `{“otp”:<4-digits>}`


#### Products-

http://127.0.0.1:8000/product/       POST      `{"id": 1, "name": "pizza", "description": "It's fantastic", "features": {}, "price": 300.0, "units": 4, "active": "active"}`

http://127.0.0.1:8000/product/       GET       `[{"id": 1, "name": "pizza", "description": "It's fantastic", "features": {}, "price": 300.0, "units": 4, "active": "active" }]`

http://127.0.0.1:8000/product/1/     GET       `{"id": 1, "name": "pizza", "description": "It's fantastic", "features": {}, "price": 300.0, "units": 4, "active": "active" }`

http://127.0.0.1:8000/product/1/     PATCH     `{“units”: 5}`

http://127.0.0.1:8000/product/1/     DELETE

#### Orders-

http://127.0.0.1:8000/order/         POST       `{"orderlines": [{"product": 1, "units": 2, "confirmed_price": 0.0}]}`
(confirmed_price is 0 till order is confirmed
client should so prevailing product price)

http://127.0.0.1:8000/order/         GET        `[{"id": 1, "orderlines": [{"product": "pizza", "units": 2,"confirmed_price": 300.0}],"status": "confirmed"}]`
(Gets all orders for admin/agent
and self orders for customer)

http://127.0.0.1:8000/order/1/       GET        `{"id": 1, "orderlines": [{"product": "pizza", "units": 2,"confirmed_price": 300.0}],"status": "confirmed"}`
(Gets any order for admin/agent
and self order for customer)

http://127.0.0.1:8000/order/1/ 	     PATCH      `{"status": "confirmed|delivered|cancelled"}`

http://127.0.0.1:8000/order/history/ GET `[{"product":1, "units":2, "confirmed_price":300.0, "total_price""}]`

#### Ledger-

http://127.0.0.1:8000/payments/user/1/ GET `[{"id": 3, "transaction_date": "2020-07-29T12:18:24.280286Z", "amount": 0.0, "post_balance": 5000.0, "customer": 2, "order": 1}]`

http://127.0.0.1:8000/payments/user/2/ POST `{"customer":2, "amount":600, "post_balance":3800}`

(post_balance added manually as a temporary shortcut,
real world API would increment from the last entry.
Note that for very first entry, no past record would exist)

http://127.0.0.1:8000/payments/user/2/?to=1-1-2030&from=30-7-2020 GET `[{"id": 7, "transaction_date": "2020-07-30T20:50:30.273567Z", "amount": -600.0, "post_balance": 2600.0, "customer": 2, "order": 1}]`

##Cases Not Handled/Simplified:

1. Cart system not asked, so not made.

2. For point 3a, API for purchase history separated from order API as it can become heavy over time. 
   So, it's more performant to break them up as slight delay in loading heavy history 
   is acceptable for user experience, but the concerned order must load fast.
   Real world example: Youtube video, comments, recommendations all loaded separately.

3. As ledger initialization is not mentioned in the question, I have used cash payments
   to create new entries and update balance. To purchase, at least one cash payment MUST
   be made first.

4. Read code comments.

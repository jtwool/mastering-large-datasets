from functools import reduce

my_products = [
    {"price": 9.99,
     "sn": '00231'},
    {"price": 59.99,
     "sn": '11010'},
    {"price": 74.99,
     "sn": '00013'},
    {"price": 19.99,
     "sn": '00831'},
]

reduce(lambda acc, nxt: acc+nxt.get("price", 0), my_products, 0)

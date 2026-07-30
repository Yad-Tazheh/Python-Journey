from enum import Enum
class Product:
    def __init__(self, name, price, stock, product_id):
        if price < 0 or stock < 0:
            raise ValueError('Please enter a valid price and stock')
        self.name = name
        self.price = price
        self.stock = stock
        self.product_id = product_id

    def __str__(self):
        return f"{self.name} | {self.price} | {self.stock}"

    def increase_stock(self, amount):
        if amount <= 0:
            raise ValueError('Please enter a valid amount')
        self.stock += amount

    def decrease_stock(self, amount):
        if amount <= 0:
            raise ValueError('Please enter a valid amount')
        if amount > self.stock:
            raise ValueError('Not enough stock')
        self.stock -= amount

class Customer:
    def __init__(self, name, customer_id):
        self.name = name
        self.customer_id = customer_id
        self.orders = [] # may have multiple order(s)

    def __str__(self):
        return f"{self.name} | {self.customer_id}"

    def show_orders(self):
        for order in self.orders:
            print(order)

class Order:
    class Status(Enum):
        PENDING = 'pending'
        PAID = 'paid'
        CANCELED = 'canceled'

    def __init__(self, customer, order_id):
        self.customer = customer
        self.order_id = order_id
        self.items = []
        self.status = Order.Status.PENDING
        customer.orders.append(self) # attach order to the customer's orders list

    def __str__(self) -> str:
        return f"Order #{self.order_id} | {self.customer.name} | {self.status.value} | Total: {self.total_price()}"

    def add_item(self, product, quantity):
        if product is None:
            raise ValueError('Please enter a valid product')
        if quantity <= 0:
            raise ValueError('Please enter a valid quantity')
        self.items.append(OrderItem(product, quantity))
        product.decrease_stock(quantity)

    def remove_item(self, product_id):
        if product_id is None:
            raise ValueError('Please enter a valid product_id')
        for item in self.items:
            if item.product.product_id == product_id:
                item.product.increase_stock(item.quantity)
                self.items.remove(item)
                return
        raise ValueError('product not found')

    def total_price(self):
        return sum(item.subtotal for item in self.items)

    def show_order(self):
        for item in self.items:
            print(
                f"{item.product.name} | {item.product.price} | {item.quantity} | {item.subtotal}"
            )
        print(f"Total: {self.total_price()}")
        print(f"Status: {self.status.value}")


class OrderItem:
    def __init__(self, product, quantity):
        if product is None:
            raise ValueError('Please enter a valid product')
        if quantity <= 0:
            raise ValueError('Please enter a valid quantity')
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} * {self.quantity} = {self.subtotal}"


class OrderManager:
    def __init__(self):
        self.customers = []
        self.orders = []
        self.products = []

    def add_product(self, product):
        if self.find_product(product.product_id):
            raise ValueError("Product already exists")
        if product is None:
            raise ValueError('Please enter a valid product')
        self.products.append(product)

    def find_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def add_customer(self, customer):
        if self.find_customer(customer.customer_id):
            raise ValueError("Customer already exists")
        if customer is None:
            raise ValueError('Please enter a valid customer')
        self.customers.append(customer)

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def create_order(self, customer_id, order_id):
        if self.find_order(order_id):
            raise ValueError('Order already created')
        if not order_id:
            raise ValueError('Please enter a valid order_id')
        customer = self.find_customer(customer_id)
        if customer is None:
            raise ValueError('Please enter a valid customer')
        order = Order(customer, order_id)
        self.orders.append(order)
        return order

    def find_order(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def pay_order(self, order_id):
        order = self.find_order(order_id)
        if order is None:
            raise ValueError('Please enter a valid order_id')
        if order.status == Order.Status.CANCELED:
            raise RuntimeError('Order canceled')
        if order.status == Order.Status.PAID:
            raise RuntimeError('Order paid')
        order.status = Order.Status.PAID

    # aval bayad order peyda koni
    # vaziate order o bbini age paid bud cancel nashe age pending bud
    # bbini quantity az har product chandtas
    # be mujudie un product ha un tedad quantity ro increase_stock koni
    # status o be canceled taghir bedi
    def cancel_order(self, order_id):
        order = self.find_order(order_id)
        if order is None:
            raise ValueError('Please enter a valid order_id')
        if order.status == Order.Status.PAID:
            raise RuntimeError('Order cant be canceled')
        if order.status == Order.Status.CANCELED:
            raise RuntimeError('Order already canceled')
        for item in order.items:
            item.product.increase_stock(item.quantity)
        order.status = Order.Status.CANCELED

    def show_all_orders(self):
        for order in self.orders:
            print(order)

    def show_products(self):
        for product in self.products:
            print(product)

    def show_customers(self):
        for customer in self.customers:
            print(customer)

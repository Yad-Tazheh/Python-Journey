class Product:
    def __init__(self, name, category, price, quantity, product_id):
        if price < 0 or quantity < 0:
            raise ValueError('Please enter a valid price and quantity')
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.product_id = product_id
        self.supplier = None

    def __str__(self):
        return f"{self.name} | {self.category} | {self.price} | {self.quantity}"

    def increase_stock(self, amount):
        if amount <= 0:
            raise ValueError('Please enter a valid amount')
        self.quantity += amount

    def decrease_stock(self, amount):
        if amount <= 0:
            raise ValueError('Please enter a valid amount')
        if amount > self.quantity:
            raise ValueError('Not enough stock')
        self.quantity -= amount

class Supplier:
    def __init__(self, name, supplier_id):
        self.name = name
        self.supplier_id = supplier_id
        self.products = []

    def __str__(self):
        return f"{self.name} | {self.supplier_id}"

    def add_product(self, product):
        if product not in self.products:
            self.products.append(product)
        return product

    def show_products(self):
        for product in self.products:
            print(product)

class InventoryManager:
    def __init__(self):
        self.products = []
        self.suppliers = []

    def add_product(self, name, category, price, quantity, product_id, stock_in):
        # make a product from Product class , append it into the mgr products list
        product = Product(name, category, price, quantity, product_id)
        self.products.append(product)
        product.increase_stock(stock_in)
        return product

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)

    def delete_product(self, product_id):
        product = self.find_product(product_id)
        if product is None:
            return None
        if product.supplier:
            product.supplier.products.remove(product)
        self.products.remove(product)
        return product

    def find_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def find_supplier(self, supplier_id):
        for supplier in self.suppliers:
            if supplier.supplier_id == supplier_id:
                return supplier
        return None

    def show_inventory(self):
        for product in self.products:
            print(product)

    def sell_product(self, product_id, quantity):
        product = self.find_product(product_id)
        if product is None:
            raise ValueError('Product not found')
        if quantity <= 0:
            raise ValueError('Invalid quantity')
        product.decrease_stock(quantity)
        return product

    def update_quantity(self, product_id, quantity):
        product = self.find_product(product_id)
        if product is None:
            raise ValueError('Product not found')
        if quantity <= 0:
            raise ValueError('Invalid quantity')
        product.quantity = quantity

    def link_product_supplier(self, product_id, supplier_id):
        product = self.find_product(product_id)
        supplier = self.find_supplier(supplier_id)
        if product is None:
            raise ValueError('Product not found')
        if supplier is None:
            raise ValueError('Supplier not found')
        if product.supplier:
            product.supplier.products.remove(product)
        product.supplier = supplier
        supplier.add_product(product)

    def show_suppliers(self):
        for supplier in self.suppliers:
            print(supplier)

    def calculate_total_value(self):
        total_value = 0
        for product in self.products:
            total_value += product.price * product.quantity
        return total_value

    def show_product_supplier(self, product_id):
        product = self.find_product(product_id)
        if product is None:
            raise ValueError('Product not found')
        if product.supplier is None:
            return f'{product.name} | No supplier'
        return f'{product.name} | {product.supplier}'


mgr = InventoryManager()
mgr.add_product("keyboard", "electronics", 50, 20, '234', 4)
mgr.sell_product('234', 5)



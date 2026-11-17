class Product:
    name: str
    description: str
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data):
        return cls(
            product_data['name'],
            product_data['description'],
            product_data['price'],
            product_data['quantity'],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    def __str__(self):
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError(
                "Складывать можно только товары одного класса"
            )
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    def __init__(self, name, description, price, quantity,
                 efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity,
                 country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    name: str
    description: str

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только объекты Product "
                "или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        total = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество продуктов: {total} шт.'

    @property
    def products(self):
        result = ''
        for product in self.__products:
            result += (
                f'{product.name}, {product.price} руб. '
                f'Остаток: {product.quantity} шт.\n'
            )
        return result


if __name__ == "__main__":  # pragma: no cover
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(Category.category_count)
    print(Category.product_count)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    print(category1)
    print(product1)

    smartphone = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB",
        180000.0,
        5,
        efficiency=98,
        model="S23 Ultra",
        memory=256,
        color="Black",
    )
    grass = LawnGrass(
        "Газонная трава",
        "Элитная",
        1500.0,
        10,
        country="Россия",
        germination_period="7 дней",
        color="Зелёный",
    )

    print(smartphone)
    print(grass)

    try:
        smartphone + grass
    except TypeError as error:
        print("Ошибка:", error)

    category2 = Category("Смартфоны", "Описание", [smartphone])
    try:
        category2.add_product("строка")
    except TypeError as error:
        print("Ошибка:", error)
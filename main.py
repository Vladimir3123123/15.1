from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Базовый абстрактный класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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


class ReprMixin:
    """Миксин, который печатает инфу о созданном объекте."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self):
        params = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({params})"


class Product(ReprMixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError(
                "Товар с нулевым количеством не может быть добавлен"
            )
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(cls, product_data):
        return cls(
            product_data['name'],
            product_data['description'],
            product_data['price'],
            product_data['quantity'],
        )


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

    def average_price(self):
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0

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

    print(product1)
    print(product2)
    print(product3)

    print(category1)
    print("Средняя цена:", category1.average_price())

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

    try:
        Product("Нулевой", "d", 100.0, 0)
    except ValueError as error:
        print("Ошибка:", error)

    empty_category = Category("Пустая", "без товаров", [])
    print("Средняя цена пустой категории:", empty_category.average_price())
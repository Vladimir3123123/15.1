import pytest

from main import (
    BaseProduct,
    ReprMixin,
    Product,
    Smartphone,
    LawnGrass,
    Category,
)


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0


# ---------- BaseProduct ----------

def test_base_product_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct("A", "d", 100.0, 1)


def test_product_is_subclass_of_base_product():
    assert issubclass(Product, BaseProduct)


# ---------- ReprMixin ----------

def test_repr_mixin_used_by_product():
    assert issubclass(Product, ReprMixin)


def test_repr_string_format():
    p = Product("A", "d", 100.0, 1)
    text = repr(p)
    assert text.startswith("Product(")
    assert "name='A'" in text
    assert "quantity=1" in text


# ---------- Product ----------

def test_product_init(capsys):
    p = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert p.name == "Iphone 15"
    assert p.description == "512GB, Gray space"
    assert p.price == 210000.0
    assert p.quantity == 8


def test_new_product():
    data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14,
    }
    p = Product.new_product(data)
    assert p.name == "Xiaomi Redmi Note 11"
    assert p.price == 31000.0
    assert p.quantity == 14


def test_price_setter_positive():
    p = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    p.price = 190000.0
    assert p.price == 190000.0


def test_price_setter_negative(capsys):
    p = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    p.price = -5
    assert p.price == 210000.0
    captured = capsys.readouterr()
    assert (
        "Цена не должна быть нулевая или отрицательная"
        in captured.out
    )


def test_product_str():
    p = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert str(p) == "Iphone 15, 210000.0 руб. Остаток: 8 шт."


# ---------- Smartphone / LawnGrass ----------

def test_smartphone_init():
    s = Smartphone(
        "Iphone 15", "512GB", 210000.0, 8,
        efficiency=95, model="15 Pro", memory=512, color="Gray",
    )
    assert s.efficiency == 95
    assert s.model == "15 Pro"
    assert s.memory == 512
    assert s.color == "Gray"
    assert isinstance(s, Product)


def test_lawn_grass_init():
    g = LawnGrass(
        "Газон", "Трава", 500.0, 20,
        country="Россия", germination_period="7 дней", color="Зелёный",
    )
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"
    assert g.color == "Зелёный"
    assert isinstance(g, Product)


# ---------- Сложение ----------

def test_product_add_same_class_ok():
    p1 = Product("A", "d", 100.0, 2)
    p2 = Product("B", "d", 200.0, 3)
    assert p1 + p2 == 100.0 * 2 + 200.0 * 3


def test_smartphone_add_same_class_ok():
    s1 = Smartphone("A", "d", 100.0, 2, 1, "m1", 64, "black")
    s2 = Smartphone("B", "d", 200.0, 3, 1, "m2", 128, "white")
    assert s1 + s2 == 100.0 * 2 + 200.0 * 3


def test_add_different_classes_raises():
    s = Smartphone("A", "d", 100.0, 2, 1, "m1", 64, "black")
    g = LawnGrass("G", "d", 50.0, 4, "RU", "7d", "green")
    with pytest.raises(TypeError):
        s + g


# ---------- Category ----------

def test_category_init():
    p1 = Product("A", "d", 100.0, 5)
    c = Category("Смартфоны", "Описание", [p1])
    assert c.name == "Смартфоны"
    assert "A" in c.products


def test_add_product():
    p1 = Product("A", "d", 100.0, 5)
    p2 = Product("B", "d", 200.0, 8)
    c = Category("Смартфоны", "Описание", [p1])
    c.add_product(p2)
    assert Category.product_count == 2
    assert "B" in c.products


def test_add_product_wrong_type_raises():
    c = Category("Смартфоны", "desc", [])
    with pytest.raises(TypeError):
        c.add_product("not a product")


def test_add_product_subclass_ok():
    c = Category("Смартфоны", "desc", [])
    s = Smartphone("A", "d", 100.0, 2, 1, "m1", 64, "black")
    c.add_product(s)
    assert Category.product_count == 1


def test_category_count():
    Category("A", "desc", [])
    Category("B", "desc", [])
    assert Category.category_count == 2


def test_category_str():
    p1 = Product("A", "d", 100.0, 5)
    p2 = Product("B", "d", 200.0, 8)
    c = Category("Смартфоны", "Описание", [p1, p2])
    assert str(c) == "Смартфоны, количество продуктов: 13 шт."


def test_products_getter():
    p1 = Product("A", "d", 100.0, 5)
    c = Category("Смартфоны", "Описание", [p1])
    assert c.products == "A, 100.0 руб. Остаток: 5 шт.\n"
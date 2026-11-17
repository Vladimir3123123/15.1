import pytest

from main import Product, Smartphone, LawnGrass, Category


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0


# ---------- Product ----------

def test_product_init():
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
    assert p.description == "1024GB, Синий"
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
    assert s.name == "Iphone 15"
    assert s.description == "512GB"
    assert s.price == 210000.0
    assert s.quantity == 8
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
    assert g.name == "Газон"
    assert g.price == 500.0
    assert g.quantity == 20
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"
    assert g.color == "Зелёный"
    assert isinstance(g, Product)


def test_smartphone_inherits_product():
    assert issubclass(Smartphone, Product)


def test_lawn_grass_inherits_product():
    assert issubclass(LawnGrass, Product)


# ---------- Сложение ----------

def test_product_add_same_class_ok():
    p1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert p1 + p2 == 2580000.0


def test_smartphone_add_same_class_ok():
    s1 = Smartphone("A", "d", 100.0, 2, 1, "m1", 64, "black")
    s2 = Smartphone("B", "d", 200.0, 3, 1, "m2", 128, "white")
    assert s1 + s2 == 100.0 * 2 + 200.0 * 3


def test_lawn_grass_add_same_class_ok():
    g1 = LawnGrass("A", "d", 100.0, 2, "RU", "7d", "green")
    g2 = LawnGrass("B", "d", 50.0, 4, "RU", "5d", "green")
    assert g1 + g2 == 100.0 * 2 + 50.0 * 4


def test_add_different_classes_raises():
    s = Smartphone("A", "d", 100.0, 2, 1, "m1", 64, "black")
    g = LawnGrass("G", "d", 50.0, 4, "RU", "7d", "green")
    with pytest.raises(TypeError):
        s + g


def test_add_product_and_smartphone_raises():
    p = Product("A", "d", 100.0, 2)
    s = Smartphone("B", "d", 100.0, 2, 1, "m1", 64, "black")
    with pytest.raises(TypeError):
        p + s


# ---------- Category ----------

def test_category_init():
    p1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    c = Category("Смартфоны", "Описание", [p1])
    assert c.name == "Смартфоны"
    assert c.description == "Описание"
    assert "Samsung Galaxy S23 Ultra" in c.products


def test_add_product():
    p1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    c = Category("Смартфоны", "Описание", [p1])
    c.add_product(p2)
    assert Category.product_count == 2
    assert "Iphone 15" in c.products


def test_add_product_subclass_ok():
    c = Category("Смартфоны", "desc", [])
    s = Smartphone("A", "d", 100.0, 2, 1, "m1", 64, "black")
    c.add_product(s)
    assert Category.product_count == 1
    assert "A" in c.products


def test_add_product_lawn_grass_ok():
    c = Category("Газон", "desc", [])
    g = LawnGrass("G", "d", 50.0, 4, "RU", "7d", "green")
    c.add_product(g)
    assert Category.product_count == 1
    assert "G" in c.products


def test_add_product_wrong_type_raises():
    c = Category("Смартфоны", "desc", [])
    with pytest.raises(TypeError):
        c.add_product("not a product")


def test_add_product_int_raises():
    c = Category("Смартфоны", "desc", [])
    with pytest.raises(TypeError):
        c.add_product(42)


def test_product_count():
    p1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    Category("Смартфоны", "Описание", [p1, p2])
    assert Category.product_count == 2


def test_category_count():
    Category("A", "desc", [])
    Category("B", "desc", [])
    assert Category.category_count == 2


def test_products_getter():
    p1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    c = Category("Смартфоны", "Описание", [p1])
    assert c.products == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
    )


def test_category_str():
    p1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    p3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    c = Category("Смартфоны", "Описание", [p1, p2, p3])
    assert str(c) == "Смартфоны, количество продуктов: 27 шт."
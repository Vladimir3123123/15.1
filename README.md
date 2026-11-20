# Магазин

Проект интернет-магазина на Python.

## Функциональность

- Абстрактный класс `BaseProduct` (ABC) — общая логика для всех продуктов.
- Миксин `ReprMixin` — печатает в консоль информацию о созданном объекте.
- Класс `Product(ReprMixin, BaseProduct)` — базовый товар.
  При создании с `quantity == 0` выбрасывает `ValueError`.
- Класс `Smartphone(Product)` — смартфон
  (`efficiency`, `model`, `memory`, `color`).
- Класс `LawnGrass(Product)` — газонная трава
  (`country`, `germination_period`, `color`).
- Класс `Category` — категория со счётчиками `category_count`
  и `product_count`. Метод `average_price()` считает среднюю цену
  товаров, при пустой категории возвращает `0`.
- Сложение (`__add__`) только для объектов одного класса — иначе `TypeError`.
- В `add_product` можно добавлять только `Product` и наследников.

## Тестирование

```bash
pytest --cov=main --cov-report=term-missing
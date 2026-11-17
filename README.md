# Магазин

Проект интернет-магазина на Python.

## Функциональность

- Класс `Product` — базовый товар (name, description, price, quantity).
- Класс `Smartphone(Product)` — смартфон с атрибутами:
  `efficiency`, `model`, `memory`, `color`.
- Класс `LawnGrass(Product)` — газонная трава с атрибутами:
  `country`, `germination_period`, `color`.
- Класс `Category` — категория товаров со счётчиками
  `category_count` и `product_count`.
- Сложение товаров (`__add__`) разрешено только для объектов
  одного и того же класса — иначе `TypeError` (проверка через `type()`).
- В категорию (`add_product`) можно добавлять только объекты
  `Product` и его наследников — иначе `TypeError`
  (проверка через `isinstance()`).

## Тестирование

Запуск тестов с отчётом о покрытии:

```bash
pytest --cov=main --cov-report=term-missing
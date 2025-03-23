from abc import ABC, abstractmethod
import datetime
import logging

# Настройка логирования
logging.basicConfig(filename='application.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class BaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidOrderError(BaseError):
    def __init__(self, message):
        super().__init__(message)

class InvalidClientDataError(BaseError):
    def __init__(self, message):
        super().__init__(self.message)


class Product(ABC):
    @abstractmethod
    def display_info(self):
        pass


class Catalog(Product):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        logging.info(f'Создан товар: {name}, цена: {price}')

    def display_info(self):
        return f"Товар: {self.name}, Цена: {self.price} руб."


class Client:
    total_clients = 0

    def __init__(self, client_id, name, phone_number, address):
        self.client_id = client_id
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.orders = []

        Client.total_clients += 1
        logging.info(f'Создан клиент: {name}, ID: {client_id}')

    @staticmethod
    def from_input(client_id):
        print(f"\nВведите данные для клиента:")
        name = input("Введите полное имя клиента: ")
        phone_number = input("Введите номер телефона клиента: ")
        address = input("Введите адрес клиента: ")
        return Client(client_id, name, phone_number, address)

    @classmethod
    def get_total_clients(cls):
        return cls.total_clients

    def add_order(self, order):
        self.orders.append(order)
        logging.info(f'Клиенту {self.name} добавлен заказ: {order}')

    def __str__(self):
        return f"Клиент ID: {self.client_id}, Имя: {self.name}, Телефон: {self.phone_number}, Адрес: {self.address}"

    def __repr__(self):
        return f"Client({self.client_id}, '{self.name}', '{self.phone_number}', '{self.address}')"


class Order:
    def __init__(self, date, time, weight, diameter, color, shape, product_name):
        self._date = date
        self._time = time
        self._weight = weight
        self._diameter = diameter
        self._color = color
        self._shape = shape
        self.product_name = product_name
        logging.info(f'Создан заказ: Дата: {date}, Время: {time}, Товар: {product_name}')

    def display_info(self):
        return (f"Информация о заказе: Дата: {self._date}, Время: {self._time}, "
                f"Вес: {self._weight} кг, Диаметр: {self._diameter} см, "
                f"Цвет: {self._color}, Форма: {self._shape}, Товар: {self.product_name}")

    def get_date(self):
        return self._date

    def get_time(self):
        return self._time

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"Order('{self._date}', '{self._time}', {self._weight}, {self._diameter}, '{self._color}', '{self._shape}', '{self.product_name}')"


class SpecialOrder(Order):
    def __init__(self, date, time, weight, diameter, color, shape, product_name, special_request):
        super().__init__(date, time, weight, diameter, color, shape, product_name)
        self.special_request = special_request
        logging.info(f'Создан специальный заказ: Дата: {date}, Время: {time}, Товар: {product_name}, Специальный запрос: {special_request}')

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Специальная просьба: {self.special_request}"

    def process_order_info(self, priority="special"):
        if priority == "special":
            print("Приоритет специального заказа:")
            print(self.display_info())
            super().display_info()
        else:
            print("Приоритет базового заказа:")
            super().display_info()
            print(self.display_info())

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"SpecialOrder('{self._date}', '{self._time}', {self._weight}, {self._diameter}, '{self._color}', '{self._shape}', '{self.product_name}', '{self.special_request}')"


class UrgentOrder(Order):
    def __init__(self, date, time, weight, diameter, color, shape, product_name, urgency_level):
        super().__init__(date, time, weight, diameter, color, shape, product_name)
        self.urgency_level = urgency_level
        logging.info(f'Создан срочный заказ: Дата: {date}, Время: {time}, Товар: {product_name}, Срочность: {urgency_level}')

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Срочность: {self.urgency_level}"

    def process_order(self):
        print(f"Обработка срочного заказа с уровнем срочности: {self.urgency_level}")
        logging.info(f'Обработан срочный заказ с уровнем срочности: {self.urgency_level}')

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"UrgentOrder('{self._date}', '{self._time}', {self._weight}, {self._diameter}, '{self._color}', '{self._shape}', '{self.product_name}', '{self.urgency_level}')"


class BulkOrder(Order):
    def __init__(self, date, time, weight, diameter, color, shape, product_name, quantity, discount=0):
        super().__init__(date, time, weight, diameter, color, shape, product_name)
        self.quantity = quantity
        self.discount = discount
        logging.info(f'Создан оптовый заказ: Дата: {date}, Время: {time}, Товар: {product_name}, Количество: {quantity}, Скидка: {discount}')

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Количество: {self.quantity}, Скидка: {self.discount}%"

    def calculate_total_price(self, product_price):
        total_price = product_price * self.quantity * (1 - self.discount / 100)
        return total_price

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"BulkOrder('{self._date}', '{self._time}', {self._weight}, {self._diameter}, '{self._color}', '{self._shape}', '{self.product_name}', {self.quantity}, {self.discount})"


class Booking:
    def __init__(self, available_times):
        self.available_times = available_times
        logging.info(f'Создано бронирование со временами: {available_times}')

    def book(self, client, order):
        if order.get_time() in self.available_times:
            self.available_times.remove(order.get_time())
            logging.info(f'Время {order.get_time()} забронировано для клиента {client.name}')
            return True
        logging.warning(f'Не удалось забронировать время для клиента {client.name}')
        return False


def create_product_list():
    product_list = [
        Catalog("Торт Шоколадный", 500),
        Catalog("Торт ванильный", 480),
        Catalog("Сложный декор", 200)
    ]

    print("Список доступных товаров:")
    for index, item in enumerate(product_list):
        print(f"{index + 1}. {item.display_info()}")
    print()

    return product_list


def find_max_attribute_item(two_dim_list, attribute_name):
    if not two_dim_list:
        return None

    max_item = None
    max_value = float('-inf')

    for row in two_dim_list:
        for item in row:
            attribute_value = getattr(item, attribute_name, None)
            if attribute_value is not None and attribute_value > max_value:
                max_value = attribute_value
                max_item = item

    return max_item

def is_valid_date(date_str):
    try:
        date_format = "%Y-%m-%d"
        order_date = datetime.datetime.strptime(date_str, date_format).date()
        today = datetime.date.today()
        max_date = today + datetime.timedelta(days=365)
        if today <= order_date <= max_date:
            return True
        return False
    except ValueError:
        return False


def main():
    product_list = create_product_list()
    logging.info('Создан список товаров')

    clients = []
    booking = Booking(["10:00", "11:00", "12:00", "13:00", "14:00"])

    print("Добавление клиентов и заказов")
    logging.info('Начало добавления клиентов и заказов')

    client_id = 1

    while True:
        try:
            client_id = len(clients) + 1
            client = Client.from_input(client_id)
            if not client.name or not client.phone_number or not client.address:
                raise InvalidClientDataError("Некорректные данные клиента.")
            clients.append(client)
            logging.info(f'Добавлен клиент: {client.name}')

            print("\nСоздаем заказ для клиента:")

            while True:
                date = input("Введите дату заказа (гггг-мм-дд): ")
                if is_valid_date(date):
                    break
                else:
                    print("Некорректная дата. Пожалуйста, введите дату не позднее 365 дней с текущей даты в формате гггг-мм-дд.")
                    logging.warning('Попытка ввести некорректную дату заказа')

            time = input("Введите время заказа (чч:мм): ")


            try:
                weight = float(input("Введите вес товара (кг): "))
            except ValueError:
                raise InvalidOrderError("Некорректный вес товара.")

            try:
                diameter = float(input("Введите диаметр товара (см): "))
            except ValueError:
                raise InvalidOrderError("Некорректный диаметр товара.")

            color = input("Введите цвет товара: ")

            print("\nВыберите форму торта:")
            print("1. Круг")
            print("2. Квадрат")
            print("3. Сердце")
            try:
                shape_choice = int(input("Введите номер формы: "))
            except ValueError:
                raise InvalidOrderError("Некорректный выбор формы.")

            if shape_choice == 1:
                shape = "круг"
            elif shape_choice == 2:
                shape = "квадрат"
            elif shape_choice == 3:
                shape = "сердце"
            else:
                raise InvalidOrderError("Неверный выбор формы.")

            print("\nВыберите товар:")
            for index, item in enumerate(product_list):
                print(f"{index + 1}. {item.display_info()}")

            try:
                product_choice = int(input("Введите номер товара: ")) - 1
            except ValueError:
                raise InvalidOrderError("Некорректный выбор товара.")

            if 0 <= product_choice < len(product_list):
                product_name = product_list[product_choice].name
                order_type = input("Выберите тип заказа (обычный, срочный, оптовый): ").lower()


                if order_type == "срочный":
                    urgency_level = input("Введите уровень срочности (высокий, средний, низкий): ")
                    order = UrgentOrder(date, time, weight, diameter, color, shape, product_name, urgency_level)
                    order.process_order()
                elif order_type == "оптовый":
                    quantity = int(input("Введите количество товаров в заказе: "))
                    discount = float(input("Введите скидку на оптовый заказ (%): "))
                    order = BulkOrder(date, time, weight, diameter, color, shape, product_name, quantity, discount)
                    total_price = order.calculate_total_price(product_list[product_choice].price)
                    print(f"Итоговая цена со скидкой: {total_price} руб.")
                    logging.info(f'Итоговая цена оптового заказа: {total_price}')
                else:
                    special_request = input("Введите специальную просьбу (если есть): ")
                    if special_request:
                        order = SpecialOrder(date, time, weight, diameter, color, shape, product_name, special_request)
                    else:
                        order = Order(date, time, weight, diameter, color, shape, product_name)

                client.add_order(order)

                print("\nПодтверждение заказа:")
                print(f"Клиент: {client.name}")
                print(f"Детали заказа: {order.display_info()}")
                print("Заказ успешно создан.")

            else:
                raise InvalidOrderError("Неверный выбор товара.")

        except InvalidClientDataError as e:
            print(f"Ошибка клиента: {e}")
            logging.error(f"Ошибка клиента: {e}")
        except InvalidOrderError as e:
            print(f"Ошибка заказа: {e}")
            logging.error(f"Ошибка заказа: {e}")
        except Exception as e:
            print(f"Произошла общая ошибка: {e}")
            logging.exception(f"Произошла общая ошибка: {e}")
        finally:
            print(f"Обработка клиента завершена.")
            print(f"Всего клиентов: {Client.get_total_clients()}")
            logging.info(f"Обработка клиента завершена. Всего клиентов: {Client.get_total_clients()}")


        another_client = input("\nХотите сделать еще один заказ? (да/нет): ").strip().lower()
        if another_client != 'да':
            break

    # Лямбда-выражения для обработки заказов
    display_order_info = lambda order: print(order.display_info())
    calculate_bulk_order_price = lambda order, product_price: order.calculate_total_price(product_price) if isinstance(order, BulkOrder) else None

    # Пример использования лямбда-выражений
    for client in clients:
        print(f"\nЗаказы клиента {client.name}:")
        for order in client.orders:
            display_order_info(order)

            if isinstance(order, BulkOrder):
                product_price = next((p.price for p in product_list if p.name == order.product_name), None)
                if product_price:
                    total_price = calculate_bulk_order_price(order, product_price)
                    print(f"  Итоговая цена оптового заказа: {total_price} руб.")

    # Лямбда-выражение для фильтрации срочных заказов
    urgent_orders = list(filter(lambda order: isinstance(order, UrgentOrder), [order for client in clients for order in client.orders]))
    print("\nСписок срочных заказов:")
    for order in urgent_orders:
        display_order_info(order)

    # Лямбда-выражение для сортировки клиентов по имени
    sorted_clients = sorted(clients, key=lambda client: client.name)
    print("\nСписок клиентов, отсортированных по имени:")
    for client in sorted_clients:
        print(client)

    print("\nРабота программы завершена.")
    logging.info('Работа программы завершена')


if __name__ == "__main__":
    main()

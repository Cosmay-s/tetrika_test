"""Необходимо реализовать декоратор @strict
Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, объявленным в прототипе функции.
(подсказка: аннотации типов аргументов можно получить из атрибута объекта функции func.__annotations__ или с помощью модуля inspect)
При несоответствии типов бросать исключение TypeError
Гарантируется, что параметры в декорируемых функциях будут следующих типов: bool, int, float, str
Гарантируется, что в декорируемых функциях не будет значений параметров, заданных по умолчанию"""

import inspect


def strict(func):
    signature = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        bound_arguments = signature.bind(*args, **kwargs)

        for param_name, value in bound_arguments.arguments.items():
            excepted_type = annotations.get(param_name)

            if excepted_type and not isinstance(value, excepted_type):
                raise TypeError(
                    "Аргумент '%s' должен быть типа %s, а получил %s" %
                    (param_name, excepted_type.__name__, type(value).__name__)
                )
        return func(*args, **kwargs)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError

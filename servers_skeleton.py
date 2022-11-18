#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, List
import abc


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        if name.isalpha() or name.isdigit():
            self.name = name
            self.price = price
        else:
            raise ValueError("Inproper value of name")

    def __eq__(self, other):
        return isinstance(other, Product) and self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(abc.ABC):
    @abc.abstractmethod
    def __init__(self, list_of_products: List[Product] = []):
        pass


class ListServer(Server):
    n_max_returned_entries = 6

    def __init__(self, list_of_products: List[Product] = []):
        self.list_of_products = list_of_products

    def search_for(self, n_letters: int = 1):
        found = []
        for each in self.list_of_products:
            match = re.search(r"[A-Za-z]{n_letters}\d{2,3}", each.name)
            found += match
        sorted(found, key=my_key)
        length = len(found)
        if length < 3:
            raise TooFewProductsFound(length)
        elif length > 7:
            raise TooManyProductsFound(length)
        return found


class MapServer(Server):
    pass


class TooManyProductsFound(BaseException):
    def __init__(self, amount, message="amount of found product is too high (must be in range 3-7)"):
        self.amount = amount
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message}: {self.amount}'


class TooFewProductsFound(BaseException):
    def __init__(self, amount, message="amount of found product is too low (must be in range 3-7)"):
        self.amount = amount
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message}: {self.amount}'


def my_key(prod: Product) -> str:
    return prod.name


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()
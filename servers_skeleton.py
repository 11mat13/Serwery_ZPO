#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, List, Dict
import abc


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        if not name.isalpha() and not name.isdigit():
            self.name: str = name
            self.price: float = price
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
    n_max_returned_entries = 6
    
    @abc.abstractmethod
    def __init__(self, list_of_products):
        self.list_of_products = list_of_products

    def my_key(self, prod: Product) -> str:
        return prod.name

    @abc.abstractmethod
    def get_list_of_products(self) -> List[Product]:
        pass

    def get_entries(self, n_letters: int = 1):
        found = []
        for each in self.get_list_of_products():
            match = re.search('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), each.name)
            if match:
                found += [each]
        sorted(found, key=self.my_key)
        length = len(found)
        if length < 3:
            raise TooFewProductsFound(length)
        elif length > 7:
            raise TooManyProductsFound(length)
        return found


class ListServer(Server):

    def __init__(self, list_of_products: List[Product] = []):
        super().__init__(list_of_products)

    def get_list_of_products(self) -> List[Product]:
        return self.list_of_products


class MapServer(Server):
    
    def __init__(self, list_of_products: List[Product] = []):
        self.list_of_products: Dict[str, Product] = {prod.name: prod for prod in list_of_products}
        super().__init__(self.list_of_products)

    def get_list_of_products(self) -> List[Product]:
        return list(self.list_of_products.values())


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


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            if n_letters is None:
                entries = self.server.get_entries()
            else:
                entries = self.server.get_entries(n_letters)
            total_price = 0
            for i in entries:
                total_price += i.price
            return total_price
        except TooManyProductsFound:
            return None
        except TooFewProductsFound:
            return None


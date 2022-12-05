#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from collections import Counter

from servers_skeleton import ListServer, Product, Client, MapServer, TooFewProductsFound, TooManyProductsFound

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('PP12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[0], products[2], products[1]]), Counter(entries))

    def test_get_entries_returns_exception_too_few(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooFewProductsFound) as context:
                server.get_entries(2)

    def test_get_entries_returns_exception_too_many(self):
        products = [Product('PP12', 1), Product('PP234', 2), Product('PP235', 1), Product('PP13', 1), Product('PP239', 2), Product('PP238', 1), Product('PP237', 1), Product('PP18', 1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFound) as context:
                server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP12', 1), Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(6, client.get_total_price(2))

    def test_get_entries_returns_exception_too_few(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_get_entries_returns_exception_too_many(self):
        products = [Product('PP12', 1), Product('PP234', 2), Product('PP235', 1), Product('PP13', 1), Product('PP239', 2), Product('PP238', 1), Product('PP237', 1), Product('PP18', 1)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()

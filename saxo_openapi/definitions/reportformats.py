# -*- coding: utf-8 -*-

"""Reportformat related definitions."""


class AccountStatement:
    """Definition representation of AccountStatement"""

    PDF = "PDF"
    Excel = "Excel"

    def __init__(self):
        self._definitions = {
            "PDF": "PDF",
            "Excel": "Excel",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class PortfolioReport:
    """Definition representation of PortfolioReport"""

    PDF = "PDF"

    def __init__(self):
        self._definitions = {
            "PDF": "PDF",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class TradeDetailsReport:
    """Definition representation of TradeDetailsReport"""

    PDF = "PDF"

    def __init__(self):
        self._definitions = {
            "PDF": "PDF",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class TradesExecutedReport:
    """Definition representation of TradesExecutedReport"""

    PDF = "PDF"
    Excel = "Excel"

    def __init__(self):
        self._definitions = {
            "PDF": "PDF",
            "Excel": "Excel",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class TransactionReport:
    """Definition representation of TransactionReport"""

    PDF = "PDF"
    Excel = "Excel"

    def __init__(self):
        self._definitions = {
            "PDF": "PDF",
            "Excel": "Excel",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class TransactionBalanceReport:
    """Definition representation of TransactionBalanceReport"""

    PDF = "PDF"
    Excel = "Excel"

    def __init__(self):
        self._definitions = {
            "PDF": "PDF",
            "Excel": "Excel",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]

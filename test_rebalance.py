import unittest
from rebalance import *
from decimal import *

AAA = Instrument('AAA', 'AAA Index ETF')
BBB = Instrument('BBB', 'BBB Index ETF')
CCC = Instrument('CCC', 'CCC Index ETF')
DDD = Instrument('DDD', 'DDD Index ETF')

class PortfolioBasicTest(unittest.TestCase):

    def setUp(self):
        self.portfolio = Portfolio({CASH: Decimal(1200), AAA: Decimal(300)})

    def test_portfolio_creation(self):
        self.assertEqual(
            self.portfolio.positions, {CASH: Decimal(1200), AAA: Decimal(300)})

    def test_portfolio_total(self):
        self.assertEqual(self.portfolio.total, Decimal(1500))

    def test_portfolio_allocations(self):
        self.assertEqual(
            self.portfolio.allocations, {CASH: Decimal(80), AAA: Decimal(20)})

class RebalanceTest(unittest.TestCase):

    def setUp(self):
        self.model_portfolio = Portfolio({
            CASH: Decimal(10),
            AAA: Decimal(40),
            BBB: Decimal(50)})

    def test_rebalance_cash(self):
        portfolio = Portfolio({CASH: Decimal(5000)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [
            (BUY, AAA, Decimal(2000)),
            (BUY, BBB, Decimal(2500))])

    def test_rebalance_balanced(self):
        portfolio = Portfolio({
            CASH: Decimal(500),
            AAA: Decimal(2000),
            BBB: Decimal(2500)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [])

    def test_rebalance_imbalanced(self):
        portfolio = Portfolio({
            AAA: Decimal(2000),
            BBB: Decimal(8000)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [
            (SELL, BBB, Decimal(3000)),
            (BUY, AAA, Decimal(2000))])

    def test_rebalance_reinvest(self):
        portfolio = Portfolio({
            CCC: Decimal(2000),
            DDD: Decimal(8000)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [
            (SELL, CCC, Decimal(2000)),
            (SELL, DDD, Decimal(8000)),
            (BUY, AAA, Decimal(4000)),
            (BUY, BBB, Decimal(5000))])

if __name__ == '__main__':
    unittest.main()

from __future__ import annotations
from base import BaseEtf
import asyncio

class EqualProportions(BaseEtf):

    def __init__(self: EqualProportions, base_url: str):
        super().__init__(base_url)
    
    @classmethod
    def _get_percentage(cls: EqualProportions, n: int) -> float: 
        """
        return the percentage allocation for each coin in the ETF.

        :param n -> ``int``: the number of coins in the ETF.
        :return -> ``float``: the percent that each coin makes up of the ETF coins price.
        """
        return round(1/n, 3)
    
    def _calc_etf_price(self: EqualProportions) -> float:
        """
        for each coin, take the coins price and calculate its $ value. Then, add all 
        $ values and return that number.

        :return -> ``float``: the price of the ETF coin.
        """
        percentages = self._get_percentage(len(self.coins_tuple))
        
        coin_price = 0
        for coin, data in self.coin_data.items():
            coin_price += percentages * (data['price'])
        
        return round(coin_price, 2)
    
    def calculate(self: EqualProportions) -> int or float:
        """
        the formula used to calculate the equal-proportion weights are:

            1. determine which % of the ETF each coin makes up (1/N where N is the number of coins in the ETF).
            2. use that % to calculate the $ value that each coin puts towards the total value of the coin.
            3. sum up the individual $ values to get the total price of the coin.
        """

        list_of_coin_data = asyncio.run(self.get_coins())
        self.coin_data = self.structure(list_of_coin_data, stats_to_extract=('price',))
        etf_price = self._calc_etf_price()

        return etf_price

# EqualProp = EqualProportions(base_url="https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug=")
# print(EqualProp.calculate())
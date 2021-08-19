from __future__ import annotations
from pos_etf.cli.weights.base import BaseEtf
import asyncio

class NetAssetValue(BaseEtf):

    def __init__(self: NetAssetValue, base_url: str):
        super().__init__(base_url)

    def calculate(self: NetAssetValue) -> int or float:
        """
        the formula used to calculate net asset value (NAV) is:

            (total assets - total liabilities) / (total shares outstanding)

        In the given context, there are no liabilities (just assets, which are market cap-driven).
        Furthermore, in this context, the total number of shares is the total number of coins in
        circulation for the given cryptocurrency.

        :return -> ``int`` or ``float``: total_market_cap / total_coins_outstanding, which is the NAV for the fund.
        """
        list_of_coin_data = asyncio.run(self.get_coins())
        self.coin_data = self.structure(list_of_coin_data, stats_to_extract=('marketCap', 'circulatingSupply'))

        total_market_cap = 0
        total_circulating_supply = 0

        for _, stats in self.coin_data.items():
            total_market_cap += stats["marketCap"]
            total_circulating_supply += stats["circulatingSupply"]

        return round((total_market_cap) / (total_circulating_supply), 2)

from __future__ import annotations
from typing import Tuple, Dict, List
import asyncio
import aiohttp
import json

class BaseEtf(object):
    """
    The Base ETF class that contains useful functions that are used across the various
    ETF-weighting strategies that inherit from it. Each uniue ETF-weighting 
    strategy defined in this folder inherits from this class and utilizes its
    functionality to calculate information for the ETF.

    Attributes:
        coins_tuple: a tuple containing the coins that make up the ETF.

    Methods:
        [TODO]
    """

    coins_tuple = (
        'algorand',
        'cardano',
        'tezos',
        'dash',
        'polkadot',
        'cosmos',
        'the-graph',
        'stellar',
        'cosmos',
        'solana',
        'near-protocol'
    )

    def __init__(self: BaseEtf, base_request_url: str) -> None:
        """
        initialize the BaseEtf object.

        :param base_request_url -> ``str``: the base request URL to be used for HTTP requests.
        :return -> ``None``:
        """
        self.base_request_url = base_request_url

    async def get_coin(self: BaseEtf, coin: str) -> Tuple[str, Dict[str, int or float or str]]:
        """
        retrieve data from coinmarketcap.com for the coins in `self.coins_tuple`.

        :param coin -> ``str``: a valid slug for a Proof-of-Stake coin.
        :return ``Dict[str, int or float or str]`` -> the JSON object containing coin data.
        """
        async with aiohttp.ClientSession() as session:
            response = await session.request("GET", f"{self.base_request_url}{coin}")
            response.raise_for_status()
            json_data = await response.json()

            return (coin, json_data)

    async def get_coins(self: BaseEtf):
        """
        for each coin in coins, setup the get_coin_market_cap() coroutine and gather them.
        Return the gathered coroutines

        :param coins -> Tuple[str]: a tuple containing valid slugs for Proof-of-Stake coins.
        :return ``Dict[str, int or float]``
        """
        list_of_coin_data = await asyncio.gather(*(
            self.get_coin(coin) for coin in self.coins_tuple
        ))

        assert len(list_of_coin_data) == len(
            self.coins_tuple), "length of market caps list != length of coins list"

        return list_of_coin_data

    @classmethod
    def extract(cls: BaseEtf, key_to_extract, object_to_extract_from: Dict[str, int or float or str]) -> int or float or str:
        """
        extract `key_to_extract` from `object_to_extract_from` and return it.

        :param key_to_extract -> ``str``: the key to extract from the JSON object.
        :param object_to_extract_from -> ``Dict[str, int or float or str]``: the object to extract data from.

        :return -> int or float or str: the value associated with `key_to_extract` in the JSON object.
        """
        return object_to_extract_from[key_to_extract]

    @property
    def coin_data(self: BaseEtf):
        """
        GETTER for ``self.structure``
        """
        return self._coin_data

    @coin_data.setter
    def coin_data(self, coin_data: Dict[str, Dict[str, int or float]]) -> None:
        """"""
        self._coin_data = coin_data

    def structure(self: BaseEtf, coin_tuples: List[Tuple[str, str, str]], stats_to_extract: Tuple[str]) -> Dict[str, Dict[str, int or float]]:
        """
        structure the coin statistics as a dictionary with each coin as the keys and
        a dictionary of coin-based statistics as the values.
        
        :param coin_tuples -> ``List[Tuple[str, str, str]]``: a list of tuples where each tuple has:
                                                              (1) coin name
                                                              (2) JSON object of coin-based data

        :returns -> ``Dict[str, Dict[str, int or float]]``: structured data points for each coin.
        """
        etf_datapoints_dict = dict()

        for coin_slug, json_data in coin_tuples:
            filtered_json_data = json_data["data"]["statistics"]
            etf_datapoints_dict[coin_slug] = self._build_json_dump(*stats_to_extract, data=filtered_json_data)

        return etf_datapoints_dict
    
    def _build_json_dump(self: BaseEtf, *stats_to_extract, **coin_statistics) -> Dict[str, int or float]:
        """
        helper function to build a JSON dump from the `kwargs` passed to the func
        
        :stats_to_extract -> ``str``:
            the keys to use as indexers to extract data from the JSON object.
        
        :coin_statistics -> :
            the JSON object to retrieve data from.

        :returns -> ``Dict[str, int or float]``: the JSON dump containing statistics for each coin.
        """
        json_dump = dict()
        for stat in stats_to_extract:
            json_dump[stat] = self.extract(stat, coin_statistics.get("data"))
        
        return json_dump

Base = BaseEtf(
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug=")
list_of_coin_response_objects = asyncio.run(Base.get_coins())

for coin_data in list_of_coin_response_objects:

    coin_name, response_obj = coin_data
    coin_statistics = response_obj["data"]["statistics"]
    print(coin_statistics)

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

    def __init__(self, base_request_url: str) -> None:
        """
        initialize the BaseEtf object.

        :param base_request_url -> ``str``: the base request URL to be used for HTTP requests.
        :return -> ``None``:
        """
        self.base_request_url = base_request_url

    async def get_coin(self, coin: str) -> Tuple[str, Dict[str, int or float or str]]:
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

    async def get_coins(self):
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

    def extract(self, key_to_extract, object_to_extract_from: Dict[str, int or float or str]) -> int or float or str:
        """
        extract `key_to_extract` from `object_to_extract_from` and return it.

        :param key_to_extract -> ``str``: the key to extract from the JSON object.
        :param object_to_extract_from -> ``Dict[str, int or float or str]``: the object to extract data from.

        :return -> int or float or str: the value associated with `key_to_extract` in the JSON object.
        """
        return object_to_extract_from[key_to_extract]

    def structure(self, coin_tuples: List[Tuple[str, str, str]]) -> Dict[str, Dict[str, int or float]]:

        etf_datapoints_dict = dict()

        for coin_slug, json_data in coin_tuples:
            filtered_json_data = json_data["data"]["statistics"]
            etf_datapoints_dict[coin_slug] = self._build_json_dump('marketCap', 'circulatingSupply', data=filtered_json_data)

        return etf_datapoints_dict
    
    def _build_json_dump(self, *args, **kwargs):
        """build a JSON dump from the `kwargs` passed to the func"""
        json_dump = dict()
        for value_to_exact in args:
            json_dump[value_to_exact] = self.extract(value_to_exact, kwargs.get("data"))
        
        return json_dump


    # def pprint_coin_data(self, *keys_to_extract: str) -> None:
    #     """
    #     pretty print useful statistics for each coin.

    #     :keys_to_extract -> ``str``: the keys to attract from the statistics portion of the Coin Market Cap JSON Object.
    #     :return -> ``None``:
    #     """


Base = BaseEtf(
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug=")
list_of_coin_response_objects = asyncio.run(Base.get_coins())


print(Base.structure(list_of_coin_response_objects))
# for coin_data in list_of_coin_response_objects:

#     coin_name, response_obj = coin_data
#     coin_statistics = response_obj["data"]["statistics"]
#     print(Base.extract('marketCap', coin_statistics))
#     print(Base.extract('circulatingSupply', coin_statistics))

# print(Base.extract('marketCap', filtered_response_object))
# test_identifiers = ('marketCap', 'circulatingSupply')
# Base.pprint_coin_data(*test_identifiers)

from typing import Tuple, Dict
import asyncio
import aiohttp


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
    
    def pprint_coin_data(self, *keys_to_extract: str) -> None:
        """
        pretty print useful statistics for each coin.
        
        :keys_to_extract -> ``str``: the keys to attract from the statistics portion of the Coin Market Cap JSON Object.
        :return -> ``None``:
        """
        print(keys_to_extract)


Base = BaseEtf("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug=")
# print(asyncio.run(Base.get_coins()))
test_identifiers = ('marketCap', 'circulatingSupply')
Base.pprint_coin_data(*test_identifiers)
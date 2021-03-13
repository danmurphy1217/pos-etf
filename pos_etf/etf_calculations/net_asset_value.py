"""
This module retrieves, structures, and formats the market cap and circulating
supply data points for the popular Proof-of-Stake coins that compose the Proof-of-Stake
ETF.

Overall, this module focuses on two things:

1. Getting market capitalization and circulating supply data for the POS coins.
2. Structuring that data and using it to calculate the Net Asset Value [which is used to price the ETF].

Data is retrieve from the Coin Market Cap public API.
"""
from typing import Dict, Tuple, List
import aiohttp
import asyncio


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


async def get_coin_market_cap(coin: str) -> Tuple[str, int or float]:
    """
    retrieve market capitalization data for a Proof-of-Stake coin.

    :param coin -> ``str``: a valid slug for a Proof-of-Stake coin.
    :return ``int`` or ``float`` -> an integer representing the market capitalization of `coin`.
    """
    async with aiohttp.ClientSession() as session:
        response = await session.request("GET", f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug={coin}")
        response.raise_for_status()
        json_data = await response.json()

        return (coin, extract_market_cap(json_data), extract_supply_in_circulation(json_data))


def extract_market_cap(json_response: Dict[str, int or float or str]) -> int or float:
    """
    extract market cap data from coinmarketcap.com JSON response

    :param json_response -> ``Dict[str, int or float or str]``: the json response object from the Coin Market Cap API.
    :return -> ``int`` or ``float``: the market cap data for a coin.
    """
    return json_response["data"]["statistics"]["marketCap"]


def extract_supply_in_circulation(json_response: Dict[str, int or float or str]) -> int or float:
    """
    extract circulated supply data from coinmarketcap.com JSON response

    :param json_response -> ``Dict[str, int or float or str]``: the json response object from the Coin Market Cap API.
    :return -> ``int`` or ``float``: the circulated supply data for a coin.
    """
    return json_response["data"]["statistics"]["circulatingSupply"]


async def get_all_market_caps(coins: Tuple[str]) -> Dict[str, int or float]:
    """
    for each coin in coins, setup the get_coin_market_cap() coroutine and gather them.
    Return the gathered coroutines

    :param coins -> Tuple[str]: a tuple containing valid slugs for Proof-of-Stake coins.
    :return ``Dict[str, int or float]``
    """
    list_of_coin_data = await asyncio.gather(*(
        get_coin_market_cap(coin) for coin in coins
    ))

    assert len(list_of_coin_data) == len(
        coins), "length of market caps list != length of coins list"

    return list_of_coin_data


def structure_etf_datapoints(coin_tuple: List[Tuple[str, str, str]]) -> Dict[str, Dict[str, int or float]]:
    """
    This function calculates and returns the % allocated to each coin in the ETF. This ETF
    is weighted by market cap, so the market cap of each individual coin is used to determine how 
    much weight it holds in the ETF.
    """
    etf_datapoints_dict = dict()

    for coin_slug, market_cap, supply in coin_tuple:
        etf_datapoints_dict[coin_slug] = {
            "market_cap": market_cap, "circulating_supply": supply}

    return etf_datapoints_dict


def calculate_net_asset_value(etf_data_dict: Dict[str, Dict[str, int or float]]) -> int or float:
    """
    the formula used to calculate net asset value (NAV) is:

        (total assets - total liabilities) / (total shares outstanding)

    In the given context, there are no liabilities (just assets, which are market cap-driven).
    Furthermore, in this context, the total number of shares is the total number of coins in
    circulation for the given cryptocurrency.

    :param total_assets -> ``int`` or ``float``: the total market cap for all POS coins in the fund.
    :param total_circulating_supply -> ``int`` or ``float``: the total number of coins in circulation for all POS coins in the fund.
    :param total_liabilities -> ``int`` or ``float``: the total liabilities, assumed to be 0.

    :return -> ``int`` or ``float``: total_market_cap / total_coins_outstanding, which is the NAV for the fund.
    """
    total_market_cap = 0
    total_circulating_supply = 0

    for coin in coins_tuple:
        total_market_cap += etf_data_dict[coin]["market_cap"]
        total_circulating_supply += etf_data_dict[coin]["circulating_supply"]

    return round((total_market_cap) / (total_circulating_supply), 2)


# market_caps_dict = asyncio.run(get_all_market_caps(coins_tuple))
# etf_data_dict = structure_etf_datapoints(market_caps_dict)
# net_asset_value = calculate_net_asset_value(etf_data_dict)
# print(net_asset_value)

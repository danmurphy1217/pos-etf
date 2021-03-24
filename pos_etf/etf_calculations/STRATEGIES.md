1. Net Asset Value: divide the sum of the total market cap by the total number of outstanding coins. This is a popular formula used to calculate ETFs in the finance world.
2. Even Distribution: Each coin holds the same weight in the ETF. This is a useful strategy if you believe equally in the possibility that each coin will rise in value.
3. Price Weighted: Rather than market cap, you use the price of the stock to determine its weight of the ETF.


Common across all of these strategies:
1. GET and EXTRACT data from HTTP Requests. This includes firing off an aiohttp request for each coin to retrieve data and extracting data from that response object. Furthermore, it includes using an async function that gathers the coroutines for each coin and fires them off.
2. Structure the data points in a uniform way. For Example:
    ```{
        'Algorand': {
            "first data point": [],
            "second data point": [] # etc...
        }
    }```
3. Calculation function that performs the calculation for that class strategy. Will override the parent `calculate` function if necessary.
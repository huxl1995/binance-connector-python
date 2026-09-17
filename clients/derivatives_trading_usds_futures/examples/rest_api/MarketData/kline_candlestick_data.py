import os
import logging
import pandas as pd

from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures,
    ConfigurationRestAPI,
    DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)
from binance_sdk_derivatives_trading_usds_futures.rest_api.models import (
    KlineCandlestickDataIntervalEnum,
)

KLINES_COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "trades",
    "taker_buy_base",
    "taker_buy_quote",
    "ignore",
]
# Configure logging
logging.basicConfig(level=logging.INFO)

# Create configuration for the REST API
configuration_rest_api = ConfigurationRestAPI(
    api_key=os.getenv("API_KEY", ""),
    api_secret=os.getenv("API_SECRET", ""),
    base_path=os.getenv(
        "BASE_PATH", DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
    ),
)

# Initialize DerivativesTradingUsdsFutures client
client = DerivativesTradingUsdsFutures(config_rest_api=configuration_rest_api)


def kline_candlestick_data():
    try:
        response = client.rest_api.kline_candlestick_data(
            symbol="BTCUSDT",
            interval=KlineCandlestickDataIntervalEnum["INTERVAL_1h"].value,
        )

        rate_limits = response.rate_limits
        logging.info(f"kline_candlestick_data() rate limits: {rate_limits}")

        data = response.data()
        logging.info(f"kline_candlestick_data() response: {data}")
        df = pd.DataFrame(data, columns=KLINES_COLUMNS)
        df["date"] = pd.to_datetime(df["open_time"], unit="ms")
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df[["date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
    except Exception as e:
        logging.error(f"kline_candlestick_data() error: {e}")


if __name__ == "__main__":
    data=kline_candlestick_data()
    logging.info("klines sample:\n%s", data.tail())


import time
from decimal import Decimal
from typing import Any, Dict, Optional, Tuple

from django.conf import settings
from django.core.cache import cache

from src.services.date_service import DateService
from src.services.third_party_service import ThirdPartyService


class CoinGeckoService:
    date_service = DateService()
    third_party_service = ThirdPartyService()
    coin_gecko_cache_key = 'coin_gecko'

    def get_details_by_contract(
        self,
        contract_address: str,
        network: str,
    ):
        coin_gecko_response = cache.get(
            f'{self.coin_gecko_cache_key}_{network}_{contract_address}',
        )
        if coin_gecko_response:
            return coin_gecko_response

        coin_gecko_response = {}
        try:
            coin_gecko_response = self.third_party_service.call(
                'GET',
                f'{settings.COIN_GECKO_URL}/coins/{network}/contract/{contract_address}',
                None,
            ).json()
        except:
            time.sleep(settings.DISCORD_BOT_FETCH_INTERVAL)
            print(
                f"Retry calling coingecko api at {self.date_service.parse('now')}",
            )

            return self.get_details_by_contract(
                contract_address,
                network,
            )

        cache.set(
            f'{self.coin_gecko_cache_key}_{network}_{contract_address}',
            coin_gecko_response,
            settings.DISCORD_BOT_FETCH_INTERVAL,
        )

        return coin_gecko_response

    def get_ticker(
        self,
        contract_details: Dict[str, Any],
        target_market: str
    ) -> Optional[Dict[str, Any]]:
        tickers = contract_details.get('tickers')
        if not tickers:
            return None

        ticker = tickers[0]
        if target_market:
            data = [
                datum
                for datum in tickers
                if target_market.lower() in datum.get('market', {}).get('identifier')
            ]
            if not data:
                return None

            ticker = data[0]

        return ticker

    def get_price_details(
        self,
        contract_details: Dict[str, Any],
        target_currency: str,
        target_market: Optional[str],
    ) -> Tuple[Optional[str], Optional[str]]:
        ticker = self.get_ticker(
            contract_details,
            target_market,
        )
        if not ticker:
            return None, None

        price = ticker.get('converted_last', {}).get(target_currency)
        if not price:

            return None, None

        return f'{round(Decimal(price), 12):12f}', ticker.get('market').get('name')

    def get_market_cap(
        self,
        contract_details: Dict[str, Any],
        target_currency: str,
        target_market: Optional[str],
    ) -> Tuple[Optional[str], Optional[str]]:
        total_supply = contract_details.get(
            'market_data',
            {},
        ).get('total_supply')
        if not total_supply:

            return None, None

        price, price_from = self.get_price_details(
            contract_details,
            target_currency,
            target_market
        )

        if not price:

            return None, None

        return f'{round(Decimal(price) * Decimal(total_supply), 2):,}', price_from

    def get_volume(
        self,
        contract_details: Dict[str, Any],
        target_currency: str,
        target_market: Optional[str],
    ) -> Tuple[Optional[str], Optional[str]]:
        ticker = self.get_ticker(
            contract_details,
            target_market,
        )
        if not ticker:
            return None, None

        volume = ticker.get('converted_volume', {}).get(target_currency)
        if not volume:
            return None, None

        return f'{target_currency.upper()} {round(Decimal(volume), 2)}', ticker.get('market', {}).get('name')

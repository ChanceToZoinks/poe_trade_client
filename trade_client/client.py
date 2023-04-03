import json
import logging
from dataclasses import dataclass, field
from typing import TypeVar

import requests

from .models import *


@dataclass
class ClientConfig:
    league: str
    poesessid: str  # could be replaced with OAuth
    url: str = "https://www.pathofexile.com/api/trade/"
    default_headers: dict[str, str] = field(
        default_factory=lambda: {
            # have to fake the User-Agent to not get a 403
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
    )
    log_level = logging.DEBUG


class TradeClient:
    _config: ClientConfig
    _sess: requests.Session | None = None
    _logger: logging.Logger

    def __init__(self, cfg: ClientConfig) -> None:
        self._config = cfg

        logging.basicConfig(level=cfg.log_level)
        self._logger = logging.getLogger("TradeClient")

    @property
    def config(self):
        return self._config

    def _build_headers(self):
        h = self.config.default_headers
        h.update({"Cookie": f"POESESSID={self.config.poesessid}"})
        return h

    def _build_search_url(self):
        return self.config.url + "search/" + self.config.league

    def _build_fetch_url(self, search_results: list[str]):
        s = ",".join(search_results)
        return self.config.url + "fetch/" + s

    def _request(self, req: requests.Request):
        if not self._sess:
            self._sess = requests.Session()

        self._logger.debug(f"Request to send\n{req.__dict__}\n")
        res = self._sess.send(req.prepare(), allow_redirects=True)
        res.raise_for_status()
        return res

    def _search(self, req: TradeRequest) -> SearchResponse:
        r = requests.Request(
            method="POST",
            url=self._build_search_url(),
            headers=self._build_headers(),
            data=json.dumps(req),
        )
        return self._request(r).json()

    def _fetch(self, built_url: str, query_id: str) -> FetchResponse:
        r = requests.Request(
            method="GET",
            url=built_url,
            params={"query": query_id},
            headers=self._build_headers(),
        )
        return self._request(r).json()

    def _build_request(
        self,
        item_name: str,
        item_type: str,
        online_opt: OnlineStatus,
        price_sort: SortPrice,
        stat_filters: list[QueryStat],
    ) -> TradeRequest:
        return {
            "query": {
                "status": {"option": online_opt},
                "name": item_name,
                "type": item_type,
                "stats": stat_filters,
            },
            "sort": {"price": price_sort},
        }

    _TPage = TypeVar("_TPage")

    def _build_pages(
        self, all_results: list[_TPage], page_width=10
    ) -> list[list[_TPage]]:
        pages = []
        page = []
        for r in all_results:
            if len(page) < page_width:
                page.append(r)
            else:
                pages.append(page)
                page = []
                page.append(r)
        return pages

    def search(
        self,
        item_name: str,
        item_type: str,
        online_opt: OnlineStatus = "online",
        price_sort: SortPrice = "asc",
        stat_filters: list[QueryStat] = [
            {"type": "and", "filters": [], "disabled": False}
        ],
    ) -> FetchResponse:
        search_res = self._search(
            self._build_request(
                item_name, item_type, online_opt, price_sort, stat_filters
            )
        )
        # if more than 10 results have to paginate them
        paged_ids = self._build_pages(search_res["result"])
        result: FetchResponse = {"result": []}
        # only going to show first 10 cos api rate limit
        # you would construct a generator for the pages and query each page when needed (e.g. on a timer to avoid the rate limit)
        fetch_res = self._fetch(self._build_fetch_url(paged_ids[0]), search_res["id"])
        result["result"] += fetch_res["result"]
        return result

#!/usr/bin/env python

import json
import os
import sys

from dotenv import load_dotenv

from trade_client import ClientConfig, SearchConfig, TradeClient

load_dotenv()


def main():
    conf = ClientConfig("Standard", os.getenv("POESESSID", ""))
    client = TradeClient(conf)
    r = client.search(SearchConfig("Redbeak", "Rusted Sword"))
    with open("redbeak_search.json", "w+") as f:
        json.dump(r, f, indent=2, sort_keys=True)

    # build a search for an item you have, open the game and login then run this to get whispered
    r = client.search(
        (
            SearchConfig(
                "Incandescent Heart",
                "Saintly Chainmail",
                query_filters={
                    "trade_filters": {
                        "disabled": False,
                        "filters": {"account": {"input": "temalamorsa"}},
                    }
                },
            )
        )
    )
    if r:
        inc_heart_listing = r["result"][0]["listing"]
        r = client.whisper(inc_heart_listing)

    client.search(
        SearchConfig(
            "Tabula Rasa",
            "Simple Robe",
            live=True,
            live_on_item_callback=lambda x: print(f"Got item {x}"),
        )
    )


if __name__ == "__main__":
    sys.exit(main())

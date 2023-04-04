#!/usr/bin/env python

import json
import os
import sys

from dotenv import load_dotenv

from trade_client import ClientConfig, SearchConfig, TradeClient

load_dotenv()


def main():
    conf = ClientConfig("Sanctum", os.getenv("POESESSID", ""), log_level=10)
    client = TradeClient(conf)
    r = client.search(SearchConfig("Redbeak", "Rusted Sword"))
    with open("redbeak_search.json", "w+") as f:
        json.dump(r, f, indent=2, sort_keys=True)

    r = client.search(
        SearchConfig(
            "Tabula Rasa",
            "Simple Robe",
            live=True,
            live_on_item_callback=lambda x: print(f"Got item {x}"),
        )
    )


if __name__ == "__main__":
    sys.exit(main())

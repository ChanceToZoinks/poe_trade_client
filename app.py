import json
import os
import sys

from trade_client import ClientConfig, TradeClient


def main():
    conf = ClientConfig("Sanctum", os.getenv("POESESSID", ""))
    client = TradeClient(conf)
    r = client.search("Redbeak", "Rusted Sword")
    with open("redbeak_search.json", "w+") as f:
        json.dump(r, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    sys.exit(main())

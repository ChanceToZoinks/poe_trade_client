from typing import Any, Literal, TypedDict


class FilterValue(TypedDict, total=False):
    min: float
    max: float


class QueryFilter(TypedDict):
    disabled: bool
    id: str  # e.g., pseudo.pseudo_adds_physical_damage
    value: FilterValue


StatType = Literal["and", "if", "count", "weight"]


class QueryStat(TypedDict):
    disabled: bool
    filters: list[QueryFilter]
    type: StatType


OnlineStatus = Literal["online", "onlineleague", "any"]


class QueryStatus(TypedDict):
    option: OnlineStatus


class TradeQuery(TypedDict):
    name: str
    stats: list[QueryStat]
    status: QueryStatus
    type: str


SortPrice = Literal["asc"]  # there are more options but im lazy


class TradeSort(TypedDict):
    price: SortPrice


class TradeRequest(TypedDict):
    query: TradeQuery
    sort: TradeSort


class ListingStash(TypedDict):
    name: str
    x: int
    y: int


class ListingAccount(TypedDict):
    name: str
    online: str | None
    language: str
    realm: str


class ListingPrice(TypedDict):
    type: str
    amount: int
    currency: str


class ItemListing(TypedDict):
    method: str
    index: str
    stash: ListingStash
    acccount: ListingAccount


class ItemSocket(TypedDict):
    group: int
    attr: Literal["S", "D", "I", "G"]
    sColour: Literal["R", "G", "B", "W"]


class ItemProperty(TypedDict):
    name: str
    values: list[list[Any]]
    displayMode: int
    type: int


class ItemModMagnitude(TypedDict):
    hash: str
    min: int
    max: int


class ItemExtensionMod(TypedDict):
    name: str
    tier: str
    level: int
    magnitudes: list[ItemModMagnitude]


class ItemExtensionMods(TypedDict):
    explicit: list[ItemExtensionMod]
    implicit: list[ItemExtensionMod]


class ItemExtensionHashes(TypedDict):
    explicit: tuple[str, list[int]]
    implicit: tuple[str, list[int]]


class ItemExtension(TypedDict):
    dps: float
    pdps: float
    edps: float
    dps_aug: bool
    pdps_aug: bool
    mods: ItemExtensionMods
    hashes: ItemExtensionHashes
    text: str


class Item(TypedDict):
    verified: bool
    w: int
    h: int
    icon: str
    league: str
    id: str
    sockets: list[ItemSocket]
    name: str
    typeLine: str
    baseType: str
    identified: bool
    ilvl: int
    properties: list[ItemProperty]
    implicitMods: list[str]
    explicitMods: list[str]
    flavourText: list[str]
    frameType: int
    extended: ItemExtension


class SearchResponse(TypedDict):
    """Send a POST with a TradeRequest to search"""

    id: str  # pass this as a query param after the POST to get the results
    complexity: int
    result: list[str]
    total: int


class SearchResult(TypedDict):
    id: str  # will match an entry in the list of results in PrepTradeResponse
    listing: ItemListing
    item: Item


class FetchResponse(TypedDict):
    """Send a GET request to fetch the search results"""

    result: list[SearchResult]

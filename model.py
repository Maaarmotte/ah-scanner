from dataclasses import dataclass
from typing import List

from reader import BufferReader


@dataclass
class InboundWakfuPacket:
    timestamp: int          # not part of the protocol
    length: int             # 2 bytes
    type: int               # 2 bytes
    unknown_byte: int       # 1 byte
    payload: bytes
    unknown_int: int        # 4 bytes

    @staticmethod
    def from_bytes(raw_data: bytes, timestamp: int):
        reader = BufferReader(raw_data)

        return InboundWakfuPacket(
            timestamp,
            reader.short(),
            reader.short(),
            reader.byte(),
            reader.bytes(reader.integer()),
            reader.integer())


@dataclass
class PetItem:
    definition_id: int          # 4 bytes
    name: str                   # 2 bytes length
    color_item_ref_id: int      # 4 bytes
    equipped_ref_item_id: int   # 4 bytes
    health: int                 # 4 bytes
    xp: int                     # 4 bytes
    last_meal_date: int         # 8 bytes
    last_hungry_date: int       # 8 bytes
    sleep_ref_item_id: int      # 4 bytes
    sleep_date: int             # 8 bytes

    @staticmethod
    def from_reader(reader: BufferReader):
        return PetItem(
            reader.integer(),
            reader.string(),
            reader.integer(),
            reader.integer(),
            reader.integer(),
            reader.integer(),
            reader.long(),
            reader.long(),
            reader.integer(),
            reader.long())


@dataclass
class RawXpItem:
    definition_id: int  # 4 bytes
    xp: int             # 8 bytes

    @staticmethod
    def from_reader(reader: BufferReader):
        return RawXpItem(
            reader.integer(),
            reader.long())


@dataclass
class Shard:
    position: int           # 1 byte
    slotted_item_id: int    # 4 bytes
    slot_color: int         # 1 byte
    shards_amount: int      # 4 bytes

    @staticmethod
    def from_reader(reader: BufferReader):
        return Shard(
            reader.byte(),
            reader.integer(),
            reader.byte(),
            reader.integer())


@dataclass
class Gem:
    property_id: int        # 1 byte
    gem_ref_id: int         # 4 bytes

    @staticmethod
    def from_reader(reader: BufferReader):
        return Gem(
            reader.byte(),
            reader.integer())


@dataclass
class ItemUpgrades:
    shard_slots: List[Shard]
    additional_gems: List[Gem]
    sublimation_item_id: int            # 4 bytes
    special_sublimation_item_id: int    # 4 bytes
    charge: int                         # 1 byte

    @staticmethod
    def from_reader(reader: BufferReader):
        return ItemUpgrades(
            [Shard.from_reader(reader) for _ in range(reader.short())],
            [Gem.from_reader(reader) for _ in range(reader.short())],
            reader.integer(),
            reader.integer(),
            reader.byte())


@dataclass
class CompanionInfo:
    xp: int     # 8 bytes

    @staticmethod
    def from_reader(reader: BufferReader):
        return CompanionInfo(reader.long())


@dataclass
class RawItemBind:
    type: int       # 1 byte
    applied: int    # 1 byte

    @staticmethod
    def from_reader(reader: BufferReader):
        return RawItemBind(
            reader.byte(),
            reader.byte())


@dataclass
class RawItemElements:
    damage_elements: int        # 1 byte
    resistance_elements: int    # 1 byte

    @staticmethod
    def from_reader(reader: BufferReader):
        return RawItemElements(
            reader.byte(),
            reader.byte())


@dataclass
class RawMergedItems:
    version: int        # 4 bytes
    items: List[int]

    @staticmethod
    def from_reader(reader: BufferReader):
        return RawMergedItems(
            reader.integer(),
            [x for x in reader.bytes(reader.short())])


@dataclass
class SkinItem:
    skin_item_ref_id: int   # 4 bytes

    @staticmethod
    def from_reader(reader: BufferReader):
        return SkinItem(reader.integer())


@dataclass
class RawItem:
    unique_id: int          # 8 bytes
    ref_id: int             # 4 bytes
    quantity: int           # 2 bytes
    pet_item: PetItem
    raw_xp: RawXpItem
    item_upgrades: ItemUpgrades
    companion_info: CompanionInfo
    raw_item_bind: RawItemBind
    raw_item_elements: RawItemElements
    raw_merged_items: RawMergedItems
    skin_item: SkinItem

    @staticmethod
    def from_reader(reader: BufferReader):
        return RawItem(
            reader.long(),
            reader.integer(),
            reader.short(),
            PetItem.from_reader(reader) if reader.byte() == 1 else None,
            RawXpItem.from_reader(reader) if reader.byte() == 1 else None,
            ItemUpgrades.from_reader(reader) if reader.byte() == 1 else None,
            CompanionInfo.from_reader(reader) if reader.byte() == 1 else None,
            RawItemBind.from_reader(reader) if reader.byte() == 1 else None,
            RawItemElements.from_reader(reader) if reader.byte() == 1 else None,
            RawMergedItems.from_reader(reader) if reader.byte() == 1 else None,
            SkinItem.from_reader(reader) if reader.byte() == 1 else None)


@dataclass
class MarketEntry:
    id: int                 # 8 bytes
    seller_id: int          # 8 bytes
    seller_name: str
    pack_type_id: int       # 1 byte
    pack_type_number: int   # 2 bytes
    pack_price: int         # 8 bytes
    duration_id: int        # 1 byte
    release_date: int       # 8 bytes
    raw_item: RawItem
    unknown_byte1: int      # 1 byte
    unknown_byte2: int      # 1 byte

    @staticmethod
    def from_reader(reader: BufferReader):
        return MarketEntry(
            reader.long(),
            reader.long(),
            reader.string(),
            reader.byte(),
            reader.short(),
            reader.long(),
            reader.byte(),
            reader.long(),
            RawItem.from_reader(reader),
            reader.byte(),
            reader.byte())


@dataclass
class MarketSearchResult:
    entries: List[MarketEntry]

    @staticmethod
    def from_payload(raw_data: bytes):
        reader = BufferReader(raw_data)

        return MarketSearchResult([MarketEntry.from_reader(reader) for _ in range(reader.integer())])


@dataclass
class OutboundWakfuPacket:
    timestamp: int  # not part of the protocol
    length: int     # 2 bytes
    type: int       # 1 byte
    id: int         # 2 bytes
    payload: bytes  # length - 5

    @staticmethod
    def from_bytes(raw_data: bytes, timestamp: int):
        reader = BufferReader(raw_data)

        return OutboundWakfuPacket(
            timestamp,
            reader.short(),
            reader.byte(),
            reader.short(),
            reader.remaining())


@dataclass
class MarketSearchRequest:
    category: int           # 2 bytes
    lvl_min: int            # 2 bytes
    lvl_max: int            # 2 bytes
    price_min: int          # 4 bytes
    price_max: int          # 4 bytes
    unknown1: int           # 1 byte always 0xff
    unknown2: int           # 2 bytes always 0x0000
    only_min_price: int     # 1 byte
    search_term: bytes

    @staticmethod
    def from_payload(payload: bytes):
        reader = BufferReader(payload)

        return MarketSearchRequest(
            reader.short(),
            reader.short(),
            reader.short(),
            reader.integer(),
            reader.integer(),
            reader.byte(),
            reader.short(),
            reader.byte(),
            reader.remaining())

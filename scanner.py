import json
import time

from content import wakfu_items, wakfu_categories
from db import MarketEntriesStorage
from model import InboundWakfuPacket, MarketSearchResult, OutboundWakfuPacket, MarketSearchRequest


def conditions_to_save_met(market_request: MarketSearchRequest):
    return (market_request.lvl_min == -1 and market_request.lvl_max == 115) \
        or (market_request.lvl_min == 116 and market_request.lvl_max == 230)


class WakfuScanner:
    def __init__(self):
        self.market_results = []
        self.storage = MarketEntriesStorage()
        self.session = "no_session"
        self.should_save = False

    def parse_raw_data(self, source, raw_data):
        now = time.time_ns()

        if source == 'client':
            packet_length = int.from_bytes(raw_data[0:2], byteorder='big')

            if packet_length >= 5:
                packet = OutboundWakfuPacket.from_bytes(raw_data, now)

                # Client search request
                if packet.type == 3 and packet.id == 12664:
                    market_request = MarketSearchRequest.from_payload(packet.payload)
                    cat_name = wakfu_categories[market_request.category]

                    self.update_session(market_request)

                    print('Searching in category "%s" between levels %d and %d '
                          % (cat_name, market_request.lvl_min, market_request.lvl_max))

        if source == 'server':
            packet_type = int.from_bytes(raw_data[2:4], byteorder='big')

            if packet_type == 15811:
                packet = InboundWakfuPacket.from_bytes(raw_data, now)
                market_result = MarketSearchResult.from_payload(packet.payload)

                self.market_results.append(market_result)

                for entry in market_result.entries:
                    if self.should_save:
                        serialized = json.dumps(entry, default=lambda o: o.__dict__)
                        self.storage.insert_market_entry(now, self.session, serialized)
                    else:
                        print("[%s] sold by [%s]" % (wakfu_items[entry.raw_item.ref_id], entry.seller_name))

    def update_session(self, market_request: MarketSearchRequest):
        if conditions_to_save_met(market_request):
            if self.session == "no_session":
                self.session = 's%d' % time.time_ns()
                self.should_save = True
                print("Switched to new scanning session %s" % self.session)
        else:
            if self.session != "no_session":
                print("Ended session %s" % self.session)
                self.session = "no_session"
                self.should_save = False

from functools import cache
from typing import Iterable
from dataclasses import dataclass

import requests


__HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "Content-Type": "application/json",
    "Accept": "application",
}


@dataclass
class BalanceInfo:
    """
    data class representing balance information of a bitcoin address.
    """
    address: str
    confirmed: int
    received: int
    txs: int
    unconfirmed: int
    utxo: int


def get_balance_info(address: str) -> BalanceInfo:
    """
    get balance info of a bitcoin address.
    
    :param address: bitcoin address
    :type address: str
    :return: balance info of the address
    :rtype: BalanceInfo
    """
    url = f"https://api.blockchain.info/haskoin-store/btc/address/{address}/balance"
    resp = requests.get(url, headers=__HEADERS).json()
    return BalanceInfo(**resp)


def get_tx_ids(address: str) -> set[str]:
    """
    get transaction ids of a bitcoin address.
    
    :param address: bitcoin address
    :type address: str
    :return: set of transaction ids
    :rtype: set[str]
    """
    url = (
        "https://api.blockchain.info/haskoin-store/btc/address/%s/transactions?limit=10000&offset=0"
        % address
    )
    resp = requests.get(url, headers=__HEADERS).json()
    tx_ids = set()
    for e in resp:
        tx_ids.add(e["txid"])
    return tx_ids


@cache
def get_tx_info(tx_id: str) -> dict:
    """
    get transaction info by a bitcoin transaction id.
    
    :param tx_id: bitcoin transaction id
    :type tx_id: str
    :return: transaction info
    :rtype: dict
    """
    url = "https://api.blockchain.info/haskoin-store/btc/transaction/" + tx_id
    resp = requests.get(url, headers=__HEADERS).json()
    return resp


def get_tx_infos(*tx_id) -> Iterable[dict]:
    """
    get transaction info by a bitcoin transaction id.
    
    :param tx_id: bitcoin transaction id
    :return: transaction info
    :rtype: Iterable[dict]
    """
    def __get_tx_infos(*tx_id):
        url = (
            "https://api.blockchain.info/haskoin-store/btc/transactions?txids="
            + ",".join(list(tx_id))
        )
        resp = requests.get(
            url, headers=__HEADERS
        ).json()  # value에는 100000000을 나눠야 btc 값이 나옴.
        return resp

    window_size = 10
    for sub_tx_ids in [
        tx_id[i : i + window_size] for i in range(0, len(tx_id), window_size)
    ]:
        for tx in __get_tx_infos(*sub_tx_ids):
            yield tx

from colorama import Fore, Style

from flashlight.blockchain import get_tx_ids, get_tx_infos


def main():
    target = ""

    tx_ids = list(get_tx_ids(target))
    for tx in get_tx_infos(*tx_ids):
        inputs = tx["inputs"]
        outputs = tx["outputs"]

        print(Style.RESET_ALL, end="")
        print("Transaction", tx["txid"][:4] + "-" + tx["txid"][-4:])
        for input_ in inputs:
            address = input_["address"][:5] + "-" + input_["address"][-5:]
            print(
                (Fore.RED if input_["address"] == target else "")
                + f"  {address} ==> {input_['value'] / 100000000:.8f} BTC"
            )
            print(Style.RESET_ALL, end="")
        for output in outputs:
            address = output["address"][:5] + "-" + output["address"][-5:]
            print(
                (Fore.RED if output["address"] == target else "")
                + f"  {address} <== {output['value'] / 100000000:.8f} BTC"
            )
            print(Style.RESET_ALL, end="")


if __name__ == "__main__":
    main()

import requests, time

def skale_abandon():
    print("SKALE — Chain Abandon Detector (> $10M withdrawn from a single SKALE chain)")
    seen = set()
    while True:
        # SKALE Manager contract – withdrawal from any SKALE chain to Ethereum
        r = requests.get("https://api.etherscan.io/api?module=account&action=txlist"
                        "&address=0x00c047f19D33c3fC0f9eb06D04C8d10F38e95b19&sort=desc"
                        "&apikey=YourApiKeyIfYouWant")
        for tx in r.json().get("result", [])[:30]:
            h = tx["hash"]
            if h in seen: continue
            seen.add(h)

            # withdrawFunds function on SKALE Manager
            if tx.get("input", "")[:10] != "0x5f5e6e6d": continue

            value = int(tx["value"]) / 1e18
            if value >= 10_000_000:  # > $10M leaving a SKALE chain
                print(f"SKALE CHAIN ABANDONED\n"
                      f"${value:,.0f} withdrawn from a SKALE chain → Ethereum\n"
                      f"Owner: {tx['from']}\n"
                      f"Tx: https://etherscan.io/tx/{h}\n"
                      f"→ Someone just pulled the plug on their entire app-chain\n"
                      f"→ All dApps, users, liquidity — now stranded\n"
                      f"→ SKALE just lost a tenant forever\n"
                      f"{'-'*75}")
        time.sleep(4.1)

if __name__ == "__main__":
    skale_abandon()

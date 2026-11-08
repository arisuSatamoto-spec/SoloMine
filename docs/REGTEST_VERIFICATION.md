# Regtest integration verification — 2026-11-08

This document records the results reported by the SoloMine operator on Ubuntu 26.04.1, Bitcoin Core 32.1 and CKPool built from pinned upstream revision `bef6dd2efa2ed803d77fb49fbc064666685cb742` with `scripts/apply-fee-patch.py`.

## Observed

- Bitcoin Core Regtest RPC at localhost:18443, SoloMine Stratum at localhost:3339.
- `mining.subscribe`, `mining.authorize` (true) and `mining.notify` passed.
- A SHA256d CPU miner submitted solutions; CKPool logged `BLOCK ACCEPTED!` twice.
- Bitcoin Core `getblock` showed accepted blocks at heights **2** and **3**.
- Each coinbase had three outputs: **4,900,000,000 sat** to the miner; **100,000,000 sat** to the regtest developer address; **0 sat** to the witness commitment. Sum: **5,000,000,000 sat**.
- Both operator-run payout checks reported `PASS`.

This is a manual, operator-reported integration test, not a reproducible automated test suite. It does not prove mainnet readiness.

## Independent recheck of the two accepted blocks

Run this on the operator's Regtest machine:

```bash
python3 - <<'PY'
import json, subprocess
from decimal import Decimal
from pathlib import Path
home = Path.home()
cli = home / "solomine-test/bitcoin-32.1/bin/bitcoin-cli"
datadir = home / "solomine-test/regtest-data"
def rpc(*args):
    return subprocess.check_output(
        [str(cli), "-regtest", f"-datadir={datadir}", *map(str, args)],
        text=True
    ).strip()
for height in (2, 3):
    block_hash = rpc("getblockhash", height)
    block = json.loads(rpc("getblock", block_hash, 2), parse_float=Decimal)
    outputs = block["tx"][0]["vout"]
    amounts = [int(o["value"] * 100_000_000) for o in outputs]
    total = sum(amounts)
    developer = total // 50
    miner = total - developer
    assert sorted(x for x in amounts if x > 0) == sorted((miner, developer))
    assert sum(x == 0 for x in amounts) >= 1
    for o in outputs:
        print(height, o["n"], o["value"], o["scriptPubKey"].get("address", "non-address"))
    print("BLOCK", height, "AMOUNTS PASS", "HASH", block_hash)
PY
```

**Important:** The sample assertion validates amounts, not ownership of the payout addresses. Before a production release, assert the developer output's exact expected network-specific address and the miner output's exact submitted username address, and test coinbases with transaction fees and SegWit transactions.

## Remaining blockers for a mainnet release

1. Automated integration suite that mines through SoloMine and checks recipients, values, and consensus acceptance.
2. Tests with transaction fees, witness commitments and varied address types.
3. Build/restart/security tests and review of Bitcoin Core RPC authentication.
4. Mainnet configuration and synchronized Bitcoin Core node; release artifacts and documentation.
5. Independent review and transparent disclosure of the 2% fee.

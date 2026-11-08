# Upstream CKPool integration audit (2026-11-08)

Upstream: https://github.com/ckolivas/ckpool (official mirror; branch `master`). This is a source inspection, **not** a code import or a successful build.

## Verified source locations

- `src/ckpool.c` around lines 1786–1791 parses the JSON `donation` setting and clamps it to the 0–99.9% range, with donations below 0.1% disabled. Around line 2274, testnet handling is discussed.
- `src/stratifier.c`, `generate_coinbase()` around lines 595–814, assembles coinbase components. Around lines 679–707, it computes the donation output and adjusts the miner output. **Current upstream uses floating-point conversion** for the donation amount; review before adopting for a fixed-fee implementation.
- `README.md` documents `ckpool -B` BTC solo mode, with per-miner Bitcoin-address usernames and reward distribution minus configured donation. It also documents `mindiff`, `startdiff`, `maxdiff`, and Stratum V2 options.

## Implementation plan

1. Import the upstream source as a tracked baseline, retaining its license, authors and history attribution.
2. Implement a clearly disclosed `SOLOMINE_FEE_BPS = 200` (2%) in the official distribution, replacing any configurable donation behavior for the SoloMine solo mode; explicitly document how upstream donation is treated to prevent double charges.
3. Use checked **integer satoshi** calculations; define rounding explicitly, then construct both miner and developer outputs with validated scripts.
4. Ensure testnet/regtest uses network-correct scripts and no accidental mainnet address output.
5. Add tests for reward arithmetic, script destinations, witness commitment preservation, solo-user address changes, and invalid addresses; run Bitcoin Core regtest integration tests.
6. Only then publish a production-ready release. **No such release exists yet.**

## Risk notes

- Fixed in official source does **not** mean tamper-proof: GPL users can modify source and rebuild.
- The actual upstream source has **not** been imported into this repository in this step.
- Mining and payout functionality are **not yet tested** in SoloMine.

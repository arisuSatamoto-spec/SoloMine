# SoloMine v0.1.0-prealpha — source preview (NOT a mining release)

Published for code review and development only. **Do not mine Bitcoin using this preview.**

## Included
- GPL-3.0 license and attribution to upstream CKPool.
- Transparent 2% developer fee specification and address.
- Standalone C and Python integer reward arithmetic reference implementations.
- A fail-closed patch script for a pinned upstream CKPool checkout.
- A build helper and GitHub Actions source/fee checks.

## Not verified
- Full upstream CKPool build.
- Stratum miner connectivity and share handling.
- Coinbase outputs and SegWit commitment correctness.
- Bitcoin Core regtest block acceptance.
- Mainnet mining or payment safety.

The upstream CKPool source is **not vendored** in this repository; the build script fetches it separately. The official GitHub Release binary and production-ready tag have **not** been created. A preview branch is not a tested mining release.

## Build experiment (developer only)
```bash
bash scripts/build-from-upstream.sh bef6dd2efa2ed803d77fb49fbc064666685cb742
```
Requires Git, Python 3, C build tools, autoconf/automake and upstream build dependencies. Do not connect real hashrate until independent regtest validation succeeds.

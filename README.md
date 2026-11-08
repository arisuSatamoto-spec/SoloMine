# SoloMine

**Self-hosted Bitcoin solo mining based on CKPool — experimental build, Regtest validated.**

SoloMine is an independent, unofficial project based on [CKPool](https://github.com/ckolivas/ckpool). It does not require a connection to a hosted SoloMine server. The source repository contains a reproducible build helper that fetches a pinned upstream CKPool revision and applies the SoloMine changes.

## Verified on Bitcoin Core Regtest (8 November 2026)

An operator running Ubuntu 26.04.1, Bitcoin Core 32.1 and the locally built SoloMine CKPool binary reported and provided terminal evidence for:

- Successful CKPool compilation and startup in Bitcoin solo mode.
- Bitcoin Core RPC connectivity, Stratum V1 subscribe/authorize and mining job delivery.
- CPU miner SHA-256d shares accepted and **two blocks accepted by Bitcoin Core at heights 2 and 3**.
- On-chain coinbase inspection at both heights: **49 BTC** to the miner's regtest address, **1 BTC** to the developer's regtest address, and a zero-value witness commitment output. Both blocks had 50 BTC coinbase totals and passed amount checks.

These are **Regtest coins without monetary value**. Results are based on the operator's logs and command output, not an independently reproduced CI integration run. The successful tests do not establish mainnet readiness.

## Fee policy

Official SoloMine builds target a **fixed 2% developer fee** of the complete coinbase reward (subsidy plus transaction fees), with the remaining amount paid to the solo miner. The fee is calculated in integer satoshis as `developer = total // 50`; the miner receives the remainder. The official mainnet developer address is:

`bc1qtqwusq7fld4y7jsrwfckalmrjpgfg0tv5rfncl`

The upstream donation mechanism is repurposed in the official patched build. The mainnet address must be verified in the actual binary before using it with real hashrate. Users can modify this GPL-licensed source; no claim is made that an open-source fee is impossible to change.

## Build from pinned upstream

```bash
sudo apt install -y git build-essential autoconf automake libtool pkg-config yasm libcurl4-openssl-dev libjansson-dev libssl-dev python3
git clone https://github.com/arisuSatamoto-spec/SoloMine.git
cd SoloMine
bash scripts/build-from-upstream.sh bef6dd2efa2ed803d77fb49fbc064666685cb742
```

This builds into `build/ckpool/src/ckpool`. **Do not use this experimental build on mainnet yet.** The build script does not provide a Bitcoin Core node or configure its RPC credentials. Protect RPC cookies/passwords, bind test Stratum to loopback, and keep regtest configuration separate from mainnet.

## Mainnet release gates

Before publishing a production mining release, complete and document: reproducible clean builds; automated Regtest mining and exact recipient-address assertions; blocks containing real transactions and transaction fees; SegWit/witness commitment tests; restarts, reconnects and invalid-share tests; address/network mismatch rejection; security review of RPC and exposed Stratum; verified mainnet developer address and complete operator documentation. A fully synchronized Bitcoin Core mainnet node is required for real Bitcoin solo mining.

See [Regtest verification](docs/REGTEST_VERIFICATION.md) and [development status](docs/DEVELOPMENT_STATUS.md).

## License

GPL-3.0. Upstream CKPool copyright notices and license obligations remain applicable. SoloMine is not affiliated with the upstream CKPool maintainers.

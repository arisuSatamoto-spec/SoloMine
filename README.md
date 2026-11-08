# SoloMine

**Self-hosted Bitcoin solo mining — based on CKPool (work in progress).**

> **Pre-alpha — not ready for production mining.** The CKPool source and reward-splitting implementation have **not** been integrated or tested yet.

SoloMine aims to let miners operate their own Bitcoin Core node, local Stratum server and ASIC workers without relying on a hosted pool. This project is independent of the original CKPool maintainers.

## Planned features

- Local, self-hosted Bitcoin solo mining using CKPool as the upstream base.
- Fixed **2% developer fee** on successful block rewards in the official build; **98%** to the miner's configured payout address.
- Explicit on-chain reward outputs in the block coinbase transaction; no fee charged for unsuccessful mining attempts.
- Local worker statistics, difficulty management, and reproducible test coverage.

## Developer fee transparency

The intended developer-fee address is `bc1qtqwusq7fld4y7jsrwfckalmrjpgfg0tv5rfncl` (Bitcoin mainnet). The fee applies to the **total block reward** (subsidy plus transaction fees), subject to exact satoshi rounding rules to be specified and tested. A fee configured in the official build cannot be made unmodifiable in open-source software: users can inspect and modify the source under its license.

**Important:** There is no functioning payout-split code in this repository yet. Do not direct hashrate to it or assume it can construct valid Bitcoin blocks.

## Development roadmap

1. Import and attribute upstream CKPool source, retaining original copyright notices.
2. Identify the coinbase output construction and block-template paths.
3. Implement explicit 98/2 output splitting with strict amount and address validation.
4. Add unit tests, regtest integration tests and coinbase-output verification before mainnet testing.
5. Document building, configuration, security and operations.

See [reward design](docs/REWARD_DESIGN.md) and [development status](docs/DEVELOPMENT_STATUS.md).

## License and attribution

GPL-3.0. Based on [CKPool by Con Kolivas and contributors](https://github.com/ckolivas/ckpool); this is an independent, unofficial project. Upstream source files and attribution will be preserved when imported.

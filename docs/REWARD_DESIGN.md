# Coinbase reward split — design specification (not implemented)

## Objective
For a valid Bitcoin block candidate, allocate exactly 2% of the total available reward (subsidy + transaction fees) to the published developer address and the remainder to the configured miner address. No remote developer server is needed.

## Rules to implement and verify

1. Use integer satoshis only. Compute `developer_sat = floor(total_reward_sat * 2 / 100)`; `miner_sat = total_reward_sat - developer_sat`. Avoid floating-point arithmetic and overflow.
2. Validate both Bitcoin addresses for the correct chain/network and convert them into valid scriptPubKeys; reject missing or invalid addresses.
3. Build two explicit coinbase transaction outputs; do not alter SegWit witness commitment outputs or block weight limits. Respect all applicable coinbase and consensus rules.
4. Ensure the transaction output sum never exceeds the available subsidy plus included fees. Verify exact output scripts and amounts before distributing work.
5. Handle template refresh, chain reorganizations, transaction-fee changes, and miner address configuration safely.
6. Run deterministic unit tests and Bitcoin Core regtest end-to-end tests. Verify the accepted block's coinbase outputs independently.
7. Disclose the fee and address in the README, release notes and runtime startup logs.

## Fee destination (Bitcoin mainnet)
`bc1qtqwusq7fld4y7jsrwfckalmrjpgfg0tv5rfncl`

## Security note
This document is a design proposal, not an implemented or audited payout system. No real BTC or production hashrate should be used until tested.

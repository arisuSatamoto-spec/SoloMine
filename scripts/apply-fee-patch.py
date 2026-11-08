#!/usr/bin/env python3
"""Apply SoloMine's transparent fixed fee to a clean upstream CKPool checkout.

Fails closed if upstream source changes. NOT a substitute for regtest testing.
"""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd()
ck = ROOT / "src/ckpool.c"
st = ROOT / "src/stratifier.c"

def replace_once(path, old, new):
    source = path.read_text()
    if source.count(old) != 1:
        raise SystemExit(f"Unsupported upstream version: expected one match in {path}: {old[:65]!r}; found {source.count(old)}")
    path.write_text(source.replace(old, new, 1))

# Replace upstream donation parsing with the official fixed fee.
replace_once(ck,
    'yyjson_obj_get_double(&ckpool.donation, json_conf, "donation");\n\t/* Avoid dust-sized donations */\n\tif (ckpool.donation < 0.1)\n\t\tckpool.donation = 0;\n\telse if (ckpool.donation > 99.9)\n\t\tckpool.donation = 99.9;',
    '/* SoloMine official build: fee is not configurable via JSON. */\n\tckpool.donation = 2.0;')

replace_once(ck,
    'parse_config();\\n\\t/* Set defaults if not found in config file */',
    'parse_config();\\n\\t/* SoloMine official distribution supports solo mining only. */\\n\\tif (!ckpool.btcsolo)\\n\\t\\tquit(0, "SoloMine requires Bitcoin solo mode (-B)");\\n\\t/* Set defaults if not found in config file */')

replace_once(ck,
    'ckpool.donaddress = "bc1q28kkr5hk4gnqe3evma6runjrd2pvqyp8fpwfzu";',
    'ckpool.donaddress = "bc1qtqwusq7fld4y7jsrwfckalmrjpgfg0tv5rfncl";')

# Preserve upstream testnet/regtest addresses: mainnet address is invalid there.
# Replace floating-point fee computation with exact integer arithmetic.
replace_once(st,
    'double dbl64 = (double)g64 / 100 * ckpool.donation;\n\n\t\td64 = dbl64;',
    '/* Exact 200 bps developer fee, rounded down to a satoshi. */\n\t\td64 = (g64 / 50) + ((g64 % 50) / 50);')

# Reject accidental non-solo operation in this official distribution.
# The upstream -B mode must be selected by the operator; this patch does
# not alter other pool modes. Do not advertise fee enforcement elsewhere.
print("SoloMine fee patch applied; build and regtest validation still required.")

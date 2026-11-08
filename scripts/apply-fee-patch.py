#!/usr/bin/env python3
"""Patch a pinned, clean upstream CKPool source checkout for SoloMine.

This is NOT a substitute for a successful build and Bitcoin Core regtest.
"""
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd()
ck = ROOT / "src/ckpool.c"
st = ROOT / "src/stratifier.c"

def replace_once(source: str, old: str, new: str, label: str) -> str:
    matches = source.count(old)
    if matches != 1:
        raise RuntimeError(f"{label}: expected exactly one upstream match, found {matches}")
    return source.replace(old, new, 1)

def main() -> None:
    ck_src = ck.read_text()
    st_src = st.read_text()

    ck_src = replace_once(ck_src,
        'yyjson_obj_get_double(&ckpool.donation, json_conf, "donation");\n\t/* Avoid dust-sized donations */\n\tif (ckpool.donation < 0.1)\n\t\tckpool.donation = 0;\n\telse if (ckpool.donation > 99.9)\n\t\tckpool.donation = 99.9;',
        '/* SoloMine official build: fixed 2% fee; JSON donation ignored. */\n\tckpool.donation = 2.0;',
        "donation setting")

    ck_src = replace_once(ck_src,
        'parse_config();\n\t/* Set defaults if not found in config file */',
        'parse_config();\n\t/* SoloMine requires Bitcoin solo mode (-B). */\n\tif (!ckpool.btcsolo)\n\t\tquit(0, "SoloMine requires Bitcoin solo mode (-B)");\n\t/* Set defaults if not found in config file */',
        "solo mode enforcement")

    ck_src = replace_once(ck_src,
        'ckpool.donaddress = "bc1q28kkr5hk4gnqe3evma6runjrd2pvqyp8fpwfzu";',
        'ckpool.donaddress = "bc1qtqwusq7fld4y7jsrwfckalmrjpgfg0tv5rfncl";',
        "developer address")

    st_src = replace_once(st_src,
        'double dbl64 = (double)g64 / 100 * ckpool.donation;\n\n\t\td64 = dbl64;',
        '/* Fixed 2% fee, integer satoshis, round down. */\n\t\td64 = g64 / 50;',
        "integer fee calculation")

    # Enforce fee availability before coinbase construction.
    marker = re.compile(r'(?m)^([ \t]*)// Generation value
    ck.write_text(ck_src)
    st.write_text(st_src)
    print("SoloMine patch applied. Full build and regtest still required.")

if __name__ == "__main__":
    main()
)
    matches = list(marker.finditer(st_src))
    if len(matches) != 1:
        raise RuntimeError(f"fee guard: expected one marker, found {len(matches)}")
    m = matches[0]
    indent = m.group(1)
    lines = [
        '/* SoloMine: validate fee before building coinbase. */',
        'if (!ckpool.donvalid || ckpool.donation != 2.0 ||',
        '    !sdata->dontxnlen) {',
        '    LOGEMERG("SoloMine: developer fee unavailable");',
        '    abort();',
        '}',
        '',
    ]
    guard = '\n'.join(indent + line if line else '' for line in lines) + '\n'
    st_src = st_src[:m.start()] + guard + st_src[m.start():]

    # Reject startup when the developer address is invalid.
    invalid = re.compile(
        r'(?m)^([ \t]*)} else\n[ \t]*LOGNOTICE\("No valid donation address found"\);'
    )
    matches = list(invalid.finditer(st_src))
    if len(matches) != 1:
        raise RuntimeError(f"invalid developer address: expected one match, found {len(matches)}")
    m = matches[0]
    indent = m.group(1)
    replacement = (
        indent + '} else {\n' +
        indent + '\tLOGEMERG("SoloMine: developer fee address validation failed; refusing to mine without the fixed 2 percent fee");\n' +
        indent + '\texit(1);\n' +
        indent + '}'
    )
    st_src = st_src[:m.start()] + replacement + st_src[m.end():]

    # Only write if all source patterns were verified first.
    ck.write_text(ck_src)
    st.write_text(st_src)
    print("SoloMine patch applied. Full build and regtest still required.")

if __name__ == "__main__":
    main()

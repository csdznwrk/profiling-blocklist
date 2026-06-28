#!/usr/bin/env python3
"""
update.py — rebuilds docs/domains.txt from seeds.txt + community sources.
"""
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
SEEDS = ROOT / "seeds.txt"
DOCS  = ROOT / "docs"

# Plain-text sources focused on ad tech / tracking / behavioral profiling
PLAIN_SOURCES = [
    # Peter Lowe — well-maintained ad server list
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=plain&showintro=0&mimetype=plaintext",
    # AdGuard tracking servers list
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/SpywareFilter/sections/tracking_servers.txt",
    # NextDNS CNAME cloaking blocklist
    "https://raw.githubusercontent.com/nextdns/cname-cloaking-blocklist/master/domains",
]

# Keywords that indicate behavioral profiling / ad tech domains
PROFILING_KEYWORDS = [
    "adserv", "adtech", "adnxs", "doubleclick", "googlesyndication",
    "adsrvr", "rubiconproject", "pubmatic", "openx", "casalemedia",
    "mathtag", "krxd", "demdex", "omtrdc", "bluekai", "tapad",
    "liveramp", "rlcdn", "criteo", "taboola", "outbrain", "sharethis",
    "addthis", "quantserve", "moatads", "doubleverify", "adsafeprotected",
    "iasds", "triplelift", "sovrn", "lijit", "spotx", "conversant",
    "advertising.com", "adtech", "adform", "adroll", "bidswitch",
    "smartadserver", "contextweb", "yieldmanager", "undertone",
    "trafficjunky", "exelator", "acuityads", "lotame", "crwdcntrl",
    "bombora", "demandbase", "zeotap", "id5-sync", "uidapi",
    "neustar", "acxiom", "experian", "exacttarget", "pardot",
    "pixel.facebook", "connect.facebook", "ads-api.tiktok",
    "static.ads-twitter", "snap.licdn", "pixel.rlcdn",
]


def load_seeds():
    domains = set()
    for line in SEEDS.read_text().splitlines():
        line = line.split("#")[0].strip().lower()
        if line and "." in line and not line.startswith("."):
            domains.add(line)
    return domains


def fetch_url(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "profiling-blocklist/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode(errors="replace")
    except Exception as e:
        print(f"  ! fetch failed: {e}")
        return ""


def parse_plain(text):
    domains = set()
    for line in text.splitlines():
        line = line.split("#")[0].strip().lower()
        if line.startswith("!") or line.startswith("["):
            continue
        parts = line.split()
        domain = parts[-1] if parts else ""
        if domain and "." in domain and not domain.startswith("."):
            if any(kw in domain for kw in PROFILING_KEYWORDS):
                domains.add(domain)
    return domains


def main():
    DOCS.mkdir(exist_ok=True)
    print("Loading seeds...")
    domains = load_seeds()
    print(f"  {len(domains)} seed domains")

    for url in PLAIN_SOURCES:
        print(f"Fetching {url[:70]}...")
        text = fetch_url(url)
        found = parse_plain(text)
        print(f"  +{len(found)} profiling domains")
        domains |= found
        time.sleep(1)

    domains = sorted(d for d in domains if d and "." in d)

    (DOCS / "domains.txt").write_text(
        "# Behavioral Profiling & Identity Graph Blocklist\n"
        f"# Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
        f"# Domains: {len(domains)}\n\n" +
        "\n".join(domains) + "\n"
    )

    (DOCS / "metadata.json").write_text(json.dumps({
        "updated": datetime.now(timezone.utc).isoformat(),
        "domain_count": len(domains),
    }, indent=2))

    (DOCS / "index.html").write_text(f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Behavioral Profiling Blocklist</title>
<style>body{{font-family:system-ui;max-width:640px;margin:40px auto;padding:0 20px;color:#222}}</style>
</head>
<body>
<h1>Behavioral Profiling Blocklist</h1>
<p>Blocks ad exchanges, data brokers, identity graphs, social tracking pixels, DSPs, and cross-app behavioral profiling infrastructure.</p>
<p><strong>{len(domains)}</strong> domains &mdash; updated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
<h2>Import to NextDNS</h2>
<pre>nextdnsctl denylist import YOUR_PROFILE_ID https://csdznwrk.github.io/profiling-blocklist/domains.txt</pre>
<p><a href="domains.txt">domains.txt</a></p>
</body>
</html>""")

    print(f"\nDone: {len(domains)} total domains")


if __name__ == "__main__":
    main()

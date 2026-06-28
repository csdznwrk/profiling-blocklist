# Behavioral Profiling Blocklist

Blocks the infrastructure used to build behavioral profiles and infer life patterns — ad exchanges, identity graphs, data brokers, social tracking pixels, DSPs, retargeting networks, and cross-app identity stitching.

## What's covered

| Category | Examples |
|---|---|
| Social tracking pixels | Meta, TikTok, Snap, Twitter/X, LinkedIn, Pinterest |
| Ad exchanges / SSPs | DoubleClick, AppNexus/Xandr, Rubicon, PubMatic, OpenX, Index Exchange |
| DSPs | The Trade Desk, Criteo, MediaMath, Amazon Ads |
| Identity graphs | LiveRamp, Tapad, ID5, Neustar |
| Data brokers | Acxiom, Oracle BlueKai, Experian, Lotame |
| Audience measurement | Nielsen, Comscore, Quantcast, MOAT, DoubleVerify, IAS |
| Content recommendation | Taboola, Outbrain |
| Location harvesters | SafeGraph, Veraset, Foursquare, Cuebiq |
| CNAME cloaking trackers | Eulerian, Webtrekk, TagCommander, Wizaly |
| Adobe Experience Cloud | Omniture, Demdex, Everesttech |

## Import to NextDNS

```bash
/Users/carson/Library/Python/3.9/bin/nextdnsctl denylist import 2a7d5a https://csdznwrk.github.io/profiling-blocklist/domains.txt
```

## Schedule

GitHub Actions rebuilds every 6 hours from community sources.

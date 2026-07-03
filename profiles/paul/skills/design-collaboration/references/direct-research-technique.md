# Direct Research Technique

Quick factual lookups without delegation. Use Wikipedia/Wiktionary APIs directly.

## Wikipedia API

```bash
# Search for articles
curl -sL "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=TERM&format=json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(r['title'],'-',r['snippet'][:300]) for r in d['query']['search'][:5]]"

# Get article extract
curl -sL "https://en.wikipedia.org/w/api.php?action=query&titles=PAGE_TITLE&prop=extracts&explaintext=1&format=json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); pages=d['query']['pages']; [print(v.get('extract','')[:2000]) for v in pages.values()]"
```

## Wiktionary API

```bash
# Get word etymology and definition
curl -sL "https://en.wiktionary.org/w/api.php?action=query&titles=WORD&prop=extracts&explaintext=1&format=json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); pages=d['query']['pages']; [print(v.get('extract','')[:1500]) for v in pages.values()]"
```

## When to use this vs delegate_task

- **Use direct curl**: single-fact lookups, terminology research, word origins, date checks, simple "what is X" questions. 2-3 queries max. Takes 10-30 seconds.
- **Use delegate_task**: multi-step research synthesis (compare 5+ sources, analyze trends, cross-reference multiple domains). Takes 2-5 minutes.

## Example: Sicilian mob terminology

Two queries resolved pizzo/bustarella/sapuri in under 30 seconds:

1. Wikipedia API for "Pizzo (mafia)" — got the full extract including "fari vagnari u pizzu" (wet the beak)
2. Wiktionary API for "bustarella" — got etymology (busta = envelope + -ella = diminutive) and definition

No subagent needed. The user called out the 300-second delegation as excessive — rightfully so.

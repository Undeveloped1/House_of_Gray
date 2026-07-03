#!/usr/bin/env python3
"""Rook's X/Twitter scraper via Firecrawl. Reads FIRECRAWL_API_KEY from env."""
import sys, json, os, time
from firecrawl import FirecrawlApp

def scrape_handle(app, handle):
    handle = handle.strip().lstrip("@")
    url = f"https://x.com/{handle}"
    try:
        result = app.scrape(url, formats=["markdown"])
        content = result.markdown if hasattr(result, 'markdown') else str(result)
        return {"handle": handle, "status": "ok", "data": content[:2000]}
    except Exception as e:
        return {"handle": handle, "status": "error", "error": str(e)}

def main():
    api_key = os.environ.get("FIRECRAWL_API_KEY", "")
    if not api_key:
        print(json.dumps({"error": "FIRECRAWL_API_KEY not set"}))
        sys.exit(1)
    
    app = FirecrawlApp(api_key=api_key)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--file":
        with open(sys.argv[2]) as f:
            handles = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    elif len(sys.argv) > 1:
        handles = sys.argv[1:]
    else:
        handles = [line.strip() for line in sys.stdin if line.strip()]
    
    results = []
    for h in handles:
        results.append(scrape_handle(app, h))
        if len(results) < len(handles):
            time.sleep(0.5)
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

# Headless Browser Auth on VPS via Playwright Remote Debugging

Use case: authenticate a web service (X/Twitter, Google, etc.) on a headless VPS without installing a desktop environment. The browser runs on the VPS; you interact with it from your local Chrome via SSH tunnel.

## Prerequisites

```bash
pip3 install playwright
playwright install chromium
```

## One-Time Setup

### 1. Create persistent profile directory
```bash
mkdir -p /root/.x-profile  # or any persistent path
```

### 2. Launch Chromium with remote debugging

The launch command must go through a wrapper script because Hermes terminal tool rejects inline `&` backgrounding and has issues with long argument lists:

```bash
# /root/.x-profile/start_chrome.sh
#!/bin/bash
exec /root/.cache/ms-playwright/chromium-*/chrome-linux64/chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/root/.x-profile \
  --no-first-run \
  --no-default-browser-check \
  --no-sandbox \
  --disable-gpu \
  --headless=new \
  "https://x.com" 2>/root/.x-profile/chrome.log
```

**Critical flags:**
- `--no-sandbox` — required when running as root
- `--disable-gpu` — avoids GPU driver errors on headless VPS
- `--headless=new` — the new headless mode (not the legacy `--headless`)
- `--user-data-dir` — persistent profile where cookies/auth state is saved

Launch with `terminal(background=true)` since it's a long-lived process.

### 3. Verify port is listening
```bash
ss -tlnp | grep 9222
# Should show: 127.0.0.1:9222 ... chrome
```

### 4. SSH tunnel from local machine
```bash
ssh -L 9222:localhost:9222 paul
```

### 5. Authenticate via local browser

**Option A — Chrome/Chromium (`chrome://inspect`):**
1. Open Chrome on local machine
2. Go to `chrome://inspect`
3. Click "Configure..." → add `localhost:9222`
4. Remote targets appear — click "inspect" on the X.com tab
5. Log into X.com through the remote browser window

**Option B — Brave, Firefox, Edge, or any browser (direct):**
1. Go directly to `http://localhost:9222` in the address bar
2. You'll see a page listing all remote tabs
3. Click the X.com tab to open DevTools and interact with it
4. Log into X.com through that window

Auth state is saved in `/root/.x-profile/` either way.

### 6. Verify auth persisted
After closing the remote debugging session, relaunch Chromium with the same `--user-data-dir` and it will still be logged in.

## Using the Authenticated Profile with Playwright

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="/root/.x-profile",
        headless=True,
        args=["--no-sandbox", "--disable-gpu"]
    )
    page = browser.new_page()
    page.goto("https://x.com/zaimiri/status/2062512177295090046")
    # page is authenticated — access content
    content = page.content()
    browser.close()
```

## Discovery

**Find Playwright's Chromium path on this VPS:**
```bash
find /root/.cache/ms-playwright -name "chrome" -path "*/chrome-linux64/*" 2>/dev/null
```
Current as of 2026-06-04: `/root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome`

## Pitfalls

- **Brave browser does NOT have the `chrome://inspect` \"Configure...\" button.** Joe uses Brave — the `chrome://inspect` page opens but has no configuration UI. Use Option B instead: go directly to `http://localhost:9222` in the address bar.
- **Snap Chromium** (`/snap/bin/chromium`) has sandbox and library issues. Use Playwright's bundled Chromium at `/root/.cache/ms-playwright/chromium-*/chrome-linux64/chrome`.
- **Forgotten `--headless=new` causes instant silent crash.** Chromium logs "Missing X server or $DISPLAY" and exits code 1. If you launch and the port isn't listening 3 seconds later, check the log file for this exact error — it means you forgot the headless flag.
- **`--headless=new`** is required — legacy `--headless` mode is deprecated and may not support remote debugging correctly.
- **Port must bind to 127.0.0.1** — never expose the debugging port publicly. It grants full browser control.
- **Chromium exits silently** if it can't open a display — `--headless=new` is what prevents this.
- **The `chrome://inspect` approach** works better than hitting `http://localhost:9222` directly because it handles CORS and DevTools protocol correctly.
- **Don't background with `&` in terminal tool** — Hermes blocks it. Use `terminal(background=true)` or a wrapper script.

## Why Not Alternatives

- **xurl/X API:** requires paid developer account ($100+/month for meaningful access). Free tier is 100 tweets/month.
- **Cookie export from local browser:** works but cookies expire. Remote debugging + persistent profile survives indefinitely.
- **X11 forwarding a full browser:** heavyweight, requires X server on local machine, more moving parts.

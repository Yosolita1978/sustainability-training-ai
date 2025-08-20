Clean start

# For a local start fresh:

```bash
rm -rf .venv outputs/
uv venv
source .venv/bin/activate
uv sync
panel serve panel_app.py --show --port=5007
```


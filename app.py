import os
import asyncio
import threading
import importlib
from flask import Flask, render_template
from shared_client import start_client

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/health")
def health():
    return "OK", 200

# -------- Plugin System (from main.py) --------
async def load_and_run_plugins():
    print("Starting shared client...")
    await start_client()

    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        print("Plugin directory not found.")
        return

    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()
        except Exception as e:
            print(f"Error loading plugin '{plugin}': {e}")

    while True:
        await asyncio.sleep(1)

def run_plugins_async():
    asyncio.run(load_and_run_plugins())

# -------- Start Flask + Bot Together --------
if __name__ == "__main__":
    # Start plugin system in a background thread
    plugin_thread = threading.Thread(target=run_plugins_async, daemon=True)
    plugin_thread.start()

    # Start Flask web server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

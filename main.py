import os
import asyncio
import threading
from flask import Flask, render_template
from shared_client import start_client
import importlib

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/health")
def health():
    return "OK", 200

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

    while True:
        await asyncio.sleep(1)

def run_plugins_async():
    asyncio.run(load_and_run_plugins())

if __name__ == "__main__":
    # Start the plugin system in the background
    plugin_thread = threading.Thread(target=run_plugins_async, daemon=True)
    plugin_thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

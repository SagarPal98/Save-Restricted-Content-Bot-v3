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

async def load_and_run_plugins():
    print("Starting shared client...", flush=True)
    await start_client()

    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        print("Plugin directory not found.", flush=True)
        return

    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"Running {plugin} plugin...", flush=True)
                await getattr(module, f"run_{plugin}_plugin")()
        except Exception as e:
            print(f"Error loading plugin '{plugin}': {e}", flush=True)

    while True:
        await asyncio.sleep(1)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    try:
        asyncio.run(load_and_run_plugins())
    except Exception as e:
        print(f"Bot crashed: {e}", flush=True)

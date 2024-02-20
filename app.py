import importlib.util
import subprocess
from flask import Flask, render_template
from threading import Thread

# Check if Flask is installed, if not, install it
try:
    importlib.util.find_spec('flask')
    from flask import Flask, render_template
except ImportError:
    subprocess.check_call(['pip', 'install', 'flask'])
    importlib.invalidate_caches()
    from flask import Flask, render_template

# Check if Gunicorn is installed, if not, install it
try:
    importlib.util.find_spec('gunicorn')
    import gunicorn.app.base
except ImportError:
    subprocess.check_call(['pip', 'install', 'gunicorn'])
    importlib.invalidate_caches()
    import gunicorn.app.base

app = Flask(__name__)

@app.route('/')
def site():
    return render_template('index.html')

def run():
    app.run('127.0.0.1', port=8808)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    # Use Gunicorn to serve the Flask app
    #  -w 4: Use 4 worker processes (you can adjust this based on your needs)
    #  -b 127.0.0.1:8808: Bind to localhost on port 8808
    #  --access-logfile - --error-logfile -: Log to stdout/stderr
    subprocess.Popen(["gunicorn", "local-storage:app", "-w", "4", "-b", "127.0.0.1:8808", "--access-logfile", "-", "--error-logfile", "-"])

    # Start the Flask app in a separate thread
    keep_alive()

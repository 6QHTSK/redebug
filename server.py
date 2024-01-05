import json
import os
import shutil
import subprocess
import time
from flask import Flask, request

app = Flask(__name__)
process_running = False


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/process')
def process():
    global process_running

    if not process_running:
        process_running = True

        try:
            git_url = request.args.get('git_url', '')
            branch = request.args.get('branch', '')

            if git_url and branch:
                git_name = os.path.basename(git_url.rstrip('/'))
                subprocess.call('git clone --branch %s --depth=1 %s' % (branch, git_url), shell=True)
                start_time = time.time()
                code = subprocess.call('python2 redebug.py %s' % git_name, shell=True)
                end_time = time.time()
                shutil.rmtree(git_name)
                if code != 0:
                    return json.dumps({'Error': 'Detect Failed'}), 500

                log_file = 'vul.json'
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        vul_json = json.load(f, encoding="utf-8")
                    response = json.dumps({"time": end_time - start_time, "vul": vul_json}, encoding="utf-8")
                else:
                    response = json.dumps({'Error': 'Log file not found.'}), 500
                os.remove(log_file)

                process_running = False
                return response
            else:
                process_running = False
                return json.dumps({'Error': 'Missing git_url or branch parameter.'}), 400

        except Exception as e:
            process_running = False
            return json.dumps({'Error': str(e)}), 500

    else:
        return json.dumps({'Error': 'Another process is already running.'}), 429


if __name__ == '__main__':
    app.run(port=8000)

from flask import Flask, render_template, request, jsonify
import os, json, hashlib

app = Flask(__name__)

# -------- VCS Functions -------- #

def init_repo():
    if not os.path.exists(".myvcs"):
        os.mkdir(".myvcs")
        os.mkdir(".myvcs/commits")
        with open(".myvcs/index.json", "w") as f:
            json.dump({}, f)
        return "Repository initialized"
    return "Already initialized"

def add_file(filename):
    if not os.path.exists(filename):
        return "File not found"

    with open(filename, "r") as f:
        content = f.read()

    file_hash = hashlib.sha1(content.encode()).hexdigest()

    with open(".myvcs/index.json", "r") as f:
        index = json.load(f)

    index[filename] = file_hash

    with open(".myvcs/index.json", "w") as f:
        json.dump(index, f)

    return f"{filename} added"

def commit_changes(message):
    with open(".myvcs/index.json", "r") as f:
        index = json.load(f)

    commit_id = hashlib.sha1(message.encode()).hexdigest()

    with open(f".myvcs/commits/{commit_id}.json", "w") as f:
        json.dump({"message": message, "files": index}, f)

    return f"Commit saved: {commit_id}"

def get_logs():
    logs = []
    if not os.path.exists(".myvcs/commits"):
        return logs

    for file in os.listdir(".myvcs/commits"):
        with open(f".myvcs/commits/{file}") as f:
            logs.append(json.load(f))
    return logs

# -------- Routes -------- #

@app.route('/')
def home():
    return render_template('vcs.html')

@app.route('/init', methods=['POST'])
def init():
    return jsonify({"msg": init_repo()})

@app.route('/add', methods=['POST'])
def add():
    filename = request.json.get("filename")
    return jsonify({"msg": add_file(filename)})

@app.route('/commit', methods=['POST'])
def commit():
    message = request.json.get("message")
    return jsonify({"msg": commit_changes(message)})

@app.route('/log')
def log():
    return jsonify(get_logs())


if __name__ == '__main__':
# app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)    
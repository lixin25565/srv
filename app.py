from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

MSG_FILE = 'msgs.json'

def load_messages_from_file(filename=MSG_FILE):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_messages_to_file(messages, filename=MSG_FILE):
    with open(filename, 'w') as file:
        json.dump(messages, file)

messages = load_messages_from_file()

@app.route('/')
def manage_messages():
    return render_template('index.html', messages=messages)

@app.route('/api', methods=['GET', 'DELETE'])
def api_messages():
    global messages

    if request.method == 'GET':
        msg = request.args.get('msg', '')
        if msg:
            messages.append(msg)
            save_messages_to_file(messages)
            return redirect(url_for('manage_messages'))
        return jsonify(messages=messages)
    elif request.method == 'DELETE':
        msg_to_delete = request.args.get('msg', '')
        if msg_to_delete in messages:
            messages.remove(msg_to_delete)
            save_messages_to_file(messages)
            return jsonify({"status": "success", "message": f"Deleted message: {msg_to_delete}"})
        else:
            return jsonify({"status": "error", "message": "Message not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
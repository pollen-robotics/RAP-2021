import os
import json

from flask import Flask, request, redirect, url_for, render_template, Response

import tools

app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)


@app.route('/update-wifi', methods=['POST'])
def update_wifi():
    tools.setup_new_wifi(request.form['ssid'], request.form['password'])
    return redirect(url_for('wifi'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wifi')
def wifi():
    return render_template(
        'wifi.html',
    )


@app.route('/halt')
def halt():
    tools.halt(delay=5)
    return render_template('halt.html')


@app.route('/api/reachy-status')
def update_status():
    return Response(
        response=json.dumps(tools.get_reachy_status()),
        mimetype='application/json',
    )

@app.route('/api/ip')
def update_ip():
    return Response(
        response=json.dumps(tools.get_ip()),
        mimetype='application/json',
    )

@app.route('/api/wlan_status')
def update_wlan_status():
    return Response(
        response=json.dumps(tools.get_wlan_status()),
        mimetype='application/json',
    )


@app.route('/api/hotspot', methods=['POST'])
def toggle_hotspot():
    tools.set_hotspot_state(state=request.data.decode())
    return Response(status=200)


@app.route('/api/available_networks')
def update_available_networks():
    return Response(
        response=json.dumps(tools.get_available_wifis()),
        mimetype='application/json',
    )

@app.route('/api/connection_card_info')
def update_connection_card_info():
    return Response(
        response=json.dumps(tools.get_connection_card_info()),
        mimetype='application/json',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3972, debug=True)

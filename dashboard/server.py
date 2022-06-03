"""Flask server for RAP-2021."""
from crypt import methods
import os
import json

from flask import Flask, request, redirect, url_for, render_template, Response

import tools.network_tools as network_tools
import tools.debug_tools as debug_tools
import tools.service_tools as service_tools
import tools.dashboard_tools as dashboard_tools

import time

app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)


# Render templates
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wifi')
def wifi():
    global wifi_list
    if not net_tools.get_connection_status()['mode'] == 'Hotspot':
        wifi_list = net_tools.get_available_wifis()
    return render_template(
        'wifi.html',
        wifi_list=wifi_list,
    )


@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/dashboard')
def dashboard():
    global reachy_dashboard
    reachy_dashboard = dashboard_tools.ReachyDashboard()
    if not reachy_dashboard.connection_succeed:
        print('Could not connect to Reachy')
    else:
        print('Connected to Reachy.')
    return render_template('dashboard.html')


# Wifi API
@app.route('/update-wifi', methods=['POST'])
def update_wifi():
    if net_tools.get_connection_status()['mode'] == 'Hotspot':
        net_tools.set_hotspot_state('off')

    net_tools.setup_new_wifi(request.form['ssid'], request.form['password'])
    return redirect(url_for('wifi'))


@app.route('/api/ip')
def update_ip():
    ip = net_tools.get_ip()
    net_tools.display_ip(ip)
    return Response(
        response=json.dumps(ip),
        mimetype='application/json',
    )


@app.route('/api/connection_status')
def update_connection_status():
    return Response(
        response=json.dumps(net_tools.get_connection_status()),
        mimetype='application/json',
    )


@app.route('/api/hotspot', methods=['POST'])
def toggle_hotspot():
    net_tools.set_hotspot_state(state=request.data.decode())
    if request.data.decode() == 'off' and net_tools.get_connection_status()['mode'] == 'None':
        net_tools.set_hotspot_state('on')
    return Response(status=200)


@app.route('/api/available_networks')
def update_available_networks():
    if net_tools.get_connection_status()['mode'] == 'Hotspot':
        global wifi_list
        available_networks = wifi_list
    else:
        available_networks = net_tools.get_available_wifis()
    return Response(
        response=json.dumps(available_networks),
        mimetype='application/json',
    )


@app.route('/api/connection_card_info')
def update_connection_card_info():
    return Response(
        response=json.dumps(net_tools.get_connection_card_info()),
        mimetype='application/json',
    )


# Index API
@app.route('/api/missing_modules_names')
def get_missing_modules_names():
    return Response(
        response=json.dumps(debug_tools.get_missing_modules_names()),
        mimetype='application/json',
    )


@app.route('/api/missing_modules_bool')
def get_missing_modules_bool():
    return Response(
        response=json.dumps(debug_tools.are_missing_modules()),
        mimetype='application/json',
    )


# Service API
@app.route('/api/list_services')
def list_services():
    return Response(
        response=json.dumps(service_tools.list_services()),
        mimetype='application/json',
    )


@app.route('/api/restart_service', methods=['POST'])
def restart_service():
    service_tools.restart_service(request.data.decode())
    return Response(status=200)


@app.route('/api/stop_service', methods=['POST'])
def stop_service():
    service_tools.stop_service(request.data.decode())
    return Response(status=200)


@app.route('/api/is_service_running', methods=['POST'])
def is_service_running():
    return Response(
        response=json.dumps(service_tools.is_service_running(request.data.decode())),
        mimetype='application/json',
    )


@app.route('/api/status_service', methods=['POST'])
def status_service():
    return service_tools.get_service_status(request.data.decode())


# Dashboard API
@app.route('/api/change-compliance', methods=['GET'])
def change_compliance():
    part_req = request.args.get('part')

    compliance_req = request.args.get('compliance')
    if compliance_req == 'false':
        compliance_req = False
    else:
        compliance_req = True

    reachy_dashboard.change_compliancy(
        part=part_req,
        compliance=compliance_req
        )
    return Response(status=200)


@app.route('/api/get-compliance-config')
def get_compliance_config():
    config = list(reachy_dashboard._compliance_config.keys())
    return Response(
        response=json.dumps(config),
        mimetype='application/json',
    )


@app.route('/api/get-fans-info')
def get_fans_info():
    return Response(
        response=json.dumps(reachy_dashboard.get_fans_info()),
        mimetype='application/json',
    )


@app.route('/api/set-fans-state', methods=['GET'])
def set_fans_state():
    fan_req = request.args.get('fan')
    state_req = request.args.get('state')

    reachy_dashboard.set_fan_state(fan=fan_req, state=state_req)
    return Response(status=200)


if __name__ == '__main__':

    # time.sleep(10.0)

    net_tools = network_tools.NetworkTools()

    connection_status = net_tools.get_connection_status()['mode']

    if not (connection_status == 'Wifi' or connection_status == 'Ethernet'):
        net_tools.set_hotspot_state('off')
        wifi_list = net_tools.get_available_wifis()
        net_tools.set_hotspot_state('on')

    else:
        wifi_list = net_tools.get_available_wifis()

    net_tools.display_ip(net_tools.get_ip())
    app.run(host='0.0.0.0', port=3972, debug=True)

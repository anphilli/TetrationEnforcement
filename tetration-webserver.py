#!/usr/bin/env python

from flask import Flask, jsonify, render_template, Response, request
import json
import pexpect
import os

app = Flask(__name__)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = False


WebServerIP = "10.8.29.10"
DBServerIP = "10.8.253.110"
NFSServerIP = "10.8.253.111"


def Disp_IPTables(host_ip):


    username = "administrator"
    host_password = "Cisco12345"

    '''
    Get display IP Tables from host chosen hosts

    '''
    ssh_cmd = "ssh -l {0} {1}".format(username, host_ip)

    print("\nSSH'ing to host {0}".format(host_ip))
    try:
        s = pexpect.spawn(ssh_cmd)
        s.expect('.*password: ')
        s.sendline(host_password)
        s.expect('.*~\\$ ')  
        s.sendline('sudo iptables -L -n ')
        s.expect('.*password for administrator: ')
        s.sendline(host_password)
        s.expect('.*~\\$ ')  
        iptables_output = s.after
        print('you are here')
        #s.expect('.*~\\$ ')
        s.close()

        #print(portstate)
    except pexpect.TIMEOUT as err:
        print("pexpect timed out! See error message below\n")
        print(err)

    return iptables_output


def dispIpTables(host_ip):


    username = "administrator"
    host_password = "Cisco12345"

    '''
    Get display IP Tables from host chosen hosts

    '''
    ssh_cmd = "ssh -l {0} {1}".format(username, host_ip)

    print("\nSSH'ing to host {0}".format(host_ip))
    try:
        s = pexpect.spawn(ssh_cmd)
        s.expect('.*password: ')
        s.sendline(host_password)
        s.expect('.*~\\$ ')  
        s.sendline('sudo iptables -L -n | grep 0.0.0.0')
        s.expect('.*password for administrator: ')
        s.sendline(host_password)
        s.expect('.*~\\$ ')  
        iptables_output = s.after
        print('you are here')
        #s.expect('.*~\\$ ')
        s.close()

        #print(portstate)
    except pexpect.TIMEOUT as err:
        print("pexpect timed out! See error message below\n")
        print(err)

    return iptables_output


@app.route('/')
def main_page():
    return render_template("index.html")

    ''' Render the index.html landing page for the application '''

# @app.route('/resetpolicy', methods=['POST'])
# def resetPolicy():
#     ''' Reset Policy Config on each host'''


@app.route('/getiptables', methods=['POST'])
def getiptables():

    ''' Display iptables policy from hosts'''

    # Create a temp file to use as a flag to stop multiple 
    # ssh session from trigger happy users

    payload = request.form

    host_ip = payload['Host']
    print(host_ip)

    if host_ip == "WebServer":
        response = Disp_IPTables(WebServerIP)
    elif host_ip == "NFSServer":
        response = Disp_IPTables(NFSServerIP)
    if host_ip == "DBServer":
        response = Disp_IPTables(DBServerIP)

    else:
        print("Invalid host: {0}, not connection possible".format(host_ip))

    print(response)
    policy = {'policyData' : response }


    print (policy)
    resp = json.dumps(policy)
    return Response(resp, status=200, mimetype='application/json')



app.run(host='127.0.0.1', port=8088)


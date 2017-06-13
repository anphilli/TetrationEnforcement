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


def Disp_IPTables(host_ip, command):


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
        s.sendline(command)
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
    port_num = payload['ports']
    #str(host_ip)
    #str(port_num)
    print(host_ip)
    print(port_num)


    #Show Application Specific IPTables Rules
    if host_ip == "WebServer" and port_num == "8082":
        command = "sudo iptables -L -n -v | grep 172.* | grep {0}".format(port_num)
        response = Disp_IPTables(WebServerIP, command )

    elif host_ip == "DBServer" and port_num == "3306":
        command = "sudo iptables -L -n -v | grep {0}".format(port_num)
        response = Disp_IPTables(DBServerIP, command)

    elif host_ip == "NFSServer" and port_num == "2049":
        command = "sudo iptables -L -n -v | grep {0}".format(port_num)
        response = Disp_IPTables(NFSServerIP, command)

    #Show clean IPtables Rules
    # elif host_ip == "WebServer" & port_num == "8082":
    #     command = "iptables -L -n -v | grep dpt{0}".format(port_num)
    #     response = Disp_IPTables(WebServerIP, command )
    # elif host_ip == "NFSServer" & port_num == "2049":
    #     response = Disp_IPTables(NFSServerIP)
    #     command = "iptables -L -n -v | grep dpt{0}".format(port_num)
    # elif host_ip == "DBServer" & port_num == "3306":
    #     command = "iptables -L -n -v | grep dpt{0}".format(port_num)
    #     response = Disp_IPTables(DBServerIP)
    else:
        print("Invalid host: {0}, and/or port number {1}, no connection possible".format(host_ip, port_num))

    print(response)
    policy = {'policyData' : response }


    print (policy)
    resp = json.dumps(policy)
    return Response(resp, status=200, mimetype='application/json')



app.run(host='127.0.0.1', port=8088)


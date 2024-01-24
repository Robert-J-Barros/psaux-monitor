import os
import paramiko
import re
import json
import dotenv
import urllib.request
from flask import Flask, jsonify

app = Flask(__name__.split('.')[0])

def OpenSSHConnection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = os.getenv('SSH_HOST')
    username = os.getenv('SSH_USERNAME')
    key_path = os.getenv('SSH_KEY_PATH')
    ssh.connect(host, username=username, key_filename=key_path)
    return ssh

def CloseSSHConnection(ssh):
    ssh.close()

def ExecuteSSHCommand(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

def ListNumOfProcess(ssh):
    try:
        comando_ps = "ps -aux | grep '/home/ubuntu/recharge' | grep -v grep | wc -l"
        saida_grep =ExecuteSSHCommand(ssh, comando_ps)
        return saida_grep.strip()
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        return '0'

def ListNumbOfPID(ssh):
    try:
        comando_grep = "ps -aux | grep '[b]ash /home/ubuntu/recharge' | awk '{print $2}'"
        saida_awk = ExecuteSSHCommand(ssh, comando_grep)
        return saida_awk.strip()
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        return '0'

def ListNameOfProcess(ssh):
    try:
        comando_grep_name = "ps -aux | grep '[b]ash /home/ubuntu/recharge' | awk '{print $12}'"
        saida_grep_name = ExecuteSSHCommand(ssh, comando_grep_name)
        return saida_grep_name.strip()
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        return '0'

def CreateJSON(ssh):
    processos = ListNameOfProcess(ssh)
    num_processos = ListNumOfProcess(ssh)
    pid_processos = ListNumbOfPID(ssh)
    data = {
        'processos': processos,
        'num_processos': num_processos,
        'pid_processos': pid_processos
    }
    return json.dumps(data, indent=True)
@app.route('/api/data', methods=['GET'])
def get_data():
    ssh = OpenSSHConnection()
    json_data = CreateJSON(ssh)
    CloseSSHConnection(ssh)
    return jsonify(json.loads(json_data))

@app.route('/', methods=['GET'])

def health_check():
    ssh = OpenSSHConnection()
    num_processos = ListNumOfProcess(ssh)
    CloseSSHConnection(ssh)
    if num_processos == '0':
        return jsonify({"status": "error", "message": "Nenhum processo em execução"}), 500
    else:
        return jsonify({"status": "ok", "message": "API está saudável"}), 200

if __name__ == '__main__':
    print("Before app.run()")
    app.run(port=7000, host='0.0.0.0', debug=True)
    print("After app.run()")

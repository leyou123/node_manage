from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)


def exec_cmd(ip):
    try:
        username = "root"
        password = "Leyou2020"
        port = 22
        cmds = "ls"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port, username=username, password=password, timeout=10)
        stdin, stdout, stderr = client.exec_command(cmds)
        results = stdout.readlines()

        if len(results) > 0:
            return True
        else:
            return False
    except Exception as e:
        # print(e)
        print("服务器无法连接")
        return False
    finally:
        client.close()


@app.route('/check_servers', methods=['POST'])
def testpost():
    if request.method == 'GET':
        return jsonify({'status': False})

    if request.method == 'POST':
        try:
            ip = request.json.get('ip')
            check_result = exec_cmd(ip)
        except Exception as e:
            return jsonify({'status': e})
        return jsonify({'status': check_result})


if __name__ == '__main__':
    """
        pip3 install flask
        nohup python3 /root/flask_servers.py > /root/flask_log.txt 2>&1 &
    """
    app.run(host='0.0.0.0', port=9000)
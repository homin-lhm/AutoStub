from flask import Flask, request
import time

app = Flask(__name__)  # 实例化应用


@app.route("/file", methods=["GET"])
def query():
    data = request.args
    file_lst = [
        "110", "111", "112", "113", "114", "1111"
    ]
    if data["file_id"] in file_lst:
        return {"msg": "success"}, 200
    else:
        return {"msg": "file not exits"}, 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8771, debug=True)

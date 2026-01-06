from flask import Flask, request, jsonify
from src.rules import rule_based_hr
from src.ml import ml_check_hr

app = Flask(__name__)

@app.route("/hr", methods=["POST"])
def receive_hr():
    data = request.get_json()
    hr = float(data["hr"])

    # 1️⃣ rule-based (an toàn trước)
    rule_status, rule_msg = rule_based_hr(hr)

    # 2️⃣ ML check
    ml_status = ml_check_hr(hr)

    return jsonify({
        "hr": hr,
        "rule_status": rule_status,
        "rule_message": rule_msg,
        "ml_status": ml_status
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

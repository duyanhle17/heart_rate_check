# from flask import Flask, request, jsonify, send_file, render_template
# from src.rules import rule_based_hr
# from src.ml import ml_check_hr
# from src.fall.fall_state import update_fall_state, fall_state


# import csv
# import time
# import os
# import pandas as pd

# import matplotlib
# matplotlib.use("Agg")   # bắt buộc cho server
# import matplotlib.pyplot as plt

# from collections import deque
# import time

# HR_WINDOW = 5                 # số HR gom lại
# DISPLAY_INTERVAL = 5          # giây

# display_hr_buffer = deque()
# last_display_time = 0
# display_hr_value = None

# # ======================
# # HR SMOOTHING CONFIG
# # ======================
# # HR_WINDOW_SIZE = 10        # ~5 giây (nếu gửi mỗi 0.5s)
# # DANGER_HOLD_TIME = 10      # giữ cảnh báo 10 giây

# # hr_buffer = deque(maxlen=HR_WINDOW_SIZE)
# # last_danger_time = 0



# # ======================
# # APP
# # ======================
# app = Flask(__name__)

# # ======================
# # PATH
# # ======================
# BASE_DIR = os.path.dirname(__file__)
# DATA_DIR = os.path.join(BASE_DIR, "data")

# HR_LOG_PATH = os.path.join(DATA_DIR, "hr_log.csv")
# HR_PLOT_PATH = os.path.join(DATA_DIR, "hr_plot.png")

# FALL_LOG_PATH = os.path.join(DATA_DIR, "fall_log.csv")

# os.makedirs(DATA_DIR, exist_ok=True)

# # ======================
# # GLOBAL STATE (REALTIME)
# # ======================
# latest_hr_state = {
#     "hr": None,
#     "rule_status": None,
#     "rule_message": None,
#     "ml_status": None,
#     "is_danger": False,
#     "timestamp": 0
# }

# latest_fall_state = {
#     "status": "WAITING",   # WAITING | SAFE | FALL | RECOVERED
#     "prob": 0.0,
#     "timestamp": 0
# }

# # ======================
# # WEB
# # ======================
# @app.route("/")
# def index():
#     return render_template("index.html")

# # ======================
# # LOGGING
# # ======================
# def log_hr(hr, rule_status, rule_message, ml_status):
#     file_exists = os.path.exists(HR_LOG_PATH)
#     with open(HR_LOG_PATH, "a", newline="") as f:
#         writer = csv.writer(f)

#         # ghi header nếu file mới
#         if not file_exists:
#             writer.writerow([
#                 "timestamp",
#                 "hr",
#                 "rule_status",
#                 "rule_message",
#                 "ml_status"
#             ])

#         writer.writerow([
#             time.time(),
#             hr,
#             rule_status,
#             rule_message,
#             ml_status
#         ])

# def log_fall(status, prob):
#     file_exists = os.path.exists(FALL_LOG_PATH)
#     with open(FALL_LOG_PATH, "a", newline="") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow([
#                 "timestamp",
#                 "status",
#                 "probability"
#             ])
#         writer.writerow([
#             time.time(),
#             status,
#             prob
#         ])

# # ======================
# # API: RECEIVE HR
# # ======================
# # @app.route("/hr", methods=["POST"])
# # def receive_hr():
# #     data = request.get_json(force=True)
# #     hr = float(data["hr"])
# #     global last_display_time, display_hr_value

# #     display_hr_buffer.append(hr)
# #     now = time.time()

# #     if now - last_display_time >= DISPLAY_INTERVAL:
# #         # lấy HR trung bình 5 giây
# #         display_hr_value = int(sum(display_hr_buffer) / len(display_hr_buffer))
# #         display_hr_buffer.clear()
# #         last_display_time = now


# #     # 1️⃣ Rule-based
# #     rule_status, rule_msg = rule_based_hr(hr)
# #     #check nguy hiểm
# #     is_danger = rule_status.startswith("DANGER")

# #     # 2️⃣ Thêm HR vào buffer
# #     hr_buffer.append(hr)

# #     # 3️⃣ ML check (CHỈ khi đủ window)
# #     ml_status = "WAITING"
# #     if len(hr_buffer) == HR_WINDOW:
# #         ml_status = ml_check_hr(list(hr_buffer))

# #     # 4️⃣ Log
# #     log_hr(hr, rule_status, rule_msg, ml_status)

# #     # 5️⃣ Update global state
# #     latest_hr_state.update({
# #         "hr": display_hr_value if display_hr_value else int(hr),
# #         "rule_status": rule_status,
# #         "rule_message": rule_msg,
# #         "ml_status": ml_status,
# #         "is_danger": is_danger,
# #         "timestamp": time.time()
# #     })

# #     return jsonify({
# #         "status": "OK",
# #         **latest_hr_state
# #     })

# @app.route("/hr", methods=["POST"])
# def receive_hr():
#     global last_display_time, display_hr_value

#     data = request.get_json(force=True)
#     try:
#         hr = float(data["hr"])
#     except:
#         return jsonify({"status": "ERROR", "message": "Invalid HR"}), 400

#     now = time.time()

#     # gom HR
#     display_hr_buffer.append(hr)

#     # mỗi 5 giây → cập nhật HR hiển thị
#     if now - last_display_time >= DISPLAY_INTERVAL and len(display_hr_buffer) > 0:
#         display_hr_value = int(sum(display_hr_buffer) / len(display_hr_buffer))
#         display_hr_buffer.clear()
#         last_display_time = now

#     hr_show = display_hr_value if display_hr_value else int(hr)

#     # rule-based ONLY (an toàn)
#     rule_status, rule_msg = rule_based_hr(hr_show)
#     is_danger = rule_status.startswith("DANGER")

#     latest_hr_state.update({
#         "hr": hr_show,
#         "rule_status": rule_status,
#         "rule_message": rule_msg,
#         "ml_status": "OFF",   # TẠM TẮT ML
#         "is_danger": is_danger,
#         "timestamp": now
#     })

#     log_hr(hr_show, rule_status, rule_msg, "OFF")

#     return jsonify({
#         "status": "OK",
#         **latest_hr_state
#     })


# # ======================
# # API: RECEIVE FALL DATA
# # ======================
# # @app.route("/fall", methods=["POST"])
# # def receive_fall():
# #     data = request.get_json(force=True)
# #     samples = data.get("samples", [])

# #     for s in samples:
# #         if len(s) == 6:
# #             update_fall_state(s)

# #     return jsonify({"status": "OK"})

# @app.route("/fall", methods=["POST"])
# def receive_fall():
#     data = request.get_json(force=True)
#     samples = data.get("samples", [])

#     result = {"status": "WAITING", "prob": 0.0}

#     for s in samples:
#         if len(s) == 6:
#             result = update_fall_state(s)

#     latest_fall_state.update({
#         "status": result.get("status", "WAITING"),
#         "prob": result.get("prob", 0.0),
#         "timestamp": time.time()
#     })

#     log_fall(latest_fall_state["status"], latest_fall_state["prob"])

#     return jsonify({
#         "status": "OK",
#         **latest_fall_state
#     })

# # ======================
# # API: LATEST STATUS (FRONTEND DÙNG)
# # ======================
# # @app.route("/latest_status", methods=["GET"])
# @app.route("/latest_status", methods=["GET"])
# def latest_status():
#     fall_status = fall_state.get("status", "WAITING")
#     fall_prob = fall_state.get("prob", 0.0)

#     alert = (
#         latest_hr_state["is_danger"] or
#         fall_status == "FALL"
#     )

#     return jsonify({
#         "hr": latest_hr_state["hr"],
#         "hr_danger": latest_hr_state["is_danger"],
#         "hr_message": latest_hr_state["rule_message"],

#         "fall_status": fall_status,
#         "fall_prob": fall_prob,

#         "alert": alert
#     })

# # ======================
# # API: HR PLOT
# # ======================
# @app.route("/plot", methods=["GET"])
# def plot_hr():
#     if not os.path.exists(HR_LOG_PATH):
#         return "No data yet", 400

#     df = pd.read_csv(HR_LOG_PATH)
#     if df.empty or "timestamp" not in df.columns:
#         return "No valid data yet", 400
#     #time relatives
#     t0 = df["timestamp"].iloc[0]
#     df["t"] = df["timestamp"] - t0

#     normal = df[df["ml_status"] == "NORMAL"]
#     abnormal = df[df["ml_status"] == "ABNORMAL"]

#     # plt.figure(figsize=(10, 4))
#     plt.figure(figsize=(8, 3), dpi=100)
    
#     if not normal.empty:
#         plt.plot(normal["t"], normal["hr"], label="Normal", color="blue")

#     if not abnormal.empty:
#         plt.scatter(
#             abnormal["t"],
#             abnormal["hr"],
#             color="red",
#             label="Abnormal",
#             zorder=3
#         )

#     plt.xlabel("Time (s)")
#     plt.ylabel("Heart Rate (bpm)")
#     plt.title("Heart Rate Monitoring")
#     plt.legend()
#     plt.grid(True)

#     plt.savefig(HR_PLOT_PATH)
#     plt.close()

#     return send_file(HR_PLOT_PATH, mimetype="image/png")

# # ======================
# # RUN
# # ======================
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)



from flask import Flask, request, jsonify, send_file, render_template
from src.rules import rule_based_hr
from src.fall.fall_state import update_fall_state, fall_state

import csv
import time
import os
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from collections import deque

# ======================
# CONFIG
# ======================
DISPLAY_INTERVAL = 5  # giây (hiển thị HR mỗi 5s)

display_hr_buffer = deque()
last_display_time = 0
display_hr_value = None

# ======================
# APP
# ======================
app = Flask(__name__)

# ======================
# PATH
# ======================
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

HR_LOG_PATH = os.path.join(DATA_DIR, "hr_log.csv")
HR_PLOT_PATH = os.path.join(DATA_DIR, "hr_plot.png")
FALL_LOG_PATH = os.path.join(DATA_DIR, "fall_log.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# ======================
# GLOBAL STATE
# ======================
latest_hr_state = {
    "hr": None,
    "rule_status": None,
    "rule_message": None,
    "is_danger": False,
    "timestamp": 0
}

latest_fall_state = {
    "status": "WAITING",
    "prob": 0.0,
    "timestamp": 0
}

# ======================
# WEB
# ======================
@app.route("/")
def index():
    return render_template("index.html")

# ======================
# LOGGING
# ======================
def log_hr(hr, rule_status, rule_message):
    file_exists = os.path.exists(HR_LOG_PATH)
    with open(HR_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "hr", "rule_status", "rule_message"])
        writer.writerow([time.time(), hr, rule_status, rule_message])

def log_fall(status, prob):
    file_exists = os.path.exists(FALL_LOG_PATH)
    with open(FALL_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "status", "probability"])
        writer.writerow([time.time(), status, prob])

# ======================
# API: RECEIVE HR
# ======================
@app.route("/hr", methods=["POST"])
def receive_hr():
    global last_display_time, display_hr_value

    data = request.get_json(force=True)
    try:
        hr = float(data["hr"])
    except:
        return jsonify({"status": "ERROR", "message": "Invalid HR"}), 400

    now = time.time()

    # gom HR
    display_hr_buffer.append(hr)

    # cập nhật HR hiển thị mỗi 5 giây
    if now - last_display_time >= DISPLAY_INTERVAL and len(display_hr_buffer) > 0:
        display_hr_value = int(sum(display_hr_buffer) / len(display_hr_buffer))
        display_hr_buffer.clear()
        last_display_time = now

    hr_show = display_hr_value if display_hr_value is not None else int(hr)

    # rule-based
    rule_status, rule_msg = rule_based_hr(hr_show)
    is_danger = rule_status.startswith("DANGER")

    latest_hr_state.update({
        "hr": hr_show,
        "rule_status": rule_status,
        "rule_message": rule_msg,
        "is_danger": is_danger,
        "timestamp": now
    })

    log_hr(hr_show, rule_status, rule_msg)

    return jsonify({
        "status": "OK",
        **latest_hr_state
    })

# ======================
# API: RECEIVE FALL DATA
# ======================
@app.route("/fall", methods=["POST"])
def receive_fall():
    data = request.get_json(force=True)
    samples = data.get("samples", [])

    result = {"status": "WAITING", "prob": 0.0}

    for s in samples:
        if len(s) == 6:
            result = update_fall_state(s)

    latest_fall_state.update({
        "status": result.get("status", "WAITING"),
        "prob": result.get("prob", 0.0),
        "timestamp": time.time()
    })

    log_fall(latest_fall_state["status"], latest_fall_state["prob"])

    return jsonify({"status": "OK"})

# ======================
# API: LATEST STATUS (FRONTEND)
# ======================
@app.route("/latest_status", methods=["GET"])
def latest_status():
    fall_status = fall_state.get("status", "WAITING")
    fall_prob = fall_state.get("prob", 0.0)

    alert = latest_hr_state["is_danger"] or fall_status == "FALL"

    return jsonify({
        "hr": latest_hr_state["hr"],
        "hr_danger": latest_hr_state["is_danger"],
        "hr_message": latest_hr_state["rule_message"],
        "fall_status": fall_status,
        "fall_prob": fall_prob,
        "alert": alert
    })

# ======================
# API: HR PLOT
# ======================
@app.route("/plot", methods=["GET"])
def plot_hr():
    if not os.path.exists(HR_LOG_PATH):
        return "No data yet", 400

    df = pd.read_csv(HR_LOG_PATH)
    if df.empty or "timestamp" not in df.columns:
        return "No valid data yet", 400

    t0 = df["timestamp"].iloc[0]
    df["t"] = df["timestamp"] - t0

    plt.figure(figsize=(8, 3), dpi=100)
    plt.plot(df["t"], df["hr"], label="HR", color="blue")

    plt.xlabel("Time (s)")
    plt.ylabel("Heart Rate (bpm)")
    plt.title("Heart Rate Monitoring")
    plt.legend()
    plt.grid(True)

    plt.savefig(HR_PLOT_PATH)
    plt.close()

    return send_file(HR_PLOT_PATH, mimetype="image/png")

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


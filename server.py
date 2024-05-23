from flask import Flask, request, jsonify
import pandas as pd
import Log_Gen  # Import the Log_Gen script

app = Flask(__name__)

# In-memory storage for logs
logs_df = pd.DataFrame(columns=['IP', 'Country', 'Timestamp', 'Sport', 'Status_Code', 'Bytes_Transferred', 'User_Agent', 'Time_Elapsed'])


@app.route('/logs', methods=['POST'])
def generate_and_receive_logs():
    global logs_df
    num_logs = int(request.json.get('num_logs', 10000))  # Default to 100 logs
    new_logs = Log_Gen.generate_sample_logs(num_logs)
    new_logs_df = pd.DataFrame(new_logs)
    logs_df = pd.concat([logs_df, new_logs_df], ignore_index=True)
    return jsonify({"message": "Logs generated and received successfully"}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    global logs_df
    num_logs = int(request.args.get('num_logs', 10000))  # Default to 100 logs
    new_logs = Log_Gen.generate_sample_logs(num_logs)
    new_logs_df = pd.DataFrame(new_logs)
    logs_df = pd.concat([logs_df, new_logs_df], ignore_index=True)
    latest_logs = logs_df.tail(num_logs).to_dict(orient='records')
    return jsonify(latest_logs), 200


if __name__ == '__main__':
    app.run(port=5000)

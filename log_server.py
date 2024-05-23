from faker import Faker
import random
import datetime
from flask import Flask, request, jsonify
import pandas as pd

# Initialize Faker
fake = Faker()

# Generate random IP address
def generate_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

# List of countries participating in the FunOlympics
olympic_countries = [
    "Algeria", "Angola", "Argentina", "Australia", "Bahrain", "Bangladesh",
    "Barbados", "Belarus", "Belgium", "Benin", "Bolivia", "Botswana", "Brazil", "Bulgaria",
    "Burkina Faso", "Burundi", "Cameroon", "Canada", "China", "Colombia", "Comoros",
    "Czech Republic", "North Korea", "Democratic Republic of the Congo", "Denmark",
    "Egypt", "Eswatini", "Ethiopia", "Finland", "France", "Gabon", "Germany", "Ghana",
    "Greece", "Guinea", "Honduras", "Hungary", "India", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Kenya", "Lesotho", "Liberia",
    "Madagascar", "Malawi", "Mali", "Mauritius", "Mexico", "Morocco", "Mozambique", "Namibia", "Netherlands",
    "New Zealand", "Nigeria", "Norway", "Pakistan", "Palestine", "Paraguay", "Philippines", "Poland", "Portugal",
    "Russia", "Rwanda", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Sweden", "Switzerland", "Syria",
    "Tanzania", "Thailand", "Trinidad and Tobago", "Tunisia", "Turkey",
    "Uganda", "Ukraine", "United Kingdom", "United States", "Uruguay", "Venezuela", "Zambia", "Zimbabwe"
]

# Generate random country
def generate_country():
    return random.choice(olympic_countries)

# Generate random timestamp within the specified range
def generate_timestamp():
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 24*60*60)  # 24 hours * 60 minutes * 60 seconds
    timestamp = start_date + datetime.timedelta(days=random_days, seconds=random_seconds)
    formatted_timestamp = timestamp.strftime('%d/%m/%Y:%H:%M:%S')
    return formatted_timestamp

# Generate random URL based on various sports-pages and endpoints
def generate_url():
    sports = [
        "Archery",
        "Athletics (Track and Field)",
        "Badminton",
        "Basketball",
        "Boxing",
        "Canoeing",
        "Cycling",
        "Fencing",
        "Football",
        "Golf",
        "Gymnastics",
        "Handball",
        "Hockey",
        "Judo",
        "Rowing",
        "Rugby",
        "Sailing",
        "Shooting",
        "Skateboarding",
        "Sport Climbing",
        "Surfing",
        "Table Tennis",
        "Taekwondo",
        "Tennis",
        "Triathlon",
        "Volleyball",
        "Weightlifting",
        "Wrestling"
    ]

    return f"GET/HTTP/1.1/{random.choice(sports)}"

# Generate random HTTP status code
def generate_status_code():
    status_codes = [200, 404, 500]
    weights = [0.8, 0.15, 0.05]  # Higher chance of successful requests (200)
    return random.choices(status_codes, weights=weights)[0]

# Sample user agents provided
sample_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.146 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3812.123",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.146 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/1.14 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/1.14 Mobile/15E148 Safari/605.1.15"
]

# Generate random user agent
def generate_user_agent():
    return random.choice(sample_user_agents)

# Generate random bytes transferred
def generate_bytes_transferred():
    return random.randint(100, 10000)

# Generate random time elapsed (milliseconds)
def generate_time_elapsed():
    return random.randint(1, 1000)  # Adjust the range as needed

# Generate web server log entry
def generate_log_entry():
    ip = generate_ip()
    country = generate_country()
    timestamp = generate_timestamp()
    url = generate_url()
    status_code = generate_status_code()
    user_agent = generate_user_agent()
    bytes_transferred = generate_bytes_transferred()
    time_elapsed = generate_time_elapsed()

    log_entry = {
        'IP': ip,
        'Country': country,
        'Timestamp': timestamp,
        'Sport': url.split('GET/HTTP/1.1/')[1],
        'Status_Code': status_code,
        'Bytes_Transferred': bytes_transferred,
        'User_Agent': user_agent,
        'Time_Elapsed': time_elapsed
    }
    return log_entry

# Generate a sample of web server logs
def generate_sample_logs(num_logs):
    logs = []
    for _ in range(num_logs):
        logs.append(generate_log_entry())
    return logs

# Initialize Flask app
app = Flask(__name__)

# In-memory storage for logs
logs_df = pd.DataFrame(columns=['IP', 'Country', 'Timestamp', 'Sport', 'Status_Code', 'Bytes_Transferred', 'User_Agent', 'Time_Elapsed'])

@app.route('/logs', methods=['POST'])
def generate_and_receive_logs():
    global logs_df
    num_logs = int(request.json.get('num_logs', 10000))  # Default to 10000 logs
    new_logs = generate_sample_logs(num_logs)
    new_logs_df = pd.DataFrame(new_logs)
    logs_df = pd.concat([logs_df, new_logs_df], ignore_index=True)
    return jsonify({"message": "Logs generated and received successfully"}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    global logs_df
    num_logs = int(request.args.get('num_logs', 10000))  # Default to 10000 logs
    new_logs = generate_sample_logs(num_logs)
    new_logs_df = pd.DataFrame(new_logs)
    logs_df = pd.concat([logs_df, new_logs_df], ignore_index=True)
    latest_logs = logs_df.tail(num_logs).to_dict(orient='records')
    return jsonify(latest_logs), 200

if __name__ == '__main__':
    app.run(port=5000)

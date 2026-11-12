from flask import Flask, render_template_string, request
from google import genai

app = Flask(__name__)

API_KEY = "AQ.Ab8RN6Jz6rmGxOk-qSptR9c7ZIhv8S-Hxlz2BwBRiddU7MUKEA"
client = genai.Client(api_key=API_KEY)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>AI Study Planner</title>
<style>
body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 20px; }
.container { max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin: auto; }
h2 { color: #333; text-align: center; }
label { display: block; margin-top: 10px; font-weight: bold; }
input, textarea { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
button { background: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; margin-top: 15px; width: 100%; font-size: 16px; }
button:hover { background: #45a049; }
.result { margin-top: 20px; background: #e9ecef; padding: 15px; border-radius: 4px; white-space: pre-wrap; }
</style>
</head>
<body>
<div class="container">
<h2>AI Study Planner</h2>
<form method="POST">
<label>Subject:</label>
<input type="text" name="subject" required value="{{ subject }}">
<label>Topics to Study/Revise:</label>
<textarea name="topics" rows="4" required>{{ topics }}</textarea>
<label>Timeframe / Available Days:</label>
<input type="text" name="timeframe" required value="{{ timeframe }}">
<button type="submit">Generate Schedule</button>
</form>
{% if schedule %}
<div class="result">
<h3>Your Study Schedule:</h3>
<p>{{ schedule }}</p>
</div>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    schedule = ""
    subject = ""
    topics = ""
    timeframe = ""
    if request.method == "POST":
        subject = request.form.get("subject")
        topics = request.form.get("topics")
        timeframe = request.form.get("timeframe")
        prompt = f"Create a detailed study schedule and revision plan for the subject {subject}. Topics to cover: {topics}. Timeframe available: {timeframe}. Format it clearly with day-wise breakdown."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        schedule = response.text
    return render_template_string(HTML_PAGE, schedule=schedule, subject=subject, topics=topics, timeframe=timeframe)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import google.generativeai as gemini
import os

# Load API key from file
with open("apikey.txt", "r") as file:
    api_key = file.read().strip()

# Configure the Gemini model
gemini.configure(api_key=api_key)
model = gemini.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Initialize Flask app
app = Flask(__name__)

# Route for frontend
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle user input and get response from Gemini
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Invalid input."}), 400

        user_input = data["message"].strip()
        if user_input == "":
            return jsonify({"reply": "Please type something."}), 400

        # Send message to Gemini
        reply = chat.send_message(user_input)
        return jsonify({"reply": reply.text})

    except Exception as e:
        print("Error:", str(e))  # Log the error in terminal
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

# Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
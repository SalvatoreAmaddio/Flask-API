from app.flaskFactory import app, is_connected

@app.route("/")
def hello_world():
    if is_connected:
        return f"<p>Ciao!</p>"
    else:
        return f"<p>Database connection failed.</p>"
    
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=8080, debug=True)
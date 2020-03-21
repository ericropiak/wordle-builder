from app.main import app

from werkzeug.serving import run_simple

if __name__ == "__main__":
    print('running local')
    # app.run(debug=True, host="0.0.0.0", port=5000)
    run_simple("0.0.0.0", 5000, app, use_reloader=True, use_debugger=True)


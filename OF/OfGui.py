from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html', title='HammerUI-OF')
    # return render_template('test.html', title='HammerUI-OF')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=12080, use_reloader=True)
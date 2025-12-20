from flask import Flask, request, redirect

app = Flask(__name__)

posts = []

@app.route("/", methods=["GET"])
def index():
    items = "".join(f"<li>{p}</li>" for p in posts) or "<li>（まだ投稿がありません）</li>"
    return f"""
    <html>
      <body>
        <h1>ミニ掲示板</h1>
        <p><a href="/write">書き込みページへ</a></p>
        <h2>投稿一覧</h2>
        <ul>{items}</ul>
      </body>
    </html>
    """

@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        msg = request.form.get("msg", "").strip()
        if msg:
            posts.append(msg)
        return redirect("/")

    return """
    <html>
      <body>
        <h1>書き込み</h1>
        <form method="POST">
          <textarea name="msg" rows="5" cols="60"></textarea><br><br>
          <button type="submit">投稿</button>
        </form>
        <p><a href="/">一覧へ戻る</a></p>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template, request, jsonify
import requests
from newspaper import Article


app = Flask(__name__)

API_KEY = '46443f1a48a90cfb586c4dbb4e3ecabb'  # ✅ Your actual GNews API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'articles': []})

    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&token={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # 🔍 Check for errors
    if 'articles' not in data:
        print("❌ ERROR: Response content =", data)
        return jsonify({'articles': []})

    print("✅ DEBUG: Articles received =", len(data.get('articles', [])))
    print("📰 DEBUG: Sample article =", data.get('articles', [{}])[0])

    return jsonify(data)

# ✅ Route for full article view
from newspaper import Article

@app.route('/article')
def article():
    url = request.args.get('url')
    if not url:
        return "Article URL missing!", 400

    try:
        article = Article(url)
        article.download()
        article.parse()

        paragraphs = article.text.strip().split('\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # Optional: Limit to first 8 paragraphs
        paragraphs = paragraphs[:8]

        return render_template('article.html',
                               title=article.title,
                               image=article.top_image,
                               paragraphs=paragraphs,
                               url=url)
    except Exception as e:
        return f"Error loading article: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)

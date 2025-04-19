from flask import Flask, request, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("shl_assessments.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

df["text_for_embedding"] = df["Assessment Name"] + " " + df["Test Type"]
embeddings = model.encode(df["text_for_embedding"].tolist(), convert_to_tensor=True)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "SHL Assessment Recommendation API is running. Use /health or POST to /recommend.", 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        req_data = request.get_json()
        query = req_data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query is required."}), 400

        query_embedding = model.encode([query], convert_to_tensor=True)
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_indices = similarities.argsort()[-10:][::-1]

        results = df.iloc[top_indices]
        recommendations = []

        for i, row in results.iterrows():
            recommendations.append({
                "Assessment Name": row["Assessment Name"],
                "URL": row["URL"],
                "Remote Testing Support": row["Remote Testing Support"],
                "Adaptive/IRT Support": row["Adaptive/IRT Support"],
                "Duration": row["Duration"],
                "Test Type": row["Test Type"],
                "Score": float(similarities[i])
            })

        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

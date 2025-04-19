import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🔍 SHL Assessment Recommendation System")
st.markdown("Enter a job description or requirement, and get the most relevant SHL assessments below:")

query = st.text_area("📝 Your Query", placeholder="e.g. Looking to hire a Java developer for 45-minute cognitive test", height=150)

if st.button("🔎 Get Recommendations"):
    if not query.strip():
        st.warning("⚠️ Please enter a query.")
    else:
        with st.spinner("Getting recommendations..."):
            try:
                response = requests.post("http://127.0.0.1:5000/recommend", json={"query": query})
                if response.status_code == 200:
                    results = response.json().get("recommendations", [])

                    if not results:
                        st.info("No matching assessments found.")
                    else:
                        st.success(f"Top {len(results)} Recommendations:")
                        for i, rec in enumerate(results, 1):
                            st.markdown(f"""
                            ---
                            **{i}. [{rec['Assessment Name']}]({rec['URL']})**
                            - 🧠 **Test Type**: {rec['Test Type']}
                            - ⏱️ **Duration**: {rec['Duration']}
                            - 🏠 **Remote**: {rec['Remote Testing Support']} | ⚙️ **Adaptive/IRT**: {rec['Adaptive/IRT Support']}
                            - 🔍 **Match Score**: `{rec['Score']:.2f}`
                            """)
                else:
                    st.error(f"API Error: {response.status_code} — {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")

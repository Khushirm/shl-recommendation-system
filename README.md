# SHL Assessment Recommendation System

This project is a full-stack AI-based recommendation system that intelligently suggests relevant SHL assessments based on job descriptions or natural language queries.
It simplifies the hiring process by helping hiring managers quickly discover the most appropriate assessments from SHL’s product catalog.

## Features

- Scrapes SHL’s official assessment catalog using Playwright
- Embeds queries and assessment metadata using Sentence Transformers
- Ranks top matching assessments using cosine similarity
- REST API with `/recommend` and `/health` endpoints
- Streamlit web UI to interactively test queries
- Fully deployable (API on Render, UI on Streamlit Cloud)

## How It Works

1. **Data Collection**
   - Dynamic scraping of assessment data from:  
     `https://www.shl.com/solutions/products/product-catalog/`
   - Stored in `shl_assessments.csv`

2. **Query Matching**
   - Uses `all-MiniLM-L6-v2` embedding model to represent both queries and assessment data
   - Computes cosine similarity to identify most relevant tests

3. **Backend**
   - Built with Flask
   - Endpoints:
     - `GET /health` — API status check
     - `POST /recommend` — Input a query, receive top matching assessments

4. **Frontend**
   - Streamlit app for user-friendly demo
   - Inputs query and displays results in a clean UI

## Project Structure
─ app.py # Flask API backend
─ ui.py # Streamlit frontend 
─ shl_scraper_playwright.py # Web scraper using Playwright 
─ shl_assessments.csv # Assessment data (scraped) 
─ test_api.py # Local testing script for POST /recommend 
─ requirements.txt # Python dependencies 


---

## Tech Stack

 Purpose         | Tool / Library                  
 Web scraping    | Playwright                      
 Data handling   | Pandas                          
 Embeddings      | Sentence Transformers (MiniLM)  
 Similarity      | Cosine similarity (sklearn)     
 API backend     | Flask                           
 Frontend        | Streamlit                       
 Deployment      | Render (API), Streamlit Cloud (UI) 

---

## How to Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/shl-recommendation-system.git
cd shl-recommendation-system
```
2. Install dependencies
   pip install -r requirements.txt
3. Run the Flask API
   python app.py


--Live Demo Links
Frontend (Streamlit App): (https://shl-recommendation-systemm.streamlit.app/)

API (Render endpoint): (https://shl-recommendation-system-7s4x.onrender.com)

GitHub Repo: (https://github.com/Khushirm/shl-recommendation-system)

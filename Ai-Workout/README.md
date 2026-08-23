# AI Workout & Diet Planner (Streamlit + Gemini)

## Setup
1. Install Python 3.9+
2. `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Get a free API key at https://aistudio.google.com → paste it in the app sidebar (do NOT hardcode it in the code).

## Structure
- `app.py` — main Streamlit app (form + AI plan generator)
- `data/exercises.json` — sample exercise dataset
- `data/foods.json` — sample food/nutrition dataset (includes Indian regional foods)

## Notes
- The API key is entered at runtime in the sidebar (kept in session, never saved to disk).
- Swap `GEMINI_MODEL` in `app.py` if you want a different Gemini model.
- To use IBM watsonx.ai instead (recommended for the internship branding), replace the `generate_plan` function with a call to the watsonx.ai text-generation endpoint.

import streamlit as st
import json
import requests
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Workout & Diet Planner", page_icon="💪", layout="centered")

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# ---------- LOAD DATASETS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "exercises.json")) as f:
    EXERCISES = json.load(f)

with open(os.path.join(BASE_DIR, "data", "foods.json")) as f:
    FOODS = json.load(f)


# ---------- AI CALL ----------
def generate_plan(api_key, profile):
    exercise_list = ", ".join(sorted(set(e["name"] for e in EXERCISES)))
    food_list = ", ".join(sorted(set(f["name"] for f in FOODS)))

    prompt = f"""
You are a certified fitness and nutrition coach for college students in India.
Create a personalized 7-day workout plan and a daily diet plan based on this profile:

- Age: {profile['age']}
- Gender: {profile['gender']}
- Weight (kg): {profile['weight']}
- Height (cm): {profile['height']}
- Fitness Goal: {profile['goal']}
- Activity Level: {profile['activity']}
- Diet Preference: {profile['diet']}
- Budget: {profile['budget']}
- Equipment Access: {profile['equipment']}
- Allergies/Restrictions: {profile['allergies'] if profile['allergies'] else 'None'}

Prefer using exercises from this list where possible (add others only if needed): {exercise_list}
Prefer using foods from this list where possible, especially culturally relevant Indian foods (add others only if needed): {food_list}

Output in clean Markdown with two sections:
## Workout Plan (Day 1 to Day 7, include rest days)
## Diet Plan (Breakfast, Lunch, Snacks, Dinner, with approx calories/protein)

Keep it practical, budget-friendly, and realistic for a student with limited time and gym access.
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": api_key}

    response = requests.post(GEMINI_URL, headers=headers, params=params, json=payload, timeout=60)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise Exception(f"Unexpected response format: {data}")


# ---------- UI ----------
st.title("💪 AI Workout & Diet Planner")
st.caption("Personalized fitness plans for students — powered by Google Gemini")

with st.sidebar:
    st.header("🔑 API Setup")
    api_key = st.text_input("Google AI Studio API Key", type="password",
                             help="Get a free key at aistudio.google.com. Never hardcode it in the app.")
    st.markdown("---")
    st.markdown("Get a key: [aistudio.google.com](https://aistudio.google.com)")

st.subheader("Your Profile")

with st.form("profile_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=15, max_value=60, value=21)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=65)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "General Fitness", "Endurance"])
    with col2:
        height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170)
        activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Eggetarian", "Vegan"])
        budget = st.selectbox("Budget", ["Low", "Medium", "High"])

    equipment = st.selectbox("Equipment Access", ["None (bodyweight only)", "Dumbbells only", "Full Gym"])
    allergies = st.text_input("Allergies / Restrictions (optional)")

    submitted = st.form_submit_button("Generate My Plan 🚀")

if submitted:
    if not api_key:
        st.error("Please enter your Google AI Studio API key in the sidebar.")
    else:
        profile = {
            "age": age, "gender": gender, "weight": weight, "height": height,
            "goal": goal, "activity": activity, "diet": diet, "budget": budget,
            "equipment": equipment, "allergies": allergies
        }
        with st.spinner("Generating your personalized plan..."):
            try:
                plan = generate_plan(api_key, profile)
                st.success("Here's your plan!")
                st.markdown(plan)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("---")
with st.expander("📋 View sample exercise & food database used"):
    st.write("**Exercises:**")
    st.table(EXERCISES)
    st.write("**Foods:**")
    st.table(FOODS)

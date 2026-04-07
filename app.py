import streamlit as st
import random
import matplotlib.pyplot as plt


st.title("🧠 AI Travel Planning Agent")

budget = st.slider("Budget", 1000, 10000, 3000)
days = st.slider("Days", 1, 5, 3)
mode = st.selectbox("Mode", ["cheap", "balanced", "luxury"])

run = st.button("Run Simulation")


places = [
    {"name": "Museum", "cost": 500, "crowd": 3, "time": 2},
    {"name": "Park", "cost": 200, "crowd": 1, "time": 1},
    {"name": "Fort", "cost": 400, "crowd": 2, "time": 2},
    {"name": "Beach", "cost": 300, "crowd": 2, "time": 3},
    {"name": "Mall", "cost": 600, "crowd": 3, "time": 2},
]

# ---------------- FUNCTIONS ---------------- #

def create_plan(budget, days, places):
    plan = []
    remaining = budget
    used = set()

    places_copy = places.copy()
    random.shuffle(places_copy)

    for _ in range(days):
        for place in places_copy:
            if place["name"] not in used and place["cost"] <= remaining:
                plan.append(place)
                remaining -= place["cost"]
                used.add(place["name"])
                break

    return plan


def utility(plan, mode="balanced"):
    enjoyment = len(plan) * 10
    cost = sum(p["cost"] for p in plan)
    crowd = sum(p["crowd"] for p in plan)
    time = sum(p["time"] for p in plan)

    if mode == "cheap":
        return enjoyment - 0.2 * cost - crowd - time
    elif mode == "luxury":
        return enjoyment * 1.5 - 0.05 * cost - 0.5 * crowd
    else:
        return enjoyment - 0.1 * cost - crowd - time


def should_replan(old_plan, new_plan, mode, threshold=2):
    return (utility(new_plan, mode) - utility(old_plan, mode)) > threshold


def generate_event():
    return random.choice([
        "none",
        "closed",
        "price_surge",
        "discount",
        "traffic_delay"
    ])

# ---------------- RUN ---------------- #

if run:

    plan = create_plan(budget, days, places)
    replans = 0
    history = []

    best_plan = plan
    best_utility = utility(plan, mode)

    for step in range(5):

        event = generate_event()
        new_places = [p.copy() for p in places]

        # Apply event effects
        if event == "closed":
            new_places = [p for p in new_places if p["name"] != "Museum"]

        elif event == "price_surge":
            for p in new_places:
                p["cost"] += 200

        elif event == "discount":
            for p in new_places:
                p["cost"] = max(50, p["cost"] - 100)

        elif event == "traffic_delay":
            for p in new_places:
                p["time"] += 2

        # 🔥 MULTI-PLAN SEARCH (major upgrade)
        candidates = [create_plan(budget, days, new_places) for _ in range(5)]
        new_plan = max(candidates, key=lambda p: utility(p, mode))

        old_u = utility(plan, mode)
        new_u = utility(new_plan, mode)

        # Update best memory
        if new_u > best_utility:
            best_plan = new_plan
            best_utility = new_u

        if should_replan(plan, new_plan, mode):
            plan = new_plan
            replans += 1

        history.append({
            "step": step + 1,
            "event": event,
            "old": old_u,
            "new": new_u
        })

    # ---------------- DISPLAY ---------------- #

    st.subheader("📍 Final Plan")
    st.write([p["name"] for p in plan])

    st.subheader("🏆 Best Plan Found")
    st.write([p["name"] for p in best_plan])

    st.write(f"**Best Utility:** {best_utility}")
    st.write(f"**Replans:** {replans}")

    # 🔥 EVENT EXPLANATION (XAI-lite)
    st.subheader("📊 Step Events & Impact")

    for h in history:
        delta = round(h["new"] - h["old"], 2)
        st.write(f"Step {h['step']} | Event: {h['event']} | ΔUtility: {delta}")

    # 🔥 COMPARISON
    st.subheader("📌 Final vs Best Comparison")
    st.write("Final Plan:", [p["name"] for p in plan])
    st.write("Best Plan:", [p["name"] for p in best_plan])

    # ---------------- GRAPH ---------------- #

    steps = [h["step"] for h in history]
    new_utils = [h["new"] for h in history]

    fig, ax = plt.subplots()
    ax.plot(steps, new_utils, marker='o')
    ax.set_xlabel("Step")
    ax.set_ylabel("Utility")
    ax.set_title("Agent Decision Improvement")
    ax.grid()

    st.pyplot(fig)
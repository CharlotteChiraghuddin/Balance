from collections import defaultdict

def analyze_exercise(exercises):
    totals = defaultdict(int)

    for ex in exercises:
        totals[ex.name] += ex.duration

    return totals

def generate_exercise_insights(totals):
    insights = []

    if not totals:
        insights.append("You haven't logged any exercise this week.")
        return insights

    # Find the dominant exercise type
    top_type = max(totals, key=totals.get)
    top_minutes = totals[top_type]

    insights.append(f"Your main exercise this week was {top_type} with {top_minutes} minutes.")

    # Add proportional insights
    total_minutes = sum(totals.values())

    for ex_type, minutes in totals.items():
        percent = round((minutes / total_minutes) * 100)
        insights.append(f"{ex_type} makes up {percent}% of your weekly exercise.")

    return insights

def analyze_finance(transactions):
    totals = defaultdict(float)

    for tx in transactions:
        totals[tx.category] += tx.amount

    return totals

def generate_finance_insights(totals):
    insights = []

    if not totals:
        insights.append("You haven't logged any transactions this week.")
        return insights

    # Find the highest spending category
    top_category = max(totals, key=totals.get)
    top_amount = totals[top_category]

    insights.append(f"You spent the most on {top_category} this week: ${top_amount:.2f}.")

    # Add proportional insights
    total_spent = sum(totals.values())

    for category, amount in totals.items():
        percent = round((amount / total_spent) * 100)
        insights.append(f"{category} accounts for {percent}% of your weekly spending.")

    return insights

def calculate_total_calories(food_entries):
    total_calories = 0
    for entry in food_entries:
        total_calories += entry.calories
    return total_calories

def generate_calorie_insights(total_calories):
    insights = []
    insights.append(f"You consumed a total of {total_calories} calories this week.")
    if total_calories > 14000:  # Example threshold
        insights.append("Consider moderating your calorie intake for better health.")
    else:
        insights.append("Great job maintaining a balanced calorie intake!")
    return insights

def analyze_mood(mood_entries):
    mood_count = defaultdict(int)

    for mood in mood_entries:
        mood_count[mood] += 1

    return mood_count

def generate_mood_insights(mood_count):
    insights = []

    if not mood_count:
        insights.append("You haven't logged any moods this week.")
        return insights

    # Find the most frequent mood
    top_mood = max(mood_count, key=mood_count.get)
    top_count = mood_count[top_mood]

    insights.append(f"Your most frequent mood this week was {top_mood}, logged {top_count} times.")

    total_entries = sum(mood_count.values())

    for mood, count in mood_count.items():
        percent = round((count / total_entries) * 100)
        insights.append(f"{mood} accounted for {percent}% of your mood entries.")

    return insights
def calculate_total_calories(food_entries):
    total_calories = 0
    for entry in food_entries:
        total_calories += entry.calories
    return total_calories

def analyze_calories(food_entries):
    total_calories = calculate_total_calories(food_entries)
    return total_calories

def generate_calorie_insights(total_calories):
    insights = []
    insights.append(f"You consumed a total of {total_calories} calories this week.")
    if total_calories > 14000:  # Example threshold
        insights.append("Consider moderating your calorie intake for better health.")
    else:
        insights.append("Great job maintaining a balanced calorie intake!")
    return insights


def interpret_weather(weathercode: int):
    if weathercode in [61, 63, 65]:
        return "Rainy"
    if weathercode in [71, 73, 75]:
        return "Snowy"
    if weathercode == 0:
        return "Clear"
    return "Moderate"
def generate_recommendation(weather: str, temperature: float):
    if weather == "Rainy":
        return "Not ideal for hiking. Consider bird watching or postponing the visit."

    if temperature and temperature > 30:
        return "High temperature detected. Visit early morning and stay hydrated."

    if weather == "Clear":
        return "Perfect conditions for hiking and guided tours."

    return "Conditions are acceptable. Follow park rules."


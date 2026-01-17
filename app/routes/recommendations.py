from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..services.weather import get_current_weather
from ..services.recommendation_logic import interpret_weather, generate_recommendation

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/park/{park_id}")
def recommend_for_park(park_id: int, db: Session = Depends(get_db)):
    park = db.query(models.Park).filter(models.Park.id == park_id).first()

    if not park or not park.park_location:
        raise HTTPException(status_code=404, detail="Park or location not found")

    weather_data = get_current_weather(
        latitude=float(park.park_location.latitude),
        longitude=float(park.park_location.longitude)
    )

    weather = interpret_weather(weather_data["weathercode"])
    recommendation = generate_recommendation(weather, weather_data["temperature"])

    return {
        "park": park.name,
        "weather": weather,
        "temperature": weather_data["temperature"],
        "recommendation": recommendation
    }

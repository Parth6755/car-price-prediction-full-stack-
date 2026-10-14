from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import predict_price
from schema import CarFeatures, PredictionResponse

app = FastAPI(
    title="AutoLux Car Price Prediction API",
    description="Predict used-vehicle selling prices using the trained Random Forest model.",
    version="1.0.0",
)

# The Streamlit frontend calls this API over HTTPS. CORS is included for browser-based
# clients too; the current Streamlit requests library does not require CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AutoLux Car Price Prediction API is running.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: CarFeatures):
    try:
        price = predict_price(features.dict())
        return PredictionResponse(prediction_price=price)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="Model artifacts are missing. Ensure random_forest_model.pkl and feature_columns.pkl are in the repository root.",
        ) from exc
    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Could not process the supplied car features: {exc}",
        ) from exc
    except Exception as exc:
        # Keep the API response useful without exposing internal file paths or tracebacks.
        raise HTTPException(
            status_code=500,
            detail="Prediction failed while loading the model or generating an estimate.",
        ) from exc

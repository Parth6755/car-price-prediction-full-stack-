# AutoLux — Car Price Prediction

A used-vehicle price estimation project using a trained Random Forest model, a FastAPI backend, and a Streamlit frontend.

## Project files

- `app.py` — Streamlit user interface
- `main.py` — FastAPI backend with `/`, `/health`, and `/predict` endpoints
- `model.py` — loads the saved model and aligns input features
- `schema.py` — validates prediction request and response data
- `random_forest_model.pkl` — trained model artifact
- `feature_columns.pkl` — feature order used during training
- `cardekho_data (1).csv` — training dataset
- `train.py` — optional script to retrain the model

## Run locally

Use Python 3.12 and run these commands from the repository root.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the API in terminal 1:

   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

   API docs: http://127.0.0.1:8000/docs

4. Start Streamlit in terminal 2:

   ```bash
   streamlit run app.py
   ```

   The local frontend defaults to http://127.0.0.1:8000/predict.

## Deploy on Render

Deploy **two Web Services** from this same GitHub repository, both on branch `main`, with the repository root as the Root Directory.

### Backend service

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

After deployment, check `/health` and `/docs` on the backend URL.

### Frontend service

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`
- Environment Variable: `CAR_PRICE_API_URL=https://YOUR-BACKEND-SERVICE.onrender.com/predict`

Replace the example API URL with the actual HTTPS URL of your backend service. Do not use `127.0.0.1` for the backend URL in a separate Render service.

## Model notes

The model predicts the selling price in lakhs, based on the dataset's target column. The saved model and feature-column artifact must come from the same training run. Do not retrain in production unless you intend to replace both artifacts together.

To retrain locally:

```bash
python train.py
```

The script writes the updated model artifacts to the repository root. Review and commit both artifacts together before deploying.

## Troubleshooting

- **Backend startup failure:** confirm Render uses `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Frontend cannot connect:** verify `CAR_PRICE_API_URL` points to the backend's public HTTPS `/predict` endpoint.
- **Missing model:** confirm `random_forest_model.pkl` and `feature_columns.pkl` are in the repository root.
- **Validation error:** inspect the JSON response from the API and make sure field names and category values match `schema.py`.

Predictions are estimates, not guaranteed resale offers.

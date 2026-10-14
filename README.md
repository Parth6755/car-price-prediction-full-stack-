# 🚗 Car Price Prediction System

A machine learning web application that predicts the estimated price of a car based on its features. The application uses **Streamlit** for the interactive frontend and **FastAPI** for the prediction API.

## ✨ Features

- **Car Price Prediction:** Predict the estimated price based on input features.
- **Interactive Frontend:** User-friendly interface built with Streamlit.
- **FastAPI Backend:** Handles prediction requests through a REST API.
- **Input Validation:** Sends car details to the backend for processing.
- **Error Handling:** Displays useful messages for connection and prediction errors.
- **Responsive Design:** Clean and modern interface for an improved user experience.

## 🛠️ Technologies Used

- Python
- Streamlit
- FastAPI
- Uvicorn
- Machine Learning
- Pandas and NumPy (if used in your model)

## 📁 Project Structure

```text
Car-Price-Prediction/
│
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend
├── model.pkl           # Trained ML model (if applicable)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

*Note: Your actual filenames may differ. Keep the file names consistent with your project.*

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Car-Price-Prediction
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt` file, install the main packages:

```bash
pip install streamlit fastapi uvicorn
```

Install any additional packages required by your machine learning model.

## 🚀 How to Run the Project

The backend and frontend must run in **two separate terminals**.

### Terminal 1: Start the FastAPI Backend

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

Backend API:

`http://127.0.0.1:8001`

API documentation:

`http://127.0.0.1:8001/docs`

### Terminal 2: Start the Streamlit Frontend

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

### API Configuration

The frontend should send prediction requests to:

```text
http://127.0.0.1:8001/predict
```

Make sure the backend is running before clicking the prediction button.

## 📊 How to Use

1. Start the FastAPI backend.
2. Start the Streamlit frontend.
3. Open the application in your browser.
4. Enter the required car details.
5. Click the **Predict Price** button.
6. View the predicted car price displayed by the application.

## 🐛 Troubleshooting

**Problem: Connection refused**

- Ensure the FastAPI backend is running on port `8001`.
- Check that the API URL in the Streamlit frontend is correct.

**Problem: 404 Not Found**

- Open `http://127.0.0.1:8001/docs`.
- Verify that the `/predict` endpoint exists.
- Confirm that the frontend uses the correct endpoint and HTTP method.

**Problem: Prediction button does not work**

- Check the terminal running Streamlit for error messages.
- Check the FastAPI terminal for request errors.
- Verify that the input fields match the backend's expected data format.

**Problem: Model file not found**

- Ensure the trained model file exists.
- Verify the model path in the backend code.

## 🔮 Future Improvements

- Add more car features for improved predictions.
- Improve model accuracy through hyperparameter tuning.
- Display prediction confidence or estimated price ranges.
- Deploy the frontend and backend online.
- Add visual analytics and historical price comparisons.

## 👨‍💻 Author

**Het Vaghasiya**

Car Price Prediction — Machine Learning Web Application.

## 📄 License

This project is intended for educational and learning purposes. Add a suitable open-source license if you plan to distribute it publicly.

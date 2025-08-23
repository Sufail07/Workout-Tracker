# 🏋️ Workout Tracker API

A robust RESTful API for tracking workouts, exercises, and user progress. Built using Django, Django REST Framework, JWT authentication, Redis caching, and rate limiting for reliability and scalability.

---

## 🚀 Features

- **User Registration & JWT Authentication**
- **Exercise Management:** Create, list, retrieve exercises
- **Workout Plans:** Create workout plans with nested exercises
- **Mark Workouts Completed**
- **View Completed Workouts**
- **Per-user Data Isolation**
- **API Documentation with drf-spectacular**
- **Redis Caching:** Caches GET requests to reduce DB load
- **Rate Limiting:** Uses DRF’s UserRateThrottle

---

## 📦 Tech Stack

- Django & Django REST Framework
- JWT (`djangorestframework-simplejwt`)
- Redis (caching)
- DRF UserRateThrottle (rate limiting)
- SQLite (default) / PostgreSQL (recommended for production)
- drf-spectacular (API docs)

---

## 🛠️ Setup Instructions

1. **Clone the repo:**
   ```sh
   git clone https://github.com/Sufail07/Workout-Tracker.git
   cd Workout-Tracker
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install requirements:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install and run Redis locally.**  
   *(See [Redis Quickstart](https://redis.io/docs/getting-started/installation/))*

5. **Migrate database:**
   ```sh
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

7. **Run the server:**
   ```sh
   python manage.py runserver
   ```

---

## 🔐 Authentication Workflow

- **Register:** `POST /api/register/`
- **Login (get tokens):** `POST /api/token/`
- **Refresh token:** `POST /api/token/refresh/`
- Use JWT access token in header:
  ```
  Authorization: Bearer <access_token>
  ```

---

## 🌐 API Endpoints & Workflow

### 1️⃣ User Authentication

- `POST /api/register/` — Register a new user
- `POST /api/token/` — Obtain JWT access and refresh tokens
- `POST /api/token/refresh/` — Refresh the access token

### 2️⃣ Exercises

- `GET /api/exercises/` — List all exercises (cached for 10 mins)
- `POST /api/exercises/` — Create a new exercise (invalidates cache)
- `GET /api/exercises/{id}/` — Retrieve exercise details

> **Caching:** All GET requests are cached using Redis to minimize repeated DB hits.

### 3️⃣ Workout Plans

- `POST /api/workoutplans/` — Create a workout plan with nested exercises  
   - Handles creation of WorkoutPlan and associated WorkoutExercise objects  
   - Invalidates cache for workout plans & completed workouts
- `GET /api/workoutplans/` — List all workout plans for the user  
   - Returns cached data if available (per-user, 5 mins), else queries DB, serializes, and caches

### 4️⃣ Mark Workout as Completed

- `POST /api/workoutplans/{id}/mark_completed/` — Marks the workout as completed  
   - Updates `completed` field  
   - Invalidates cache for completed workouts and all workouts

### 5️⃣ Completed Workouts

- `GET /api/completed_workouts/` — List all completed workouts for the user (cached, 5 mins)

---

## ⚡ Caching & Rate Limiting Logic

- **Exercises:** Cached for 10 mins (`exercise_data`)
- **Workout Plans per User:** Cached for 5 mins (`workout_data_{user_id}`)
- **Completed Workouts per User:** Cached for 5 mins (`completed_workouts_{user_id}`)
- **Cache Invalidation:** On create, update, delete, or marking completed
- **Rate Limiting:** All endpoints use DRF’s UserRateThrottle to prevent abuse

---


---

## 📝 Example: Creating a Workout Plan

**Request:**  
`POST /api/workoutplans/`
```json
{
  "name": "Push Day",
  "scheduled_date": "2025-08-24",
  "workout_exercises": [
    {
      "exercise": 1,
      "sets": 4,
      "reps": 10,
      "weight": 60
    },
    {
      "exercise": 2,
      "sets": 3,
      "reps": 8,
      "weight": 25
    }
  ]
}
```

**Response:**  
Returns the created workout plan with associated exercises.

---

## 📖 API Documentation

- Auto-generated docs at `/api/schema/` (OpenAPI/Swagger via drf-spectacular)

---

## ✨ To Do

- Add more statistics endpoints
- Add social features (friend leaderboards)
- More granular permissions
- Improved test coverage

---

## 👨‍💻 Author

Built with ❤️ by [Sufail07](https://github.com/Sufail07)

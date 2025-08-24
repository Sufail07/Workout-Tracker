# 🏋️ Workout Tracker API

A RESTful API for managing user workout plans, exercises, and progress tracking — built using **Django** and **Django REST Framework**, with **JWT authentication** for secure access.

---

## 🚀 Features

- ✅ User registration and login with JWT authentication  
- ✅ Exercise management with categories and muscle groups  
- ✅ Workout plan creation with scheduled date/time  
- ✅ Assign multiple exercises to a workout with sets, reps, and weights  
- ✅ Mark workouts as completed  
- ✅ View completed workouts  
- ✅ Permissions: users can only access their own data
- ✅ API documentation: contains proper API documentation using drf-spectacular  

---

## 📦 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Authentication**: JWT (via `djangorestframework-simplejwt`)  
- **Database**: SQLite (default, can switch to PostgreSQL)  
- **Testing**: Django `TestCase` and DRF `APITestCase`  

---

## 🛠️ Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/Workout-Tracker.git
   cd Workout-Tracker
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed Initial Exercises**
   *(Optional — only if you've written a custom management command)*
   ```bash
   python manage.py seed_exercises
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

---

## 🔐 API Authentication

Uses **JWT tokens**:

* Get tokens: `POST /api/login/`
* Refresh token: `POST /api/token/refresh/`
* Register: `POST /api/register/`

Use the access token in headers:

```http
Authorization: Bearer <your-access-token>
```

---

## 📡 API Endpoints

| Method | Endpoint                             | Description               |
| ------ | ------------------------------------ | ------------------------- |
| POST   | `/api/register/`                     | Register new user         |
| POST   | `/api/login/`                        | Login and get JWT token   |
| GET    | `/api/exercises/`                    | List all exercises        |
| POST   | `/api/workouts/`                     | Create new workout plan   |
| GET    | `/api/workouts/`                     | List user's workouts      |
| GET    | `/api/workouts/{id}/`                | View specific workout     |
| PUT    | `/api/workouts/{id}/`                | Update workout            |
| DELETE | `/api/workouts/{id}/`                | Delete workout            |
| POST   | `/api/workouts/{id}/mark_completed/` | Mark workout as completed |
| GET    | `/api/workouts/get_completed/`       | List completed workouts   |

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🔍 Sample WorkoutPlan JSON

Example `POST /api/workouts/` request body:

```json
{
  "name": "Push-Pull Day",
  "scheduled_time": "2025-07-05T07:00:00Z",
  "exercises": [
    {
      "exercise": 1,
      "sets": 4,
      "reps": 10,
      "weights": 40
    },
    {
      "exercise": 2,
      "sets": 3,
      "reps": 12,
      "weights": 15
    }
  ]
}
```

---

## ✨ To Do

* [x] Add Swagger/OpenAPI docs
* [ ] Add progress reports (e.g., weekly summary)
* [ ] Add support for recurring workouts
* [ ] Frontend integration (React or mobile app)

---

Project URL: https://roadmap.sh/projects/fitness-workout-tracker

## 👨‍💻 Author

Built with ❤️ by Sufail :))

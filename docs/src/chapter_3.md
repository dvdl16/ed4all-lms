# Part 3: Design

The back-end architecture design is detailed below.

### Requirements

- Basic account management (account creation and authentication).
- Users can be assigned to a course.
- User account integration with [Siyavula accounts](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#337dd598-f6b3-4991-bd01-840f8b3d16e8) via the API.
- [Siyavula activity integration](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#ce982f8b-525e-4223-a6ab-40df6676f8be) specifically [practice](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#bf3ede23-c039-423d-8c0e-579bcedfd180):
  - [Activity creation](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#dca3d699-17f2-470a-a9dc-1bb554ced3b7)
  - [Answer submission](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#05039a94-9671-4452-8b29-bcfd9b387c6d)
  - [Next question](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#66c78fcd-0217-4af0-9b1c-1989410849be)
  - [Retry question](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#fe265a89-8767-4c79-bc8a-7c3aea08a1fe)

### Design

#### Stack

- Framework: Flask
- Authentication: Flask-Login
- Data Validation: Pydantic
- ORM: SQLAlchemy
- API Communication: httpx
- Dependency Management: uv

#### Architecture
##### Database Design

Tables:

- Users
  - `id`
  - `email`: Unique, for authentication
  - `name`
  - `surname`
  - `password_hash`
  - `grade`
  - `country`
  - `curriculum`
  - `siyavula_account_id`: To link to Siyavula account
  - `role`: Either "Learner" or "Teacher".
  - `created_at`: Timestamp

- Courses
  - `id`
  - `name`: 'maths', 'science', 'physics' or 'chemistry'
  - `created_at`: Timestamp

- UserCourses
  - `id`:
  - `user_id`
  - `course_id`
  - `assigned_at`: Timestamp


##### Flask Blueprint Structure

- auth: user authentication and account creation.
- courses: course assignments
- siyavula: Siyavula API integration

##### API Workflow

- Account Management:
  - `/user` `POST` and `GET` endpoints
    - Flask + SQLAlchemy + Flask-Login

- Course Management:
  - List Courses for User: `/assignment` (`GET`)
  - Assign Users to Courses: `/assignment` (`POST`)

- Siyavula Integration:
  - Activity Creation: 
    - `GET` `/siyavula/activity`
    - [Siyavula API](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#dca3d699-17f2-470a-a9dc-1bb554ced3b7)
  - Answer Submission:
    - `POST` `/siyavula/activity/answer`
    - [Siyavula API](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#05039a94-9671-4452-8b29-bcfd9b387c6d)
  - Next Question:
    - `GET` `/siyavula/activity/question`
    - [Siyavula API](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#66c78fcd-0217-4af0-9b1c-1989410849be)
  - Retry Question:
    - `GET` `/siyavula/activity/retry`
    - [Siyavula API](https://documenter.getpostman.com/view/11391438/2s9YC5xBnb#fe265a89-8767-4c79-bc8a-7c3aea08a1fe)

##### Future-Proofing:

- Scalability: Use an SQL database (e.g., PostgreSQL)
- Cost-Effectiveness: Host on a minimal AWS/GCP/Fly.io instance
- Strict Pydantic models for API payloads

Example Pydantic Model:

```python
from pydantic import BaseModel

class SiyavulaUser(BaseModel):
    external_user_id: str
    uuid: str
    role: str
    name: str
    surname: str
    grade: int
    country: str
    curriculum: str
    email: str
    dialling_code: Optional[str]
    telephone: Optional[str]
    created_at: str
    updated_at: str
```
# PlanFlow Backend

## Project Overview
PlanFlow is a full-stack project planning tool designed for efficient project management. This web application allows authenticated users to create, manage, and track their projects. Key features include AI-generated project descriptions, PDF export functionality, and a user-friendly dashboard for project management.

## Screenshot

![Project Screenshot](https://raw.githubusercontent.com/abdrrahim2002/planflow_backend/refs/heads/main/images/1.png)

---
![Project Screenshot](https://raw.githubusercontent.com/abdrrahim2002/planflow_backend/refs/heads/main/images/2.png)

---
![Project Screenshot](https://raw.githubusercontent.com/abdrrahim2002/planflow_backend/refs/heads/main/images/3.png)

---
![Project Screenshot](https://raw.githubusercontent.com/abdrrahim2002/planflow_backend/refs/heads/main/images/4.png)

---


## Tech Stack
- **Backend:** Django, Django Rest Framework (DRF) with Token Authentication

## Features

### 1. Authentication
- Secure Sign Up, Login, and Logout functionalities
- Token-based authentication (DRF Token Authentication)
- Restricted access to dashboard and project management features for authenticated users only

### 2. Project Management (CRUD)
- Create, view, edit, and delete projects
- Project attributes include:
  - **Title**
  - **Description** (manual or AI-generated)
  - **Start and End Dates**
  - **Priority** (High, Medium, Low)
  - **Category**
  - **Status** (Not Started, In Progress, Completed)
  - **Image uploads** (1–2 images)

### 3. AI-Generated Descriptions
- Integrated with a free AI API (Hugging Face) to generate project summaries
- Option to use AI-generated content or manually input descriptions

### 4. Export as PDF
- Export project details as a formatted PDF, including all fields and uploaded images

### 5. Share by Email
- Share the project description or the entire project as a PDF via email

## Deployment
- The backend is deployed using **Docker** on the **Render** platform.

## Environment Variables
Ensure the following environment variables are set for proper project functionality:

```env
HUGGING_FACE_API_TOKEN= tocken you get when creating a hugging face account
SECRET_KEY= django secret key
DEBUG= True/False
ALLOWED_HOSTS= localhost,127.0.0.1,.onrender.com
EMAIL_HOST_USER= Google email
EMAIL_HOST_PASSWORD= Google email app password
CORS_ALLOWED_ORIGINS= url of the frontend 
```



# 🚀 Deployment Guide for QuarterClose.ai

This project is configured for easy deployment on **Render.com** (Free Tier available).

## Method 1: One-Click Deploy (Render)

1.  **Push your code to GitHub** (if you haven't already).
2.  Create an account on [Render.com](https://render.com/).
3.  Go to **Blueprints** -> **New Blueprint Instance**.
4.  Connect your GitHub repository.
5.  Render will automatically detect the `render.yaml` file.
6.  Click **Apply**.

Render will automatically provision:
- A **PostgreSQL Database**.
- The **Backend API**.
- The **Frontend UI**.
- It will verify the connections between them automagically.

---

## Method 2: Docker / manual Cloud

If you prefer using AWS, Azure, or DigitalOcean with Docker:

1.  **Build the Image**:
    ```bash
    docker build -t quarterclose-ai .
    ```

2.  **Run Container**:
    ```bash
    docker run -p 8000:8000 -p 8501:8501 quarterclose-ai
    ```

> *Note: For production, we recommend splitting the Backend and Frontend into separate containers/services as done in the `render.yaml` configuration.*

---

## Environment Variables

If configuring manually, ensure these are set:

| Service | Variable | Value |
|:---:|:---:|:---|
| **Backend** | `DATABASE_URL` | `postgresql://user:pass@host:5432/db` |
| **Frontend** | `API_URL` | `https://your-backend-url.onrender.com` |

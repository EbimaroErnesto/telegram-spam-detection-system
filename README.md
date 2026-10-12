# Telegram Spam Detection System

## Overview

This project implements a machine-learning-based Telegram spam detection and moderation system. It classifies messages as spam or ham and, when the bot has the required permissions, attempts to remove messages classified as spam.

## Features

- Text classification using TF-IDF and a trained Support Vector Machine (LinearSVC).
- FastAPI backend for prediction requests.
- Telegram bot integration for message moderation.
- SQLite database for recording classification events.
- Streamlit dashboard for monitoring recorded activity.

## Technologies

Python, scikit-learn, TF-IDF, LinearSVC, FastAPI, Uvicorn, Python Telegram Bot, SQLite, SQLAlchemy, Streamlit, Pandas, Joblib, and python-dotenv.

## Project Structure

- `backend/` — prediction API and database logic
- `bot/` — Telegram bot integration
- `dashboard/` — monitoring dashboard
- `models/` — saved model and vectorizer
- `requirements.txt` — Python dependencies

## Setup

1. Install Python and Git.
2. Create and activate a virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Create a local `.env` file with the required configuration variables.
5. Start the API, Telegram bot, and dashboard using the instructions in the project.

## Security

Never commit your `.env` file, bot token, passwords, or private message logs.

## Academic Project

Developed as a machine-learning-based Telegram spam detection and moderation project. Update this section with the correct author, supervisor, institution, and project details.

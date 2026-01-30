# Audition Evaluator Site Overview

## Project Overview

The **Audition Tracker Evaluator Site** is a web-based application designed to modernize and streamline the audition and adjudication process for performing arts programs specifically marching band–related activities. While performer skill levels have continued to rise, the tools used by adjudicators have largely remained inefficient and outdated (e.g., spreadsheets and manual data entry).

This project aims to replace those workflows with a focused, easy-to-use platform that allows instructors and adjudicators to quickly view, edit, and track performer information and scores in real time.

---

## Problem Statement

Adjudicators are often required to split their attention between observing performers and navigating cumbersome spreadsheets to locate names, scores, and attributes. This slows down evaluations, increases the chance of error, and detracts from the performer’s experience.

There is a clear need for a lightweight, purpose-built system that:

- Respects performers’ time and effort
- Reduces cognitive load on adjudicators
- Improves accuracy and efficiency during auditions

---

## Project Goal

Build a **simple, fast, and reliable audition tracking system** that allows educators to:

- View all registered performers in one place
- Quickly access and update performer attributes and scores
- Filter performers by key attributes (name, section, age, etc.)
- Perform all data operations through a clean API-backed workflow

---

## What I Will Build

The project consists of three main components:

### 1. Database Layer

A lightweight relational database built with **PostgreSQL**.

**Core entities:**

- **Performer**
- **Score**

**Relationships:**

- One performer → many scores (multiple adjudicators)

**Performer attributes:**

- Performer ID (Primary Key)
- Name
- Section
- Age
- Additional identifying attributes

**Score attributes:**

- Adjudicator ID (Primary Key)
- Performer ID (Foreign Key)
- Performance score
- Timing score
- Rhythm score

This structure supports clean CRUD operations and future expansion.

---

### 2. Backend API

The backend will be built using **Python 3.12** with **FastAPI**.

**Key responsibilities:**

- Expose REST API endpoints for all CRUD operations
- Handle requests from the web client
- Execute database operations against PostgreSQL

**Technical details:**

- FastAPI for route and API design
- Uvicorn as the ASGI server to support asynchronous, concurrent requests
- Modularized route files for maintainability and readability

This ensures multiple adjudicators can use the system simultaneously without blocking or performance issues.

---

### 3. Web Interface

A lightweight frontend built with:

- HTML
- CSS
- JavaScript

**User experience:**

- Adjudicators see a list of registered performers upon login
- Performer attributes are displayed on demand to avoid clutter
- Buttons allow users to edit scores and performer information
- All interactions communicate with backend API endpoints

**Basic interaction flow:**

1. User selects a performer
2. Frontend sends a GET request to retrieve performer data
3. User edits scores or attributes
4. Frontend sends a POST/PUT request to apply changes
5. Backend updates the PostgreSQL database

The same flow supports adding new performers (e.g., late registrants).

---

## Why This Project Matters

This application allows adjudicators to focus on what truly matters evaluating performers while removing unnecessary technical friction. By replacing spreadsheets with a structured, API-driven system, the evaluation process becomes faster, more accurate, and more respectful of everyone’s time.

---

## Notes

This specification represents the foundational design for the project. Implementation details may evolve during development, but the core goal remains the same: **streamline the audition evaluation process through clean, modern software design.**


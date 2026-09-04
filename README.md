# Customer Support API

A simple Customer Support Ticket API built using FastAPI and Pydantic.

## Features

- Get all support tickets
- Filter tickets by customer name, status, priority, and category
- Get a ticket by ID
- Create new tickets
- View ticket statistics
- View category statistics
- Get high-priority tickets
- Get tickets for a specific customer

## API Endpoints

- GET `/tickets`
- GET `/tickets/{ticket_id}`
- POST `/tickets`
- GET `/tickets/statistics`
- GET `/tickets/statistics/categories`
- GET `/tickets/high-priority`

## Technologies

- Python
- FastAPI
- Pydantic
- JSON

## How to Run

Install the required packages:

```bash
pip install -r requirement.txt
import json
from pathlib import Path
import time
from starlette.templating import Jinja2Templates

from config.logger_config import logger


from datetime import datetime
from fastapi import Request
from config.templates_config import templates
from fastapi.staticfiles import StaticFiles

import os

from fastapi import FastAPI, status ,BackgroundTasks
from starlette.responses import JSONResponse, FileResponse, HTMLResponse, PlainTextResponse
from utils import read_tickets_json_file
from schemas import TicketsInput
app=FastAPI()
logger.info("Customer Support API started")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Log file path setup (Absolute Path)
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE_PATH = BASE_DIR / "logs" / "app.log"
###############################################################################
@app.get("/logs", response_class=HTMLResponse)
async def show_logs(request: Request):
    logs_content = []

    # Check karein ke log file exist karti hai ya nahi
    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
            logs_content = file.readlines()
    else:
        logger.warning("Log file not found at path: %s", LOG_FILE_PATH)
        logs_content = ["Log file nahi mili."]

    return templates.TemplateResponse(
        request=request,
        name="logs.html",
        context={"logs": logs_content}
    )
################################################################################3
@app.get("/return-all-tickets")
def return_all_tickets():
    tickets=read_tickets_json_file()
    all_tickets = []
    if  tickets:
        all_tickets.append(tickets)
        logger.info("ticket found")
    else:
         logger.info("ticket  not found")
    return {"tickets": tickets}


@app.get("/tickets")
def get_tickets(status: str = None,
    priority: str = None,
    category: str = None,
    customer_name: str = None):
    tickets = read_tickets_json_file()
    filtered_tickets=[]
    if tickets:
        for ticket in tickets:
            match=True
            if status:
                if ticket["status"].lower() == status.lower():
                    logger.info("Fetching tickets")
            if priority:
                if ticket["priority"].lower() == priority.lower():
                    logger.info("prority matched")
            if category:
                if ticket["category"].lower() == category.lower():
                    logger.info("category matched")
            if customer_name:
                if ticket["customer_name"].lower() == customer_name.lower():
                    logger.info("customer name matched")
            if match:
                filtered_tickets.append(ticket)
                logger.info("Tickets found")
            logger.warning("No tickets found")
            match = False
    if filtered_tickets:
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "tickets found",
                        "tickets": filtered_tickets
                    }
                )
    else:
        return JSONResponse(
            status_code=400,
            content={
                "message": "tickets  not found",
            })
############################################
def send_email_background( customer_name:str,ticket_id: int):
    # 10 seconds ka pause
    time.sleep(6)
    # Email bhejne ka log
    logger.info(f"Email sent to {customer_name} for Ticket #{ticket_id}")
    time.sleep(6)
    logger.info("creadted sucsessfully")
@app.post("/add-tickets")
def create_ticket(ticket: TicketsInput,background_tasks: BackgroundTasks):
    tickets = read_tickets_json_file()

    # Safe ticket list check
    if not isinstance(tickets, list):
        tickets = []

    # Safe Dynamic ID generation
    if tickets:
        new_ticket_id = max(t.get("id", 0) for t in tickets) + 1
    else:
        new_ticket_id = 1

    new_ticket = {
        "id": new_ticket_id,
        "customer_name": ticket.customer_name,
        "category": ticket.category,
        "priority": ticket.priority,
        "description": ticket.description,
        "created_at": datetime.now().isoformat(),
        "status": "open"
    }

    tickets.append(new_ticket)

    with open("tickets.json", "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)

    logger.info(f"Ticket {new_ticket_id} created successfully")
    # Function name ke baad Customer Name aur New Ticket ID dono pass karein
    background_tasks.add_task(send_email_background, ticket.customer_name, new_ticket_id)
    return JSONResponse(
        status_code=201,
        content={
            "message": "ticket created successfully",
            "ticket": new_ticket
        }
    )
############################################################
@app.get("/tickets/statistics")
def ticket_statistics():
    logger.info("Calculating ticket statistics")
    tickets = read_tickets_json_file()
    total_tickets = len(tickets)

    open_tickets = 0
    in_progress_tickets = 0
    resolved_tickets = 0
    closed_tickets = 0
    urgent_tickets = 0
    high_priority_tickets = 0

    for ticket in tickets:

        if ticket["status"].lower() == "open":
            open_tickets += 1

        if ticket["status"].lower() == "in-progress":
            in_progress_tickets += 1

        if ticket["status"].lower() == "resolved":
            resolved_tickets += 1

        if ticket["status"].lower() == "closed":
            closed_tickets += 1

        if ticket["priority"].lower() == "urgent":
            urgent_tickets += 1

        if ticket["priority"].lower() == "high":
            high_priority_tickets += 1
    logger.info("Ticket statistics calculated successfully")
    return JSONResponse(
        status_code=200,
        content={
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "closed_tickets": closed_tickets,
            "urgent_tickets": urgent_tickets,
            "high_priority_tickets": high_priority_tickets
        }
    )
##############################################################################
###########################################################
@app.get("/tickets/statistics/category")
def ticket_statistics():

    tickets = read_tickets_json_file()
    authentication = 0
    payment = 0
    account = 0
    billing = 0
    other = 0
    technical = 0
    for ticket in tickets:
        if ticket["category"].lower() == "payment":
            payment += 1
        if ticket["category"].lower() == "authentication":
            authentication += 1
        if ticket["category"].lower() == "account":
            account += 1
        if ticket["category"].lower() == "billing":
            billing += 1
        if ticket["category"].lower() == "other":
            other += 1
        if ticket["category"].lower() == "technical":
            technical += 1
    return JSONResponse(
        status_code=200,
        content={
            "authentication": authentication,
            "payment": payment,
            "technical": technical,
            "account": account,
            "billing": billing,
            "other": other
        }
    )
#####################################################
@app.get("/tickets/statistics/priority")
def ticket_statistics():

    tickets = read_tickets_json_file()
    high = 0
    urgent = 0
    for ticket in tickets:
        if ticket["priority"].lower() == "urgent":
            urgent += 1
        if ticket["priority"].lower() == "high":
            high += 1
    return JSONResponse(
        status_code=200,
        content={
            "urgent": urgent,
            "high": high
        }
    )
#################################################################
@app.post("/return-detail")
def return_detail(tickets: TicketsInput):
        logger.info("/return-detail api is called")
        logger.info(tickets)
        tickets = read_tickets_json_file()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "tickets input ok",
                "patient_detail": tickets
            }
        )
################################################################# #
@app.get("/dashboard")
async def dashboard(request:Request, ):
    tickets=read_tickets_json_file()
    logger.info("TOTAL =", len(tickets))
    total_tickets = len(tickets)
    category_count = {}

    for ticket in tickets:
        category = ticket["category"].strip().lower()

        if category not in category_count:
            category_count[category] =0

        category_count[category] += 1
        if not tickets:
            logger.warning("Tickets not found")
    logger.info(f"category_count = {category_count}")
    logger.info(f"CATEGORY TOTAL = {sum(category_count.values())}")
    category_percentage={}
    for category, count in category_count.items():
        percentage = (count / total_tickets) * 100
        category_percentage[category] = round(percentage, 2)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
        "tickets":tickets,
        "total_tickets":total_tickets,
         "category_count":category_count,
        "category_percentage":category_percentage
         },
    )




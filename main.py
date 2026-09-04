import json

from datetime import datetime
from fastapi import FastAPI, status
from starlette.responses import JSONResponse
from utils import read_tickets_json_file
from schemas import TicketsInput
app=FastAPI()


@app.get("/return-all-tickets")
def return_all_tickets():
    tickets=read_tickets_json_file()
    all_tickets = []
    if  tickets:
        all_tickets.append(tickets)
        print("ticket found")
    else:
         print("ticket  not found")
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
                    print("status matched")
            if priority:
                if ticket["priority"].lower() == priority.lower():
                    print("prority matched")
            if category:
                if ticket["category"].lower() == category.lower():
                    print("category matched")
            if customer_name:
                if ticket["customer_name"].lower() == customer_name.lower():
                    print("customer name matched")
            if match:
                filtered_tickets.append(ticket)
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
@app.post("/tickets")
def create_ticket(ticket: TicketsInput):
    tickets = read_tickets_json_file()
    if tickets:
        new_ticket_id = tickets[-1]["ticket_id"] + 1
    else:
        new_ticket_id = 1
    new_ticket = {
        "ticket_id": new_ticket_id,
        "customer_name": ticket.customer_name,
        "category": ticket.category,
        "priority": ticket.priority,
        "description": ticket.description,
        "created_at": datetime.now().isoformat(),
        "status": "open"
    }

    tickets.append(new_ticket)
    with open("tickets.json", "w") as file:
        json.dump(tickets, file, indent=4)
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
        print("/return-detail api is called")
        print(tickets)
        tickets = read_tickets_json_file()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "tickets input ok",
                "patient_detail": tickets
            }
        )




"""FastAPI app wiring."""

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from app import (
    auth,
    calculator,
    inventory,
    orders,
    reports,
    users,
    validators,
)


app = FastAPI(title="issue-pilot-benchmark")


class LoginBody(BaseModel):
    email: str
    password: str


class OrderItem(BaseModel):
    sku: str = "widget"
    price: float
    qty: int


class CreateOrderBody(BaseModel):
    items: list[OrderItem]
    coupon: str | None = None


class EmailBody(BaseModel):
    email: str


def _bearer(authorization: str) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    return authorization.split(" ", 1)[1].strip()


@app.post("/auth/login")
def login(body: LoginBody) -> dict:
    token = users.login(body.email, body.password)
    return {"access_token": token}


@app.get("/auth/me")
def me(authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    user_id = auth.get_current_user_id(token)
    return {"user_id": user_id}


@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int) -> dict:
    user = users.get_user(user_id)
    return {"id": user_id, "email": user["email"], "role": user["role"]}


@app.post("/users/{user_id}/promote")
def promote_endpoint(user_id: int, authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    auth.require_admin(token)
    user = users.promote_user(user_id)
    return {"id": user_id, "role": user["role"]}


@app.post("/orders")
def create_order_endpoint(
    body: CreateOrderBody,
    authorization: str = Header(...),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> dict:
    token = _bearer(authorization)
    user_id = auth.get_current_user_id(token)
    items = [i.model_dump() for i in body.items]
    return orders.create_order(
        user_id=user_id,
        items=items,
        idempotency_key=idempotency_key,
        coupon=body.coupon,
    )


@app.post("/orders/{order_id}/refund")
def refund_endpoint(order_id: int, authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    auth.get_current_user_id(token)
    return orders.refund_order(order_id)


@app.get("/inventory/{sku}")
def stock_endpoint(sku: str) -> dict:
    return {"sku": sku, "stock": inventory.get_stock(sku)}


@app.post("/validate/email")
def validate_email(email: str) -> dict:
    return {"valid": validators.is_valid_email(email)}


@app.get("/calc/sum")
def calc_sum(start: int, end: int) -> dict:
    return {"result": calculator.sum_inclusive(start, end)}


@app.patch("/users/me/email")
def change_email_endpoint(body: EmailBody, authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    user_id = auth.get_current_user_id(token)
    return users.change_email(user_id, body.email)


@app.get("/notifications/inbox")
def inbox_endpoint(authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    user_id = auth.get_current_user_id(token)
    from app import notifications

    return {"messages": notifications.list_messages(user_id)}


@app.get("/audit/events")
def audit_events_endpoint(order_id: int, authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    auth.get_current_user_id(token)
    from app import audit

    return {"events": audit.events_for_order(order_id)}


@app.get("/reports/sales")
def sales_report_endpoint(authorization: str = Header(...)) -> dict:
    token = _bearer(authorization)
    user_id = auth.get_current_user_id(token)
    if users.get_user(user_id).get("role") != "admin":
        raise HTTPException(status_code=403, detail="admin required")
    return reports.build_snapshot()


@app.get("/quotes/surcharge")
def surcharge_quote(amount: float, region: str = "home") -> dict:
    from app import tax

    return {
        "amount": amount,
        "region": region,
        "surcharge": (
            tax.away_levy(amount)
            if region == "remote"
            else tax.tax_on(amount, region)
        ),
    }


@app.get("/quotes/delivery")
def delivery_quote(sku: str, qty: int = 1, zone: str | None = None) -> dict:
    from app import shipping

    items = [{"sku": sku, "qty": qty}]
    return {"sku": sku, "postage": shipping.quote_shipment(items, zone)}

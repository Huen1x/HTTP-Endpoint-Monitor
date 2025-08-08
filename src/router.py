import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from models import Endpoint, SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class EndpointIn(BaseModel):
    url: HttpUrl


class EndpointOut(BaseModel):
    id: int
    url: HttpUrl
    count: int


class CheckOut(BaseModel):
    status: int
    counted: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EndpointOut, status_code=201)
def add_endpoint(data: EndpointIn, db: Session = Depends(get_db)) -> EndpointOut:
    existing = db.query(Endpoint).filter(Endpoint.url == str(data.url)).first()
    if existing:
        logger.error(f"Endpoint already exists: {data.url}")
        raise HTTPException(status_code=400, detail="Endpoint already exists")
    endpoint = Endpoint(url=str(data.url))
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    logger.info(f"Added new endpoint: {endpoint.url}")
    return endpoint


@router.post("/{id}/check", response_model=CheckOut)
async def check_endpoint(id: int, db: Session = Depends(get_db)) -> CheckOut:
    endpoint = db.get(Endpoint, id)
    if not endpoint:
        logger.error(f"Endpoint not found: {id}")
        raise HTTPException(status_code=404, detail="Endpoint not found")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint.url, timeout=10.0)
        counted = 200 <= response.status_code < 300
    except httpx.RequestError as e:
        logger.warning(f"Request error for endpoint {id}: {e}")
        counted = False
        response = None
    if counted:
        endpoint.count += 1
        db.commit()
        db.refresh(endpoint)
        logger.info(
            f"Endpoint {id} checked successfully, count updated to {endpoint.count}"
        )
    return {"status": response.status_code if response else 0, "counted": counted}


@router.get("/", response_model=list[EndpointOut], status_code=200)
def list_endpoints(
    sort: str = "desc", db: Session = Depends(get_db)
) -> list[EndpointOut]:
    query = db.query(Endpoint)
    if sort == "asc":
        query = query.order_by(Endpoint.count.asc())
    else:
        query = query.order_by(Endpoint.count.desc())
    return query.all()


@router.delete("/{id}", status_code=204)
def delete_endpoint(id: int, db: Session = Depends(get_db)):
    endpoint = db.get(Endpoint, id)
    if not endpoint:
        logger.error(f"Endpoint not found for deletion: {id}")
        raise HTTPException(status_code=404, detail="Endpoint not found")
    db.delete(endpoint)
    db.commit()
    logger.info(f"Deleted endpoint: {id}")

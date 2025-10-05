from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import deps
from ..models.event import Event
from ..models.media import Media
from ..schemas.event import EventCreate, EventOut, EventUpdate


router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("/", response_model=list[EventOut])
async def list_events(db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)) -> Sequence[Event]:
	events = (
		db.query(Event)
		.filter(Event.owner_id == current_user.id)
		.order_by(Event.event_date.desc())
		.all()
	)
	return events


@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)) -> Event:
	event = Event(
		title=payload.title,
		description=payload.description,
		event_date=payload.event_date,
		owner_id=current_user.id,
	)
	db.add(event)
	db.commit()
	db.refresh(event)
	if payload.media_ids:
		_assign_media(db, payload.media_ids, current_user.id, event.id)
	db.refresh(event)
	return event


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: int, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)) -> Event:
	event = _get_owned_event(db, event_id, current_user.id)
	return event


@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)) -> Event:
	event = _get_owned_event(db, event_id, current_user.id)
	if payload.title is not None:
		event.title = payload.title
	if payload.description is not None:
		event.description = payload.description
	if payload.event_date is not None:
		event.event_date = payload.event_date
	if payload.media_ids is not None:
		_assign_media(db, payload.media_ids, current_user.id, event.id)
	db.commit()
	db.refresh(event)
	return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)) -> None:
	event = _get_owned_event(db, event_id, current_user.id)
	db.delete(event)
	db.commit()


def _get_owned_event(db: Session, event_id: int, user_id: int) -> Event:
	event = db.query(Event).filter(Event.id == event_id, Event.owner_id == user_id).first()
	if not event:
		raise HTTPException(status_code=404, detail="Event not found")
	return event


def _assign_media(db: Session, media_ids: list[int], user_id: int, event_id: int) -> None:
	media_items = db.query(Media).filter(Media.id.in_(media_ids), Media.owner_id == user_id).all()
	for media in media_items:
		media.event_id = event_id
	db.commit()

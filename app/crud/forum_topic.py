from typing import Optional, Type

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models.forum_topic import ForumTopic, ForumTopicStatus, ForumTopicType
from app.schemas.forum_topic import ForumTopicCreate, ForumTopicUpdate


def create_forum_topic(db: Session, topic: ForumTopicCreate, creator_id: int) -> ForumTopic:
    """Create a new forum topic"""
    db_topic = ForumTopic(
        title=topic.title,
        description=topic.description,
        topic_type=topic.topic_type,
        is_pinned=topic.is_pinned,
        course_id=topic.course_id,
        creator_id=creator_id
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_forum_topic(db: Session, topic_id: int) -> Optional[ForumTopic]:
    """Get a forum topic by ID"""
    return db.query(ForumTopic).filter(ForumTopic.topic_id == topic_id).first()


def get_forum_topics(
        db: Session,
        course_id: Optional[int] = None,
        creator_id: Optional[int] = None,
        topic_type: Optional[ForumTopicType] = None,
        status: Optional[ForumTopicStatus] = None,
        is_pinned: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
) -> list[Type[ForumTopic]]:
    """Get forum topics with optional filters"""
    query = db.query(ForumTopic)

    if course_id:
        query = query.filter(ForumTopic.course_id == course_id)

    if creator_id:
        query = query.filter(ForumTopic.creator_id == creator_id)

    if topic_type:
        query = query.filter(ForumTopic.topic_type == topic_type)

    if status:
        query = query.filter(ForumTopic.status == status)
    else:
        # By default, exclude hidden topics
        query = query.filter(ForumTopic.status != ForumTopicStatus.HIDDEN)

    if is_pinned is not None:
        query = query.filter(ForumTopic.is_pinned == is_pinned)

    # Order by pinned topics first, then by last activity
    query = query.order_by(
        desc(ForumTopic.is_pinned),
        desc(ForumTopic.last_activity)
    )

    return query.offset(skip).limit(limit).all()


def count_forum_topics(
        db: Session,
        course_id: Optional[int] = None,
        creator_id: Optional[int] = None,
        topic_type: Optional[ForumTopicType] = None,
        status: Optional[ForumTopicStatus] = None,
        is_pinned: Optional[bool] = None
) -> int:
    """Count forum topics with optional filters"""
    query = db.query(func.count(ForumTopic.topic_id))

    if course_id:
        query = query.filter(ForumTopic.course_id == course_id)

    if creator_id:
        query = query.filter(ForumTopic.creator_id == creator_id)

    if topic_type:
        query = query.filter(ForumTopic.topic_type == topic_type)

    if status:
        query = query.filter(ForumTopic.status == status)
    else:
        # By default, exclude hidden topics
        query = query.filter(ForumTopic.status != ForumTopicStatus.HIDDEN)

    if is_pinned is not None:
        query = query.filter(ForumTopic.is_pinned == is_pinned)

    return query.scalar()


def update_forum_topic(db: Session, topic_id: int, topic_update: ForumTopicUpdate) -> Optional[ForumTopic]:
    """Update a forum topic"""
    db_topic = get_forum_topic(db, topic_id)
    if db_topic:
        update_data = topic_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_topic, key, value)

        db.commit()
        db.refresh(db_topic)
    return db_topic


def delete_forum_topic(db: Session, topic_id: int) -> bool:
    """Delete a forum topic"""
    db_topic = get_forum_topic(db, topic_id)
    if db_topic:
        db.delete(db_topic)
        db.commit()
        return True
    return False


def increment_view_count(db: Session, topic_id: int) -> Optional[ForumTopic]:
    """Increment the view count of a forum topic"""
    db_topic = get_forum_topic(db, topic_id)
    if db_topic:
        db_topic.view_count += 1
        db.commit()
        db.refresh(db_topic)
    return db_topic


def update_last_activity(db: Session, topic_id: int) -> Optional[ForumTopic]:
    """Update the last activity timestamp of a forum topic"""
    db_topic = get_forum_topic(db, topic_id)
    if db_topic:
        db_topic.last_activity = func.current_timestamp()
        db.commit()
        db.refresh(db_topic)
    return db_topic

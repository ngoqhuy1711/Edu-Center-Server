from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.models.forum import ForumTopic, ForumPost, PostLike
from app.schemas.forum import (
    ForumTopicCreate, ForumTopicBase,
    ForumPostCreate, PostLikeCreate, )


def get_topic(db: Session, topic_id: int) -> Type[ForumTopic]:
    topic = (
        db.query(ForumTopic)
        .options(selectinload(ForumTopic.posts))
        .filter(ForumTopic.topic_id == topic_id, ForumTopic.is_deleted.is_(False))
        .first()
    )
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic


def list_topics(db: Session, course_id: int, skip: int = 0, limit: int = 100) -> list[Type[ForumTopic]]:
    return (
        db.query(ForumTopic)
        .filter(ForumTopic.course_id == course_id, ForumTopic.is_deleted.is_(False))
        .order_by(ForumTopic.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_topic(db: Session, topic_in: ForumTopicCreate, user_id: int) -> ForumTopic:
    topic = ForumTopic(**topic_in.model_dump(), created_by=user_id, updated_by=user_id)
    try:
        with db.begin():
            db.add(topic)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create topic")
    db.refresh(topic)
    return topic


def update_topic(db: Session, topic_id: int, topic_in: ForumTopicBase, user_id: int) -> Type[ForumTopic]:
    topic = db.query(ForumTopic).filter(ForumTopic.topic_id == topic_id, ForumTopic.is_deleted.is_(False)).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    for field, value in topic_in.model_dump(exclude_unset=True).items():
        setattr(topic, field, value)
    topic.updated_by = user_id
    try:
        with db.begin():
            db.add(topic)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update topic")
    db.refresh(topic)
    return topic


def delete_topic(db: Session, topic_id: int, user_id: int) -> None:
    topic = db.query(ForumTopic).filter(ForumTopic.topic_id == topic_id, ForumTopic.is_deleted.is_(False)).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    topic.is_deleted = True
    topic.updated_by = user_id
    try:
        with db.begin():
            db.add(topic)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete topic")


def get_post(db: Session, post_id: int) -> Type[ForumPost]:
    post = (
        db.query(ForumPost)
        .options(selectinload(ForumPost.topic), selectinload(ForumPost.likes))
        .filter(ForumPost.post_id == post_id, ForumPost.is_deleted.is_(False))
        .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def list_posts(db: Session, topic_id: int, skip: int = 0, limit: int = 100) -> list[Type[ForumPost]]:
    return (
        db.query(ForumPost)
        .filter(ForumPost.topic_id == topic_id, ForumPost.is_deleted.is_(False))
        .order_by(ForumPost.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_post(db: Session, post_in: ForumPostCreate, user_id: int) -> ForumPost:
    post = ForumPost(**post_in.model_dump(), created_by=user_id, updated_by=user_id)
    try:
        with db.begin():
            db.add(post)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create post")
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, post_in: ForumPostCreate, user_id: int) -> Type[ForumPost]:
    post = db.query(ForumPost).filter(ForumPost.post_id == post_id, ForumPost.is_deleted.is_(False)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    for field, value in post_in.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    post.updated_by = user_id
    try:
        with db.begin():
            db.add(post)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update post")
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int, user_id: int) -> None:
    post = db.query(ForumPost).filter(ForumPost.post_id == post_id, ForumPost.is_deleted.is_(False)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.is_deleted = True
    post.updated_by = user_id
    try:
        with db.begin():
            db.add(post)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete post")


def add_like(db: Session, like_in: PostLikeCreate) -> PostLike:
    existing = (
        db.query(PostLike)
        .filter(
            PostLike.post_id == like_in.post_id,
            PostLike.user_id == like_in.user_id,
            PostLike.is_deleted.is_(False),
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already liked")
    like = PostLike(**like_in.model_dump())
    try:
        with db.begin():
            db.add(like)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not add like")
    db.refresh(like)
    return like


def remove_like(db: Session, like_id: int) -> None:
    like = db.query(PostLike).filter(PostLike.like_id == like_id, PostLike.is_deleted.is_(False)).first()
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    like.is_deleted = True
    try:
        with db.begin():
            db.add(like)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not remove like")

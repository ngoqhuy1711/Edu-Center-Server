from typing import Optional, Dict, Any, Type, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.forum_post import ForumPost, ForumPostLike, ForumPostStatus, ForumPostType
from app.schemas.forum_post import ForumPostCreate, ForumPostUpdate


def create_post(db: Session, post: ForumPostCreate, author_id: int) -> ForumPost:
    """Create a new forum post"""
    db_post = ForumPost(
        title=post.title,
        content=post.content,
        author_id=author_id,
        course_id=post.course_id,
        parent_post_id=post.parent_post_id,
        post_type=post.post_type,
        status=post.status,
        is_pinned=post.is_pinned
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int) -> Optional[ForumPost]:
    """Get a forum post by ID"""
    return db.query(ForumPost).filter(ForumPost.post_id == post_id).first()


def get_posts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        author_id: Optional[int] = None,
        post_type: Optional[ForumPostType] = None,
        status: Optional[ForumPostStatus] = None,
        parent_post_id: Optional[int] = None,
        is_pinned: Optional[bool] = None
) -> Dict[str, Any]:
    """Get forum posts with optional filtering"""
    query = db.query(ForumPost)

    # Apply filters if provided
    if course_id is not None:
        query = query.filter(ForumPost.course_id == course_id)

    if author_id is not None:
        query = query.filter(ForumPost.author_id == author_id)

    if post_type is not None:
        query = query.filter(ForumPost.post_type == post_type)

    if status is not None:
        query = query.filter(ForumPost.status == status)

    if parent_post_id is not None:
        query = query.filter(ForumPost.parent_post_id == parent_post_id)

    if is_pinned is not None:
        query = query.filter(ForumPost.is_pinned == is_pinned)

    # Count total before applying pagination
    total = query.count()

    # Order posts by pinned status and creation date
    query = query.order_by(desc(ForumPost.is_pinned), desc(ForumPost.created_at))

    # Apply pagination
    posts = query.offset(skip).limit(limit).all()

    return {
        "posts": posts,
        "total": total
    }


def update_post(db: Session, post_id: int, post_update: ForumPostUpdate) -> Optional[ForumPost]:
    """Update a forum post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return None

    # Update only fields that are provided
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    """Delete a forum post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return False

    db.delete(db_post)
    db.commit()
    return True


def increment_view_count(db: Session, post_id: int) -> Optional[ForumPost]:
    """Increment the view count of a post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return None

    db_post.view_count += 1
    db.commit()
    db.refresh(db_post)
    return db_post


# Like-related functions

def add_like(db: Session, post_id: int, user_id: int) -> Optional[Union[Type[ForumPostLike], ForumPostLike]]:
    """Add a like to a post"""
    # Check if post exists
    post = get_post(db, post_id)
    if not post:
        return None

    # Check if like already exists
    existing_like = db.query(ForumPostLike).filter(
        ForumPostLike.post_id == post_id,
        ForumPostLike.user_id == user_id
    ).first()

    if existing_like:
        return existing_like

    # Create new like
    new_like = ForumPostLike(post_id=post_id, user_id=user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


def remove_like(db: Session, post_id: int, user_id: int) -> bool:
    """Remove a like from a post"""
    like = db.query(ForumPostLike).filter(
        ForumPostLike.post_id == post_id,
        ForumPostLike.user_id == user_id
    ).first()

    if not like:
        return False

    db.delete(like)
    db.commit()
    return True


def get_replies(db: Session, post_id: int) -> list[Type[ForumPost]]:
    """Get all replies for a post"""
    return db.query(ForumPost).filter(ForumPost.parent_post_id == post_id).all()

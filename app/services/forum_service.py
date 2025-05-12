from sqlmodel import Session
from app.crud import *

# Service cho ForumPost

def create_forum_post_service(session: Session, post):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_forum_post(session, post)

# Service cho ForumTopic, PostLike có thể làm tương tự. 
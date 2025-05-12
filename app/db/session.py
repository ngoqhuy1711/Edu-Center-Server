from sqlmodel import create_engine, Session

# Thay đổi thông tin kết nối bên dưới cho phù hợp với database của bạn
DATABASE_URL = "postgresql://ngoqhuy:1711@localhost:5432/EduCenterDB"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session 
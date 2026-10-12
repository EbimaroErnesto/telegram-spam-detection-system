from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'spam_detection.db')}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


class MessageLog(Base):

    __tablename__ = "message_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    message = Column(
        String,
        nullable=False
    )

    prediction = Column(
        String,
        nullable=False
    )

    confidence_score = Column(
        Float,
        nullable=False
    )

    action = Column(
        String,
        nullable=False,
        default="ALLOWED"
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


Base.metadata.create_all(bind=engine)
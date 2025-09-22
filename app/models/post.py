from sqlalchemy import String, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(512), default="")
    project_code: Mapped[str] = mapped_column(String(64), default="")
    category_name: Mapped[str] = mapped_column(String(128), default="")
    topic_name: Mapped[str] = mapped_column(String(128), default="")
    tags: Mapped[list] = mapped_column(JSON, default=[])
    is_available_in_public_feed: Mapped[bool] = mapped_column(Boolean, default=True)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    stats: Mapped[dict] = mapped_column(JSON, default={})  # view_count, upvote_count, exit_count, rating_count, average_rating, etc.
    media: Mapped[dict] = mapped_column(JSON, default={})  # video_link, thumbnail_url, gif_thumbnail_url
    owner: Mapped[dict] = mapped_column(JSON, default={})  # owner object

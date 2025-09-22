from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Owner(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    picture_url: Optional[str] = None
    user_type: Optional[str] = None
    has_evm_wallet: Optional[bool] = None
    has_solana_wallet: Optional[bool] = None

class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    count: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class TopicOwner(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    profile_url: Optional[str] = None
    user_type: Optional[str] = None
    has_evm_wallet: Optional[bool] = None
    has_solana_wallet: Optional[bool] = None

class Topic(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    slug: Optional[str] = None
    is_public: Optional[bool] = None
    project_code: Optional[str] = None
    posts_count: Optional[int] = None
    language: Optional[str] = None
    created_at: Optional[str] = None
    owner: Optional[TopicOwner] = None

class BaseToken(BaseModel):
    address: str = ""
    name: str = ""
    symbol: str = ""
    image_url: str = ""

class PostOut(BaseModel):
    id: int
    owner: Owner | Any = {}
    category: Category | Any = {}
    topic: Topic | Any = {}
    title: str
    is_available_in_public_feed: bool = True
    is_locked: bool = False
    slug: str
    upvoted: bool = False
    bookmarked: bool = False
    following: bool = False
    identifier: str = ""
    comment_count: int = 0
    upvote_count: int = 0
    view_count: int = 0
    exit_count: int = 0
    rating_count: int = 0
    average_rating: int = 0
    share_count: int = 0
    bookmark_count: int = 0
    video_link: str = ""
    thumbnail_url: str = ""
    gif_thumbnail_url: str = ""
    contract_address: str = ""
    chain_id: str = ""
    chart_url: str = ""
    baseToken: BaseToken = BaseToken()
    created_at: int = 0
    tags: List[str] = []

class FeedResponse(BaseModel):
    status: str = Field(default="success")
    post: List[PostOut] = Field(default_factory=list)

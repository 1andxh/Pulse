from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    String,
    Boolean,
    CheckConstraint,
    UniqueConstraint,
)
from src.db.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime, timezone
from src.probe.models import Probe


class Monitor(Base):
    # specific target to watch

    __tablename__ = "monitors"

    __table_args__ = (
        UniqueConstraint("url", name="uq_monitor_url"),
        CheckConstraint(
            "url LIKE 'http://%' OR url LIKE 'https://%'", name="check_url_protocol"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    check_interval: Mapped[int] = mapped_column(default=30)

    # relationships
    probes: Mapped[list["Probe"]] = relationship(
        "Probe", back_populates="monitor", cascade="all, delete-orphan"
    )

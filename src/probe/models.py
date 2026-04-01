from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, String, func, Boolean
from src.db.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime, timezone
from src.monitor.models import Monitor


class Probe(Base):
    # single recorded ping event

    __tablename__ = "probes"

    id: Mapped[int] = mapped_column(primary_key=True)
    monitor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("monitors.id"), nullable=False
    )
    timestampt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_up: Mapped[bool] = mapped_column(Boolean, default=True)
    latency_ms: Mapped[float | None] = mapped_column(nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # relationships
    monitor: Mapped["Monitor"] = relationship(
        "Monitor", back_populates="probes", lazy="selectin"
    )

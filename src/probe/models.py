from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, String, func, Boolean, Index
from src.db.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime, timezone


if TYPE_CHECKING:

    from src.monitor.models import Monitor


class Probe(Base):
    # single recorded ping event

    __tablename__ = "probes"

    __table_args__ = (Index("ix_probe_monitor_timestamp", "monitor_id", "timestamp"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    monitor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("monitors.id"), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    is_up: Mapped[bool] = mapped_column(Boolean, default=True)
    latency_ms: Mapped[float | None] = mapped_column(nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # relationships
    monitor: Mapped["Monitor"] = relationship(
        "Monitor", back_populates="probes", lazy="selectin"
    )

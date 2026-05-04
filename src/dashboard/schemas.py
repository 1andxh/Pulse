from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_monitors: int
    total_probes_recorded: int
    overall_uptime_percentage: float
    average_response_time: float

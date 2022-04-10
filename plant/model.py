from datetime import timedelta
from pydantic import BaseModel
from datetime import timedelta

class PumpSettings(BaseModel):
    pump_speed: float
    pump_time: float
    pump_repeat: int
    pump_delay: float
    
class MoistureSettings(BaseModel):
    channel: int
    active: bool
    dry_point: float
    wet_point: float

class WateringSettings(BaseModel):
    pump_channel: int
    pump_settings: PumpSettings
    moisture_setting: MoistureSettings
    water_interval: timedelta
    water_level: float
    warn_level: float
    auto_water: False

class Plant(BaseModel):
    name: str
    settings: WateringSettings
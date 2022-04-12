from datetime import timedelta
from pydantic import BaseModel, validator


class PumpSettings(BaseModel):
    speed = 0.4
    time= 1.0
    repeat = 1
    delay = 10.0
    
class MoistureSettings(BaseModel):
    channel: int
    active = False
    dry_point = 1.8
    wet_point = 0.9

    @validator('channel')
    def valid_channel(cls, v):
        if v < 1 or v > 3:
            raise ValueError("Moisture channel can only be 1, 2 or 3")
        return v


class WateringSettings(BaseModel):
    pump_channel: int
    pump_settings: PumpSettings
    moisture_setting: MoistureSettings
    water_interval = timedelta(seconds=10800)
    water_level = 1.7
    warn_level = 1.8
    auto_water = False

    @validator('pump_channel')
    def valid_channel(cls, v):
        if v < 1 or v > 3:
            raise ValueError("Pump channel can only be 1, 2 or 3")
        return v

class Plant(BaseModel):
    name: str
    watering_settings: WateringSettings
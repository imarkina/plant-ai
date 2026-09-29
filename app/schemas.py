from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Identification(BaseModel):
    commonName: str = Field(description="Название на русском языке, например: филодендрон розовая принцесса")
    botanicalName: str = Field(description="Латинское название, например: Philodendron 'Pink Princess'")
    confidencePercent: float = Field(description="Степень уверенности в %", ge=0, le=100)

class PlantHealthEnum(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

class ThreatLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Health(BaseModel):
    status: Optional[PlantHealthEnum] = None
    description: Optional[str] = None
    diagnosis: Optional[str] = None
    threatLevel: Optional[ThreatLevelEnum] = None
    pestsOrDiseasesFound: Optional[bool] = None

class ActionPlan(BaseModel):
    urgentActions: list[str] = Field(description='Шаги прямо сейчас (карантин, опора и т.д.)', default=[])
    prohibitions: list[str] = Field(description='Чего делать КАТЕГОРИЧЕСКИ нельзя', default=[])

class Identification(BaseModel):
    commonName: str = Field(description="Название на русском языке, например: филодендрон розовая принцесса")
    botanicalName: str = Field(description="Латинское название, например: Philodendron 'Pink Princess'")
    confidencePercent: float = Field(description="Степень уверенности в %", ge=0, le=100)

class Lighting(BaseModel):
   summary: str = Field(description='Краткое резюме (например: Яркий рассеянный свет)')
   details: str = Field(description='Детали и риски потери вариегатности')
   idealPlacement: str = Field(description='Идеальное расположение (окна, фитолампа)')

class SoilAndPot(BaseModel):
    soilMix: str = Field(description='Состав грунта')
    potType: str = Field(description='Требования к горшку')
    repottedWhen: str = Field(description='Когда нужна пересадка')

class Watering(BaseModel):
    frequency: str = Field(description='Правило полива (например: По мере просыхания на 1/2)')
    waterQuality: str = Field(description='Требования к воде')
    intervalDays: Optional[int] = Field(ge=1, le=60, default=None, description='Среднее количество дней между поливами')

class Fertilizing(BaseModel):
    schedule: str = Field(description='График подкормок')
    dosage: str = Field(description='Дозировка')
    warnings: str = Field(description='Ограничения (например: не перекармливать азотом)')
    intervalDays: Optional[int] = Field(default=None, ge=1, le=120, description='Среднее количество дней между подкормками')


class Environment(BaseModel):
    humidity: str = Field(description='Требования к влажности (например: 50-70%)')
    temperatureMinC: int = Field(description='Минимальная критическая температура')
    temperatureOptimal: str = Field(description='Оптимальный диапазон температур')
    notes: Optional[str] = Field(default=None, description='Примечания по сквознякам или опрыскиванию')
    mistingIntervalDays: Optional[int] = Field(default=None, ge=1, le=14, description='Как часто опрыскивать, в днях — указывать только если растению это нужно')

class CarePassport(BaseModel):
    lighting: Lighting
    watering: Watering
    environment: Environment
    soilAndPot: SoilAndPot
    fertilizing: Fertilizing

class PlantReport(BaseModel):
    identification: Identification
    health: Health
    actionPlan: ActionPlan
    carePassport: CarePassport


from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    category = Column(String(50), index=True)  # 系别
    image_url = Column(String(500))
    bloodline = Column(String(50))  # 血脉
    
    # 资质值 (JSON格式)
    stats = Column(JSON, default={
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "magic_attack": 0,
        "magic_defense": 0,
        "speed": 0
    })
    
    # 培养推荐 (JSON格式)
    recommended_nature = Column(JSON, default=[])  # 推荐性格
    recommended_talent = Column(JSON, default=[])  # 推荐天分
    recommended_skills = Column(JSON, default=[])  # 推荐技能
    
    # 捕获信息
    capture_location = Column(String(200))
    capture_condition = Column(String(200))
    capture_time = Column(String(100))
    
    # 进阶信息
    can_evolve = Column(Boolean, default=False)
    evolution_forms = Column(JSON, default=[])  # [{"id": 1, "name": "xxx", "condition": "xxx"}]
    
    # 异色
    has_albinism = Column(Boolean, default=False)
    albinism_image = Column(String(500))
    
    # 描述
    description = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "image_url": self.image_url,
            "bloodline": self.bloodline,
            "stats": self.stats or {},
            "recommended_nature": self.recommended_nature or [],
            "recommended_talent": self.recommended_talent or [],
            "recommended_skills": self.recommended_skills or [],
            "capture_location": self.capture_location,
            "capture_condition": self.capture_condition,
            "capture_time": self.capture_time,
            "can_evolve": self.can_evolve,
            "evolution_forms": self.evolution_forms or [],
            "has_albinism": self.has_albinism,
            "albinism_image": self.albinism_image,
            "description": self.description
        }

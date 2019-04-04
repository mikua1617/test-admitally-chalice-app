import json

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..db import base


class Reminder(base):
  __tablename__ = 'reminder'

  id = Column(Integer, primary_key=True)
  user_id = Column(UUID(as_uuid=True), nullable=False)
  appointment_id = Column(UUID(as_uuid=True))
  execution_time = Column(DateTime(timezone=True))
  status = Column(String)
  role = Column(String)
  template_key = Column(String)
  mail_data = Column(JSONB)
  sms_data = Column(JSONB)
  created = Column(DateTime(timezone=True), default=func.now())
  last_updated = Column(DateTime(timezone=True), onupdate=func.now())

  def __repr__(self):
    return json.dumps({
        "id": str(self.id),
        "user_id": str(self.user_id), 
        "execution_time":str(self.execution_time),
        "status": self.status,
        "role": self.role,
        "template_key": self.template_key,
        "mail_data": self.mail_data,
        "sms_data": self.sms_data,
        "appointment_id": str(self.appointment_id)
    })

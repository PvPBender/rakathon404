from db.tables.Base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum
import enum

class Gender(enum.Enum):
    male = 0
    female = 1
    other = 2


class Pacient(Base):
    __tablename__ = "pacient"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    year: Mapped[int]
    gender: Mapped[Gender] = mapped_column(Enum(Gender))


    def __repr__(self) -> str:
        return f"Pacient(ID={self.id!r}, year={self.year!r}, sex={self.gender!r})"

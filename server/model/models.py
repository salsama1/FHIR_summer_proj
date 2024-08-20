from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sql_con.connection import Base

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    gender = Column(String(10))
    date_of_birth = Column(Date)

    coverages = relationship("Coverage", back_populates="patient")

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    type = Column(String(50))

    coverages = relationship("Coverage", back_populates="insurer")
    insurer_networks = relationship("ProviderNetwork", foreign_keys="[ProviderNetwork.insurer_id]", back_populates="insurer")
    provider_networks = relationship("ProviderNetwork", foreign_keys="[ProviderNetwork.provider_id]", back_populates="provider")

class Coverage(Base):
    __tablename__ = 'coverages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    insurer_id = Column(Integer, ForeignKey('organizations.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50))

    patient = relationship("Patient", back_populates="coverages")
    insurer = relationship("Organization", back_populates="coverages")

class ProviderNetwork(Base):
    __tablename__ = 'provider_networks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    insurer_id = Column(Integer, ForeignKey('organizations.id'))
    provider_id = Column(Integer, ForeignKey('organizations.id'))

    insurer = relationship("Organization", foreign_keys=[insurer_id], back_populates="insurer_networks")
    provider = relationship("Organization", foreign_keys=[provider_id], back_populates="provider_networks")

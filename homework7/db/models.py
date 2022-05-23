from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Logs(Base):
    __tablename__ = "logs"
    __table_args__ = {"mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True)
    remote_addr = Column(Text, nullable=False)
    remote_user = Column(Text)
    time_local = Column(DateTime, nullable=False)
    request_method = Column(String(8), nullable=False)
    request_url = Column(Text, nullable=False)
    protocol = Column(String(8), nullable=False)
    status = Column(Integer, nullable=False)
    body_bytes_sent = Column(Integer)
    http_referer = Column(Text)
    http_user_agent = Column(Text)
    gzip_ratio = Column(Integer)


class RequestsCount(Base):
    __tablename__ = "requests_count"
    __table_args__ = {"mysql_charset": "utf8"}

    count = Column(Integer, primary_key=True)


class MethodsCount(Base):
    __tablename__ = "methods_count"
    __table_args__ = {"mysql_charset": "utf8"}

    method = Column(String(8), primary_key=True)
    count = Column(Integer)


class TopRequestsUrl(Base):
    __tablename__ = "top_requests_url"
    __table_args__ = {"mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    count = Column(Integer)


class TopRequestsSize4xx(Base):
    __tablename__ = "top_requests_size_4xx"
    __table_args__ = {"mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    status = Column(Integer)
    size = Column(Integer)
    ip = Column(Text)


class TopRequestsIp5xx(Base):
    __tablename__ = "top_requests_ip_5xx"
    __table_args__ = {"mysql_charset": "utf8"}

    ip = Column(String(50), primary_key=True)
    count = Column(Integer)

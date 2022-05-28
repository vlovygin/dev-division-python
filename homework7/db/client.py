from datetime import datetime
import re
from pathlib import Path
import pytz
import sqlalchemy
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

from db.models import Base, Logs, RequestsCount, MethodsCount, TopRequestsUrl, TopRequestsSize4xx, TopRequestsIp5xx

METHODS = ("GET", "POST", "PUT", "HEAD", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH")


class MysqlORMClient:

    def __init__(self, user, password, db_name, host='localhost', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)
        self.session = sm()

    def recreate_db(self):
        self.connect(db_created=False)

        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)

        self.connection.close()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)

    def parse_log(self, log_path: Path):
        """Parse access.log file and insert data at Logs table"""

        log_pattern = re.compile(
            r"(?P<remote_addr>(\d{1,3}\.){3}\d{1,3}) "
            r"(?P<remote_user>.*) - "
            r"\[(?P<time_local>\d{2}/[a-z]{3}/\d{4}(:\d{2}){3} (\+|-)\d{4})\] "
            r"((\"(?P<request_method>.+) )(?P<request_url>.+)(?P<protocol>http/\d{1}.\d{1})\") "
            r"(?P<status>\d{3}) "
            r"(?P<body_bytes_sent>.*) "
            r"(\"(?P<http_referer>.*)\") "
            r"(\"(?P<http_user_agent>.*)\") "
            r"(\"(?P<gzip_ratio>.*)\")", re.IGNORECASE)

        with open(log_path, "r") as f:
            for line in f.readlines():
                r = re.search(log_pattern, line)
                log_dict: dict = r.groupdict()

                log_dict["time_local"] = datetime.strptime(log_dict["time_local"], '%d/%b/%Y:%H:%M:%S %z').astimezone(
                    pytz.utc)

                # Parse only real http methods, not trash
                if log_dict["request_method"] not in METHODS:
                    continue

                if not log_dict["body_bytes_sent"].isdigit():
                    log_dict["body_bytes_sent"] = None

                if not log_dict["gzip_ratio"].isdigit():
                    log_dict["gzip_ratio"] = None

                if not log_dict["status"].isdigit():
                    log_dict["status"] = None

                if log_dict["remote_user"] == "-":
                    log_dict["remote_user"] = None

                if log_dict["http_referer"] == "-":
                    log_dict["http_referer"] = None

                if log_dict["http_user_agent"] == "-":
                    log_dict["http_user_agent"] = None

                if log_dict["gzip_ratio"] == "-":
                    log_dict["gzip_ratio"] = None

                log = Logs(**log_dict)
                self.session.add(log)

            self.session.commit()

    def prepare_db(self):
        """Fill table data"""

        # Add responses count information to Requests table
        total_rows = self.session.query(Logs).count()
        self.session.add(RequestsCount(count=total_rows))

        # Add methods count information to Requests table
        method_counts = (self.session.query(Logs.request_method.label("method"),
                                            func.count(Logs.request_method).label("count"))
                         .group_by(Logs.request_method).all())
        for row in method_counts:
            self.session.add(MethodsCount(method=row.method, count=row.count))

        # Add top requests url information to TopRequestUrl table
        top_requests_url = (self.session.query(Logs.request_url.label("url"),
                                               func.count(Logs.request_url).label("count"))
                            .group_by(Logs.request_url)
                            .order_by(desc("count"))
                            .limit(10)
                            .all())
        for row in top_requests_url:
            self.session.add(TopRequestsUrl(url=row.url, count=row.count))

        # Add top byte size requests with client error information to TopSendBytes4xx table
        top_requests_size_4xx = (self.session.query(Logs.request_url.label("url"),
                                                    Logs.status.label("status"),
                                                    Logs.body_bytes_sent.label("size"),
                                                    Logs.remote_addr.label("ip"))
                                 .filter(Logs.status.between(400, 499))
                                 .order_by(desc("size"))
                                 .limit(5)
                                 .all())
        for row in top_requests_size_4xx:
            self.session.add(TopRequestsSize4xx(url=row.url, status=row.status, size=row.size, ip=row.ip))

        # Add top IP with server error information to TopRequestsIp5xx table
        top_requests_ip_5xx = (self.session.query(Logs.remote_addr.label("ip"),
                                                  func.count(Logs.remote_addr).label("count"))
                               .filter(Logs.status.between(500, 599))
                               .group_by(Logs.remote_addr)
                               .order_by(desc("count"))
                               .limit(5)
                               .all())
        for row in top_requests_ip_5xx:
            self.session.add(TopRequestsIp5xx(ip=row.ip, count=row.count))

        self.session.commit()

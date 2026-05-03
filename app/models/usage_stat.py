from datetime import date
from app import db


class DailyStat(db.Model):
    __tablename__ = 'daily_stats'

    date = db.Column(db.Date, primary_key=True, default=date.today)
    word_to_pdf_count = db.Column(db.Integer, default=0)
    pdf_to_word_count = db.Column(db.Integer, default=0)
    image_conversion_count = db.Column(db.Integer, default=0)
    total_bytes_processed = db.Column(db.BigInteger, default=0)
    avg_conversion_ms = db.Column(db.Integer, default=0)
    failure_count = db.Column(db.Integer, default=0)

    @classmethod
    def get_or_create_today(cls):
        today = date.today()
        stat = cls.query.get(today)
        if not stat:
            stat = cls(date=today)
            db.session.add(stat)
            db.session.commit()
        return stat

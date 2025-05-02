from sqlalchemy.orm import Session
from report.models.report import Report

def create_report(db: Session, user_id: int, image_path: str, description: str):
    report = Report(
        user_id=user_id,
        image_path=image_path,
        description=description,
        status="Menunggu"
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_reports_by_user(db: Session, user_id: int):
    return db.query(Report).filter(Report.user_id == user_id).all()
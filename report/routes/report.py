# from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# from sqlalchemy.orm import Session
# import shutil
# import os
# from auth.models.user import User
# from report.schemas.report import ReportCreate, ReportResponse
# from report.crud.report import create_report, get_reports_by_user
# from auth.database import get_db
# from auth.dependencies import get_current_user

# router = APIRouter(prefix="/api/report", tags=["report"])

# UPLOAD_DIR = "uploads/reports"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/", response_model=ReportResponse)
# def submit_report(
#     description: str = Form(...),
#     image: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     try:
#         file_path = os.path.join(UPLOAD_DIR, image.filename)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)

#         report = create_report(
#             db=db,
#             user_id=current_user.id,
#             image_path=file_path,
#             description=description
#         )
#         return report

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Gagal upload laporan: {str(e)}")


# @router.get("/my", response_model=list[ReportResponse])
# def list_my_reports(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return get_reports_by_user(db, current_user.id)
from fastapi import FastAPI
from auth.routers.auth import router as auth_router
from auth.database import init_db as init_auth_db
# from users.routes import router as users_router
from chatbot.chat import chat_router
# from cctv.main import cctv_router
# from cctv.main_video import cctv_video_router
# from routers import park
from park.database import init_db as init_park_db
from fastapi.middleware.cors import CORSMiddleware
from weather.routers import weather
# from report.routes import report

init_auth_db()
init_park_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua domain
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode (GET, POST, OPTIONS, dll.)
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(weather.router)
app.include_router(auth_router)
# app.include_router(report.router)
# app.include_router(users_router)
app.include_router(chat_router)
# app.include_router(cctv_router)
# app.include_router(cctv_video_router)
# app.include_router(park.router)
# @app.on_event("startup")
# async def startup_event():
#     from park.utils import fetch_parks_data, parse_park_element
#     from park.crud.park import ParkCRUD
#     from park.database import SessionLocal
#     import traceback
    
#     print("Memulai sinkronisasi data taman...")
    
#     try:
#         elements = fetch_parks_data()
#         print(f"Berhasil mengambil {len(elements)} data taman")
        
#         db = SessionLocal()
#         try:
#             count = 0
#             for element in elements:
#                 try:
#                     park_data = parse_park_element(element)
#                     ParkCRUD.create_or_update_park(db, park_data)
#                     count += 1
#                     if count % 100 == 0:  
#                         db.commit()
#                 except Exception as e:
#                     print(f"Error memproses element {element.get('id')}: {str(e)}")
#                     db.rollback()
#             db.commit()
#             print(f"Berhasil menyimpan {count} taman")
#         except Exception as e:
#             print(f"Database error: {traceback.format_exc()}")
#             db.rollback()
#         finally:
#             db.close()
#     except Exception as e:
#         print(f"Error utama: {traceback.format_exc()}")
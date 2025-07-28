from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.index import api_router
from app.core.config import settings


# def verify_api_key(request: Request):
#     api_key = request.headers.get("x-api-key")
#     if api_key != settings.API_KEY:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
#         )


app = FastAPI(
    title="Alibaba Energy Expert API",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(api_router, dependencies=[Depends(verify_api_key)])
app.include_router(api_router)


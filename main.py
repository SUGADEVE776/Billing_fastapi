from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(
    title="DevLedger",
    docs_url="/docs",
    redoc_url=None,
    description="Our Application provides Invoicing an History"
)


@app.get("/check")
def healthcheck():
    return JSONResponse({"message" : "Healthy"})
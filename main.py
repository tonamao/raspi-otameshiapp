from fastapi import FastAPI
import RPi.GPIO as GPIO
from fastapi.responses import JSONResponse

app = FastAPI()
LED_PIN = 25

# アプリケーション起動時の初期設定
@app.on_event("startup")
async def startup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

# アプリケーション終了時のクリーンアップ
@app.on_event("shutdown")
async def shutdown():
    GPIO.cleanup()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/power/{times}/{interval}")
async def power_custom(times: int, interval: float):
    try:
        for _ in range(times):
            GPIO.output(LED_PIN, GPIO.HIGH)
            await asyncio.sleep(interval)
            GPIO.output(LED_PIN, GPIO.LOW)
            await asyncio.sleep(interval)
        return JSONResponse(content={"message": f"LED blinked {times} times"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
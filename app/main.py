"""hello —— DevOps 課的範例 FastAPI app。

一路用到：pytest（單元測試）、GitHub Actions（CI）、Docker、K8S、ArgoCD。
"""
import os

from fastapi import FastAPI

from app.login import router as login_router

# 預設 v3.0；blue-green / canary demo 時，用環境變數 APP_VERSION 覆蓋，
# 讓同一顆 image 跑出不同的版本字串，curl 一眼就看出流量打到哪個版本。
VERSION = os.getenv("APP_VERSION", "v3.0")

app = FastAPI(title="hello")
app.include_router(login_router)


@app.get("/")
def root():
    # version 字串之後做 blue-green / canary、確認新版上線時會用到
    return {"service": "hello", "version": VERSION}


@app.get("/health")
def health():
    # 給 K8S liveness/readiness、Docker healthcheck 用
    return {"status": "ok"}

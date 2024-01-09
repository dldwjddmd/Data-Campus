#!/bin/bash

uvicorn  --app-dir exposure --reload --host 0.0.0.0 --port 8000 main:app
from pathlib import Path

modelStoreConfig = {
    "paths": {
        "logs": Path(__file__).parent / 'logs',
    },
    "weights": {
        "best": Path(__file__).parent / 'weights' / 'best.pt',
    },
    "data": Path(__file__).parent.parent / 'YOLOv5n' / 'data' / 'custom_data.yaml',
}

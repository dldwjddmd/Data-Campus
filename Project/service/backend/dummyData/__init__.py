from pathlib import Path

dummyStoreConfig = {
    "paths": {
        "Object": Path(__file__).parent / "Object.json",
        "Image": Path(__file__).parent / "Image.json",
        "Video": Path(__file__).parent / "Video.json",
        "Log": Path(__file__).parent / "Log.json",
        "Frame": Path(__file__).parent / "Frame.json",
    }
}


# Main Photo Organizer Agent

Organizes 3K+ RAW photos by date, analyzes batches, routes to specialized sub-agents.

## Config
```python
SOURCE_DIR = "/path/to/raw/photos"        # UPDATE
ORGANIZED_DIR = "/path/organized"         # UPDATE  
SELECTED_DIR = "/path/best"              # UPDATE
TIME_CLUSTER = 30  # minutes
```

## Logic
- EXIF date → `YYYY/MM/` folders
- Focal length: 14-35mm→Landscape, 50-85mm→Portrait, 85mm+→Event
- Faces: 0→Landscape/Street, 1→Portrait, 2+→Event
- Burst→Event, Spread→Lifestyle
import os
import shutil
import random
import pandas as pd
from pathlib import Path

# ------------------
# CONFIG
# ------------------
INPUT_DIR = "glass_break_extended_dataset"
OUTPUT_AUDIO_DIR = "audio_extended"
OUTPUT_META_DIR = "meta_extended"
CSV_NAME = "esc50_extended.csv"

CLASSES = {
    "background": 0,
    "glass_break": 1
}

NUM_FOLDS = 5
random.seed(42)

# ------------------
# CREATE DIRS
# ------------------
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_META_DIR, exist_ok=True)

rows = []
clip_id = 0

# ------------------
# PROCESS FILES
# ------------------
for class_name, target in CLASSES.items():
    class_dir = Path(INPUT_DIR) / class_name
    files = list(class_dir.glob("*.wav"))

    random.shuffle(files)

    for i, wav_path in enumerate(files):
        fold = (i % NUM_FOLDS) + 1
        take = "A"
        clip_id += 1

        new_filename = f"{fold}-{clip_id:06d}-{take}-{target}.wav"
        dst_path = Path(OUTPUT_AUDIO_DIR) / new_filename

        shutil.copy(wav_path, dst_path)

        rows.append({
            "filename": new_filename,
            "fold": fold,
            "target": target,
            "category": class_name,
            "esc10": False,
            "src_file": wav_path.name,
            "take": take
        })

# ------------------
# SAVE CSV
# ------------------
df = pd.DataFrame(rows)
df.to_csv(Path(OUTPUT_META_DIR) / CSV_NAME, index=False)

print(" Dataset organized successfully!")
print(df.head())

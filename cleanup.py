#!/usr/bin/env python3
import os
import glob

# Find and delete all .db files
db_files = glob.glob("**/*.db", recursive=True)
for db_file in db_files:
    try:
        os.remove(db_file)
        print(f"Deleted: {db_file}")
    except Exception as e:
        print(f"Failed to delete {db_file}: {e}")

print("Cleanup complete")

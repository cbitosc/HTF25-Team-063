import streamlit
print("Streamlit version:", streamlit.__version__)

import pandas
print("Pandas version:", pandas.__version__)

from PIL import Image
print("PIL imported successfully")

import glob
print("Glob imported successfully")

try:
    import dashboard
    print("Dashboard module imported successfully")
except Exception as e:
    print(f"Dashboard import failed: {e}")

#!/bin/bash

set -eou pipefail

# Give services time to start
sleep 10

python3 schema.py

python3 base64_convert.py

python3 upload_img.py

streamlit run streamlit_app.py
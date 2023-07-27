#!/bin/bash

set -eou pipefail

# Give services time to start
sleep 5

python schema.py

python base64_convert.py

python upload_img.py

streamlit run streamlit_app.py
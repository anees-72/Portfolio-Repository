#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Copy files to Vercel's output directory
cp -r public/ /vercel/output/
cp -r project4/ /vercel/output/
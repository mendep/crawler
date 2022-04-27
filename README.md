This image crawler downloads .png images from a URL into an output directory.
It also supports BasicAuth with username and password.

# Install
```pip3 install -r requirements.txt```

# Comamnd-line Arguments
1) Required:
- -u URL, --url URL     URL as source of images
- -o OUTPUT_DIR, --output_dir OUTPUT_DIR     Output directory for downloaded images
2) Optional:
- -n USERNAME, --username USERNAME     Username for BasicAuth
- -p PASSWORD, --password PASSWORD     Password for BasicAuth

# Usage
```python3 crawler.py -h```

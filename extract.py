import zipfile, pandas as pd, io, requests

def read_csv_from_zip(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Python script)"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed to download {url}: HTTP {resp.status_code}")
    content_type = resp.headers.get('Content-Type', '')
    if 'zip' not in content_type:
        raise Exception(f"URL did not return a zip file: {content_type}")
    zbytes = io.BytesIO(resp.content)
    try:
        with zipfile.ZipFile(zbytes) as zf:
            # pick the first CSV in the zip
            csv_name = [n for n in zf.namelist() if n.lower().endswith('.csv')][0]
            with zf.open(csv_name) as f:
                df = pd.read_csv(f, low_memory=False)
        return df
    except zipfile.BadZipFile:
        raise Exception(f"Downloaded file is not a valid zip file from {url}")

wbresp = read_csv_from_zip("https://www.bls.gov/tus/datafiles/wbresp-2021.zip")
wbact  = read_csv_from_zip("https://www.bls.gov/tus/datafiles/wbact-2021.zip")

len(wbresp), len(wbact)

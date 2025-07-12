import httpx

async def fetch_flood_data():
    url = "https://poskobanjir.dsdadki.web.id/datatmalaststatus.json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            filtered = [
                {
                    "NAMA_PINTU_AIR": item["NAMA_PINTU_AIR"],
                    "LATITUDE": item["LATITUDE"],
                    "LONGITUDE": item["LONGITUDE"],
                    "RECORD_STATUS": item["RECORD_STATUS"],
                    "TINGGI_AIR": item["TINGGI_AIR"],
                    "TINGGI_AIR_SEBELUMNYA": item["TINGGI_AIR_SEBELUMNYA"],
                    "TANGGAL": item["TANGGAL"],
                    "STATUS_SIAGA": item["STATUS_SIAGA"]
                }
                for item in data
            ]
            return filtered
    except Exception as e:
        raise RuntimeError(f"Gagal mengambil data banjir: {e}")

import json
import traceback
import requests
from typing import Dict, Any, List

HERE_API_KEY = "LJ4nJnBbpAPWeqQfRmDhdb1-QzqCchjQV7mlgCBT700"

def fetch_parks_data() -> List[Dict[str, Any]]:

    try:
        overpass_url = "https://overpass.kumi.systems/api/interpreter"

        query = """
        [out:json][timeout:30];
        (
            node["leisure"~"park|garden"](-6.6146,106.1585,-6.0515,107.1191);
            way["leisure"~"park|garden"](-6.6146,106.1585,-6.0515,107.1191);
            relation["leisure"~"park|garden"](-6.6146,106.1585,-6.0515,107.1191);
        );
        out center;
        >;
        out skel qt;
        """

        response = requests.post(
            overpass_url,
            data=query,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Encoding': 'gzip'
            },
            timeout=(3.05, 45)
        )

        if response.status_code != 200:
            print(f"Response error: {response.status_code}")
            print(f"Response text: {response.text[:200]}...")
            return []

        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Invalid JSON response")
            print(f"Raw response (first 200 chars): {response.text[:200]}...")
            return []

        if 'elements' not in data:
            print("Invalid API response structure")
            print(f"Sample response: {json.dumps(data, indent=2)[:200]}...")
            return []

        elements = data['elements']
        print(f"Received {len(elements)} raw elements from API")

        valid_elements = [
            e for e in elements
            if isinstance(e.get('tags'), dict) and
            e.get('tags', {}).get('leisure') in ['park', 'garden'] and
            (e.get('lat') or e.get('center')) and
            e.get('tags', {}).get('name') 
        ]

        print(f"Found {len(valid_elements)} valid park elements")

        if not valid_elements:
            print("\nWARNING: No valid park elements found")
            print("Possible reasons:")
            print("- Query area out of bounds")
            print("- Missing 'leisure' tag in OSM data")
            print("- Server overload, try again later")
            print(f"\nQuery used:\n{query}")

        return valid_elements

    except requests.exceptions.Timeout:
        print("Error: Request timeout (45 seconds)")
        return []
    except requests.exceptions.TooManyRedirects:
        print("Error: Too many redirects")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")
        print(f"Error details: {traceback.format_exc()}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return []
    
def parse_park_element(element: Dict[str, Any]) -> Dict[str, Any]:
    try:
        tags = element.get('tags', {})
        name = tags.get('name')
        if not name:
            print(f"Skipping element {element.get('id')} karena tidak ada nama")
            return {}

        lat = element.get('lat') or element.get('center', {}).get('lat')
        lon = element.get('lon') or element.get('center', {}).get('lon')
        if not lat or not lon:
            print(f"Skipping element {element.get('id')} karena tidak ada koordinat")
            return {}

        # ambil dari OSM tags
        street = tags.get('addr:street')
        subdistrict = tags.get('addr:subdistrict')
        district = tags.get('addr:district')
        postcode = tags.get('addr:postcode')

        # klo kosong, pakai HERE API
        if not (street and subdistrict and district and postcode):
            address = get_address(lat, lon)
            street = street or address.get('street')
            subdistrict = subdistrict or address.get('subdistrict')
            district = district or address.get('district')
            postcode = postcode or address.get('postcode')

        # fallback manual
        if not district:
            district = "Jakarta"
        if not subdistrict:
            subdistrict = "Tidak diketahui"

        facilities = parse_facilities(tags)

        return {
            'osm_id': element['id'],
            'name': name,
            'lat': round(float(lat), 6),
            'lon': round(float(lon), 6),
            'address': {
                'street': street or 'Tidak diketahui',
                'subdistrict': subdistrict,
                'district': district,
                'postcode': postcode or 'Tidak diketahui'
            },
            'facilities': facilities,
            'osm_type': element.get('type', 'node')
        }
    except Exception as e:
        print(f"Error parsing element {element.get('id')}: {e}")
        return {}

    
def parse_facilities(tags: Dict[str, Any]) -> list[str]:
    facilities_map = {
        'playground': 'Taman Bermain',
        'fitness_station': 'Peralatan Fitness',
        'toilets': 'Toilet Umum',
        'bench': 'Bangku',
        'picnic_table': 'Meja Picnic',
        'bbq': 'Area BBQ',
        'sport': 'Area Olahraga',
        'lighting': 'Penerangan',
        'parking': 'Parkir',
        'drinking_water': 'Air Minum'
    }
    
    facilities = []
    for tag, name in facilities_map.items():
        if tags.get(tag) == 'yes':
            facilities.append(name)

    if tags.get('sport'):
        facilities.append(f"Lapangan {tags['sport'].title()}")
    
    return sorted(facilities)

def get_address(lat, lon):
    try:
        url = f"https://revgeocode.search.hereapi.com/v1/revgeocode?at={lat},{lon}&lang=id-ID&apikey={HERE_API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            if items:
                address = items[0].get('address', {})
                return {
                    'street': address.get('street'),
                    'subdistrict': address.get('district'),
                    'district': address.get('city') or address.get('county'),
                    'postcode': address.get('postalCode'),
                    'city': address.get('city')
                }
        else:
            print(f"Here API error: {response.status_code} {response.text[:100]}...")
    except Exception as e:
        print(f"Reverse geocode error: {e}")
    return {}

def parse_all_parks(osm_data):
    parks = []
    for element in osm_data.get('elements', []):
        park = parse_park_element(element)
        if park:
            parks.append(park)
    return parks

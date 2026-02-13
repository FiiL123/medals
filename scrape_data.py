#!/usr/bin/env python3
"""
Data scraper for International Olympiad medal counts.
Scrapes IMO (Math), IOI (Informatics), and IPhO (Physics) data.
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Any
from datetime import datetime

# User agent for web scraping
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Historical countries to exclude
HISTORICAL_COUNTRIES = {
    "Soviet Union",
    "Yugoslavia",
    "East Germany",
    "Czechoslovakia",
    "German Democratic Republic",
    "Socialist Federal Republic of Yugoslavia",
    "Commonwealth of Independent States",
    "Serbia and Montenegro",
    "CIS",
    "Union of Soviet Socialist Republics",
    "Czechoslovakia",
}

# Country name to ISO 3166-1 alpha-3 code mapping
COUNTRY_CODE_MAP = {
    "United States": "USA",
    "United States of America": "USA",
    "China": "CHN",
    "People's Republic of China": "CHN",
    "Russia": "RUS",
    "South Korea": "KOR",
    "Republic of Korea": "KOR",
    "Hungary": "HUN",
    "Romania": "ROU",
    "Vietnam": "VNM",
    "United Kingdom": "GBR",
    "Bulgaria": "BGR",
    "Germany": "DEU",
    "Iran": "IRN",
    "Islamic Republic of Iran": "IRN",
    "Japan": "JPN",
    "Taiwan": "TWN",
    "Ukraine": "UKR",
    "Canada": "CAN",
    "Poland": "POL",
    "Thailand": "THA",
    "Australia": "AUS",
    "Singapore": "SGP",
    "France": "FRA",
    "Israel": "ISR",
    "Turkey": "TUR",
    "Türkiye": "TUR",
    "Italy": "ITA",
    "India": "IND",
    "North Korea": "PRK",
    "Democratic People's Republic of Korea": "PRK",
    "Belarus": "BLR",
    "Kazakhstan": "KAZ",
    "Hong Kong": "HKG",
    "Serbia": "SRB",
    "Brazil": "BRA",
    "Austria": "AUT",
    "Netherlands": "NLD",
    "Mongolia": "MNG",
    "Peru": "PER",
    "Slovakia": "SVK",
    "Czech Republic": "CZE",
    "Sweden": "SWE",
    "Mexico": "MEX",
    "Croatia": "HRV",
    "Indonesia": "IDN",
    "Argentina": "ARG",
    "Georgia": "GEO",
    "Malaysia": "MYS",
    "Greece": "GRC",
    "Moldova": "MDA",
    "Philippines": "PHL",
    "Switzerland": "CHE",
    "Bosnia and Herzegovina": "BIH",
    "Norway": "NOR",
    "North Macedonia": "MKD",
    "Portugal": "PRT",
    "Belgium": "BEL",
    "New Zealand": "NZL",
    "Lithuania": "LTU",
    "Macau": "MAC",
    "Luxembourg": "LUX",
    "Armenia": "ARM",
    "Colombia": "COL",
    "South Africa": "ZAF",
    "Finland": "FIN",
    "Latvia": "LVA",
    "Slovenia": "SVN",
    "Bangladesh": "BGD",
    "Cuba": "CUB",
    "Denmark": "DNK",
    "Tunisia": "TUN",
    "Kyrgyzstan": "KGZ",
    "Algeria": "DZA",
    "Uzbekistan": "UZB",
    "Saudi Arabia": "SAU",
    "Estonia": "EST",
    "Spain": "ESP",
    "Azerbaijan": "AZE",
    "Turkmenistan": "TKM",
    "Cyprus": "CYP",
    "Tajikistan": "TJK",
    "Syria": "SYR",
    "Morocco": "MAR",
    "Ireland": "IRL",
    "Chile": "CHL",
    "Montenegro": "MNE",
    "Albania": "ALB",
    "Pakistan": "PAK",
    "Trinidad and Tobago": "TTO",
    "Venezuela": "VEN",
    "Costa Rica": "CRI",
    "Iceland": "ISL",
    "Paraguay": "PRY",
    "El Salvador": "SLV",
    "Liechtenstein": "LIE",
    "Ivory Coast": "CIV",
    "Sri Lanka": "LKA",
    "Ecuador": "ECU",
    "Afghanistan": "AFG",
    "Albania": "ALB",
    "Bahrain": "BHR",
    "Benin": "BEN",
    "Bolivia": "BOL",
    "Botswana": "BWA",
    "Brunei": "BRN",
    "Burkina Faso": "BFA",
    "Cambodia": "KHM",
    "Egypt": "EGY",
    "Gambia": "GMB",
    "Ghana": "GHA",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "Iraq": "IRQ",
    "Kenya": "LKA",
    "Kosovo": "KSV",
    "Kuwait": "KWT",
    "Madagascar": "MDG",
    "Mauritania": "MRT",
    "Mozambique": "MOZ",
    "Myanmar": "MMR",
    "Nepal": "NPL",
    "Nicaragua": "NIC",
    "Nigeria": "NGA",
    "Panama": "PAN",
    "Puerto Rico": "PRI",
    "Qatar": "QAT",
    "Senegal": "SEN",
    "Suriname": "SUR",
    "Tanzania": "TZA",
    "Uganda": "UGA",
    "United Arab Emirates": "ARE",
    "Uruguay": "URY",
    "Zimbabwe": "ZWE",
    "Jordan": "JOR",
    "Malta": "MLT",
    "Palestine": "PSE",
    "Dominican Republic": "DOM",
    "Gabon": "GAB",
    "Libya": "LBY",
    "Mauritius": "MUS",
    "Rwanda": "RWA",
}


def parse_imo_data() -> Dict[str, Dict[str, int]]:
    """
    Parse IMO medal data from Wikipedia.
    Returns dict: {country_name: {gold, silver, bronze}}
    """
    print("Fetching IMO data from Wikipedia...")
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_medal_count_at_International_Mathematical_Olympiad"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the medal table (first wikitable after the intro)
    table = soup.find("table", class_="wikitable")
    if not table:
        print("ERROR: Could not find IMO table")
        return {}

    data = {}
    rows = table.find_all("tr")

    for row in rows[1:]:  # Skip header row
        cells = row.find_all(["td", "th"])
        if len(cells) < 6:
            continue

        # Extract country name (second cell contains flag span + link)
        country_cell = cells[1]
        links = country_cell.find_all("a")
        if links:
            # Filter out footnote links (single char, no title, or title doesn't match)
            country_name = ""
            for link in links:
                text = link.get_text(strip=True)
                title = link.get("title", "")
                # Skip footnote links: single char, no title, or title mismatch
                if text and len(text) > 1 and (text == title or not title):
                    country_name = text
        else:
            country_name = country_cell.get_text(strip=True)

        # Skip if country name is invalid (too short, likely a footnote)
        if len(country_name) <= 2:
            continue

        # Check for historical countries in the cell content (not just extracted name)
        cell_text = country_cell.get_text(strip=True)
        is_historical = False
        for historical in HISTORICAL_COUNTRIES:
            if historical.lower() in cell_text.lower():
                country_name = historical  # Use proper historical name
                is_historical = True
                break

        # Skip historical countries
        if is_historical and country_name in HISTORICAL_COUNTRIES:
            continue

        try:
            gold = int(cells[2].get_text(strip=True))
            silver = int(cells[3].get_text(strip=True))
            bronze = int(cells[4].get_text(strip=True))
            total = gold + silver + bronze

            data[country_name] = {
                "gold": gold,
                "silver": silver,
                "bronze": bronze,
                "total": total,
            }
        except (ValueError, IndexError):
            continue

    print(f"Parsed {len(data)} countries from IMO")
    return data


def parse_ioi_data() -> Dict[str, Dict[str, int]]:
    """
    Parse IOI medal data from stats.ioinformatics.org.
    Returns dict: {country_name: {gold, silver, bronze}}
    """
    print("Fetching IOI data from stats.ioinformatics.org...")
    url = "https://stats.ioinformatics.org/countries/?sort=medals_desc"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table
    table = soup.find("table")
    if not table:
        print("ERROR: Could not find IOI table")
        return {}

    data = {}
    rows = table.find_all("tr")

    for row in rows[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        # Country name is in second cell (first is empty)
        country_link = cells[1].find("a")
        if country_link:
            country_name = country_link.get_text(strip=True)
        else:
            country_name = cells[1].get_text(strip=True)

        # Skip historical countries
        if country_name in HISTORICAL_COUNTRIES:
            continue

        try:
            # Columns: (empty), Country, IOI Host, Gold, Silver, Bronze, Total
            gold = int(cells[3].get_text(strip=True))
            silver = int(cells[4].get_text(strip=True))
            bronze = int(cells[5].get_text(strip=True))
            total = gold + silver + bronze

            data[country_name] = {
                "gold": gold,
                "silver": silver,
                "bronze": bronze,
                "total": total,
            }
        except (ValueError, IndexError):
            continue

    print(f"Parsed {len(data)} countries from IOI")
    return data


def parse_ipho_data() -> Dict[str, Dict[str, int]]:
    """
    Parse IPhO medal data from ipho-unofficial.org.
    Returns dict: {country_name: {gold, silver, bronze}}
    """
    print("Fetching IPhO data from ipho-unofficial.org...")
    url = "http://ipho-unofficial.org/countries/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table
    table = soup.find("table")
    if not table:
        print("ERROR: Could not find IPhO table")
        return {}

    data = {}
    rows = table.find_all("tr")

    for row in rows[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        # Country name is in second cell (first is code)
        country_link = cells[1].find("a")
        if country_link:
            country_name = country_link.get_text(strip=True)
        else:
            country_name = cells[1].get_text(strip=True)

        # Skip historical countries
        if country_name in HISTORICAL_COUNTRIES:
            continue

        try:
            # Columns: Code, Country, Site, Host, Gold, Silver, Bronze, HM
            gold = int(cells[4].get_text(strip=True))
            silver = int(cells[5].get_text(strip=True))
            bronze = int(cells[6].get_text(strip=True))
            total = gold + silver + bronze

            data[country_name] = {
                "gold": gold,
                "silver": silver,
                "bronze": bronze,
                "total": total,
            }
        except (ValueError, IndexError):
            continue

    print(f"Parsed {len(data)} countries from IPhO")
    return data


def normalize_country_names(data_dict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Normalize country names to standard ISO codes.
    Returns dict with country codes as keys.
    """
    normalized = {}

    for country_name, medals in data_dict.items():
        # Try exact match
        code = COUNTRY_CODE_MAP.get(country_name)

        # Try partial match (e.g., "United Kingdom" should match)
        if not code:
            for name, iso_code in COUNTRY_CODE_MAP.items():
                if (
                    name.lower() in country_name.lower()
                    or country_name.lower() in name.lower()
                ):
                    code = iso_code
                    break

        # If still no match, use the name as-is (for manual review)
        if not code:
            print(f"Warning: No ISO code found for '{country_name}'")
            code = country_name[:3].upper()

        # If this code already exists, prefer the shorter/cleaner name
        if code in normalized:
            existing_name = normalized[code]["name"]
            # Prefer shorter name (e.g., "China" over "Macao, China")
            if len(country_name) >= len(existing_name):
                # Keep the existing (shorter) entry
                continue

        normalized[code] = {"name": country_name, "medals": medals}

    return normalized


def aggregate_data(
    imo_data: Dict, ioi_data: Dict, ipho_data: Dict
) -> List[Dict[str, Any]]:
    """
    Aggregate data from all three Olympiads into a single list.
    """
    # Normalize all data
    imo_normalized = normalize_country_names(imo_data)
    ioi_normalized = normalize_country_names(ioi_data)
    ipho_normalized = normalize_country_names(ipho_data)

    # Get all unique country codes
    all_codes = (
        set(imo_normalized.keys())
        | set(ioi_normalized.keys())
        | set(ipho_normalized.keys())
    )

    result = []

    for code in all_codes:
        imo_info = imo_normalized.get(code, {})
        ioi_info = ioi_normalized.get(code, {})
        ipho_info = ipho_normalized.get(code, {})

        # Use the first available country name
        country_name = (
            imo_info.get("name") or ioi_info.get("name") or ipho_info.get("name")
        )

        imo_medals = imo_info.get(
            "medals", {"gold": 0, "silver": 0, "bronze": 0, "total": 0}
        )
        ioi_medals = ioi_info.get(
            "medals", {"gold": 0, "silver": 0, "bronze": 0, "total": 0}
        )
        ipho_medals = ipho_info.get(
            "medals", {"gold": 0, "silver": 0, "bronze": 0, "total": 0}
        )

        combined_total = (
            imo_medals["total"] + ioi_medals["total"] + ipho_medals["total"]
        )
        combined_gold = imo_medals["gold"] + ioi_medals["gold"] + ipho_medals["gold"]
        combined_silver = (
            imo_medals["silver"] + ioi_medals["silver"] + ipho_medals["silver"]
        )
        combined_bronze = (
            imo_medals["bronze"] + ioi_medals["bronze"] + ipho_medals["bronze"]
        )

        result.append(
            {
                "code": code,
                "name": country_name,
                "medals": {
                    "IMO": imo_medals,
                    "IOI": ioi_medals,
                    "IPhO": ipho_medals,
                    "combined": {
                        "gold": combined_gold,
                        "silver": combined_silver,
                        "bronze": combined_bronze,
                        "total": combined_total,
                    },
                },
            }
        )

    # Sort by total medals (descending)
    result.sort(key=lambda x: x["medals"]["combined"]["total"], reverse=True)

    return result


def main():
    """
    Main function to scrape all data and generate medals.json.
    """
    print("=" * 60)
    print("Olympiad Medal Data Scraper")
    print("=" * 60)
    print()

    # Scrape data from all sources
    imo_data = parse_imo_data()
    ioi_data = parse_ioi_data()
    ipho_data = parse_ipho_data()

    print()
    print("Aggregating data...")

    # Aggregate data
    aggregated = aggregate_data(imo_data, ioi_data, ipho_data)

    # Create final JSON structure
    output = {
        "countries": aggregated,
        "metadata": {
            "imo_years": "1959-2025",
            "ioi_years": "1989-2025",
            "ipho_years": "1967-2025",
            "generated": datetime.now().isoformat(),
        },
    }

    # Write to JSON file
    output_file = "medals.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Data successfully written to {output_file}")
    print(f"Total countries: {len(aggregated)}")
    print()

    # Print top 10 countries
    print("Top 10 countries by total medals:")
    print("-" * 60)
    for i, country in enumerate(aggregated[:10], 1):
        print(
            f"{i:2}. {country['name']:30} {country['medals']['combined']['total']:4} total"
        )

    print()
    print("Done!")


if __name__ == "__main__":
    main()

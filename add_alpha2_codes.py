#!/usr/bin/env python3
"""
Add ISO alpha-2 codes to medals.json for correct flag emoji display.
"""

import json

# ISO 3166-1 alpha-3 to alpha-2 mapping
ALPHA3_TO_ALPHA2 = {
    "AFG": "AF",  # Afghanistan
    "ALB": "AL",  # Albania
    "ARE": "AE",  # United Arab Emirates
    "ARG": "AR",  # Argentina
    "ARM": "AM",  # Armenia
    "AUS": "AU",  # Australia
    "AUT": "AT",  # Austria
    "AZE": "AZ",  # Azerbaijan
    "BEL": "BE",  # Belgium
    "BEN": "BJ",  # Benin
    "BFA": "BF",  # Burkina Faso
    "BGD": "BD",  # Bangladesh
    "BGR": "BG",  # Bulgaria
    "BHR": "BH",  # Bahrain
    "BIH": "BA",  # Bosnia and Herzegovina
    "BLR": "BY",  # Belarus
    "BOL": "BO",  # Bolivia
    "BRA": "BR",  # Brazil
    "BRN": "BH",  # Bahrain (duplicate, but keeping as is)
    "BWA": "BW",  # Botswana
    "CAN": "CA",  # Canada
    "CHE": "CH",  # Switzerland
    "CHL": "CL",  # Chile
    "CHN": "CN",  # China
    "CIV": "CI",  # Ivory Coast
    "COL": "CO",  # Colombia
    "CRI": "CR",  # Costa Rica
    "CUB": "CU",  # Cuba
    "CYP": "CY",  # Cyprus
    "CZE": "CZ",  # Czech Republic
    "DEU": "DE",  # Germany
    "DNK": "DK",  # Denmark
    "DOM": "DO",  # Dominican Republic
    "DZA": "DZ",  # Algeria
    "ECU": "EC",  # Ecuador
    "EGY": "EG",  # Egypt
    "ESP": "ES",  # Spain
    "EST": "EE",  # Estonia
    "FIN": "FI",  # Finland
    "FRA": "FR",  # France
    "GAB": "GA",  # Gabon
    "GBR": "GB",  # United Kingdom
    "GEO": "GE",  # Georgia
    "GHA": "GH",  # Ghana
    "GMB": "GM",  # Gambia
    "GRC": "GR",  # Greece
    "GTM": "GT",  # Guatemala
    "HKG": "HK",  # Hong Kong
    "HND": "HN",  # Honduras
    "HRV": "HR",  # Croatia
    "HUN": "HU",  # Hungary
    "IDN": "ID",  # Indonesia
    "IND": "IN",  # India
    "IRL": "IE",  # Ireland
    "IRN": "IR",  # Iran
    "IRQ": "IQ",  # Iraq
    "ISL": "IS",  # Iceland
    "ISR": "IL",  # Israel
    "ITA": "IT",  # Italy
    "JOR": "JO",  # Jordan
    "JPN": "JP",  # Japan
    "KAZ": "KZ",  # Kazakhstan
    "KGZ": "KG",  # Kyrgyzstan
    "KHM": "KH",  # Cambodia
    "KOR": "KR",  # South Korea
    "KSV": "XK",  # Kosovo
    "KWT": "KW",  # Kuwait
    "LBY": "LY",  # Libya
    "LIE": "LI",  # Liechtenstein
    "LKA": "LK",  # Sri Lanka
    "LTU": "LT",  # Lithuania
    "LUX": "LU",  # Luxembourg
    "LVA": "LV",  # Latvia
    "MAC": "MO",  # Macau
    "MAR": "MA",  # Morocco
    "MDA": "MD",  # Moldova
    "MDG": "MG",  # Madagascar
    "MEX": "MX",  # Mexico
    "MKD": "MK",  # North Macedonia
    "MLT": "MT",  # Malta
    "MMR": "MM",  # Myanmar
    "MNE": "ME",  # Montenegro
    "MNG": "MN",  # Mongolia
    "MOZ": "MZ",  # Mozambique
    "MRT": "MR",  # Mauritania
    "MUS": "MU",  # Mauritius
    "MYS": "MY",  # Malaysia
    "NGA": "NG",  # Nigeria
    "NIC": "NI",  # Nicaragua
    "NLD": "NL",  # Netherlands
    "NOR": "NO",  # Norway
    "NPL": "NP",  # Nepal
    "NZL": "NZ",  # New Zealand
    "PAK": "PK",  # Pakistan
    "PAN": "PA",  # Panama
    "PER": "PE",  # Peru
    "PHL": "PH",  # Philippines
    "POL": "PL",  # Poland
    "PRI": "PR",  # Puerto Rico
    "PRK": "KP",  # North Korea
    "PRT": "PT",  # Portugal
    "PRY": "PY",  # Paraguay
    "PSE": "PS",  # Palestine
    "QAT": "QA",  # Qatar
    "ROU": "RO",  # Romania
    "RUS": "RU",  # Russia
    "RWA": "RW",  # Rwanda
    "SAU": "SA",  # Saudi Arabia
    "SEN": "SN",  # Senegal
    "SGP": "SG",  # Singapore
    "SLV": "SV",  # El Salvador
    "SRB": "RS",  # Serbia
    "SUR": "SR",  # Suriname
    "SVK": "SK",  # Slovakia
    "SVN": "SI",  # Slovenia
    "SWE": "SE",  # Sweden
    "SYR": "SY",  # Syria
    "THA": "TH",  # Thailand
    "TJK": "TJ",  # Tajikistan
    "TKM": "TM",  # Turkmenistan
    "TTO": "TT",  # Trinidad and Tobago
    "TUN": "TN",  # Tunisia
    "TUR": "TR",  # Turkey
    "TWN": "TW",  # Taiwan
    "TZA": "TZ",  # Tanzania
    "UGA": "UG",  # Uganda
    "UKR": "UA",  # Ukraine
    "URY": "UY",  # Uruguay
    "USA": "US",  # United States
    "UZB": "UZ",  # Uzbekistan
    "VEN": "VE",  # Venezuela
    "VNM": "VN",  # Vietnam
    "ZAF": "ZA",  # South Africa
    "ZWE": "ZW",  # Zimbabwe
}


def main():
    # Read the medals.json file
    with open("medals.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Add alpha2 code to each country
    countries_updated = 0
    for country in data["countries"]:
        code = country.get("code")
        if code in ALPHA3_TO_ALPHA2:
            country["alpha2"] = ALPHA3_TO_ALPHA2[code]
            countries_updated += 1
        else:
            print(f"Warning: No alpha2 code found for {code} ({country.get('name')})")

    print(f"Added alpha2 codes to {countries_updated} countries")

    # Write the updated JSON back to file
    with open("medals.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Updated medals.json successfully!")


if __name__ == "__main__":
    main()

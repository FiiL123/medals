# Olympiad Medals Visualization

Interactive world map visualization of medal counts from International Olympiads.

## Features

- 🗺️ Interactive choropleth map showing medal counts by country
- 📊 Filter by Olympiad type (All/IMO/IOI/IPhO)
- 🎖️ Detailed medal breakdowns on hover/click
- 🎨 Pleasant green gradient color scaling
- 📱 Responsive design for mobile and desktop

## Olympiads Included

- **IMO** - International Mathematical Olympiad (1959-2025)
- **IOI** - International Olympiad in Informatics (1989-2025)
- **IPhO** - International Physics Olympiad (1967-2025)

## Quick Start

### View Visualization

Simply open `index.html` in your web browser:
```bash
python -m http.server 8000
```

### Update Data

To refresh data from official Olympiad sources:

```bash
# Install dependencies (using uv)
uv sync

# Run scraper
uv run python scrape_data.py
```

This will update `medals.json` with the latest data. The `index.html` file fetches this file on page load, so there's no need to redeploy anything - just refresh the page!

## Deployment to GitHub Pages

1. Create a new GitHub repository
2. Push these files to repository
3. Enable GitHub Pages:
   - Go to repository Settings → Pages
   - Set source to `main` branch, root folder
4. Access your site at: `https://yourusername.github.io/repository-name`

## Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript (no build tools required)
- **Map Library**: Leaflet.js with OpenStreetMap tiles
- **Backend**: Python scraper using `uv` for dependency management
- **Country Codes**: ISO 3166-1 alpha-3
- **Data Format**: JSON file fetched via fetch API

## Project Structure

```
medals/
├── scrape_data.py      # Data scraper script
├── medals.json         # Generated medal data (updated by scraper)
├── index.html         # Main visualization (fetches medals.json)
├── pyproject.toml      # Python dependencies
├── README.md           # This file
└── uv.lock            # Lock file for uv
```

## Data Notes

- Only includes current countries (historical countries like Soviet Union, Yugoslavia are excluded)
- Medal counts are cumulative from each Olympiad's inception through 2025
- Medal types (Gold, Silver, Bronze) are weighted equally for total counts

## License

This project is open source and available for educational purposes.

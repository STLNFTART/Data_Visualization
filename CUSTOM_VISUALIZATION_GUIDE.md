# 🎨 Custom Data Visualization Platform

## Your Personalized Data Visualization System

This platform automatically discovers and visualizes **YOUR data** from multiple sources:

- ✅ GitHub repositories (CSV, JSON, databases)
- ✅ APIs (REST, GraphQL)
- ✅ Live data streams (WebSocket, MQTT, Kafka)
- ✅ Databases (PostgreSQL, MySQL, MongoDB, SQLite)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ~/Data_Visualization  # or wherever you cloned the repo
source venv/bin/activate
pip install requests aiohttp websockets
```

### 2. Run Universal Data Visualizer

This scans **all your GitHub repositories** for data files and creates visualizations automatically:

```bash
python3 universal_data_visualizer.py
```

**What it does:**
- 🔍 Scans all your GitHub repos for CSV/JSON files
- 📊 Automatically detects data types
- 📈 Creates appropriate visualizations (line charts, histograms, correlations, etc.)
- 💾 Saves interactive HTML visualizations to `visualizations_output/`

### 3. Run Streaming Visualizer (for live data)

```bash
python3 streaming_visualizer.py
```

**What it does:**
- 📡 Connects to live data streams
- ⚡ Updates visualizations in real-time
- 📊 Creates interactive dashboards

---

## 📋 Configuration

Edit `data_sources_config.json` to configure your data sources:

```json
{
  "github": {
    "username": "STLNFTART",
    "token": "your_github_token_here"
  },
  "apis": {
    "endpoints": [
      {
        "name": "My API",
        "url": "https://api.example.com/data",
        "enabled": true
      }
    ]
  },
  "live_streams": {
    "websocket_servers": [
      "wss://example.com/stream"
    ]
  }
}
```

---

## 🎯 How It Works

### Universal Data Visualizer

```
1. Discovers all your GitHub repos
   ↓
2. Scans each repo for data files
   ↓
3. Downloads and analyzes each file
   ↓
4. Auto-generates appropriate visualizations
   ↓
5. Saves interactive HTML dashboards
```

### Streaming Visualizer

```
1. Connects to live data source
   ↓
2. Buffers incoming data points
   ↓
3. Updates charts in real-time
   ↓
4. Saves snapshots periodically
```

---

## 📊 Visualization Types

The platform automatically creates:

### For Time Series Data
- Line charts showing trends over time
- Moving averages
- Anomaly detection

### For Numeric Data
- Histograms (distribution)
- Box plots (outlier detection)
- Scatter plots (relationships)
- Correlation heatmaps

### For Categorical Data
- Bar charts
- Pie charts
- Count plots

### For Multi-dimensional Data
- 3D scatter plots
- Parallel coordinates
- Scatter matrices

---

## 🔧 Advanced Usage

### Connect to Your Own API

```python
from universal_data_visualizer import UniversalDataVisualizer

visualizer = UniversalDataVisualizer("STLNFTART")

# Add custom API endpoint
api_data = requests.get("https://your-api.com/data").json()
df = pd.DataFrame(api_data)

visualizations = visualizer.auto_visualize_dataframe(df, "My API Data")
```

### Connect to Live Stream

```python
from streaming_visualizer import StreamingVisualizer
import asyncio

async def main():
    visualizer = StreamingVisualizer()
    visualizer.create_realtime_dashboard("my_stream", ['value1', 'value2'])

    # Add your data points
    while True:
        data_point = {'value1': get_sensor_data(), 'value2': get_other_data()}
        visualizer.update_stream_data("my_stream", data_point)
        await asyncio.sleep(1)

asyncio.run(main())
```

### Database Connection

```python
import pandas as pd
from universal_data_visualizer import UniversalDataVisualizer

# Example: PostgreSQL
import psycopg2
conn = psycopg2.connect("dbname=mydb user=user password=pass")
df = pd.read_sql_query("SELECT * FROM my_table", conn)

visualizer = UniversalDataVisualizer()
viz = visualizer.auto_visualize_dataframe(df, "Database Data")
```

---

## 📂 Output Structure

```
Data_Visualization/
├── visualizations_output/          # Auto-generated visualizations
│   ├── viz_001_histogram.html
│   ├── viz_002_time_series.html
│   ├── viz_003_correlation.html
│   └── ...
├── realtime_*.html                 # Live stream visualizations
├── universal_data_visualizer.py    # Main scanner
├── streaming_visualizer.py         # Real-time handler
└── data_sources_config.json        # Configuration
```

---

## 🎓 Examples

### Example 1: Visualize All CSV Files in Your Repos

```bash
python3 universal_data_visualizer.py
# Enter your GitHub username when prompted
# Visualizations will be saved to visualizations_output/
```

### Example 2: Monitor Live Sensor Data

```bash
python3 streaming_visualizer.py
# Demo will run for 30 seconds showing real-time updates
# Check realtime_demo_stream.html
```

### Example 3: Custom Data Source

```python
import pandas as pd
from universal_data_visualizer import UniversalDataVisualizer

# Load your data
df = pd.read_csv("your_data.csv")

# Create visualizer
viz = UniversalDataVisualizer()

# Generate visualizations
visualizations = viz.auto_visualize_dataframe(df, "My Data")

# Save them
for i, (viz_type, fig) in enumerate(visualizations):
    fig.write_html(f"my_viz_{i}.html")
```

---

## 🆘 Troubleshooting

### "No repositories found"
- Check your GitHub username
- If repos are private, provide a GitHub token

### "No data files found"
- Make sure your repos contain CSV, JSON, or database files
- Check that files are in the root directory (not in subfolders - working on recursive scan)

### "Rate limit exceeded"
- Create a GitHub Personal Access Token
- Provide it when running the visualizer

---

## 🔐 GitHub Personal Access Token

To avoid API rate limits and access private repos:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo` (for private repos), `public_repo` (for public)
4. Copy the token
5. Provide it when running the visualizer

---

## 🚧 Coming Soon

- [ ] Recursive directory scanning
- [ ] Direct database connectors
- [ ] Real-time collaborative dashboards
- [ ] Machine learning insights
- [ ] Automated anomaly detection
- [ ] Export to PDF/PowerPoint
- [ ] Email/Slack notifications for anomalies
- [ ] Mobile app

---

## 📝 Your Data Sources

Configure these in `data_sources_config.json`:

- **GitHub Repos**: Auto-discovered from your account
- **APIs**: Add endpoint URLs
- **WebSockets**: Add stream URLs
- **Databases**: Add connection strings

---

## ✅ Next Steps

1. **Run the visualizer** to see what data you already have
2. **Configure your API endpoints** in the config file
3. **Add streaming sources** for real-time data
4. **Customize visualizations** by editing the Python files

---

Built specifically for **STLNFTART** to visualize all your data automatically! 🎨

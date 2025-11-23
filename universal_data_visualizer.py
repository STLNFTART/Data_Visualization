#!/usr/bin/env python3
"""
Universal Data Visualization Platform
Connects to GitHub repos, pulls CSV/database files, APIs, and live streams
Generates visualizations for ALL your data automatically
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import requests
from datetime import datetime

class UniversalDataVisualizer:
    """
    Automatically discover and visualize data from multiple sources
    """

    def __init__(self, github_username="STLNFTART"):
        self.github_username = github_username
        self.data_sources = {
            'csv_files': [],
            'databases': [],
            'apis': [],
            'live_streams': []
        }
        self.visualizations = []

    def discover_github_repos(self, github_token=None):
        """
        Discover all repositories for a GitHub user
        """
        print(f"🔍 Discovering repositories for {self.github_username}...")

        headers = {}
        if github_token:
            headers['Authorization'] = f'token {github_token}'

        try:
            url = f"https://api.github.com/users/{self.github_username}/repos"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                repos = response.json()
                print(f"✅ Found {len(repos)} repositories")
                return repos
            else:
                print(f"❌ Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error discovering repos: {e}")
            return []

    def scan_repo_for_data(self, repo_name, repo_url):
        """
        Scan a repository for CSV, database, and JSON files
        """
        print(f"\n📂 Scanning {repo_name}...")

        # Use GitHub API to list files
        api_url = f"https://api.github.com/repos/{self.github_username}/{repo_name}/contents"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                contents = response.json()
                data_files = []

                for item in contents:
                    if item['type'] == 'file':
                        name = item['name']
                        if name.endswith(('.csv', '.json', '.db', '.sqlite', '.parquet')):
                            data_files.append({
                                'name': name,
                                'download_url': item.get('download_url'),
                                'type': name.split('.')[-1],
                                'repo': repo_name
                            })

                if data_files:
                    print(f"  ✅ Found {len(data_files)} data files:")
                    for f in data_files:
                        print(f"     - {f['name']} ({f['type']})")

                return data_files

        except Exception as e:
            print(f"  ⚠️  Error scanning repo: {e}")

        return []

    def load_csv_from_url(self, url, filename):
        """
        Load CSV file from GitHub URL
        """
        try:
            df = pd.read_csv(url)
            print(f"✅ Loaded {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return None

    def auto_visualize_dataframe(self, df, title="Data Visualization"):
        """
        Automatically create appropriate visualizations based on data type
        """
        if df is None or df.empty:
            return None

        visualizations = []

        # Detect numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Detect datetime columns
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

        # Strategy 1: Time series if datetime column exists
        if datetime_cols and numeric_cols:
            for time_col in datetime_cols[:1]:  # Use first datetime column
                for num_col in numeric_cols[:3]:  # Plot first 3 numeric columns
                    fig = px.line(df, x=time_col, y=num_col,
                                 title=f"{title}: {num_col} over time")
                    visualizations.append(('time_series', fig))

        # Strategy 2: Histograms for numeric data
        if numeric_cols:
            for col in numeric_cols[:5]:  # First 5 numeric columns
                fig = px.histogram(df, x=col, title=f"{title}: Distribution of {col}")
                visualizations.append(('histogram', fig))

        # Strategy 3: Correlation heatmap if multiple numeric columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix,
                           title=f"{title}: Correlation Matrix",
                           labels=dict(color="Correlation"))
            visualizations.append(('correlation', fig))

        # Strategy 4: Scatter matrix for first few numeric columns
        if len(numeric_cols) >= 2:
            cols_to_plot = numeric_cols[:min(4, len(numeric_cols))]
            fig = px.scatter_matrix(df, dimensions=cols_to_plot,
                                   title=f"{title}: Scatter Matrix")
            visualizations.append(('scatter_matrix', fig))

        # Strategy 5: Box plots
        if len(numeric_cols) > 0:
            for col in numeric_cols[:3]:
                fig = px.box(df, y=col, title=f"{title}: Box Plot of {col}")
                visualizations.append(('box_plot', fig))

        return visualizations

    def generate_report(self):
        """
        Generate HTML report with all visualizations
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Visualization Report - {self.github_username}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                h1 {{ color: #333; }}
                .viz-container {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .summary {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>🎨 Data Visualization Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>GitHub User:</strong> {self.github_username}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Total Visualizations:</strong> {len(self.visualizations)}</p>
            </div>

            <div id="visualizations">
                <!-- Visualizations will be embedded here -->
            </div>
        </body>
        </html>
        """

        return html

    def run_full_scan(self, github_token=None):
        """
        Run complete scan and visualization pipeline
        """
        print("="*80)
        print("🚀 UNIVERSAL DATA VISUALIZER")
        print("="*80)

        # Step 1: Discover repositories
        repos = self.discover_github_repos(github_token)

        if not repos:
            print("\n⚠️  No repositories found. Check your GitHub username or token.")
            return

        # Step 2: Scan each repo for data files
        all_data_files = []
        for repo in repos:
            repo_name = repo['name']
            repo_url = repo['html_url']
            data_files = self.scan_repo_for_data(repo_name, repo_url)
            all_data_files.extend(data_files)

        print(f"\n{'='*80}")
        print(f"📊 TOTAL DATA FILES FOUND: {len(all_data_files)}")
        print(f"{'='*80}")

        # Step 3: Load and visualize each data file
        for data_file in all_data_files:
            if data_file['type'] == 'csv' and data_file.get('download_url'):
                print(f"\n📈 Processing {data_file['name']}...")
                df = self.load_csv_from_url(data_file['download_url'], data_file['name'])

                if df is not None:
                    title = f"{data_file['repo']}/{data_file['name']}"
                    viz_list = self.auto_visualize_dataframe(df, title)

                    if viz_list:
                        self.visualizations.extend(viz_list)
                        print(f"  ✅ Created {len(viz_list)} visualizations")

        print(f"\n{'='*80}")
        print(f"✅ COMPLETE: Generated {len(self.visualizations)} total visualizations")
        print(f"{'='*80}")

        return self.visualizations


def main():
    """
    Main entry point
    """
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         UNIVERSAL DATA VISUALIZATION PLATFORM                 ║
║                                                               ║
║  Automatically discovers and visualizes ALL your data from:   ║
║  • GitHub repositories (CSV, JSON, databases)                 ║
║  • APIs (coming soon)                                         ║
║  • Live streams (coming soon)                                 ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    # Get GitHub username
    username = input("\n📝 Enter your GitHub username (or press Enter for 'STLNFTART'): ").strip()
    if not username:
        username = "STLNFTART"

    # Optional: GitHub token for higher API rate limits
    print("\n💡 Optional: Enter GitHub Personal Access Token for higher API limits")
    print("   (or press Enter to skip)")
    token = input("🔑 Token: ").strip() or None

    # Create visualizer
    visualizer = UniversalDataVisualizer(username)

    # Run full scan
    visualizations = visualizer.run_full_scan(token)

    # Save visualizations
    if visualizations:
        output_dir = Path("visualizations_output")
        output_dir.mkdir(exist_ok=True)

        print(f"\n💾 Saving visualizations to {output_dir}/...")

        for i, (viz_type, fig) in enumerate(visualizations):
            filename = output_dir / f"viz_{i:03d}_{viz_type}.html"
            fig.write_html(str(filename))
            print(f"  ✅ Saved: {filename}")

        print(f"\n🎉 All visualizations saved to {output_dir}/")
        print(f"   Open the HTML files in your browser to view them!")
    else:
        print("\n⚠️  No visualizations created. Make sure you have CSV files in your repos!")


if __name__ == "__main__":
    main()

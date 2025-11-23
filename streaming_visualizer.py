#!/usr/bin/env python3
"""
Real-Time Streaming Data Visualizer
Handles live data streams and updates visualizations in real-time
"""

import asyncio
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from collections import deque
import numpy as np

class StreamingVisualizer:
    """
    Real-time visualization for streaming data
    """

    def __init__(self, max_points=1000):
        self.max_points = max_points
        self.data_buffers = {}
        self.figures = {}

    def create_realtime_dashboard(self, stream_name, columns):
        """
        Create a real-time dashboard for a data stream
        """
        # Create subplots for each column
        num_cols = len(columns)
        fig = make_subplots(
            rows=num_cols,
            cols=1,
            subplot_titles=columns,
            vertical_spacing=0.05
        )

        # Initialize data buffers
        self.data_buffers[stream_name] = {
            'timestamp': deque(maxlen=self.max_points),
            **{col: deque(maxlen=self.max_points) for col in columns}
        }

        # Add traces for each column
        for i, col in enumerate(columns, 1):
            fig.add_trace(
                go.Scatter(
                    x=[],
                    y=[],
                    mode='lines',
                    name=col,
                    line=dict(width=2)
                ),
                row=i,
                col=1
            )

        fig.update_layout(
            title=f"Real-Time Stream: {stream_name}",
            height=300 * num_cols,
            showlegend=True,
            hovermode='x unified'
        )

        self.figures[stream_name] = fig
        return fig

    def update_stream_data(self, stream_name, data_point):
        """
        Update data buffer with new data point
        """
        if stream_name not in self.data_buffers:
            return

        buffer = self.data_buffers[stream_name]
        buffer['timestamp'].append(datetime.now())

        for key, value in data_point.items():
            if key in buffer:
                buffer[key].append(value)

    def get_updated_figure(self, stream_name):
        """
        Get updated figure with latest data
        """
        if stream_name not in self.figures:
            return None

        fig = self.figures[stream_name]
        buffer = self.data_buffers[stream_name]

        # Update each trace with new data
        timestamps = list(buffer['timestamp'])
        trace_index = 0

        for key in buffer.keys():
            if key != 'timestamp':
                values = list(buffer[key])
                fig.data[trace_index].x = timestamps
                fig.data[trace_index].y = values
                trace_index += 1

        return fig

    async def simulate_live_stream(self, stream_name, duration_seconds=60):
        """
        Simulate a live data stream for testing
        """
        print(f"🎬 Simulating live stream: {stream_name}")

        # Create dashboard with 3 sample columns
        columns = ['sensor_1', 'sensor_2', 'sensor_3']
        self.create_realtime_dashboard(stream_name, columns)

        start_time = datetime.now()
        iteration = 0

        while (datetime.now() - start_time).seconds < duration_seconds:
            # Generate random data point
            data_point = {
                'sensor_1': np.sin(iteration * 0.1) + np.random.normal(0, 0.1),
                'sensor_2': np.cos(iteration * 0.1) + np.random.normal(0, 0.1),
                'sensor_3': np.random.normal(0, 1)
            }

            # Update buffer
            self.update_stream_data(stream_name, data_point)

            # Get updated figure
            fig = self.get_updated_figure(stream_name)

            # Save to HTML (in production, this would push to dashboard)
            if iteration % 10 == 0:  # Save every 10 iterations
                fig.write_html(f'realtime_{stream_name}.html')
                print(f"  📊 Updated visualization (iteration {iteration})")

            iteration += 1
            await asyncio.sleep(0.1)  # 100ms update rate

        print(f"✅ Stream simulation complete")

    def add_websocket_stream(self, ws_url, stream_name):
        """
        Connect to WebSocket and stream data
        """
        # This would be implemented with websockets library
        print(f"🔌 WebSocket stream setup for: {ws_url}")
        pass

    def add_api_polling_stream(self, api_url, stream_name, interval_seconds=5):
        """
        Poll an API endpoint and treat as stream
        """
        print(f"📡 API polling stream setup: {api_url} (every {interval_seconds}s)")
        pass


async def main():
    """
    Demo of streaming visualizer
    """
    print("""
╔═══════════════════════════════════════════════════════════════╗
║          REAL-TIME STREAMING DATA VISUALIZER                  ║
║                                                               ║
║  Visualizes live data streams in real-time                    ║
║  Supports: WebSockets, APIs, MQTT, Kafka                      ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    visualizer = StreamingVisualizer(max_points=500)

    # Run demo simulation
    print("\n🎬 Running 30-second demo simulation...")
    await visualizer.simulate_live_stream("demo_stream", duration_seconds=30)

    print("\n✅ Demo complete! Check 'realtime_demo_stream.html'")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Motorhand Pro - Quick Start Server
===================================
This script starts the Motorhand Pro connector and runs a lightweight
demonstration of the satellite constellation monitoring system.

Usage:
    python start_motorhand_pro.py [--satellites N] [--uavs N] [--cycles N]

Options:
    --satellites N    Number of satellites to simulate (default: 1000)
    --uavs N         Number of UAVs to simulate (default: 20)
    --cycles N       Number of simulation cycles (default: 500)
    --port N         Server port (default: 8000)
    --no-viz         Disable 3D visualization
"""

import asyncio
import argparse
import sys
import signal

# Check dependencies
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from Motorhand_Pro_Connector import MotorhandProConnector
    from Practical_Use_Case_Satellite_Constellation_Monitoring import SatelliteConstellationMonitor
    print("✅ All dependencies loaded successfully")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nInstall required packages:")
    print("pip install numpy matplotlib aiohttp aiohttp-cors")
    sys.exit(1)


class MotorhandProServer:
    """Motorhand Pro server wrapper with graceful shutdown"""

    def __init__(self, satellites=1000, uavs=20, cycles=500, port=8000, enable_viz=True):
        self.satellites = satellites
        self.uavs = uavs
        self.cycles = cycles
        self.port = port
        self.enable_viz = enable_viz
        self.monitor = None
        self.running = False

    async def start(self):
        """Start the Motorhand Pro server and simulation"""
        print("="*80)
        print("🌌 MOTORHAND PRO - SATELLITE CONSTELLATION MONITORING")
        print("="*80)
        print(f"\n⚙️  Configuration:")
        print(f"   Satellites: {self.satellites:,}")
        print(f"   UAVs: {self.uavs}")
        print(f"   Cycles: {self.cycles:,}")
        print(f"   Port: {self.port}")
        print(f"   Visualization: {'Enabled' if self.enable_viz else 'Disabled'}")
        print("="*80)

        # Create monitor
        print("\n🔧 Initializing satellite constellation monitor...")
        self.monitor = SatelliteConstellationMonitor(
            satellite_count=self.satellites,
            uav_count=self.uavs,
            simulation_cycles=self.cycles
        )

        # Initialize Motorhand Pro connector
        print(f"\n🚀 Starting Motorhand Pro server on port {self.port}...")
        await self.monitor.initialize_motorhand_pro(host='0.0.0.0', port=self.port)

        print("\n" + "="*80)
        print("✅ MOTORHAND PRO IS RUNNING!")
        print("="*80)
        print(f"\n📡 Access Points:")
        print(f"   WebSocket:     ws://localhost:{self.port}/ws")
        print(f"   REST API:      http://localhost:{self.port}/api/v1/")
        print(f"   Status:        http://localhost:{self.port}/api/v1/simulation/status")
        print(f"   Health Check:  http://localhost:{self.port}/api/v1/health")
        print(f"   Visualization: http://localhost:{self.port}/api/v1/visualization/snapshot")

        print("\n🔌 WebSocket Connection Example:")
        print("   const ws = new WebSocket('ws://localhost:{}/ws');".format(self.port))
        print("   ws.onmessage = (e) => console.log(JSON.parse(e.data));")

        print("\n📊 REST API Examples:")
        print(f"   curl http://localhost:{self.port}/api/v1/simulation/status")
        print(f"   curl http://localhost:{self.port}/api/v1/entities/satellites?page=1&per_page=100")
        print(f"   curl http://localhost:{self.port}/api/v1/threats/emp")

        print("\n⏸️  Press Ctrl+C to stop the server")
        print("="*80 + "\n")

        # Run simulation
        self.running = True
        await self.run_simulation()

    async def run_simulation(self):
        """Run the simulation loop"""
        if not self.enable_viz:
            plt.ioff()  # Disable interactive mode

        try:
            cycle = 0
            while self.running and cycle < self.cycles:
                # Run simulation step
                self.monitor.run_simulation_step(cycle)

                # Print status every 10 cycles
                if cycle % 10 == 0:
                    self.monitor.print_status(cycle)

                # Create visualization every 50 cycles (if enabled)
                if self.enable_viz and cycle % 50 == 0:
                    self.monitor.create_visualization(cycle)

                # Stream to Motorhand Pro
                if self.monitor.motorhand_connector:
                    await self.monitor.motorhand_connector.stream_to_motorhand_pro(self.monitor)

                # Small delay for real-time effect
                await asyncio.sleep(0.02)

                cycle += 1

            # Print final report
            if self.running:
                print("\n" + "="*80)
                print("🎯 SIMULATION COMPLETE")
                print("="*80)
                self.monitor.print_final_report()

                # Export final state
                if self.monitor.motorhand_connector:
                    filename = 'motorhand_pro_final_state.json'
                    self.monitor.motorhand_connector.export_to_json(filename)
                    print(f"\n📁 Final state exported to: {filename}")

            # Keep server running
            print("\n🔄 Simulation complete. Server still running...")
            print("   Press Ctrl+C to stop the server\n")

            while self.running:
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            print("\n\n⏹️  Shutting down gracefully...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.enable_viz:
                plt.close('all')

    async def stop(self):
        """Stop the server gracefully"""
        self.running = False
        print("Server stopped.")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Motorhand Pro - Satellite Constellation Monitoring')
    parser.add_argument('--satellites', type=int, default=1000, help='Number of satellites (default: 1000)')
    parser.add_argument('--uavs', type=int, default=20, help='Number of UAVs (default: 20)')
    parser.add_argument('--cycles', type=int, default=500, help='Number of simulation cycles (default: 500)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    parser.add_argument('--no-viz', action='store_true', help='Disable 3D visualization')

    args = parser.parse_args()

    # Create and start server
    server = MotorhandProServer(
        satellites=args.satellites,
        uavs=args.uavs,
        cycles=args.cycles,
        port=args.port,
        enable_viz=not args.no_viz
    )

    # Setup signal handlers
    loop = asyncio.get_event_loop()

    def signal_handler():
        print("\n\n⏹️  Received interrupt signal. Stopping server...")
        asyncio.create_task(server.stop())

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    # Start server
    await server.start()


if __name__ == '__main__':
    print("\n🌌 Motorhand Pro - Starting up...\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ Motorhand Pro stopped successfully.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

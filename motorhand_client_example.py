#!/usr/bin/env python3
"""
Quick Python Client Example for Motorhand Pro
==============================================
This demonstrates how to connect to Motorhand Pro and receive live updates.
"""

import asyncio
import aiohttp
import json
from datetime import datetime


async def connect_to_motorhand_pro():
    """Connect to Motorhand Pro and stream live data"""

    print("🌌 Motorhand Pro - Python Client")
    print("=" * 60)
    print("Connecting to ws://localhost:8000/ws")
    print()

    async with aiohttp.ClientSession() as session:
        # Connect to WebSocket
        async with session.ws_connect('ws://localhost:8000/ws') as ws:
            print("✅ Connected to Motorhand Pro!")
            print()

            # Subscribe to updates
            await ws.send_json({
                'type': 'subscribe',
                'channels': ['simulation_update', 'emp_events', 'collision_alerts']
            })
            print("📡 Subscribed to real-time updates")
            print()

            # Listen for messages
            update_count = 0
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)

                    if data['type'] == 'subscription_confirmed':
                        print(f"✅ Subscription confirmed: {data['channels']}")
                        print()

                    elif data['type'] == 'snapshot' or data['type'] == 'simulation_update':
                        update_count += 1
                        snapshot = data['data']
                        entities = snapshot.get('entities', {})
                        threats = snapshot.get('threats', {})

                        print(f"\n{'='*60}")
                        print(f"📊 Update #{update_count} - Cycle {snapshot.get('cycle', 0)}")
                        print(f"{'='*60}")
                        print(f"🛰️  Satellites: {entities.get('satellites_count', 0):,}")
                        print(f"🚁 UAVs: {entities.get('uavs_count', 0)}")
                        print(f"🤖 Digital Twins: {entities.get('twins_count', 0)}")
                        print(f"⚡ EMP Events: {threats.get('emp_events_count', 0)}")
                        print(f"🚨 Collision Risks: {threats.get('collision_risks_count', 0)}")

                        # Show sample satellite data
                        satellites = entities.get('satellites_sample', [])
                        if satellites:
                            print(f"\n📡 Sample Satellite (ID {satellites[0]['id']}):")
                            print(f"   Position: {satellites[0]['pos'][:3]}")
                            print(f"   Health: {satellites[0]['health']*100:.1f}%")
                            print(f"   Trust: {satellites[0]['trust']*100:.1f}%")
                            print(f"   EMP: {'⚡ Affected' if satellites[0].get('emp_affected') else '✅ Normal'}")

                        # Show sample UAV data
                        uavs = entities.get('uavs_sample', [])
                        if uavs:
                            print(f"\n🚁 Sample UAV (ID {uavs[0]['id']}):")
                            print(f"   Position: {uavs[0]['pos'][:3]}")
                            print(f"   Health: {uavs[0]['health']*100:.1f}%")
                            print(f"   Fuel: {uavs[0]['fuel_level']*100:.1f}%")

                        print()

                        # Stop after 10 updates for demo
                        if update_count >= 10:
                            print("✅ Received 10 updates. Demo complete!")
                            break

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f"❌ WebSocket error: {ws.exception()}")
                    break


async def test_rest_api():
    """Test REST API endpoints"""
    print("\n🔍 Testing REST API Endpoints")
    print("=" * 60)

    async with aiohttp.ClientSession() as session:
        # Get simulation status
        async with session.get('http://localhost:8000/api/v1/simulation/status') as resp:
            data = await resp.json()
            print(f"📊 Simulation Status:")
            print(f"   Cycle: {data['cycle']}")
            print(f"   Status: {data['status']}")
            print(f"   Clients: {data['connected_clients']}")

        # Get satellite count
        async with session.get('http://localhost:8000/api/v1/entities/satellites?page=1&per_page=1') as resp:
            data = await resp.json()
            print(f"\n🛰️  Satellites:")
            print(f"   Total: {data['total_count']:,}")

        # Check for threats
        async with session.get('http://localhost:8000/api/v1/threats/emp') as resp:
            data = await resp.json()
            print(f"\n⚡ EMP Threats:")
            print(f"   Active: {data['count']}")


if __name__ == '__main__':
    print("\n🚀 Motorhand Pro - Python Client Example")
    print("=" * 60)
    print()

    # Choose what to run
    print("1. Stream live WebSocket updates")
    print("2. Test REST API")
    print("3. Both")
    print()

    choice = input("Choose option (1-3) [default: 1]: ").strip() or "1"

    try:
        if choice == "2":
            asyncio.run(test_rest_api())
        elif choice == "3":
            asyncio.run(test_rest_api())
            asyncio.run(connect_to_motorhand_pro())
        else:
            asyncio.run(connect_to_motorhand_pro())
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

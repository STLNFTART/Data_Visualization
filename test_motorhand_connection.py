#!/usr/bin/env python3
"""
Test Motorhand Pro Connection
==============================
This script tests the Motorhand Pro connection by:
1. Checking if the server is running
2. Testing REST API endpoints
3. Testing WebSocket connection
4. Displaying sample data
"""

import asyncio
import json
import sys

try:
    import aiohttp
    print("✅ aiohttp imported successfully")
except ImportError:
    print("❌ aiohttp not installed. Run: pip install aiohttp")
    sys.exit(1)


async def test_rest_api(host='localhost', port=8000):
    """Test REST API endpoints"""
    print(f"\n🔍 Testing REST API at http://{host}:{port}")
    print("="*60)

    endpoints = [
        '/api/v1/health',
        '/api/v1/simulation/status',
        '/api/v1/entities/satellites?page=1&per_page=10',
        '/api/v1/entities/uavs?page=1&per_page=10',
        '/api/v1/threats/emp',
        '/api/v1/visualization/snapshot'
    ]

    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            url = f"http://{host}:{port}{endpoint}"
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ {endpoint}")

                        # Show sample data
                        if endpoint == '/api/v1/health':
                            print(f"   Status: {data.get('status')}")
                        elif endpoint == '/api/v1/simulation/status':
                            print(f"   Cycle: {data.get('cycle')}")
                            print(f"   Status: {data.get('status')}")
                            print(f"   Clients: {data.get('connected_clients')}")
                        elif 'entities' in endpoint:
                            print(f"   Total: {data.get('total_count')}")
                            print(f"   Page: {data.get('page')}")
                        elif 'emp' in endpoint:
                            print(f"   Active EMP events: {data.get('count')}")
                        elif 'visualization' in endpoint:
                            meta = data.get('metadata', {})
                            print(f"   Satellites: {meta.get('total_satellites')}")
                            print(f"   UAVs: {meta.get('total_uavs')}")
                    else:
                        print(f"⚠️  {endpoint} - Status {response.status}")
            except asyncio.TimeoutError:
                print(f"❌ {endpoint} - Timeout")
            except aiohttp.ClientConnectorError:
                print(f"❌ {endpoint} - Connection refused (server not running?)")
                return False
            except Exception as e:
                print(f"❌ {endpoint} - Error: {e}")

    return True


async def test_websocket(host='localhost', port=8000):
    """Test WebSocket connection"""
    print(f"\n🔌 Testing WebSocket at ws://{host}:{port}/ws")
    print("="*60)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f'ws://{host}:{port}/ws') as ws:
                print("✅ WebSocket connected!")

                # Send subscription message
                await ws.send_json({
                    'type': 'subscribe',
                    'channels': ['simulation_update', 'emp_events']
                })
                print("📤 Sent subscription request")

                # Wait for response
                try:
                    msg = await asyncio.wait_for(ws.receive(), timeout=5.0)
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        print(f"✅ Received: {data.get('type')}")
                        print(f"   Channels: {data.get('channels')}")
                    else:
                        print(f"⚠️  Received unexpected message type: {msg.type}")
                except asyncio.TimeoutError:
                    print("⚠️  No response received (timeout)")

                # Request snapshot
                await ws.send_json({'type': 'get_snapshot'})
                print("📤 Requested snapshot")

                try:
                    msg = await asyncio.wait_for(ws.receive(), timeout=5.0)
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        if data.get('type') == 'snapshot':
                            snapshot = data.get('data', {})
                            entities = snapshot.get('entities', {})
                            print(f"✅ Snapshot received:")
                            print(f"   Cycle: {snapshot.get('cycle')}")
                            print(f"   Satellites: {entities.get('satellites_count')}")
                            print(f"   UAVs: {entities.get('uavs_count')}")
                            print(f"   Twins: {entities.get('twins_count')}")
                except asyncio.TimeoutError:
                    print("⚠️  No snapshot received (timeout)")

                print("✅ WebSocket test complete!")
                return True

    except aiohttp.ClientConnectorError:
        print("❌ WebSocket connection refused (server not running?)")
        return False
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return False


async def main():
    """Main test function"""
    print("="*60)
    print("🧪 MOTORHAND PRO CONNECTION TEST")
    print("="*60)

    # Test REST API
    rest_ok = await test_rest_api()

    if not rest_ok:
        print("\n" + "="*60)
        print("❌ Motorhand Pro is NOT RUNNING")
        print("="*60)
        print("\nTo start Motorhand Pro:")
        print("  python start_motorhand_pro.py")
        print("\nOr run with custom settings:")
        print("  python start_motorhand_pro.py --satellites 5000 --uavs 50")
        sys.exit(1)

    # Test WebSocket
    ws_ok = await test_websocket()

    # Summary
    print("\n" + "="*60)
    if rest_ok and ws_ok:
        print("✅ ALL TESTS PASSED - Motorhand Pro is connected!")
    elif rest_ok:
        print("⚠️  REST API working, WebSocket issues")
    else:
        print("❌ CONNECTION FAILED")
    print("="*60)

    print("\n📊 Next Steps:")
    print("  1. Access dashboard: http://localhost:8000/api/v1/simulation/status")
    print("  2. View entities: http://localhost:8000/api/v1/entities/satellites")
    print("  3. Monitor threats: http://localhost:8000/api/v1/threats/emp")
    print("  4. Connect your visualization client to: ws://localhost:8000/ws")


if __name__ == '__main__':
    asyncio.run(main())

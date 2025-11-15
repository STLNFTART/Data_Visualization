"""
Motorhand Pro Integration Connector
====================================
Real-time data streaming and visualization interface for EMP Multiswarm Simulation

FEATURES:
- WebSocket server for real-time data streaming
- REST API for historical data queries
- JSON export for Motorhand Pro dashboard integration
- Algorithm performance metrics streaming
- 3D visualization data export
- Threat event notifications
- Network health monitoring

PRACTICAL USE CASES:
1. Real-time satellite constellation monitoring
2. EMP attack simulation and response training
3. UAV swarm coordination visualization
4. Space traffic management dashboard
5. Digital twin network operations center
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque
import numpy as np

try:
    from aiohttp import web
    import aiohttp_cors
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    print("Warning: aiohttp not available. Install with: pip install aiohttp aiohttp-cors")


class MotorhandProConnector:
    """
    Connector class for streaming simulation data to Motorhand Pro platform
    """

    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.websocket_clients = set()
        self.data_buffer = deque(maxlen=10000)
        self.simulation_state = {
            'running': False,
            'cycle': 0,
            'entities': {
                'satellites': [],
                'uavs': [],
                'digital_twins': []
            },
            'threats': {
                'emp_events': [],
                'collision_risks': [],
                'missile_threats': []
            },
            'algorithms': {},
            'performance': {}
        }

    async def start_server(self):
        """Start the WebSocket and REST API server"""
        if not AIOHTTP_AVAILABLE:
            print("Cannot start server: aiohttp not installed")
            return

        app = web.Application()

        # Configure CORS
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # REST API endpoints
        app.router.add_get('/api/v1/simulation/status', self.get_simulation_status)
        app.router.add_get('/api/v1/entities/{entity_type}', self.get_entities)
        app.router.add_get('/api/v1/algorithms/{algorithm_type}', self.get_algorithm_results)
        app.router.add_get('/api/v1/threats/emp', self.get_emp_events)
        app.router.add_get('/api/v1/threats/all', self.get_all_threats)
        app.router.add_get('/api/v1/visualization/snapshot', self.get_visualization_snapshot)
        app.router.add_get('/api/v1/health', self.health_check)

        # WebSocket endpoint
        app.router.add_get('/ws', self.websocket_handler)

        # Configure CORS on all routes
        for route in list(app.router.routes()):
            cors.add(route)

        # Start server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        print(f"🚀 Motorhand Pro Connector started on {self.host}:{self.port}")
        print(f"📡 WebSocket: ws://{self.host}:{self.port}/ws")
        print(f"🌐 REST API: http://{self.host}:{self.port}/api/v1/")

    async def websocket_handler(self, request):
        """Handle WebSocket connections"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self.websocket_clients.add(ws)
        print(f"✅ WebSocket client connected. Total clients: {len(self.websocket_clients)}")

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    # Handle client messages
                    data = json.loads(msg.data)
                    await self.handle_client_message(ws, data)
                elif msg.type == web.WSMsgType.ERROR:
                    print(f'WebSocket error: {ws.exception()}')
        finally:
            self.websocket_clients.discard(ws)
            print(f"❌ WebSocket client disconnected. Total clients: {len(self.websocket_clients)}")

        return ws

    async def handle_client_message(self, ws, data: Dict):
        """Handle messages from WebSocket clients"""
        msg_type = data.get('type', '')

        if msg_type == 'subscribe':
            channels = data.get('channels', [])
            response = {
                'type': 'subscription_confirmed',
                'channels': channels,
                'timestamp': datetime.now().isoformat()
            }
            await ws.send_json(response)

        elif msg_type == 'get_snapshot':
            snapshot = self.get_current_snapshot()
            await ws.send_json({
                'type': 'snapshot',
                'data': snapshot,
                'timestamp': datetime.now().isoformat()
            })

    async def broadcast_update(self, update_type: str, data: Dict):
        """Broadcast updates to all connected WebSocket clients"""
        if not self.websocket_clients:
            return

        message = {
            'type': update_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }

        # Send to all connected clients
        disconnected = set()
        for ws in self.websocket_clients:
            try:
                await ws.send_json(message)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected.add(ws)

        # Remove disconnected clients
        self.websocket_clients -= disconnected

    def update_simulation_state(self, satellites=None, uavs=None, twins=None,
                                emp_events=None, threats=None, algorithms=None,
                                performance=None, cycle=None):
        """Update the internal simulation state"""
        if satellites is not None:
            self.simulation_state['entities']['satellites'] = satellites
        if uavs is not None:
            self.simulation_state['entities']['uavs'] = uavs
        if twins is not None:
            self.simulation_state['entities']['digital_twins'] = twins
        if emp_events is not None:
            self.simulation_state['threats']['emp_events'] = emp_events
        if threats is not None:
            for threat in threats:
                threat_type = threat.get('type', '')
                if threat_type == 'COLLISION_RISK':
                    self.simulation_state['threats']['collision_risks'].append(threat)
                elif threat_type == 'MISSILE_THREAT':
                    self.simulation_state['threats']['missile_threats'].append(threat)
        if algorithms is not None:
            self.simulation_state['algorithms'] = algorithms
        if performance is not None:
            self.simulation_state['performance'] = performance
        if cycle is not None:
            self.simulation_state['cycle'] = cycle

        # Add to data buffer
        self.data_buffer.append({
            'cycle': cycle,
            'timestamp': datetime.now().isoformat(),
            'state': self.get_current_snapshot()
        })

    def get_current_snapshot(self) -> Dict:
        """Get current simulation snapshot"""
        return {
            'cycle': self.simulation_state['cycle'],
            'entities': {
                'satellites_count': len(self.simulation_state['entities']['satellites']),
                'uavs_count': len(self.simulation_state['entities']['uavs']),
                'twins_count': len(self.simulation_state['entities']['digital_twins']),
                'satellites_sample': self.simulation_state['entities']['satellites'][:100],
                'uavs_sample': self.simulation_state['entities']['uavs'][:50],
                'twins_sample': self.simulation_state['entities']['digital_twins'][:20]
            },
            'threats': {
                'emp_events_count': len(self.simulation_state['threats']['emp_events']),
                'emp_events': self.simulation_state['threats']['emp_events'],
                'collision_risks_count': len(self.simulation_state['threats']['collision_risks']),
                'missile_threats_count': len(self.simulation_state['threats']['missile_threats'])
            },
            'algorithms': self.simulation_state['algorithms'],
            'performance': self.simulation_state['performance']
        }

    # REST API Handlers
    async def get_simulation_status(self, request):
        """GET /api/v1/simulation/status"""
        return web.json_response({
            'status': 'running' if self.simulation_state['running'] else 'stopped',
            'cycle': self.simulation_state['cycle'],
            'timestamp': datetime.now().isoformat(),
            'connected_clients': len(self.websocket_clients)
        })

    async def get_entities(self, request):
        """GET /api/v1/entities/{entity_type}"""
        entity_type = request.match_info['entity_type']

        if entity_type not in ['satellites', 'uavs', 'digital_twins']:
            return web.json_response({'error': 'Invalid entity type'}, status=400)

        entities = self.simulation_state['entities'][entity_type]

        # Pagination
        page = int(request.query.get('page', 1))
        per_page = int(request.query.get('per_page', 100))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        return web.json_response({
            'entity_type': entity_type,
            'total_count': len(entities),
            'page': page,
            'per_page': per_page,
            'data': entities[start_idx:end_idx]
        })

    async def get_algorithm_results(self, request):
        """GET /api/v1/algorithms/{algorithm_type}"""
        algorithm_type = request.match_info['algorithm_type']

        if algorithm_type not in self.simulation_state['algorithms']:
            return web.json_response({'error': 'Algorithm not found'}, status=404)

        return web.json_response({
            'algorithm_type': algorithm_type,
            'results': self.simulation_state['algorithms'][algorithm_type]
        })

    async def get_emp_events(self, request):
        """GET /api/v1/threats/emp"""
        return web.json_response({
            'emp_events': self.simulation_state['threats']['emp_events'],
            'count': len(self.simulation_state['threats']['emp_events']),
            'timestamp': datetime.now().isoformat()
        })

    async def get_all_threats(self, request):
        """GET /api/v1/threats/all"""
        return web.json_response({
            'threats': self.simulation_state['threats'],
            'timestamp': datetime.now().isoformat()
        })

    async def get_visualization_snapshot(self, request):
        """GET /api/v1/visualization/snapshot"""
        return web.json_response(self.get_current_snapshot())

    async def health_check(self, request):
        """GET /api/v1/health"""
        return web.json_response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })

    def export_to_json(self, filename: str):
        """Export current state to JSON file for Motorhand Pro import"""
        snapshot = self.get_current_snapshot()
        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=2)
        print(f"📁 Exported simulation state to {filename}")

    def export_visualization_data(self, satellites, uavs, emp_events) -> Dict:
        """Export formatted visualization data for Motorhand Pro 3D viewer"""
        vis_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_satellites': len(satellites),
                'total_uavs': len(uavs),
                'active_emp_events': len(emp_events)
            },
            'satellites': {
                'positions': [[s['pos'][0], s['pos'][1], s['pos'][2]] for s in satellites],
                'health': [s.get('health', 1.0) for s in satellites],
                'colors': [self._get_entity_color(s) for s in satellites]
            },
            'uavs': {
                'positions': [[u['pos'][0], u['pos'][1], u['pos'][2]] for u in uavs],
                'health': [u.get('health', 1.0) for u in uavs],
                'fuel': [u.get('fuel_level', 1.0) for u in uavs],
                'colors': [self._get_entity_color(u) for u in uavs]
            },
            'emp_events': [
                {
                    'position': [e['position'][0], e['position'][1], e['position'][2]],
                    'range': e['range'],
                    'intensity': e['intensity'],
                    'type': e['source_type']
                }
                for e in emp_events
            ]
        }
        return vis_data

    def _get_entity_color(self, entity: Dict) -> str:
        """Determine entity color based on status"""
        if entity.get('emp_affected', False):
            return '#FF0000'  # Red for EMP affected
        elif entity.get('health', 1.0) < 0.5:
            return '#FFA500'  # Orange for low health
        elif entity.get('emergency_landing', False):
            return '#FFFF00'  # Yellow for emergency
        else:
            return '#00FF00'  # Green for healthy

    async def stream_to_motorhand_pro(self, simulation_engine):
        """
        Main streaming loop to send data to Motorhand Pro
        Call this in your simulation loop
        """
        # Convert entity objects to dictionaries
        satellites_data = [
            {
                'id': s.id,
                'pos': s.pos.tolist(),
                'health': s.health,
                'trust': s.trust,
                'emp_affected': getattr(s, 'emp_affected', False)
            }
            for s in simulation_engine.satellites[:500]  # Sample for performance
        ]

        uavs_data = [
            {
                'id': u.id,
                'pos': u.pos.tolist(),
                'health': u.health,
                'fuel_level': u.fuel_level,
                'emp_affected': getattr(u, 'emp_affected', False),
                'emergency_landing': getattr(u, 'emergency_landing', False)
            }
            for u in simulation_engine.uavs
        ]

        twins_data = [
            {
                'id': t.id,
                'type': t.type,
                'status': t.status,
                'cpu_load': t.cpu_load
            }
            for t in simulation_engine.all_twins
        ]

        # Update state
        self.update_simulation_state(
            satellites=satellites_data,
            uavs=uavs_data,
            twins=twins_data,
            emp_events=simulation_engine.emp_system.active_emp_events,
            performance=simulation_engine.performance_stats,
            cycle=simulation_engine.performance_stats.get('current_cycle', 0)
        )

        # Broadcast to WebSocket clients
        await self.broadcast_update('simulation_update', self.get_current_snapshot())


# Standalone server for testing
async def main():
    """Run standalone server for testing"""
    connector = MotorhandProConnector()
    await connector.start_server()

    # Keep server running
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    print("🌌 Motorhand Pro Connector - Standalone Mode")
    print("=" * 80)

    if not AIOHTTP_AVAILABLE:
        print("Error: aiohttp not installed")
        print("Install with: pip install aiohttp aiohttp-cors")
    else:
        asyncio.run(main())

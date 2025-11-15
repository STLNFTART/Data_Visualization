# Motorhand Pro Integration - Data Visualization Repository

## 🌌 Overview

This repository now integrates with **Motorhand Pro** to provide real-time visualization and monitoring of complex multi-domain simulations, specifically focused on:

- **Satellite Constellation Management** (150,000+ satellites)
- **EMP Threat Response Systems**
- **Autonomous UAV Swarm Coordination** (150 UAVs)
- **Digital Twin Network Operations** (40 twins)
- **Multi-Algorithm Framework** (IPU, Temporal, Sovereign, JPL, Primal Logic)

## 📦 What's Included

### Core Components

1. **EMP_Multiswarm_Simulation.py**
   - Complete simulation framework with 5 advanced algorithms
   - EMP weapon systems with area-of-effect damage
   - Flight response and evasive maneuver systems
   - Satellite, UAV, and Digital Twin entities

2. **Motorhand_Pro_Connector.py**
   - WebSocket server for real-time data streaming
   - REST API for historical data queries
   - JSON export capabilities
   - 3D visualization data formatting

3. **Practical_Use_Case_Satellite_Constellation_Monitoring.py**
   - Complete working example
   - Demonstrates satellite constellation monitoring
   - Shows EMP threat response training
   - Integrates with Motorhand Pro dashboard

4. **motorhand_pro_config.json**
   - Configuration file for integration
   - API endpoint definitions
   - Algorithm descriptions
   - Practical application specifications

## 🚀 Quick Start

### Installation

```bash
# Install required dependencies
pip install numpy matplotlib aiohttp aiohttp-cors

# Clone this repository
cd Data_Visualization
```

### Running the Satellite Constellation Monitor

```bash
# Run the practical use case example
python Practical_Use_Case_Satellite_Constellation_Monitoring.py
```

This will:
1. Initialize a satellite constellation with 5,000 satellites and 50 UAVs
2. Start the Motorhand Pro WebSocket server on port 8000
3. Run the simulation with real-time threat detection
4. Stream data to connected Motorhand Pro dashboards

### Accessing the Motorhand Pro Dashboard

Once running, you can access:

- **WebSocket Stream**: `ws://localhost:8000/ws`
- **REST API Base**: `http://localhost:8000/api/v1/`
- **Simulation Status**: `http://localhost:8000/api/v1/simulation/status`
- **Health Check**: `http://localhost:8000/api/v1/health`

## 🎯 Practical Use Cases

### 1. Satellite Constellation Management

**Industry**: Commercial Satellite Operators (SpaceX, Amazon, OneWeb)

**Application**: Monitor and manage large LEO/MEO satellite networks in real-time

**Business Value**:
- Prevent collisions in congested orbital shells
- Optimize constellation health and performance
- Reduce operational costs through automated monitoring
- Improve network uptime and reliability

**Usage**:
```python
from Practical_Use_Case_Satellite_Constellation_Monitoring import SatelliteConstellationMonitor
import asyncio

async def run_constellation_monitoring():
    monitor = SatelliteConstellationMonitor(
        satellite_count=150000,  # Full Starlink-scale constellation
        uav_count=150,
        simulation_cycles=64800   # 36 hours of simulation
    )
    await monitor.initialize_motorhand_pro(host='0.0.0.0', port=8000)
    await monitor.run_with_motorhand_pro()

asyncio.run(run_constellation_monitoring())
```

### 2. EMP Threat Response Training

**Industry**: Defense, Military, Critical Infrastructure

**Application**: Train operators on electromagnetic pulse attack scenarios

**Business Value**:
- Prepare for extreme threat scenarios
- Test infrastructure resilience
- Develop response protocols
- Reduce recovery time after EMP events

**Features**:
- Realistic EMP blast propagation (500km range)
- Damage assessment based on distance and shielding
- Recovery time simulation (300 seconds average)
- Multiple EMP source types (Nuclear, HERF, Solar Flare, Cyber)

### 3. Space Traffic Management

**Industry**: Space Agencies (NASA, ESA, ROSCOSMOS)

**Application**: Manage crowded orbital environments and prevent collisions

**Business Value**:
- Ensure safety of crewed missions
- Protect valuable space assets
- Comply with international space regulations
- Enable sustainable space operations

**Collision Detection**:
- Real-time proximity alerts (10km threshold)
- Relative velocity calculations
- Time-to-collision estimates
- Automated evasive maneuvers

### 4. Autonomous UAV Swarm Coordination

**Industry**: Defense, Agriculture, Logistics, Search & Rescue

**Application**: Test and validate coordinated UAV swarm behaviors

**Business Value**:
- Optimize mission efficiency
- Reduce operator workload
- Improve swarm resilience
- Enable complex multi-agent operations

**Swarm Features**:
- 55,000 micro-movements per UAV
- JPL autonomous control algorithms
- Emergency landing protocols
- Fuel management and constraints

### 5. Digital Twin Network Operations

**Industry**: IoT, Smart Cities, Industrial Automation

**Application**: Simulate and optimize distributed sensor networks

**Business Value**:
- Predict network failures before they occur
- Optimize resource allocation
- Test algorithm performance
- Reduce downtime and maintenance costs

**Digital Twin Types**:
- DDPS (Data Distribution and Processing System)
- GNSS (Global Navigation Satellite System)
- URC (Universal Radio Communication)
- NGSR (Next Generation Sensor Relay)

## 📊 API Reference

### REST API Endpoints

#### GET /api/v1/simulation/status
Get current simulation status
```json
{
  "status": "running",
  "cycle": 1234,
  "timestamp": "2025-11-15T22:30:00Z",
  "connected_clients": 3
}
```

#### GET /api/v1/entities/{entity_type}
Get entity data (satellites, uavs, digital_twins)

Query Parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 100)

```json
{
  "entity_type": "satellites",
  "total_count": 5000,
  "page": 1,
  "per_page": 100,
  "data": [...]
}
```

#### GET /api/v1/algorithms/{algorithm_type}
Get algorithm results (ipu, temporal_processor, sovereign_kernel, jpl, primal_logic)

```json
{
  "algorithm_type": "ipu",
  "results": {
    "resource_imbalance": 0.234,
    "processing_pressure": 0.456,
    "system_efficiency": 0.876,
    "optimization_recommendation": "OPTIMAL_PERFORMANCE"
  }
}
```

#### GET /api/v1/threats/emp
Get active EMP events

```json
{
  "emp_events": [
    {
      "id": "EMP_1234_0",
      "position": [1000.0, 2000.0, 500.0],
      "range": 500.0,
      "intensity": 0.85,
      "source_type": "NUCLEAR_EMP"
    }
  ],
  "count": 1,
  "timestamp": "2025-11-15T22:30:00Z"
}
```

#### GET /api/v1/threats/all
Get all threat types

#### GET /api/v1/visualization/snapshot
Get current visualization snapshot

#### GET /api/v1/health
Health check endpoint

### WebSocket API

#### Connect
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

#### Subscribe to Updates
```javascript
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['simulation_update', 'emp_events', 'collision_alerts']
}));
```

#### Receive Updates
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update type:', data.type);
  console.log('Data:', data.data);
  console.log('Timestamp:', data.timestamp);
};
```

## 🧠 Algorithm Framework

### 1. IPU (Intelligent Processing Unit)
- **Purpose**: Resource optimization and market analysis
- **Use Case**: Optimize satellite CPU/memory/network usage
- **Key Metrics**: Resource imbalance (e(t)), Processing pressure (Θ(t))

### 2. Temporal Processor
- **Purpose**: Time-series signal processing with latency optimization
- **Use Case**: Analyze satellite communication signals
- **Key Metrics**: Signal quality score, Latency anomalies

### 3. Sovereign Kernel
- **Purpose**: Multi-sensor fusion and anomaly detection
- **Use Case**: Combine data from multiple satellites for consensus
- **Key Metrics**: Fusion confidence, System health status

### 4. JPL (Jet Propulsion Laboratory)
- **Purpose**: Autonomous vehicle control and trajectory optimization
- **Use Case**: Control UAV flight paths with PID controllers
- **Key Metrics**: Position error, Trajectory smoothness, Safety score

### 5. Primal Logic
- **Purpose**: Trust vector analysis and consensus decision-making
- **Use Case**: Determine which satellites to trust for critical decisions
- **Key Metrics**: Trust score, Consensus reached, Network health

## 🔧 Configuration

Edit `motorhand_pro_config.json` to customize:

- API endpoints and ports
- Algorithm parameters
- Performance targets
- Integration modes
- Export formats

## 📈 Performance Considerations

### Scaling
- **Small Demo**: 5,000 satellites, 50 UAVs (< 1 GB RAM)
- **Medium Scale**: 50,000 satellites, 100 UAVs (~ 4 GB RAM)
- **Full Scale**: 150,000 satellites, 150 UAVs (~ 12 GB RAM)

### Optimization Tips
1. Adjust `BATCH_SIZE` in simulation code for performance
2. Reduce `VISUALIZATION_SAMPLE` for faster rendering
3. Use `page` and `per_page` parameters in API queries
4. Enable/disable EMP and flight response systems as needed

## 🛠️ Development

### Adding New Algorithms

1. Create algorithm class extending `BaseAlgorithm`
2. Implement `process()` and `update_state()` methods
3. Add to `UnifiedFramework.algorithms` dictionary
4. Update `motorhand_pro_config.json`

### Adding New Entity Types

1. Create entity class with required attributes
2. Add to simulation engine initialization
3. Update Motorhand Pro connector streaming logic
4. Add API endpoint for new entity type

### Customizing Visualization

Edit `create_visualization()` method in practical use case files:
- Change colors, sizes, markers
- Add new plot types
- Modify update frequency
- Export to different formats

## 🐛 Troubleshooting

### WebSocket Connection Fails
```bash
# Check if port 8000 is available
lsof -i :8000

# Try different port
monitor.initialize_motorhand_pro(host='0.0.0.0', port=8080)
```

### High Memory Usage
```python
# Reduce entity counts
monitor = SatelliteConstellationMonitor(
    satellite_count=1000,  # Reduced from 5000
    uav_count=10,          # Reduced from 50
    simulation_cycles=100  # Reduced from 1000
)
```

### Slow Visualization
```python
# Increase visualization interval
if cycle % 100 != 0:  # Changed from % 50
    return  # Skip visualization
```

## 📚 Additional Resources

### Related Files in Repository
- `3D_Display_Mathematical_Calculations.py` - 3D mathematical visualization
- `3D_Trigonometric_Relationship.py` - Trigonometric function visualization
- `01.3D_Graph_Visualizations.py` - General 3D plotting examples

### Documentation
- [Motorhand Pro Configuration](motorhand_pro_config.json)
- [Simulation Module](EMP_Multiswarm_Simulation.py)
- [Connector API](Motorhand_Pro_Connector.py)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional algorithm implementations
- New practical use cases
- Performance optimizations
- Enhanced visualization options
- Integration with other platforms

## 📄 License

MIT License - see repository root for details

## 🙋 Support

For questions or issues:
1. Check this README and configuration files
2. Review practical use case examples
3. Open an issue in the repository
4. Contact the development team

---

**Built with:** Python, NumPy, Matplotlib, asyncio, aiohttp
**Optimized for:** Motorhand Pro visualization platform
**Industry Applications:** Aerospace, Defense, IoT, Smart Cities, Space Operations

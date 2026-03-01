# mitigation_module/network_config.py
"""
DYNAMIC NETWORK CONFIGURATION - NO HARDCODING
All routes are generated dynamically based on warehouse and hub configuration
"""

# =========================================
# DYNAMIC WAREHOUSE CONFIGURATION
# =========================================
# Can be expanded dynamically - just add warehouses here!
WAREHOUSES = {
    "Warehouse_North": {"capacity": 3000, "location": "North", "priority": 1},
    "Warehouse_South": {"capacity": 3000, "location": "South", "priority": 2},
    "Warehouse_East": {"capacity": 2500, "location": "East", "priority": 3},
    "Warehouse_West": {"capacity": 2500, "location": "West", "priority": 4},
    "Warehouse_Central": {"capacity": 3500, "location": "Central", "priority": 5}
}

# =========================================
# INTERMEDIATE DISTRIBUTION HUBS
# For multi-hop routing optimization
# =========================================
DISTRIBUTION_HUBS = {
    "Hub_Northeast": {"location": "Northeast", "max_throughput": 5000},
    "Hub_Midwest": {"location": "Midwest", "max_throughput": 4500},
    "Hub_Southeast": {"location": "Southeast", "max_throughput": 4000}
}

# =========================================
# PREDEFINED CITIES (Legacy Support)
# Default demand for known cities
# =========================================
DEMAND_REQ = {
    "Boston": 250, 
    "New York": 400, 
    "Chicago": 300, 
    "Philadelphia": 400, 
    "Miami": 200, 
    "Dallas": 350
}

# =========================================
# DYNAMIC ROUTE GENERATION
# Routes are NO LONGER hardcoded!
# They are generated dynamically in dynamic_network.py
# =========================================
# Legacy route_map for backward compatibility (Routes 1-10)
# These are the ONLY hardcoded routes (for CSV data compatibility)
route_map = {
    1: ("Warehouse_North", "Boston"),
    2: ("Warehouse_North", "New York"),
    3: ("Warehouse_North", "Chicago"),
    4: ("Warehouse_South", "Boston"),
    5: ("Warehouse_North", "Philadelphia"),
    6: ("Warehouse_South", "Chicago"),
    7: ("Warehouse_South", "New York"),
    8: ("Warehouse_South", "Philadelphia"),
    9: ("Warehouse_North", "Miami"),
    10: ("Warehouse_North", "Dallas")
}

# Primary routes (for risk application logic)
PRIMARY_ROUTES = {1, 2, 3, 5, 9, 10}

# Dynamic routes start from ID 100
DYNAMIC_ROUTE_START_ID = 100

# Multi-hop routes start from ID 1000
MULTIHOP_ROUTE_START_ID = 1000

# Backward compatibility
ROUTE_MAP = route_map
SUPPLY_CAPACITY = {name: info["capacity"] for name, info in WAREHOUSES.items()}
SOURCES = list(WAREHOUSES.keys())
DESTINATIONS = list(DEMAND_REQ.keys())

def get_total_warehouse_capacity():
    """Calculate total capacity across all warehouses"""
    return sum(info["capacity"] for info in WAREHOUSES.values())

def get_warehouse_list():
    """Get list of all warehouse names sorted by priority"""
    return sorted(WAREHOUSES.keys(), key=lambda x: WAREHOUSES[x]["priority"])

def get_hub_list():
    """Get list of all distribution hub names"""
    return list(DISTRIBUTION_HUBS.keys())

def validate_network():
    """Validate network configuration including dynamic routes"""
    from mitigation_module.dynamic_network import get_full_route_map
    
    total_supply = get_total_warehouse_capacity()
    total_demand = sum(DEMAND_REQ.values())
    
    # Get full route map including dynamic routes
    full_map = get_full_route_map(include_dynamic=True, include_multihop=True)
    
    # Count route types
    direct_routes = sum(1 for route in full_map.values() if len(route) == 2)
    multihop_routes = sum(1 for route in full_map.values() if len(route) == 3)
    
    return {
        "total_supply": total_supply,
        "total_demand": total_demand,
        "surplus": total_supply - total_demand,
        "num_routes": len(route_map),
        "num_total_routes": len(full_map),
        "num_direct_routes": direct_routes,
        "num_multihop_routes": multihop_routes,
        "num_warehouses": len(WAREHOUSES),
        "num_hubs": len(DISTRIBUTION_HUBS),
        "num_clients": len(DEMAND_REQ),
        "dynamic_routing": "ENABLED"
    }

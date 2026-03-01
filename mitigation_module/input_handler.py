import json
import re

# Indian Cities (Major cities for detection)
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Bengaluru", "Hyderabad", "Chennai", 
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", 
    "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam",
    "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana",
    "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi",
    "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai",
    "Allahabad", "Prayagraj", "Ranchi", "Howrah", "Coimbatore", "Jabalpur",
    "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota"
]

# Current USD to INR exchange rate (as of Feb 2026)
USD_TO_INR_RATE = 83.50

def extract_quantity(user_text):
    """
    Extracts quantity/units from user input.
    Examples: "500 units", "1,000 units", "250 unit"
    Returns: integer or None
    """
    patterns = [
        r'(\d+(?:,\d{3})*)\s*units?',  # "500 units" or "1,000 unit"
        r'ship\s+(\d+(?:,\d{3})*)',     # "ship 500"
        r'deliver\s+(\d+(?:,\d{3})*)',  # "deliver 500"
        r'(\d+(?:,\d{3})*)\s*(?:pieces|items|boxes|pallets)',  # other quantity words
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_text, re.IGNORECASE)
        if match:
            qty_str = match.group(1).replace(',', '')
            qty = int(qty_str)
            print(f"[INPUT PARSER] Extracted quantity: {qty} units")
            return qty
    
    return None

def is_indian_city(city_name):
    """
    Check if the given city is an Indian city.
    Returns: True if Indian city, False otherwise
    """
    if not city_name:
        return False
    return city_name in INDIAN_CITIES

def extract_budget(user_text):
    """
    Extracts budget/cost limit from user input.
    NOW SUPPORTS: USD ($) and INR (₹/Rs/Rupees)
    Examples: "$10,000", "Rs 50,000", "₹1,00,000", "budget of $5000"
    Returns: dict with 'amount' and 'currency' or None
    """
    # Patterns for USD
    usd_patterns = [
        r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # "$10,000" or "$10000.00"
        r'budget\s+(?:of\s+)?\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',  # "budget of $5000"
        r'max(?:imum)?\s+cost\s+\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',  # "max cost 15000"
        r'under\s+\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',  # "under $10000"
    ]
    
    # Patterns for INR (Indian Rupees)
    inr_patterns = [
        r'₹\s*(\d+(?:,\d{2,3})*(?:\.\d{2})?)',  # "₹50,000" or "₹1,00,000"
        r'Rs\.?\s*(\d+(?:,\d{2,3})*(?:\.\d{2})?)',  # "Rs 50000" or "Rs. 50,000"
        r'rupees?\s+(\d+(?:,\d{2,3})*(?:\.\d{2})?)',  # "rupees 50000"
        r'INR\s*(\d+(?:,\d{2,3})*(?:\.\d{2})?)',  # "INR 50000"
    ]
    
    # Check for INR first
    for pattern in inr_patterns:
        match = re.search(pattern, user_text, re.IGNORECASE)
        if match:
            budget_str = match.group(1).replace(',', '')
            budget = float(budget_str)
            print(f"[INPUT PARSER] Extracted budget: ₹{budget:,.2f}")
            return {'amount': budget, 'currency': 'INR'}
    
    # Check for USD
    for pattern in usd_patterns:
        match = re.search(pattern, user_text, re.IGNORECASE)
        if match:
            budget_str = match.group(1).replace(',', '')
            budget = float(budget_str)
            print(f"[INPUT PARSER] Extracted budget: ${budget:,.2f}")
            return {'amount': budget, 'currency': 'USD'}
    
    return None

def extract_date(user_text):
    """
    Extracts delivery date from user input.
    Examples: "on Feb 4th", "by February 10", "deliver March 15"
    Returns: string or None
    """
    patterns = [
        r'(?:on|by|before)\s+([A-Z][a-z]+\s+\d{1,2}(?:st|nd|rd|th)?)',  # "on Feb 4th"
        r'(?:on|by|before)\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)',  # "by 2/4" or "by 2/4/2026"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            print(f"[INPUT PARSER] Extracted date: {date_str}")
            return date_str
    
    return None

def extract_priority(user_text):
    """
    Extracts priority/urgency keywords.
    Examples: "urgent", "expedited", "express", "standard"
    Returns: string or None
    """
    text_lower = user_text.lower()
    
    priority_keywords = {
        'urgent': 'URGENT',
        'emergency': 'URGENT',
        'critical': 'URGENT',
        'expedited': 'EXPEDITED',
        'express': 'EXPEDITED',
        'rush': 'EXPEDITED',
        'fast': 'EXPEDITED',
        'standard': 'STANDARD',
        'normal': 'STANDARD',
        'regular': 'STANDARD'
    }
    
    for keyword, priority_level in priority_keywords.items():
        if keyword in text_lower:
            print(f"[INPUT PARSER] Detected priority: {priority_level}")
            return priority_level
    
    return None

def extract_shipment_requirements(user_text):
    """
    MAIN FUNCTION: Extracts ALL shipment requirements from user input.
    NOW SUPPORTS: Indian cities and currency conversion!
    
    Input: "I need to ship 500 units to Mumbai with budget Rs 50,000"
    Output: {
        'destination': 'Mumbai',
        'quantity': 500,
        'budget': 50000.0,
        'currency': 'INR',
        'is_indian_city': True,
        'date': None,
        'priority': None
    }
    """
    print(f"\n[INPUT PARSER] Analyzing user input: {user_text}")
    
    destination = extract_shipment_plan_city(user_text)
    budget_info = extract_budget(user_text)
    is_indian = is_indian_city(destination)
    
    # Handle budget and currency
    budget_amount = None
    currency = None
    
    if budget_info:
        budget_amount = budget_info['amount']
        currency = budget_info['currency']
        
        # Auto-detect currency based on city if not explicitly stated
        if destination and not currency:
            currency = 'INR' if is_indian else 'USD'
        
        # Convert USD to INR for Indian cities if budget was given in USD
        if is_indian and currency == 'USD':
            budget_amount = budget_amount * USD_TO_INR_RATE
            print(f"[INPUT PARSER] Converted budget: ${budget_info['amount']:,.2f} → ₹{budget_amount:,.2f}")
            currency = 'INR'
    else:
        # Auto-set currency based on destination
        currency = 'INR' if is_indian else 'USD'
    
    requirements = {
        'destination': destination,
        'quantity': extract_quantity(user_text),
        'budget': budget_amount,
        'currency': currency,
        'is_indian_city': is_indian,
        'date': extract_date(user_text),
        'priority': extract_priority(user_text)
    }
    
    if is_indian:
        print(f"[INPUT PARSER] 🇮🇳 Indian city detected: {destination} - Using INR currency")
    
    print(f"[INPUT PARSER] Parsed requirements: {requirements}")
    return requirements

def extract_shipment_plan_city(user_text):
    """
    Parses the user's shipment plan to find the destination city.
    NOW SUPPORTS ANY CITY NAME (for GDELT integration)
    Input: "I need to ship 500 units to Boston on Feb 4th."
    Output: "Boston"
    """
    text_lower = user_text.lower()
    
    # We map common text inputs to our internal City Keys
    known_cities = {
        "boston": "Boston",
        "new york": "New York",
        "chicago": "Chicago",
        "philadelphia": "Philadelphia",
        "nyc": "New York",
        "philly": "Philadelphia",
        "miami": "Miami",
        "dallas": "Dallas",
        # Indian cities with common variations
        "mumbai": "Mumbai",
        "delhi": "Delhi",
        "bangalore": "Bangalore",
        "bengaluru": "Bangalore",
        "hyderabad": "Hyderabad",
        "chennai": "Chennai",
        "kolkata": "Kolkata",
        "pune": "Pune",
        "ahmedabad": "Ahmedabad",
        "jaipur": "Jaipur"
    }
    
    # First, check known cities (optimized routes)
    for key, city_name in known_cities.items():
        if key in text_lower:
            return city_name
    
    # NEW: Extract any capitalized city name (for GDELT)
    # Pattern: "to <City>" or "in <City>"
    import re
    patterns = [
        r'to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # "to Seattle" or "to Los Angeles"
        r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # "in Seattle"
        r'destination[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'  # "destination: Seattle"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_text)
        if match:
            city_name = match.group(1)
            return city_name
    
    return None

def extract_shipment_plan(user_text):
    """
    LEGACY WRAPPER: For backward compatibility.
    Use extract_shipment_requirements() for new code.
    """
    return extract_shipment_plan_city(user_text)

def extract_risk_info(user_input_text):
    """
    LEGACY function for backward compatibility with old disruption extraction
    Kept for any code that still calls this function
    """
    text_lower = user_input_text.lower()
    
    detected_data = {}
    
    if "bridge" in text_lower or "collapse" in text_lower:
        detected_data = {"target_route_id": [1, 5], "impact_type": "Infrastructure Collapse", "cost_multiplier": 20.0}
    elif "spill" in text_lower or "chemical" in text_lower:
        detected_data = {"target_route_id": [3, 5], "impact_type": "Toxic Spill", "cost_multiplier": 10.0}
    elif "strike" in text_lower or "jfk" in text_lower:
        detected_data = {"target_route_id": [2], "impact_type": "Labor Strike", "cost_multiplier": 5.0}
    else:
        detected_data = {"target_route_id": [1, 3], "impact_type": "Generic Delay", "cost_multiplier": 2.0}

    return [detected_data]


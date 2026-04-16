import json
import pandas as pd
from datetime import datetime
import streamlit as st

# File paths
DATA_DIR = "data"
STATE_FILE = f"{DATA_DIR}/valuation_state.json"

def save_state(data):
    """Save valuation state to JSON file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        st.error(f"Error saving state: {e}")
        return False

def load_state():
    """Load valuation state from JSON file"""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        st.error(f"Error loading state: {e}")
        return {}

def format_currency(value, suffix="M"):
    """Format number as currency"""
    return f"${value:,.0f}{suffix}"

def format_percentage(value):
    """Format number as percentage"""
    return f"{value:.2%}"

def calculate_growth_rate(current, previous):
    """Calculate growth rate between two values"""
    if previous == 0:
        return 0
    return (current - previous) / previous

def get_current_timestamp():
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
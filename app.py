# CEP Policy Intelligence Platform - ENHANCED v2
# Phase 2 Enhancements:
# 1. New interactive US map with full state names and bold color categories
# 2. Redesigned Explore States panel with state flags and category grouping
# 3. Consistency fix applied to ALL state pages (map/table status alignment)

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import pandas as pd

application = dash.Dash(__name__, suppress_callback_exceptions=True)
server = application.server

# Enhanced Color System with NEW bold, high-contrast map categories
COLORS = {
    'navy': '#1e40af', 'indigo': '#4f46e5', 'teal': '#047857', 'teal_light': '#0891b2',
    'charcoal': '#334155', 'slate': '#64748b', 'forest_green': '#065f46', 'emerald': '#059669',
    'white': '#ffffff', 'off_white': '#f8f9fa', 'light_gray': '#f1f3f5', 'border': '#dee2e6',
    'text_primary': '#1a1a1a', 'text_secondary': '#6c757d',
    # CEP Status - Shared across map and table
    'full_cep': '#10b981',  # Green
    'partial_cep': '#fbbf24',  # Yellow  
    'no_cep': '#ef4444',  # Red
    # Political Party - For executive names
    'democrat_name': '#1d4ed8',  # Blue
    'republican_name': '#991b1b',  # Maroon
    # NEW: Bold Map Categories (high-contrast for easy distinction)
    'universal_meals': '#059669',  # Bold emerald green
    'universal_breakfast': '#f59e0b',  # Bold amber/orange
    'fpl_states': '#3b82f6',  # Bold blue - Federal Poverty Level states
    'other_states': '#cbd5e1'  # Light slate gray
}

# STATE MEAL PROGRAM CATEGORIES (Updated March 2026)
STATE_CATEGORIES = {
    'universal_meals': ['CA', 'ME', 'CO', 'NM', 'MI', 'MN', 'MA', 'VT', 'NY'],  # 9 states with free breakfast + lunch
    'universal_breakfast': ['AR', 'DE', 'PA'],  # 3 states with free breakfast only (added DE - Delaware)
    'fpl_states': ['HI', 'NJ', 'ND']  # 3 states with Federal Poverty Level eligibility
}

# FPL percentages for hover display on landing page
FPL_PERCENTAGES = {
    'HI': '300% of FPL',
    'NJ': '225% of FPL',
    'ND': '225% of FPL'
}

# State flag icons as inline SVG (simple, reliable, no external dependencies)
STATE_FLAGS = {
    'WI': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMzYTAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzM2EwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+V0k8L3RleHQ+PC9zdmc+',
    'NJ': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNkNWE1MzMiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjZDVhNTMzIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+Tko8L3RleHQ+PC9zdmc+',
    'VA': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDJhNmEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAyYTZhIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+VkE8L3RleHQ+PC9zdmc+',
    'SC': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDJhNmEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAyYTZhIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+U0M8L3RleHQ+PC9zdmc+',
    'NV': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMzYTAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmMiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzM2EwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+TlY8L3RleHQ+PC9zdmc+',
    'AR': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNiZDAwMjEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjYmQwMDIxIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+QVI8L3RleHQ+PC9zdmc+'
}

# ====================
# SHARED HELPERS - SINGLE SOURCE OF TRUTH
# ====================

def get_party_color(party):
    """Get color for executive NAME based on party"""
    if party == 'Democrat':
        return COLORS['democrat_name']
    elif party == 'Republican':
        return COLORS['republican_name']
    return COLORS['text_primary']

def normalize_status(status_str):
    """Normalize status - used by map, table, and summaries - SINGLE SOURCE OF TRUTH"""
    if not status_str:
        return 'NO CEP'
    status_upper = str(status_str).upper().strip()
    if 'FULL' in status_upper:
        return 'FULL CEP'
    elif 'PARTIAL' in status_upper:
        return 'PARTIAL CEP'
    return 'NO CEP'

def get_status_color(status):
    """Get color for status badge/map"""
    normalized = normalize_status(status)
    if normalized == 'FULL CEP':
        return COLORS['full_cep']
    elif normalized == 'PARTIAL CEP':
        return COLORS['partial_cep']
    else:
        return COLORS['no_cep']

def status_to_numeric(status):
    """Convert status to numeric for map coloring (0=No, 1=Partial, 2=Full)"""
    normalized = normalize_status(status)
    if normalized == 'FULL CEP':
        return 2
    elif normalized == 'PARTIAL CEP':
        return 1
    return 0

def get_state_category(state_abbr):
    """Get meal program category for a state"""
    if state_abbr in STATE_CATEGORIES['universal_meals']:
        return 'universal_meals'
    elif state_abbr in STATE_CATEGORIES['universal_breakfast']:
        return 'universal_breakfast'
    elif state_abbr in STATE_CATEGORIES.get('fpl_states', []):
        return 'fpl_states'
    return 'other'

def get_state_category_color(state_abbr):
    """Get map color based on state meal program category"""
    category = get_state_category(state_abbr)
    if category == 'universal_meals':
        return COLORS['universal_meals']
    elif category == 'universal_breakfast':
        return COLORS['universal_breakfast']
    return COLORS['other_states']

# ====================
# DATA LOADING
# ====================

def load_wisconsin_data():
    """Load complete Wisconsin county data - 72 counties, all 11 columns"""
    data = {
        'County': ['Milwaukee', 'Dane', 'Waukesha', 'Brown', 'Racine', 'Outagamie', 'Kenosha', 'Rock', 'Winnebago', 'Marathon', 'Washington', 'Ozaukee', 'Sheboygan', 'La Crosse', 'Fond du Lac', 'Eau Claire', 'Walworth', 'Wood', 'St. Croix', 'Dodge', 'Jefferson', 'Portage', 'Barron', 'Chippewa', 'Grant', 'Columbia', 'Manitowoc', 'Sauk', 'Shawano', 'Clark', 'Pierce', 'Polk', 'Waupaca', 'Waushara', 'Adams', 'Green', 'Marinette', 'Dunn', 'Douglas', 'Juneau', 'Trempealeau', 'Monroe', 'Vernon', 'Calumet', 'Sawyer', 'Crawford', 'Richland', 'Jackson', 'Iowa', 'Green Lake', 'Burnett', 'Rusk', 'Ashland', 'Marquette', 'Lafayette', 'Bayfield', 'Oneida', 'Taylor', 'Vilas', 'Price', 'Lincoln', 'Door', 'Langlade', 'Washburn', 'Iron', 'Buffalo', 'Pepin', 'Forest', 'Florence', 'Menominee', 'Kewaunee', 'Oconto'],
        'Population': [945726, 546695, 404198, 264542, 195859, 187885, 169151, 163687, 171631, 134932, 136761, 91907, 115340, 118498, 103403, 104205, 106295, 72795, 93369, 88759, 84748, 70919, 45870, 66018, 52496, 57920, 79795, 65243, 41949, 34772, 41521, 43548, 51812, 24443, 20875, 37093, 42663, 45368, 44159, 26664, 30760, 46253, 30760, 50089, 18526, 16260, 17304, 20449, 23687, 18291, 16093, 14188, 12890, 15592, 16516, 15014, 35998, 20461, 22643, 13321, 28171, 27722, 19189, 16866, 5687, 13390, 7469, 9024, 4295, 4255, 20563, 38000],
        'Children_in_Poverty': [81246, 37254, 15779, 17627, 15826, 11835, 14528, 12958, 10835, 8654, 5179, 2689, 7072, 7657, 6382, 6694, 6525, 5043, 3643, 5433, 4848, 4335, 3328, 4038, 3414, 3544, 4888, 3991, 3229, 2678, 2028, 2666, 3172, 1885, 1607, 2271, 2611, 2776, 2702, 2054, 1883, 2833, 1883, 3072, 1428, 996, 1060, 1252, 1450, 1119, 985, 868, 789, 954, 1011, 919, 2204, 1252, 1386, 815, 1724, 1697, 1174, 1032, 348, 820, 457, 552, 263, 260, 1259, 2327],
        'School_Districts': [23, 17, 15, 12, 8, 10, 6, 7, 9, 11, 6, 5, 6, 7, 8, 7, 6, 5, 8, 6, 7, 6, 4, 5, 5, 6, 5, 6, 5, 4, 5, 5, 6, 4, 3, 4, 4, 5, 4, 4, 4, 5, 4, 5, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 5, 3, 4, 3, 4, 4, 3, 3, 2, 3, 2, 2, 2, 1, 4, 5],
        'Eligible_Schools': [187, 89, 42, 56, 41, 38, 35, 32, 37, 32, 21, 15, 24, 27, 25, 24, 23, 19, 17, 21, 22, 20, 13, 16, 15, 17, 19, 18, 14, 11, 10, 13, 15, 9, 8, 11, 12, 13, 12, 10, 9, 14, 9, 15, 7, 6, 6, 8, 9, 7, 6, 6, 5, 7, 7, 6, 12, 8, 9, 5, 10, 10, 8, 7, 3, 6, 3, 4, 3, 2, 8, 11],
        'CEP_Schools': [124, 68, 12, 38, 29, 24, 27, 22, 25, 18, 9, 4, 14, 19, 15, 17, 12, 11, 8, 12, 13, 12, 7, 9, 8, 10, 11, 10, 8, 6, 5, 7, 9, 5, 4, 6, 7, 8, 7, 6, 5, 8, 5, 9, 4, 3, 3, 5, 5, 4, 3, 3, 3, 4, 4, 3, 7, 5, 5, 3, 6, 6, 6, 4, 2, 3, 2, 2, 2, 2, 5, 6],
        'Students_in_CEP': [52438, 28956, 4128, 15748, 11954, 9912, 11151, 9086, 10325, 7434, 3717, 1651, 5782, 7843, 6195, 7023, 4956, 4543, 3304, 4956, 5369, 4956, 2891, 3718, 3304, 4130, 4543, 4130, 3304, 2478, 2065, 2891, 3718, 2065, 1652, 2478, 2891, 3304, 2891, 2478, 2065, 3304, 2065, 3718, 1652, 1239, 1239, 2065, 2065, 1652, 1239, 1239, 1239, 1652, 1652, 1239, 2891, 2065, 2065, 1239, 2478, 2478, 2478, 1652, 826, 1239, 826, 826, 826, 826, 2065, 2478],
        'Coverage_Pct': [65, 78, 26, 89, 75, 84, 77, 70, 95, 86, 72, 61, 82, 102, 99, 105, 76, 90, 91, 91, 111, 114, 89, 92, 97, 117, 93, 103, 106, 93, 102, 109, 117, 110, 103, 109, 111, 119, 107, 121, 110, 117, 110, 121, 116, 124, 117, 165, 142, 148, 126, 143, 157, 173, 163, 135, 131, 165, 149, 152, 144, 146, 211, 160, 237, 151, 181, 150, 315, 318, 164, 106],
        'Status': ['PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'FULL CEP', 'PARTIAL CEP', 'FULL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'FULL CEP', 'FULL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP']
    }
    df = pd.DataFrame(data)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    # CONSISTENCY FIX: Normalize status using shared function
    df['Status'] = df['Status'].apply(normalize_status)
    # Add numeric status for map
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df

WI_FIPS = {'Milwaukee': '55079', 'Dane': '55025', 'Waukesha': '55133', 'Brown': '55009', 'Racine': '55101', 'Outagamie': '55087', 'Kenosha': '55059', 'Rock': '55105', 'Winnebago': '55139', 'Marathon': '55073', 'Washington': '55131', 'Ozaukee': '55089', 'Sheboygan': '55117', 'La Crosse': '55063', 'Fond du Lac': '55039', 'Eau Claire': '55035', 'Walworth': '55127', 'Wood': '55141', 'St. Croix': '55109', 'Dodge': '55027', 'Jefferson': '55055', 'Portage': '55097', 'Barron': '55005', 'Chippewa': '55017', 'Grant': '55043', 'Columbia': '55021', 'Manitowoc': '55071', 'Sauk': '55111', 'Shawano': '55115', 'Clark': '55019', 'Pierce': '55093', 'Polk': '55095', 'Waupaca': '55135', 'Waushara': '55137', 'Adams': '55001', 'Green': '55045', 'Marinette': '55075', 'Dunn': '55033', 'Douglas': '55031', 'Juneau': '55057', 'Trempealeau': '55121', 'Monroe': '55081', 'Vernon': '55123', 'Calumet': '55015', 'Sawyer': '55113', 'Crawford': '55023', 'Richland': '55103', 'Jackson': '55053', 'Iowa': '55049', 'Green Lake': '55047', 'Burnett': '55013', 'Rusk': '55107', 'Ashland': '55003', 'Marquette': '55077', 'Lafayette': '55065', 'Bayfield': '55007', 'Oneida': '55085', 'Taylor': '55119', 'Vilas': '55125', 'Price': '55099', 'Lincoln': '55069', 'Door': '55029', 'Langlade': '55067', 'Washburn': '55129', 'Iron': '55051', 'Buffalo': '55011', 'Pepin': '55091', 'Forest': '55041', 'Florence': '55037', 'Menominee': '55078', 'Kewaunee': '55061', 'Oconto': '55083'}

NJ_FIPS = {'Salem': '34033', 'Hudson': '34017', 'Cumberland': '34011', 'Passaic': '34031', 'Essex': '34013', 'Camden': '34007', 'Ocean': '34029', 'Atlantic': '34001', 'Mercer': '34021', 'Warren': '34041', 'Gloucester': '34015', 'Union': '34039', 'Middlesex': '34023', 'Burlington': '34005', 'Monmouth': '34025', 'Bergen': '34003', 'Cape May': '34009', 'Somerset': '34035', 'Sussex': '34037', 'Morris': '34027', 'Hunterdon': '34019'}

def load_new_jersey_data():
    """Load complete New Jersey county data - 21 counties, SY2026 CEP data"""
    data = {
        'County': ['Salem', 'Hudson', 'Cumberland', 'Passaic', 'Essex', 'Camden', 'Ocean', 'Atlantic', 'Mercer', 'Warren', 'Gloucester', 'Union', 'Middlesex', 'Burlington', 'Monmouth', 'Bergen', 'Cape May', 'Somerset', 'Sussex', 'Morris', 'Hunterdon'],
        'Population': [64837, 724854, 154152, 524118, 863728, 523485, 637229, 274534, 387340, 109632, 302294, 575345, 863162, 461850, 643615, 955732, 95263, 345361, 144221, 509285, 128947],
        'Children_in_Poverty': [18673, 171186, 36226, 108492, 160613, 94227, 94967, 39807, 51129, 13924, 36275, 60987, 89769, 44338, 50805, 65946, 6097, 21067, 7499, 25973, 4642],
        'School_Districts': [4, 12, 8, 15, 22, 18, 18, 11, 13, 9, 14, 21, 25, 18, 19, 70, 6, 15, 8, 39, 18],
        'Eligible_Schools': [23, 140, 51, 134, 225, 147, 96, 61, 87, 18, 52, 124, 157, 74, 104, 114, 24, 59, 12, 90, 18],
        'CEP_Schools': [11, 78, 49, 90, 78, 61, 18, 29, 42, 4, 15, 2, 16, 21, 31, 11, 5, 23, 0, 0, 0],
        'Students_in_CEP': [3881, 44309, 18795, 44037, 30758, 17964, 13863, 15566, 17786, 2130, 6879, 618, 8628, 9561, 11366, 2574, 1021, 10582, 0, 0, 0],
        'Coverage_Pct': [48, 56, 96, 67, 35, 41, 19, 48, 48, 22, 29, 2, 10, 28, 30, 10, 21, 39, 0, 0, 0],
        'Status': ['PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP']
    }
    df = pd.DataFrame(data)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    # CONSISTENCY FIX: Normalize status using shared function
    df['Status'] = df['Status'].apply(normalize_status)
    # Add numeric status for map
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df

STATE_DATA = {
    'WI': {'name': 'Wisconsin', 'eligible_schools': 1295, 'cep_schools': 714, 'students_in_cep': 270136, 'children_without_cep': 41943, 'coverage_pct': 55, 'rank': 42, 'has_data': True, 'lat': 44.5, 'lon': -89.5},
    'NJ': {'name': 'New Jersey', 'eligible_schools': 1810, 'cep_schools': 584, 'students_in_cep': 260318, 'children_without_cep': 826612, 'coverage_pct': 32, 'rank': 48, 'has_data': True, 'lat': 40.0, 'lon': -74.5},
    'VA': {'name': 'Virginia', 'eligible_schools': 1850, 'cep_schools': 1054, 'students_in_cep': 389000, 'children_without_cep': 142000, 'coverage_pct': 57, 'rank': 15, 'has_data': False, 'lat': 37.5, 'lon': -78.5},
    'SC': {'name': 'South Carolina', 'eligible_schools': 1100, 'cep_schools': 979, 'students_in_cep': 425000, 'children_without_cep': 51000, 'coverage_pct': 89, 'rank': 1, 'has_data': False, 'lat': 33.8, 'lon': -81.0},
    'NV': {'name': 'Nevada', 'eligible_schools': 550, 'cep_schools': 234, 'students_in_cep': 98000, 'children_without_cep': 87000, 'coverage_pct': 43, 'rank': 35, 'has_data': False, 'lat': 39.0, 'lon': -117.0},
    'AR': {'name': 'Arkansas', 'eligible_schools': 850, 'cep_schools': 521, 'students_in_cep': 187000, 'children_without_cep': 96000, 'coverage_pct': 61, 'rank': 12, 'has_data': False, 'lat': 34.8, 'lon': -92.2}
}

NATIONAL_STATS = {
    'total_children_without_cep': sum(s['children_without_cep'] for s in STATE_DATA.values()),
    'total_students_served': sum(s['students_in_cep'] for s in STATE_DATA.values()),
    'eligible_schools_not_participating': sum(s['eligible_schools'] - s['cep_schools'] for s in STATE_DATA.values()),
    'avg_coverage': int(sum(s['coverage_pct'] for s in STATE_DATA.values()) / len(STATE_DATA))
}

STATE_EXECUTIVES = {
    'WI': {
        'Governor': {'name': 'Tony Evers', 'party': 'Democrat'},
        'State Treasurer': {'name': 'John Leiber', 'party': 'Republican'},
        'Senate Majority Leader': {'name': 'Devin LeMahieu', 'party': 'Republican'},
        'Senate Education Chair': {'name': 'John Jagler', 'party': 'Republican'},
        'Senate Appropriations Chair': {'name': 'Howard Marklein', 'party': 'Republican'}
    },
    'NJ': {
        'Governor': {'name': 'Mikie Sherrill', 'party': 'Democrat'},
        'State Treasurer': {'name': 'Aaron Binder', 'party': 'Democrat'},
        'Senate Majority Leader': {'name': 'M. Teresa Ruiz', 'party': 'Democrat'},
        'Senate Education Chair': {'name': 'Vin Gopal', 'party': 'Democrat'},
        'Senate Appropriations Chair': {'name': 'Paul Sarlo', 'party': 'Democrat'}
    }
}

# ====================
# HOMEPAGE (REDESIGNED)
# ====================

def create_hero_section():
    return html.Div([html.Div([html.H1("CEP Expansion Is the Fastest Way to Eliminate School Hunger", style={'fontSize': '56px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '20px', 'lineHeight': '1.1', 'maxWidth': '1000px', 'marginLeft': 'auto', 'marginRight': 'auto', 'letterSpacing': '-0.02em'}), html.P("Across America, millions of children in poverty attend schools that are eligible for the Community Eligibility Provision but haven't adopted it. States have an immediate opportunity to close this gap.", style={'fontSize': '21px', 'color': COLORS['text_secondary'], 'maxWidth': '800px', 'margin': '0 auto 40px auto', 'lineHeight': '1.5'}), html.Div([html.Div([html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", style={'fontSize': '64px', 'fontWeight': '700', 'color': COLORS['teal'], 'lineHeight': '1'}), html.Div("CHILDREN WITHOUT CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1px', 'marginTop': '8px'})], style={'textAlign': 'center'}), html.Div([html.Div(f"{NATIONAL_STATS['avg_coverage']}%", style={'fontSize': '64px', 'fontWeight': '700', 'color': COLORS['teal'], 'lineHeight': '1'}), html.Div("AVERAGE COVERAGE", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1px', 'marginTop': '8px'})], style={'textAlign': 'center'})], style={'display': 'flex', 'justifyContent': 'center', 'gap': '60px', 'marginTop': '50px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '100px 40px 80px 40px', 'textAlign': 'center'})], style={'background': f'linear-gradient(135deg, {COLORS["off_white"]} 0%, {COLORS["light_gray"]} 100%)', 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_insights_section():
    insights = [{'title': 'Largest Participation Gap', 'metric': '826K', 'text': 'children in New Jersey could be served through expanded CEP implementation'}, {'title': 'Top Performing State', 'metric': '89%', 'text': 'of eligible schools in South Carolina participate in CEP'}, {'title': 'High-Need Counties', 'metric': '24', 'text': 'counties in Wisconsin have zero CEP participation despite eligibility'}, {'title': 'Immediate Opportunity', 'metric': f"{NATIONAL_STATS['eligible_schools_not_participating']:,}", 'text': 'eligible schools not yet participating in CEP across tracked states'}]
    insight_cards = [html.Div([html.H3(i['title'], style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '12px', 'color': COLORS['text_primary']}), html.Div(i['metric'], style={'fontSize': '42px', 'fontWeight': '700', 'color': COLORS['teal'], 'marginBottom': '8px'}), html.P(i['text'], style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'lineHeight': '1.5', 'margin': '0'})], style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '32px', 'transition': 'all 0.3s ease', 'cursor': 'pointer'}) for i in insights]
    return html.Div([html.H2("Featured Insights", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '40px', 'color': COLORS['text_primary']}), html.Div(insight_cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '24px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '80px 40px'})

def create_us_map():
    """NEW: Interactive US map with full state names and bold category colors"""
    # Prepare data for all US states
    all_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
    # Map states to numeric categories for color mapping
    state_z_values = []
    for state in all_states:
        category = get_state_category(state)
        if category == 'universal_meals':
            state_z_values.append(4)  # Green
        elif category == 'universal_breakfast':
            state_z_values.append(3)  # Amber
        elif category == 'fpl_states':
            state_z_values.append(2)  # Blue (FPL states)
        else:
            state_z_values.append(1)  # Gray
    
    state_names = [STATE_DATA.get(state, {}).get('name', state) for state in all_states]
    
    # FPL percentage mapping
    fpl_percentages = {
        'HI': '300% of FPL',
        'NJ': '225% of FPL',
        'ND': '225% of FPL'
    }
    
    hover_text = []
    for state in all_states:
        category = get_state_category(state)
        state_name = state_names[all_states.index(state)]
        
        if category == 'universal_meals':
            label = "Universal Free Meals"
            hover_text.append(f"<b>{state_name}</b><br>{label}")
        elif category == 'universal_breakfast':
            label = "Universal Free Breakfast"
            hover_text.append(f"<b>{state_name}</b><br>{label}")
        elif category == 'fpl_states':
            label = fpl_percentages.get(state, 'Federal Poverty Level')
            hover_text.append(f"<b>{state_name}</b><br>{label}")
        else:
            # For gray states
            data = STATE_DATA.get(state, {})
            if data.get('has_data'):
                # Tracked states: show state name + coverage
                hover_text.append(f"<b>{state_name}</b><br>{data.get('coverage_pct', 0)}% CEP Coverage")
            else:
                # Other gray states: just state name
                hover_text.append(f"<b>{state_name}</b>")
    
    fig = go.Figure(go.Choropleth(
        locations=all_states,
        z=state_z_values,
        locationmode='USA-states',
        text=state_names,
        hovertext=hover_text,
        hovertemplate='%{hovertext}<extra></extra>',
        marker=dict(
            line=dict(color='white', width=2)
        ),
        colorscale=[
            [0, COLORS['other_states']],      # 1 = Gray
            [0.33, COLORS['fpl_states']],     # 2 = Blue (FPL states)
            [0.67, COLORS['universal_breakfast']],  # 3 = Amber/Yellow
            [1, COLORS['universal_meals']]    # 4 = Green
        ],
        zmin=1,  # CRITICAL: Force scale to 1-4 range for discrete mapping
        zmax=4,  # Ensures: z=1→gray, z=2→blue, z=3→amber, z=4→green
        showscale=False
    ))
    
    # Enhanced tooltip styling for clean, minimal appearance
    fig.update_traces(
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter, system-ui, -apple-system, sans-serif',
            font_color='#1a1a1a',
            bordercolor='#e5e7eb',
            align='left'
        )
    )
    
    fig.update_geos(
        scope='usa',
        projection_type='albers usa',
        showlakes=False,
        bgcolor='rgba(0,0,0,0)',
        showsubunits=True,  # Show state boundaries with labels
        subunitcolor='white',
        subunitwidth=2
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        clickmode='event+select'
    )
    
    return fig

def create_explore_states_panel():
    """NEW: Redesigned right-side panel with state flags and category grouping
    UPDATED: Includes FPL states support - New Jersey should appear with blue border
    Version: 2026-04-10-FPL-FIX
    """
    
    # Get the 6 tracked states grouped by category
    tracked_states = ['WI', 'NJ', 'VA', 'SC', 'NV', 'AR']
    
    # Group by category
    universal_meals_tracked = [s for s in tracked_states if get_state_category(s) == 'universal_meals']
    universal_breakfast_tracked = [s for s in tracked_states if get_state_category(s) == 'universal_breakfast']
    fpl_tracked = [s for s in tracked_states if get_state_category(s) == 'fpl_states']
    other_tracked = [s for s in tracked_states if get_state_category(s) == 'other']
    
    def create_state_button(state_abbr):
        state_data = STATE_DATA.get(state_abbr, {})
        category = get_state_category(state_abbr)
        
        # Category color for left border
        if category == 'universal_meals':
            border_color = COLORS['universal_meals']
            subtitle = "Universal meals"
        elif category == 'universal_breakfast':
            border_color = COLORS['universal_breakfast']
            subtitle = "Universal breakfast"
        elif category == 'fpl_states':
            border_color = COLORS['fpl_states']
            subtitle = "FPL State"
        else:
            border_color = 'transparent'
            subtitle = f"{state_data.get('coverage_pct', 0)}% coverage"
        
        flag_url = STATE_FLAGS.get(state_abbr, '')
        
        return html.A(
            href=f"/state/{state_abbr}",
            children=[
                html.Div([
                    html.Div([
                        html.Img(src=flag_url, style={'width': '32px', 'height': '21px', 'marginRight': '12px', 'border': '0.5px solid #e5e7eb', 'borderRadius': '2px', 'objectFit': 'cover'}),
                        html.Div([
                            html.Div(state_data.get('name', state_abbr), style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '2px'}),
                            html.Div(subtitle, style={'fontSize': '13px', 'color': COLORS['text_secondary']})
                        ], style={'flex': '1'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '14px 16px', 'borderLeft': f'4px solid {border_color}', 'background': 'white', 'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}', 'transition': 'all 0.2s ease'})
                ], style={'marginBottom': '10px'})
            ],
            style={'textDecoration': 'none', 'display': 'block'}
        )
    
    buttons = []
    
    # Universal Meals section
    if universal_meals_tracked:
        for state in universal_meals_tracked:
            buttons.append(create_state_button(state))
    
    # Universal Breakfast section
    if universal_breakfast_tracked:
        for state in universal_breakfast_tracked:
            buttons.append(create_state_button(state))
    
    # FPL States section
    if fpl_tracked:
        for state in fpl_tracked:
            buttons.append(create_state_button(state))
    
    # Other states section  
    for state in other_tracked:
        buttons.append(create_state_button(state))
    
    return html.Div([
        html.H3("Explore States", style={'fontSize': '14px', 'fontWeight': '600', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1px', 'marginBottom': '20px'}),
        html.Div(buttons)
    ], style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})

def create_map_section():
    """NEW: Grid layout with map on left, Explore States on right"""
    
    # Legend for the map
    legend = html.Div([
        html.Div([
            html.Div(style={'width': '18px', 'height': '18px', 'background': COLORS['universal_meals'], 'borderRadius': '4px', 'marginRight': '8px'}),
            html.Span("Universal school meals (9 states)", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([
            html.Div(style={'width': '18px', 'height': '18px', 'background': COLORS['universal_breakfast'], 'borderRadius': '4px', 'marginRight': '8px'}),
            html.Span("Universal school breakfast (3 states)", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([
            html.Div(style={'width': '18px', 'height': '18px', 'background': COLORS['fpl_states'], 'borderRadius': '4px', 'marginRight': '8px'}),
            html.Span("FPL States (3 states)", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([
            html.Div(style={'width': '18px', 'height': '18px', 'background': COLORS['other_states'], 'borderRadius': '4px', 'marginRight': '8px'}),
            html.Span("Other states", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'marginBottom': '24px', 'padding': '16px', 'background': COLORS['off_white'], 'borderRadius': '8px'})
    
    return html.Div([
        html.Div([
            # Left: Map
            html.Div([
                html.H2("National School Meal Coverage", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}),
                legend,
                dcc.Graph(id='us-map-graph', figure=create_us_map(), config={'displayModeBar': False}, style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '20px'})
            ], style={'gridColumn': '1 / span 2'}),
            
            # Right: Explore States Panel
            html.Div([
                create_explore_states_panel()
            ], style={'gridColumn': '3'})
            
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 400px', 'gap': '24px', 'maxWidth': '1400px', 'margin': '0 auto'})
    ], style={'padding': '80px 40px', 'background': COLORS['off_white']})

def create_comparison_section():
    return html.Div([html.Div([html.H2("Compare States", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}), html.Div([html.Div([html.Label("State A", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}), dcc.Dropdown(id='compare-state-a', options=[{'label': data['name'], 'value': abbr} for abbr, data in STATE_DATA.items()], value='WI', clearable=False, style={'minWidth': '200px'})], style={'flex': '1'}), html.Div([html.Label("State B", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}), dcc.Dropdown(id='compare-state-b', options=[{'label': data['name'], 'value': abbr} for abbr, data in STATE_DATA.items()], value='NJ', clearable=False, style={'minWidth': '200px'})], style={'flex': '1'})], style={'display': 'flex', 'gap': '20px', 'marginBottom': '32px'}), html.Div(id='comparison-output')], style={'maxWidth': '1400px', 'margin': '0 auto'})], style={'padding': '80px 40px', 'background': 'white'})

def create_cta_section():
    return html.Div([html.Div([html.H2("Take Action for Universal School Meals", style={'fontSize': '40px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '20px', 'textAlign': 'center'}), html.P("Contact your state representatives to advocate for CEP expansion in your community", style={'fontSize': '18px', 'color': COLORS['text_secondary'], 'textAlign': 'center', 'marginBottom': '40px'}), html.Div([html.A("Find Your Representatives", href="#", style={'background': COLORS['teal'], 'color': 'white', 'padding': '16px 40px', 'borderRadius': '8px', 'textDecoration': 'none', 'fontSize': '16px', 'fontWeight': '600', 'display': 'inline-block'})], style={'textAlign': 'center'})], style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '80px 40px'})], style={'background': f'linear-gradient(135deg, {COLORS["off_white"]} 0%, {COLORS["light_gray"]} 100%)'})

def create_landing_page():
    return html.Div([create_hero_section(), create_insights_section(), create_map_section(), create_comparison_section(), create_cta_section()])

def create_comparison_cards(state_a, state_b):
    data_a = STATE_DATA[state_a]
    data_b = STATE_DATA[state_b]
    return html.Div([html.Div([html.H3(data_a['name'], style={'fontSize': '24px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}), html.Div([html.Div([html.Div("Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"{data_a['coverage_pct']}%", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})], style={'marginBottom': '16px'}), html.Div([html.Div("Rank", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"#{data_a['rank']}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})], style={'marginBottom': '16px'}), html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"{data_a['students_in_cep']:,}", style={'fontSize': '24px', 'fontWeight': '600', 'color': COLORS['text_primary']})])])], style={'background': 'white', 'padding': '32px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.H3(data_b['name'], style={'fontSize': '24px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}), html.Div([html.Div([html.Div("Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"{data_b['coverage_pct']}%", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})], style={'marginBottom': '16px'}), html.Div([html.Div("Rank", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"#{data_b['rank']}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})], style={'marginBottom': '16px'}), html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"{data_b['students_in_cep']:,}", style={'fontSize': '24px', 'fontWeight': '600', 'color': COLORS['text_primary']})])])], style={'background': 'white', 'padding': '32px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px'})

# ====================
# STATE DETAIL PAGES (ENHANCED WITH CONSISTENCY FIX)
# ====================

def create_state_executives_section(state_abbr):
    """Executive names colored by party with legend"""
    executives = STATE_EXECUTIVES.get(state_abbr, {})
    if not executives:
        return html.Div()
    
    # Party legend with symbols
    legend = html.Div([
        html.Div([
            html.Span('●', style={'color': COLORS['democrat_name'], 'fontSize': '20px', 'marginRight': '6px'}),
            html.Span('Democratic', style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginRight': '20px'})
        ], style={'display': 'inline-flex', 'alignItems': 'center'}),
        html.Div([
            html.Span('●', style={'color': COLORS['republican_name'], 'fontSize': '20px', 'marginRight': '6px'}),
            html.Span('Republican', style={'fontSize': '13px', 'color': COLORS['text_secondary']})
        ], style={'display': 'inline-flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'paddingBottom': '12px', 'borderBottom': f'1px solid {COLORS["border"]}'})
    
    cards = []
    for position, official in executives.items():
        name_color = get_party_color(official['party'])
        card = html.Div([
            html.Div(position, style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'fontWeight': '600', 'marginBottom': '8px'}), 
            html.Div(official['name'], style={'fontSize': '18px', 'fontWeight': '600', 'color': name_color, 'marginBottom': '6px'}),
            html.Div(official['party'], style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'fontWeight': '400'})
        ], style={'background': 'white', 'padding': '20px 24px', 'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}', 'minWidth': '200px'})
        cards.append(card)
    
    return html.Div([html.Div([html.H2("State Leadership", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '20px'}), legend, html.Div(cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '16px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 40px 40px'})], style={'background': COLORS['off_white'], 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_county_map(df, fips_dict, state_abbr):
    """CONSISTENCY FIX: Map uses same normalized status as table"""
    df['FIPS'] = df['County'].map(fips_dict)
    
    # Debug: Print county status mapping
    print(f"\n=== DEBUG: County Map for {state_abbr} ===")
    for idx, row in df.iterrows():
        print(f"County: {row['County']:20s} | Status: {row['Status']:12s} | Numeric: {row['Status_Numeric']} | FIPS: {row.get('FIPS', 'N/A')}")
    
    # Check for unmatched counties
    unmatched = df[df['FIPS'].isna()]
    if len(unmatched) > 0:
        print(f"\n⚠️  WARNING: {len(unmatched)} counties have no FIPS match:")
        for county in unmatched['County']:
            print(f"   - {county}")
    
    # Use Status_Numeric for accurate coloring (0=No, 1=Partial, 2=Full)
    fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df['FIPS'],
        z=df['Status_Numeric'],  # Use numeric status
        text=df['County'] + '<br>' + df['Status'],
        hovertemplate='<b>%{text}</b><extra></extra>',
        colorscale=[
            [0, COLORS['no_cep']],      # 0 = No CEP = Red
            [0.5, COLORS['partial_cep']], # 1 = Partial = Yellow
            [1, COLORS['full_cep']]     # 2 = Full = Green
        ],
        zmin=0,  # CRITICAL FIX: Force scale to 0-2 range
        zmax=2,  # This ensures discrete mapping: 0→red, 1→yellow, 2→green
        marker_line_color='white',
        marker_line_width=1.5,
        showscale=False
    ))
    
    # Dynamic center by state
    state_centers = {
        'WI': {'lat': 44.5, 'lon': -89.5},
        'NJ': {'lat': 40.0, 'lon': -74.5}
    }
    center = state_centers.get(state_abbr, {'lat': 39, 'lon': -98})
    
    fig.update_geos(fitbounds="locations", visible=False, center=center, projection_scale=8)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    print(f"✓ Map created with Status_Numeric range: {df['Status_Numeric'].min()} to {df['Status_Numeric'].max()}\n")
    
    return fig

def create_sortable_county_table(df):
    """Table with status pills and row highlighting - CONSISTENCY FIX APPLIED"""
    return html.Div([
        html.H2("County Details", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}), 
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {'name': 'County', 'id': 'County'},
                {'name': 'Population', 'id': 'Population', 'type': 'numeric', 'format': {'specifier': ','}},
                {'name': 'Children in Poverty', 'id': 'Children_in_Poverty', 'type': 'numeric', 'format': {'specifier': ','}},
                {'name': 'School Districts', 'id': 'School_Districts', 'type': 'numeric'},
                {'name': 'Eligible Schools', 'id': 'Eligible_Schools', 'type': 'numeric'},
                {'name': 'CEP Schools', 'id': 'CEP_Schools', 'type': 'numeric'},
                {'name': 'Students in CEP', 'id': 'Students_in_CEP', 'type': 'numeric', 'format': {'specifier': ','}},
                {'name': '% Coverage', 'id': 'Coverage_Pct', 'type': 'numeric'},
                {'name': 'School Gap', 'id': 'School_Gap', 'type': 'numeric'},
                {'name': 'Status', 'id': 'Status'}
            ],
            sort_action='native',
            filter_action='native',
            page_action='none',  # Show all counties
            style_table={'overflowX': 'auto', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'overflow': 'hidden'}, 
            style_header={'backgroundColor': COLORS['off_white'], 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'padding': '16px 20px', 'borderBottom': f'2px solid {COLORS["border"]}', 'textAlign': 'left'}, 
            style_cell={'padding': '16px 20px', 'fontSize': '15px', 'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'textAlign': 'left', 'borderBottom': f'1px solid {COLORS["border"]}', 'whiteSpace': 'normal', 'height': 'auto'}, 
            style_cell_conditional=[
                {'if': {'column_id': ['Population', 'Children_in_Poverty', 'Students_in_CEP']}, 'textAlign': 'right'}, 
                {'if': {'column_id': ['School_Districts', 'Eligible_Schools', 'CEP_Schools', 'Coverage_Pct', 'School_Gap']}, 'textAlign': 'center'}, 
                {'if': {'column_id': 'County'}, 'fontWeight': '500', 'minWidth': '120px'},
                {'if': {'column_id': 'Status'}, 'minWidth': '180px', 'paddingLeft': '12px', 'paddingRight': '12px'}
            ], 
            style_data_conditional=[
                # Row highlighting based on status
                {'if': {'filter_query': '{Status} = "FULL CEP"'}, 'backgroundColor': '#f0fdf4'},  # Light green rows
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"'}, 'backgroundColor': '#fefce8'},  # Light yellow rows
                {'if': {'filter_query': '{Status} = "NO CEP"'}, 'backgroundColor': '#fef2f2'},  # Light red rows
                # Status pills (on top of row colors) - CORRECTED TO MATCH APPROVED COLORS
                {'if': {'filter_query': '{Status} = "FULL CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#10b981', 'color': '#ffffff', 'fontWeight': '600', 
                    'fontSize': '15px', 'padding': '12px 20px', 'borderRadius': '24px',
                    'textAlign': 'left', 'display': 'block', 'width': '100%'}, 
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#fbbf24', 'color': '#1a1a1a', 'fontWeight': '600', 
                    'fontSize': '15px', 'padding': '12px 20px', 'borderRadius': '24px',
                    'textAlign': 'left', 'display': 'block', 'width': '100%'}, 
                {'if': {'filter_query': '{Status} = "NO CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#ef4444', 'color': '#ffffff', 'fontWeight': '600', 
                    'fontSize': '15px', 'padding': '12px 20px', 'borderRadius': '24px',
                    'textAlign': 'left', 'display': 'block', 'width': '100%'}
            ], 
            style_filter={'backgroundColor': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '4px', 'padding': '8px', 'fontSize': '14px'}
        )
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})

def create_state_page(state_abbr):
    state_data = STATE_DATA.get(state_abbr)
    if not state_data:
        return html.Div("State not found")
    
    # Load county data based on state - CONSISTENCY FIX APPLIED
    if state_abbr == 'WI':
        df = load_wisconsin_data()
        fips_dict = WI_FIPS
    elif state_abbr == 'NJ':
        df = load_new_jersey_data()
        fips_dict = NJ_FIPS
    else:
        df = pd.DataFrame({'County': ['Sample'], 'Population': [100000], 'Children_in_Poverty': [15000], 'School_Districts': [10], 'Eligible_Schools': [25], 'CEP_Schools': [10], 'Students_in_CEP': [5000], 'Status': ['PARTIAL CEP'], 'Coverage_Pct': [40], 'School_Gap': [15]})
        df['Status'] = df['Status'].apply(normalize_status)  # CONSISTENCY FIX
        df['Status_Numeric'] = df['Status'].apply(status_to_numeric)  # CONSISTENCY FIX
        fips_dict = {}
    
    return html.Div([
        html.Div([html.Div([html.A("← All States", href="/", style={'color': COLORS['teal'], 'textDecoration': 'none', 'fontSize': '15px', 'fontWeight': '500', 'marginBottom': '24px', 'display': 'inline-block'}), html.H1(state_data['name'], style={'fontSize': '56px', 'fontWeight': '600', 'letterSpacing': '-0.02em', 'color': COLORS['text_primary'], 'marginBottom': '12px'}), html.P(f"{state_data['coverage_pct']}% CEP Coverage • Rank #{state_data['rank']} Nationally", style={'fontSize': '21px', 'color': COLORS['text_secondary']})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '60px 40px'})], style={'background': COLORS['white']}), 
        create_state_executives_section(state_abbr), 
        html.Div([html.Div([html.Div([html.Div("CEP Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['coverage_pct']}%", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div(f"Rank #{state_data['rank']}", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['students_in_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("In CEP schools", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Opportunity", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['children_without_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("Children without CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Schools", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['cep_schools']}/{state_data['eligible_schools']}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("CEP vs Eligible", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}), 
        (html.Div([html.Div([html.H2("County-Level Coverage", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}), html.Div([dcc.Graph(figure=create_county_map(df, fips_dict, state_abbr), config={'displayModeBar': False})], style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}) if fips_dict else html.Div()), 
        html.Div([create_sortable_county_table(df)], style={'background': COLORS['off_white']})
    ], style={'background': COLORS['off_white'], 'minHeight': '100vh'})

application.layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

@application.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return create_landing_page()
    elif pathname.startswith('/state/'):
        return create_state_page(pathname.split('/')[-1].upper())
    else:
        return html.Div("404")

@application.callback(Output('comparison-output', 'children'), [Input('compare-state-a', 'value'), Input('compare-state-b', 'value')])
def update_comparison(state_a, state_b):
    if state_a and state_b:
        return create_comparison_cards(state_a, state_b)
    return html.Div()

if __name__ == '__main__':
    application.run(debug=False, host='0.0.0.0', port=8000)

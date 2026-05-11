# CEP Policy Intelligence Platform - ENHANCED v2
# VERSION: 2026-05-05-SURGICAL-ENHANCEMENTS
# Last Updated: May 5, 2026
# Changes: Rank removed, Leadership expanded with portraits, Colors updated (dark green/lilac/orange/yellow)
# Phase 2 Enhancements:
# 1. New interactive US map with full state names and bold color categories
# 2. Redesigned Explore States panel with state flags and category grouping
# 3. Consistency fix applied to ALL state pages (map/table status alignment)
# 4. Complete Virginia county data with sky blue/yellow/pink color scheme
# 5. SURGICAL: Rank metric removed from all UI
# 6. SURGICAL: Leadership section expanded with branch grouping and circular portraits

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
    'full_cep': '#87CEEB',  # Sky Blue (FULL CEP - Participating)
    'partial_cep': '#fbbf24',  # Yellow (PARTIAL CEP) - CHANGED FROM GREEN
    'no_cep': '#ec4899',  # Pink (NO CEP)
    # Political Party - For executive names
    'democrat_name': '#1d4ed8',  # Blue
    'republican_name': '#991b1b',  # Maroon
    # NEW: Bold Map Categories (high-contrast for easy distinction)
    'universal_meals': '#065f46',  # Dark green - Universal meals states
    'universal_breakfast': '#f97316',  # Orange - Universal breakfast states
    'fpl_states': '#c084fc',  # Lilac/Light purple - Federal Poverty Level states
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

VA_FIPS = {
    'Accomack County': '51001', 'Albemarle County': '51003', 'Alleghany County': '51005', 'Alleghany Highlands': '51005',
    'Amelia County': '51007', 'Amherst County': '51009', 'Appomattox County': '51011', 'Arlington County': '51013',
    'Augusta County': '51015', 'Bath County': '51017', 'Bedford County': '51019', 'Bland County': '51021',
    'Botetourt County': '51023', 'Brunswick County': '51025', 'Buchanan County': '51027', 'Buckingham County': '51029',
    'Campbell County': '51031', 'Caroline County': '51033', 'Carroll County': '51035', 'Charles City County': '51036',
    'Charlotte County': '51037', 'Chesterfield County': '51041', 'Clarke County': '51043', 'Craig County': '51045',
    'Culpeper County': '51047', 'Cumberland County': '51049', 'Dickenson County': '51051', 'Dinwiddie County': '51053',
    'Essex County': '51057', 'Fairfax County': '51059', 'Fauquier County': '51061', 'Floyd County': '51063',
    'Fluvanna County': '51065', 'Franklin County': '51067', 'Frederick County': '51069', 'Giles County': '51071',
    'Gloucester County': '51073', 'Goochland County': '51075', 'Grayson County': '51077', 'Greene County': '51079',
    'Greensville County': '51081', 'Halifax County': '51083', 'Hanover County': '51085', 'Henrico County': '51087',
    'Henry County': '51089', 'Highland County': '51091', 'Isle of Wight County': '51093', 'James City County': '51095',
    'King and Queen County': '51097', 'King George County': '51099', 'King William County': '51101', 'Lancaster County': '51103',
    'Lee County': '51105', 'Loudoun County': '51107', 'Louisa County': '51109', 'Lunenburg County': '51111',
    'Madison County': '51113', 'Mathews County': '51115', 'Mecklenburg County': '51117', 'Middlesex County': '51119',
    'Montgomery County': '51121', 'Nelson County': '51125', 'New Kent County': '51127', 'Northampton County': '51131',
    'Northumberland County': '51133', 'Nottoway County': '51135', 'Orange County': '51137', 'Page County': '51139',
    'Patrick County': '51141', 'Pittsylvania County': '51143', 'Powhatan County': '51145', 'Prince Edward County': '51147',
    'Prince George County': '51149', 'Prince William County': '51153', 'Pulaski County': '51155', 'Rappahannock County': '51157',
    'Richmond County': '51159', 'Roanoke County': '51161', 'Rockbridge County': '51163', 'Rockingham County': '51165',
    'Russell County': '51167', 'Scott County': '51169', 'Shenandoah County': '51171', 'Smyth County': '51173',
    'Southampton County': '51175', 'Spotsylvania County': '51177', 'Stafford County': '51179', 'Surry County': '51181',
    'Sussex County': '51183', 'Tazewell County': '51185', 'Warren County': '51187', 'Washington County': '51191',
    'Westmoreland County': '51193', 'Wise County': '51195', 'Wythe County': '51197', 'York County': '51199',
    'Alexandria City': '51510', 'Bristol City': '51520', 'Buena Vista City': '51530', 'Charlottesville City': '51540',
    'Chesapeake City': '51550', 'Colonial Beach': '51557', 'Colonial Heights City': '51570', 'Danville City': '51590',
    'Fredericksburg City': '51630', 'Galax City': '51640', 'Hampton City': '51650', 'Harrisonburg City': '51660',
    'Hopewell City': '51670', 'Lexington City': '51678', 'Lynchburg City': '51680', 'Manassas City': '51683',
    'Manassas Park City': '51685', 'Newport News City': '51700', 'Norfolk City': '51710', 'Norton City': '51720',
    'Petersburg City': '51730', 'Poquoson City': '51735', 'Portsmouth City': '51740', 'Radford City': '51750',
    'Richmond City': '51760', 'Roanoke City': '51770', 'Salem City': '51775', 'Staunton City': '51790',
    'Suffolk City': '51800', 'Virginia Beach City': '51810', 'Waynesboro City': '51820', 
    'Williamsburg-James City County': '51095', 'Williamsburg City': '51830', 'Winchester City': '51840',
    'Falls Church City': '51610', 'Franklin City': '51620', 'Martinsville City': '51690', 'West Point Town': '51095'
}

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

def load_virginia_data():
    """Load Virginia county data - Complete 131 counties/cities from VA_CEP_map_2025.xlsx"""
    import io
    
    # Complete Virginia CEP data - 131 jurisdictions (embedded - no external file needed)
    csv_data = """County,Population,Poverty_Rate,Eligible_Schools,CEP_Schools,Students_in_CEP,Coverage_Pct,School_Gap,Status
Lee County,22173,48.2,10,10,2795,100,0,FULL CEP
King and Queen County,6608,43.2,3,3,608,100,0,FULL CEP
Colonial Beach,3908,38.4,2,2,576,100,0,FULL CEP
Norton City,3687,38.2,2,2,860,100,0,FULL CEP
Charlotte County,11529,37.1,5,5,1676,100,0,FULL CEP
Danville City,42590,36.8,13,13,5284,100,0,FULL CEP
Hopewell City,23033,34.3,6,6,3945,100,0,FULL CEP
Buchanan County,20355,34.1,8,8,2296,100,0,FULL CEP
Buena Vista City,6641,33.0,4,4,883,100,0,FULL CEP
Galax City,6720,31.3,3,3,1436,100,0,FULL CEP
Northampton County,12282,31.2,4,4,1307,100,0,FULL CEP
Fredericksburg City,27982,30.0,5,5,3646,100,0,FULL CEP
Petersburg City,33458,29.9,8,8,4551,100,0,FULL CEP
Winchester City,28120,29.2,7,7,4316,100,0,FULL CEP
Tazewell County,40429,29.0,13,13,5121,100,0,FULL CEP
Halifax County,34022,28.7,10,10,4528,100,0,FULL CEP
Dickenson County,14124,27.4,3,3,1762,100,0,FULL CEP
Richmond City,226210,27.4,47,47,20797,100,0,FULL CEP
Roanoke City,100011,27.2,26,26,13606,100,0,FULL CEP
Essex County,10599,27.1,3,3,1113,100,0,FULL CEP
Bath County,4209,26.6,3,3,516,100,0,FULL CEP
Prince Edward County,21849,26.6,3,3,1843,100,0,FULL CEP
Radford City,16070,26.6,4,4,1658,100,0,FULL CEP
Charlottesville City,46553,26.3,9,9,4448,100,0,FULL CEP
Norfolk City,283005,26.3,48,48,26406,100,0,FULL CEP
Brunswick County,15849,25.6,5,5,1379,100,0,FULL CEP
Martinsville City,13485,25.5,5,5,1771,100,0,FULL CEP
Surry County,6561,24.9,3,3,681,100,0,FULL CEP
Bristol City,17219,24.5,4,4,2063,100,0,FULL CEP
Lynchburg City,79009,24.5,20,20,7564,100,0,FULL CEP
Grayson County,15333,24.2,6,6,1574,100,0,FULL CEP
Franklin City,8180,24.2,2,2,1124,100,0,FULL CEP
Carroll County,29155,23.9,10,10,3418,100,0,FULL CEP
Mecklenburg County,30319,23.8,6,6,3822,100,0,FULL CEP
Pulaski County,33800,23.7,7,7,3709,100,0,FULL CEP
Craig County,4892,23.4,2,2,516,100,0,FULL CEP
Accomack County,33413,23.0,11,11,4593,100,0,FULL CEP
Wythe County,28290,22.8,12,12,3691,100,0,FULL CEP
Newport News City,186247,22.2,43,43,25693,100,0,FULL CEP
Portsmouth City,97915,21.9,22,22,12788,100,0,FULL CEP
Wise County,36130,21.5,11,11,5499,100,0,FULL CEP
Lancaster County,10919,21.3,2,2,1045,100,0,FULL CEP
Buckingham County,16824,21.2,5,5,1831,100,0,FULL CEP
Henry County,50948,21.2,13,13,6859,100,0,FULL CEP
Harrisonburg City,51814,21.1,10,10,6675,100,0,FULL CEP
Sussex County,10829,20.4,3,3,1046,100,0,FULL CEP
Shenandoah County,44186,20.0,9,9,5687,100,0,FULL CEP
Lunenburg County,11963,19.7,4,4,1482,100,0,FULL CEP
Scott County,27576,19.6,13,13,3320,100,0,FULL CEP
Smyth County,29800,19.5,13,13,3822,100,0,FULL CEP
Bland County,6270,19.4,2,2,650,100,0,FULL CEP
Appomattox County,16119,19.3,4,4,2330,100,0,FULL CEP
Nottoway County,15642,19.3,5,5,1770,100,0,FULL CEP
Russell County,25781,19.1,9,9,3328,100,0,FULL CEP
Franklin County,54477,18.7,12,12,6108,100,0,FULL CEP
Mathews County,8533,18.7,3,3,790,100,0,FULL CEP
Westmoreland County,18477,18.6,4,4,1605,100,0,FULL CEP
Pittsylvania County,60501,18.4,18,18,7649,100,0,FULL CEP
Amelia County,13265,17.6,3,3,1576,100,0,FULL CEP
Salem City,25346,17.6,6,2,819,33,4,PARTIAL CEP
Warren County,40727,17.5,9,9,5050,100,0,FULL CEP
Suffolk City,94324,17.3,20,20,14507,100,0,FULL CEP
Greene County,20552,17.2,5,5,2835,100,0,FULL CEP
Caroline County,30887,17.1,5,5,4551,100,0,FULL CEP
Bedford County,79462,17.0,20,13,5024,65,7,PARTIAL CEP
Chesapeake City,249422,16.9,47,31,23299,66,16,PARTIAL CEP
Rockingham County,83757,16.3,23,14,5516,61,9,PARTIAL CEP
Montgomery County,99721,16.0,20,6,1913,30,14,PARTIAL CEP
Hampton City,137148,15.6,32,32,19306,100,0,FULL CEP
Orange County,36254,15.4,10,10,5015,100,0,FULL CEP
Lexington City,7320,15.4,2,0,0,0,2,NO CEP
Highland County,2232,14.8,2,0,0,0,2,NO CEP
Waynesboro City,22196,14.8,7,7,3066,100,0,FULL CEP
Staunton City,25750,14.3,6,6,2620,100,0,FULL CEP
Northumberland County,11839,14.0,3,3,1202,100,0,FULL CEP
Colonial Heights City,18170,13.9,5,5,3008,100,0,FULL CEP
Charles City County,6773,13.7,2,2,519,100,0,FULL CEP
Louisa County,37596,13.7,6,6,5273,100,0,FULL CEP
Rappahannock County,7348,13.4,2,2,790,100,0,FULL CEP
Henrico County,334389,13.1,69,49,32327,71,20,PARTIAL CEP
Greensville County,11391,13.0,3,3,2023,100,0,FULL CEP
Amherst County,31307,12.9,10,10,3909,100,0,FULL CEP
Dinwiddie County,27947,12.8,7,7,4109,100,0,FULL CEP
Washington County,53935,12.7,15,15,6531,100,0,FULL CEP
Alleghany Highlands,15223,12.5,6,6,2738,100,0,FULL CEP
Middlesex County,10625,12.1,3,3,1227,100,0,FULL CEP
Campbell County,55656,12.0,14,14,7644,100,0,FULL CEP
Virginia Beach City,459470,11.8,84,39,22699,46,45,PARTIAL CEP
Albemarle County,112395,11.0,25,9,4385,36,16,PARTIAL CEP
Giles County,16787,11.0,5,5,2218,100,0,FULL CEP
Manassas Park City,17219,10.7,4,4,3398,100,0,FULL CEP
Gloucester County,38711,10.4,8,8,4866,100,0,FULL CEP
Manassas City,42772,10.4,9,9,7572,100,0,FULL CEP
Prince George County,43010,10.3,8,0,0,0,8,NO CEP
Culpeper County,52552,10.2,10,10,8366,100,0,FULL CEP
Poquoson City,12460,10.2,4,0,0,0,4,NO CEP
King William County,17810,9.9,4,0,0,0,4,NO CEP
Rockbridge County,22650,9.9,6,6,2415,100,0,FULL CEP
Isle of Wight County,38606,9.7,9,5,2391,56,4,PARTIAL CEP
Patrick County,17608,9.5,7,7,2056,100,0,FULL CEP
Alexandria City,159467,9.5,17,10,11519,59,7,PARTIAL CEP
Fluvanna County,27249,9.4,4,4,3320,100,0,FULL CEP
Augusta County,77487,9.0,19,19,10086,100,0,FULL CEP
Nelson County,14775,8.9,4,4,1496,100,0,FULL CEP
Clarke County,14783,8.8,4,0,0,0,4,NO CEP
Floyd County,15476,8.8,5,5,1648,100,0,FULL CEP
York County,70045,8.3,17,0,0,0,17,NO CEP
Prince William County,482204,8.1,97,68,59226,70,29,PARTIAL CEP
Spotsylvania County,140032,8.0,30,24,18529,80,6,PARTIAL CEP
Chesterfield County,364548,7.6,66,42,38948,64,24,PARTIAL CEP
Fairfax County,1150309,7.4,191,47,37501,25,144,PARTIAL CEP
Page County,23709,7.4,8,8,2972,100,0,FULL CEP
Williamsburg-James City County,78254,7.4,16,8,5161,50,8,PARTIAL CEP
Southampton County,17996,7.3,6,6,2380,100,0,FULL CEP
Madison County,13837,7.0,4,4,1592,100,0,FULL CEP
Roanoke County,96929,6.6,27,10,4927,37,17,PARTIAL CEP
Arlington County,283643,6.4,36,9,6772,25,27,PARTIAL CEP
King George County,26723,6.4,5,1,682,20,4,PARTIAL CEP
Frederick County,91419,6.0,21,9,4230,43,12,PARTIAL CEP
Botetourt County,33596,5.2,11,2,405,18,9,PARTIAL CEP
Hanover County,109979,4.6,22,3,1675,14,19,PARTIAL CEP
Loudoun County,420959,4.6,98,11,6443,11,87,PARTIAL CEP
Stafford County,156927,4.5,33,9,6195,27,24,PARTIAL CEP
New Kent County,22945,4.3,5,0,0,0,5,NO CEP
Fauquier County,72972,4.0,19,2,342,11,17,PARTIAL CEP
Cumberland County,9675,3.6,3,3,1292,100,0,FULL CEP
Goochland County,24727,3.3,5,0,0,0,5,NO CEP
Richmond County,8923,2.3,2,2,1421,100,0,FULL CEP
Powhatan County,30333,1.5,5,0,0,0,5,NO CEP
Falls Church City,14658,0.9,0,0,0,0,0,NO CEP
West Point Town,3414,0.0,2,2,859,100,0,FULL CEP"""
    
    df = pd.read_csv(io.StringIO(csv_data))
    
    # Convert numeric columns
    df['Population'] = df['Population'].astype(int)
    df['Poverty_Rate'] = df['Poverty_Rate'].astype(float)
    df['Eligible_Schools'] = df['Eligible_Schools'].astype(int)
    df['CEP_Schools'] = df['CEP_Schools'].astype(int)
    df['Students_in_CEP'] = df['Students_in_CEP'].astype(int)
    df['Coverage_Pct'] = df['Coverage_Pct'].astype(int)
    df['School_Gap'] = df['School_Gap'].astype(int)
    
    # Add School_Districts column (all Virginia counties have 1 district)
    df['School_Districts'] = 1
    
    # Calculate Children_in_Poverty from Poverty_Rate
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    
    # CONSISTENCY FIX: Normalize status using shared function
    df['Status'] = df['Status'].apply(normalize_status)
    # Add numeric status for map
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    
    return df

STATE_DATA = {
    'WI': {'name': 'Wisconsin', 'eligible_schools': 1295, 'cep_schools': 714, 'students_in_cep': 270136, 'children_without_cep': 41943, 'coverage_pct': 55, 'has_data': True, 'lat': 44.5, 'lon': -89.5},
    'NJ': {'name': 'New Jersey', 'eligible_schools': 1810, 'cep_schools': 584, 'students_in_cep': 260318, 'children_without_cep': 826612, 'coverage_pct': 32, 'has_data': True, 'lat': 40.0, 'lon': -74.5},
    'VA': {'name': 'Virginia', 'eligible_schools': 1850, 'cep_schools': 1054, 'students_in_cep': 389000, 'children_without_cep': 142000, 'coverage_pct': 57, 'has_data': True, 'lat': 37.5, 'lon': -78.5},
    'SC': {'name': 'South Carolina', 'eligible_schools': 1100, 'cep_schools': 979, 'students_in_cep': 425000, 'children_without_cep': 51000, 'coverage_pct': 89, 'has_data': False, 'lat': 33.8, 'lon': -81.0},
    'NV': {'name': 'Nevada', 'eligible_schools': 550, 'cep_schools': 234, 'students_in_cep': 98000, 'children_without_cep': 87000, 'coverage_pct': 43, 'has_data': False, 'lat': 39.0, 'lon': -117.0},
    'AR': {'name': 'Arkansas', 'eligible_schools': 850, 'cep_schools': 521, 'students_in_cep': 187000, 'children_without_cep': 96000, 'coverage_pct': 61, 'has_data': False, 'lat': 34.8, 'lon': -92.2}
}

# Border states for quick comparison (helps elected officials)
BORDER_STATES = {
    'WI': ['IL', 'IA', 'MI', 'MN'],
    'NJ': ['NY', 'PA', 'DE'],
    'VA': ['MD', 'NC', 'TN', 'WV', 'KY'],
    'SC': ['NC', 'GA'],
    'NV': ['CA', 'OR', 'ID', 'UT', 'AZ'],
    'AR': ['MO', 'TN', 'MS', 'LA', 'TX', 'OK'],
    'HI': [],  # No border states
    'ND': ['MN', 'SD', 'MT'],
    'AL': ['TN', 'GA', 'FL', 'MS'],
    'AK': [],
    'AZ': ['CA', 'NV', 'UT', 'NM'],
    'CA': ['OR', 'NV', 'AZ'],
    'CO': ['WY', 'NE', 'KS', 'OK', 'NM', 'UT'],
    'CT': ['MA', 'RI', 'NY'],
    'DE': ['PA', 'MD', 'NJ'],
    'FL': ['AL', 'GA'],
    'GA': ['FL', 'AL', 'TN', 'NC', 'SC'],
    'ID': ['MT', 'WY', 'UT', 'NV', 'OR', 'WA'],
    'IL': ['WI', 'IA', 'MO', 'KY', 'IN'],
    'IN': ['MI', 'OH', 'KY', 'IL'],
    'IA': ['MN', 'WI', 'IL', 'MO', 'NE', 'SD'],
    'KS': ['NE', 'MO', 'OK', 'CO'],
    'KY': ['IL', 'IN', 'OH', 'WV', 'VA', 'TN', 'MO'],
    'LA': ['TX', 'AR', 'MS'],
    'ME': ['NH'],
    'MD': ['PA', 'DE', 'VA', 'WV'],
    'MA': ['NH', 'VT', 'NY', 'CT', 'RI'],
    'MI': ['WI', 'IN', 'OH'],
    'MN': ['WI', 'IA', 'SD', 'ND'],
    'MS': ['TN', 'AL', 'LA', 'AR'],
    'MO': ['IA', 'IL', 'KY', 'TN', 'AR', 'OK', 'KS', 'NE'],
    'MT': ['ND', 'SD', 'WY', 'ID'],
    'NE': ['SD', 'IA', 'MO', 'KS', 'CO', 'WY'],
    'NH': ['ME', 'MA', 'VT'],
    'NM': ['CO', 'OK', 'TX', 'AZ'],
    'NY': ['VT', 'MA', 'CT', 'NJ', 'PA'],
    'NC': ['VA', 'TN', 'GA', 'SC'],
    'OH': ['MI', 'PA', 'WV', 'KY', 'IN'],
    'OK': ['KS', 'MO', 'AR', 'TX', 'NM', 'CO'],
    'OR': ['WA', 'ID', 'NV', 'CA'],
    'PA': ['NY', 'NJ', 'DE', 'MD', 'WV', 'OH'],
    'RI': ['MA', 'CT'],
    'SD': ['ND', 'MN', 'IA', 'NE', 'WY', 'MT'],
    'TN': ['KY', 'VA', 'NC', 'GA', 'AL', 'MS', 'AR', 'MO'],
    'TX': ['OK', 'AR', 'LA', 'NM'],
    'UT': ['ID', 'WY', 'CO', 'NM', 'AZ', 'NV'],
    'VT': ['NY', 'NH', 'MA'],
    'WA': ['ID', 'OR'],
    'WV': ['OH', 'PA', 'MD', 'VA', 'KY'],
    'WY': ['MT', 'SD', 'NE', 'CO', 'UT', 'ID']
}

# Extended state data for border state comparisons (coverage percentages)
ALL_STATES_COVERAGE = {
    'AL': 28, 'AK': 31, 'AZ': 42, 'AR': 61, 'CA': 48, 'CO': 35, 'CT': 41,
    'DE': 52, 'FL': 38, 'GA': 44, 'HI': 45, 'ID': 29, 'IL': 47, 'IN': 36,
    'IA': 38, 'KS': 33, 'KY': 72, 'LA': 51, 'ME': 68, 'MD': 45, 'MA': 49,
    'MI': 54, 'MN': 67, 'MS': 58, 'MO': 42, 'MT': 31, 'NE': 35, 'NV': 43,
    'NH': 27, 'NJ': 32, 'NM': 76, 'NY': 45, 'NC': 46, 'ND': 34, 'OH': 41,
    'OK': 39, 'OR': 62, 'PA': 52, 'RI': 44, 'SC': 89, 'SD': 30, 'TN': 48,
    'TX': 37, 'UT': 26, 'VT': 65, 'VA': 57, 'WA': 58, 'WV': 71, 'WI': 55, 'WY': 24
}

NATIONAL_STATS = {
    'total_children_without_cep': sum(s['children_without_cep'] for s in STATE_DATA.values()),
    'total_students_served': sum(s['students_in_cep'] for s in STATE_DATA.values()),
    'eligible_schools_not_participating': sum(s['eligible_schools'] - s['cep_schools'] for s in STATE_DATA.values()),
    'avg_coverage': int(sum(s['coverage_pct'] for s in STATE_DATA.values()) / len(STATE_DATA))
}

STATE_EXECUTIVES = {
    'WI': [
        # Executive Branch
        {'title': 'Governor', 'name': 'Tony Evers', 'party': 'Democrat', 'portrait_url': 'https://evers.wi.gov/PublishingImages/GovEvers_social.jpg', 'branch': 'Executive'},
        # Legislative Branch - Senate
        {'title': 'Senate Majority Leader', 'name': 'Devin LeMahieu', 'party': 'Republican', 'portrait_url': 'https://docs.legis.wisconsin.gov/2023/legislators/senate/1875/lemahieu_devin.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'John Jagler', 'party': 'Republican', 'portrait_url': 'https://docs.legis.wisconsin.gov/2023/legislators/senate/1971/jagler_john.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Appropriations Chair', 'name': 'Howard Marklein', 'party': 'Republican', 'portrait_url': 'https://docs.legis.wisconsin.gov/2023/legislators/senate/1871/marklein_howard_l.jpg', 'branch': 'Legislative'},
        # Legislative Branch - House
        {'title': 'Assembly Speaker', 'name': 'Robin Vos', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Majority Leader', 'name': 'Tyler August', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Education Chair', 'name': 'Joel Kitchens', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Appropriations Co-Chair', 'name': 'Mark Born', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'NJ': [
        # Executive Branch
        {'title': 'Governor', 'name': 'Mikie Sherrill', 'party': 'Democrat', 'portrait_url': 'https://sherrill.house.gov/sites/evo-subsites/sherrill.house.gov/files/evo-media-image/sherrill_official.jpg', 'branch': 'Executive'},
        # Legislative Branch - Senate
        {'title': 'Senate President', 'name': 'Nicholas Scutari', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/scutari_nicholas_p.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'M. Teresa Ruiz', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/ruiz_m_teresa.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Vin Gopal', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/gopal_vin.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Appropriations Chair', 'name': 'Paul Sarlo', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/sarlo_paul_a.jpg', 'branch': 'Legislative'},
        # Legislative Branch - Assembly
        {'title': 'Assembly Speaker', 'name': 'Craig Coughlin', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/coughlin_craig_j.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Majority Leader', 'name': 'Louis Greenwald', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Education Chair', 'name': 'Pamela Lampitt', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Appropriations Chair', 'name': 'Eliana Pintor Marin', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'VA': [
        # Executive Branch
        {'title': 'Governor', 'name': 'Glenn Youngkin', 'party': 'Republican', 'portrait_url': 'https://www.governor.virginia.gov/media/governorvirginiagov/images/governor/Glenn_Youngkin_Headshot.jpg', 'branch': 'Executive'},
        {'title': 'Lieutenant Governor', 'name': 'Winsome Sears', 'party': 'Republican', 'portrait_url': 'https://www.ltgov.virginia.gov/media/ltgovvirginiagov/images/lt-governor/Headshot---Lt.-Governor-Sears.jpg', 'branch': 'Executive'},
        # Legislative Branch - Senate
        {'title': 'Senate Majority Leader', 'name': 'Scott Surovell', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/S0036.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Ghazala Hashmi', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/S0010.jpg', 'branch': 'Legislative'},
        # Legislative Branch - House
        {'title': 'House Speaker', 'name': 'Don Scott', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/H0080.jpg', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Charniele Herring', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Education Chair', 'name': 'Schuyler VanValkenburg', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/H0072.jpg', 'branch': 'Legislative'},
        {'title': 'House Appropriations Chair', 'name': 'Luke Torian', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/H0052.jpg', 'branch': 'Legislative'}
    ]
}

# ====================
# HOMEPAGE (REDESIGNED)
# ====================

def create_hero_section():
    return html.Div([
        html.Div([
            html.H1("CEP Expansion Is the Fastest Way to Eliminate School Hunger", 
                style={
                    'fontSize': '60px', 
                    'fontWeight': '700', 
                    'color': COLORS['text_primary'], 
                    'marginBottom': '24px', 
                    'lineHeight': '1.08', 
                    'maxWidth': '1100px', 
                    'marginLeft': 'auto', 
                    'marginRight': 'auto', 
                    'letterSpacing': '-0.025em'
                }
            ), 
            html.P("Across America, millions of children in poverty attend schools that are eligible for the Community Eligibility Provision but haven't adopted it. States have an immediate opportunity to close this gap.", 
                style={
                    'fontSize': '22px', 
                    'color': COLORS['text_secondary'], 
                    'maxWidth': '820px', 
                    'margin': '0 auto 16px auto', 
                    'lineHeight': '1.6',
                    'fontWeight': '400'
                }
            ),
            # Credibility marker
            html.Div("Last Updated: May 6, 2026 | CEP Policy Intelligence Platform",
                style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'opacity': '0.7',
                    'marginBottom': '48px',
                    'letterSpacing': '0.3px'
                }
            ),
            html.Div([
                html.Div([
                    html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", 
                        style={
                            'fontSize': '68px', 
                            'fontWeight': '700', 
                            'color': COLORS['teal'], 
                            'lineHeight': '1',
                            'letterSpacing': '-0.02em'
                        }
                    ), 
                    html.Div("CHILDREN WITHOUT CEP", 
                        style={
                            'fontSize': '13px', 
                            'color': COLORS['text_secondary'], 
                            'textTransform': 'uppercase', 
                            'letterSpacing': '1.2px', 
                            'marginTop': '12px',
                            'fontWeight': '600'
                        }
                    )
                ], style={'textAlign': 'center'}), 
                html.Div([
                    html.Div(f"{NATIONAL_STATS['avg_coverage']}%", 
                        style={
                            'fontSize': '68px', 
                            'fontWeight': '700', 
                            'color': COLORS['teal'], 
                            'lineHeight': '1',
                            'letterSpacing': '-0.02em'
                        }
                    ), 
                    html.Div("AVERAGE COVERAGE", 
                        style={
                            'fontSize': '13px', 
                            'color': COLORS['text_secondary'], 
                            'textTransform': 'uppercase', 
                            'letterSpacing': '1.2px', 
                            'marginTop': '12px',
                            'fontWeight': '600'
                        }
                    )
                ], style={'textAlign': 'center'})
            ], style={
                'display': 'flex', 
                'justifyContent': 'center', 
                'gap': '80px', 
                'marginTop': '56px'
            })
        ], style={
            'maxWidth': '1400px', 
            'margin': '0 auto', 
            'padding': '120px 40px 100px 40px', 
            'textAlign': 'center'
        })
    ], style={
        'background': f'linear-gradient(135deg, #fafafa 0%, #f3f4f6 100%)', 
        'borderBottom': f'1px solid {COLORS["border"]}'
    })

def create_insights_section():
    insights = [
        {
            'title': 'Largest Coverage Gap', 
            'metric': '826K', 
            'text': 'children in New Jersey could gain access through expanded CEP adoption'
        }, 
        {
            'title': 'Leading Implementation', 
            'metric': '89%', 
            'text': 'of eligible schools in South Carolina currently participate in CEP'
        }, 
        {
            'title': 'Unserved Communities', 
            'metric': '24', 
            'text': 'counties in Wisconsin have zero CEP participation despite clear eligibility'
        }, 
        {
            'title': 'National Opportunity', 
            'metric': f"{NATIONAL_STATS['eligible_schools_not_participating']:,}", 
            'text': 'eligible schools not yet participating across all tracked states'
        }
    ]
    
    insight_cards = [
        html.Div([
            html.H3(i['title'], style={
                'fontSize': '16px', 
                'fontWeight': '600', 
                'marginBottom': '16px', 
                'color': COLORS['text_secondary'],
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            }), 
            html.Div(i['metric'], style={
                'fontSize': '48px', 
                'fontWeight': '700', 
                'color': COLORS['teal'], 
                'marginBottom': '12px',
                'lineHeight': '1',
                'letterSpacing': '-0.02em'
            }), 
            html.P(i['text'], style={
                'fontSize': '15px', 
                'color': COLORS['text_secondary'], 
                'lineHeight': '1.6', 
                'margin': '0'
            })
        ], style={
            'background': 'white', 
            'border': f'1px solid {COLORS["border"]}', 
            'borderRadius': '12px', 
            'padding': '36px 32px', 
            'boxShadow': '0 1px 3px rgba(0,0,0,0.05)',
            'transition': 'all 0.2s ease'
        }) 
        for i in insights
    ]
    
    return html.Div([
        html.H2("Policy Impact Snapshot", style={
            'fontSize': '36px', 
            'fontWeight': '600', 
            'marginBottom': '48px', 
            'color': COLORS['text_primary'],
            'letterSpacing': '-0.015em'
        }), 
        html.Div(insight_cards, style={
            'display': 'grid', 
            'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 
            'gap': '24px'
        })
    ], style={
        'maxWidth': '1400px', 
        'margin': '0 auto', 
        'padding': '96px 40px'
    })

def create_us_map():
    """Enhanced: Interactive US map with state names on hover and FPL visual boost
    FPL states (HI, NJ, ND) have thicker borders for visibility"""
    # Prepare data for all US states
    all_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
    # Map states to numeric categories for color mapping
    state_z_values = []
    state_line_widths = []  # Custom line widths for FPL emphasis
    
    for state in all_states:
        category = get_state_category(state)
        if category == 'universal_meals':
            state_z_values.append(4)  # Green
            state_line_widths.append(2)
        elif category == 'universal_breakfast':
            state_z_values.append(3)  # Amber
            state_line_widths.append(2)
        elif category == 'fpl_states':
            state_z_values.append(2)  # Blue (FPL states)
            state_line_widths.append(4)  # THICKER borders for FPL states (HI, NJ, ND)
        else:
            state_z_values.append(1)  # Gray
            state_line_widths.append(2)
    
    state_names = [STATE_DATA.get(state, {}).get('name', state) for state in all_states]
    
    # FPL percentage mapping
    fpl_percentages = {
        'HI': '300% of FPL',
        'NJ': '225% of FPL',
        'ND': '225% of FPL'
    }
    
    # RESTORED: Hover text showing state names and categories
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
        hovertemplate='%{hovertext}<extra></extra>',  # RESTORED
        marker=dict(
            line=dict(color='white', width=3)  # Base width, FPL states get thicker visual emphasis
        ),
        colorscale=[
            [0, COLORS['other_states']],      # 1 = Gray
            [0.33, COLORS['fpl_states']],     # 2 = Blue (FPL states)
            [0.67, COLORS['universal_breakfast']],  # 3 = Amber/Yellow
            [1, COLORS['universal_meals']]    # 4 = Green
        ],
        zmin=1,
        zmax=4,
        showscale=False
    ))
    
    # Enhanced tooltip styling for clean appearance
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
        showsubunits=True,
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

def create_state_detail_panel(state_abbr=None):
    """Enhanced: Premium detail panel with FPL emphasis and border states comparison"""
    if not state_abbr:
        # Default state - emphasize FPL states
        return html.Div([
            html.Div([
                html.Div("Click any state to view detailed information", 
                    style={
                        'fontSize': '14px',
                        'color': COLORS['text_secondary'],
                        'marginBottom': '20px',
                        'textAlign': 'center'
                    }),
                html.Div([
                    html.Div("Featured FPL States:", style={
                        'fontSize': '13px',
                        'fontWeight': '600',
                        'color': COLORS['text_secondary'],
                        'marginBottom': '12px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }),
                    html.Div([
                        html.Div("🔵 Hawaii (HI)", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '4px'}),
                        html.Div("300% FPL - Highest threshold", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '12px'})
                    ]),
                    html.Div([
                        html.Div("🔵 New Jersey (NJ)", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '4px'}),
                        html.Div("225% FPL - 32% coverage", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '12px'})
                    ]),
                    html.Div([
                        html.Div("🔵 North Dakota (ND)", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '4px'}),
                        html.Div("225% FPL - 34% coverage", style={'fontSize': '12px', 'color': COLORS['text_secondary']})
                    ])
                ])
            ])
        ], style={
            'background': 'white',
            'padding': '24px',
            'borderRadius': '12px',
            'border': f'1px solid {COLORS["border"]}',
            'minHeight': '400px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        })
    
    # Get state data
    state_data = STATE_DATA.get(state_abbr, {})
    state_name = state_data.get('name', state_abbr)
    category = get_state_category(state_abbr)
    
    # FPL percentages
    fpl_percentages = {'HI': 300, 'NJ': 225, 'ND': 225}
    
    # Category badge styling
    if category == 'universal_meals':
        badge_color = COLORS['universal_meals']
        badge_text = '🟢 Universal School Meals'
    elif category == 'universal_breakfast':
        badge_color = COLORS['universal_breakfast']
        badge_text = '🟡 Universal School Breakfast'
    elif category == 'fpl_states':
        badge_color = COLORS['fpl_states']
        badge_text = '🔵 Federal Poverty Level'
    else:
        badge_color = COLORS['text_secondary']
        badge_text = 'CEP Tracked'
    
    content = [
        # State name
        html.H3(state_name, style={
            'fontSize': '22px',
            'fontWeight': '600',
            'margin': '0 0 12px 0',
            'color': COLORS['text_primary']
        }),
        
        # Category badge
        html.Div(badge_text, style={
            'display': 'inline-block',
            'background': badge_color,
            'color': 'white',
            'padding': '6px 14px',
            'borderRadius': '16px',
            'fontSize': '13px',
            'fontWeight': '500',
            'marginBottom': '20px'
        })
    ]
    
    # FPL percentage (if applicable)
    if category == 'fpl_states' and state_abbr in fpl_percentages:
        content.append(
            html.Div([
                html.Div('FPL Threshold', style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'marginBottom': '4px'
                }),
                html.Div(f"{fpl_percentages[state_abbr]}% of FPL", style={
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': COLORS['text_primary']
                })
            ], style={
                'marginBottom': '16px',
                'paddingBottom': '16px',
                'borderBottom': f'0.5px solid {COLORS["border"]}'
            })
        )
    
    # CEP Coverage
    coverage = state_data.get('coverage_pct') or ALL_STATES_COVERAGE.get(state_abbr, 0)
    if coverage:
        content.append(
            html.Div([
                html.Div('CEP Coverage', style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'marginBottom': '4px'
                }),
                html.Div(f"{coverage}%", style={
                    'fontSize': '24px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary']
                })
            ], style={
                'marginBottom': '16px',
                'paddingBottom': '16px',
                'borderBottom': f'0.5px solid {COLORS["border"]}'
            })
        )
    
    # Schools and students (if detailed data available)
    if state_data:
        content.append(
            html.Div([
                html.Div('Schools Participating', style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'marginBottom': '4px'
                }),
                html.Div(f"{state_data.get('cep_schools', 0):,} of {state_data.get('eligible_schools', 0):,}", style={
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': COLORS['text_primary']
                })
            ], style={
                'marginBottom': '16px',
                'paddingBottom': '16px',
                'borderBottom': f'0.5px solid {COLORS["border"]}'
            })
        )
        
        content.append(
            html.Div([
                html.Div('Students Served', style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'marginBottom': '4px'
                }),
                html.Div(f"{state_data.get('students_in_cep', 0):,}", style={
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': COLORS['text_primary']
                })
            ], style={'marginBottom': '20px'})
        )
    
    # Border states comparison
    border_states = BORDER_STATES.get(state_abbr, [])
    if border_states:
        border_items = []
        for bs in border_states[:4]:  # Show max 4 border states
            bs_coverage = ALL_STATES_COVERAGE.get(bs, 0)
            bs_name = STATE_DATA.get(bs, {}).get('name', bs)
            if not bs_name or bs_name == bs:
                # Fallback to state name lookup
                state_names_map = {
                    'IL': 'Illinois', 'IA': 'Iowa', 'MI': 'Michigan', 'MN': 'Minnesota',
                    'NY': 'New York', 'PA': 'Pennsylvania', 'DE': 'Delaware',
                    'MD': 'Maryland', 'NC': 'North Carolina', 'TN': 'Tennessee',
                    'WV': 'West Virginia', 'KY': 'Kentucky', 'GA': 'Georgia',
                    'CA': 'California', 'OR': 'Oregon', 'ID': 'Idaho', 'UT': 'Utah',
                    'AZ': 'Arizona', 'MO': 'Missouri', 'MS': 'Mississippi',
                    'LA': 'Louisiana', 'TX': 'Texas', 'OK': 'Oklahoma'
                }
                bs_name = state_names_map.get(bs, bs)
            
            border_items.append(
                html.Div(f"• {bs_name}: {bs_coverage}%", style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'marginBottom': '6px'
                })
            )
        
        content.append(
            html.Div([
                html.Div('Border States', style={
                    'fontSize': '13px',
                    'fontWeight': '600',
                    'color': COLORS['text_secondary'],
                    'marginBottom': '8px',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                }),
                html.Div(border_items)
            ], style={
                'marginBottom': '20px',
                'paddingBottom': '20px',
                'borderBottom': f'0.5px solid {COLORS["border"]}'
            })
        )
    
    # View Details button
    content.append(
        html.A('View County Details →', 
            href=f'/state/{state_abbr}',
            style={
                'display': 'block',
                'width': '100%',
                'padding': '12px',
                'background': 'transparent',
                'border': f'0.5px solid {COLORS["border"]}',
                'borderRadius': '8px',
                'fontSize': '14px',
                'fontWeight': '500',
                'color': COLORS['text_primary'],
                'textAlign': 'center',
                'textDecoration': 'none',
                'transition': 'all 0.2s'
            }
        )
    )
    
    return html.Div(content, style={
        'background': 'white',
        'padding': '24px',
        'borderRadius': '12px',
        'border': f'1px solid {COLORS["border"]}',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.04)',
        'minHeight': '400px'
    })

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
    """Enhanced: 3-column layout - Map + Detail Panel + Explore States"""
    
    # Legend for the map - polished pills
    legend = html.Div([
        html.Div([
            html.Div(style={
                'width': '20px', 
                'height': '20px', 
                'background': COLORS['universal_meals'], 
                'borderRadius': '6px', 
                'marginRight': '10px',
                'boxShadow': '0 1px 2px rgba(0,0,0,0.1)'
            }),
            html.Span("Universal Meals (9)", style={
                'fontSize': '14px', 
                'color': COLORS['text_secondary'],
                'fontWeight': '500'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '28px'}),
        html.Div([
            html.Div(style={
                'width': '20px', 
                'height': '20px', 
                'background': COLORS['universal_breakfast'], 
                'borderRadius': '6px', 
                'marginRight': '10px',
                'boxShadow': '0 1px 2px rgba(0,0,0,0.1)'
            }),
            html.Span("Universal Breakfast (3)", style={
                'fontSize': '14px', 
                'color': COLORS['text_secondary'],
                'fontWeight': '500'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '28px'}),
        html.Div([
            html.Div(style={
                'width': '20px', 
                'height': '20px', 
                'background': COLORS['fpl_states'], 
                'borderRadius': '6px', 
                'marginRight': '10px',
                'boxShadow': '0 1px 2px rgba(0,0,0,0.1)'
            }),
            html.Span("FPL States (3)", style={
                'fontSize': '14px', 
                'color': COLORS['text_secondary'],
                'fontWeight': '500'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '28px'}),
        html.Div([
            html.Div(style={
                'width': '20px', 
                'height': '20px', 
                'background': COLORS['other_states'], 
                'borderRadius': '6px', 
                'marginRight': '10px',
                'border': f'1px solid {COLORS["border"]}'
            }),
            html.Span("Other States", style={
                'fontSize': '14px', 
                'color': COLORS['text_secondary'],
                'fontWeight': '500'
            })
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={
        'display': 'flex', 
        'flexWrap': 'wrap', 
        'gap': '8px',
        'marginBottom': '28px', 
        'padding': '20px 24px', 
        'background': COLORS['off_white'], 
        'borderRadius': '10px',
        'border': f'1px solid {COLORS["border"]}'
    })
    
    # All state options for search dropdown
    all_state_options = [
        {'label': 'Alabama', 'value': 'AL'}, {'label': 'Alaska', 'value': 'AK'},
        {'label': 'Arizona', 'value': 'AZ'}, {'label': 'Arkansas', 'value': 'AR'},
        {'label': 'California', 'value': 'CA'}, {'label': 'Colorado', 'value': 'CO'},
        {'label': 'Connecticut', 'value': 'CT'}, {'label': 'Delaware', 'value': 'DE'},
        {'label': 'Florida', 'value': 'FL'}, {'label': 'Georgia', 'value': 'GA'},
        {'label': 'Hawaii', 'value': 'HI'}, {'label': 'Idaho', 'value': 'ID'},
        {'label': 'Illinois', 'value': 'IL'}, {'label': 'Indiana', 'value': 'IN'},
        {'label': 'Iowa', 'value': 'IA'}, {'label': 'Kansas', 'value': 'KS'},
        {'label': 'Kentucky', 'value': 'KY'}, {'label': 'Louisiana', 'value': 'LA'},
        {'label': 'Maine', 'value': 'ME'}, {'label': 'Maryland', 'value': 'MD'},
        {'label': 'Massachusetts', 'value': 'MA'}, {'label': 'Michigan', 'value': 'MI'},
        {'label': 'Minnesota', 'value': 'MN'}, {'label': 'Mississippi', 'value': 'MS'},
        {'label': 'Missouri', 'value': 'MO'}, {'label': 'Montana', 'value': 'MT'},
        {'label': 'Nebraska', 'value': 'NE'}, {'label': 'Nevada', 'value': 'NV'},
        {'label': 'New Hampshire', 'value': 'NH'}, {'label': 'New Jersey', 'value': 'NJ'},
        {'label': 'New Mexico', 'value': 'NM'}, {'label': 'New York', 'value': 'NY'},
        {'label': 'North Carolina', 'value': 'NC'}, {'label': 'North Dakota', 'value': 'ND'},
        {'label': 'Ohio', 'value': 'OH'}, {'label': 'Oklahoma', 'value': 'OK'},
        {'label': 'Oregon', 'value': 'OR'}, {'label': 'Pennsylvania', 'value': 'PA'},
        {'label': 'Rhode Island', 'value': 'RI'}, {'label': 'South Carolina', 'value': 'SC'},
        {'label': 'South Dakota', 'value': 'SD'}, {'label': 'Tennessee', 'value': 'TN'},
        {'label': 'Texas', 'value': 'TX'}, {'label': 'Utah', 'value': 'UT'},
        {'label': 'Vermont', 'value': 'VT'}, {'label': 'Virginia', 'value': 'VA'},
        {'label': 'Washington', 'value': 'WA'}, {'label': 'West Virginia', 'value': 'WV'},
        {'label': 'Wisconsin', 'value': 'WI'}, {'label': 'Wyoming', 'value': 'WY'}
    ]
    
    return html.Div([
        html.Div([
            html.H2("National School Meal Coverage", style={
                'fontSize': '36px',
                'fontWeight': '600',
                'marginBottom': '24px',
                'color': COLORS['text_primary'],
                'letterSpacing': '-0.015em'
            }),
            
            # Search box
            html.Div([
                dcc.Dropdown(
                    id='state-search-dropdown',
                    options=all_state_options,
                    placeholder='🔍 Search states...',
                    clearable=True,
                    searchable=True,
                    style={'maxWidth': '400px'}
                )
            ], style={'marginBottom': '24px'}),
            
            legend,
            
            # 2-SECTION LAYOUT: Map (left) + Explore States (right)
            html.Div([
                # Left: Map (takes most of the space)
                html.Div([
                    dcc.Graph(
                        id='us-map-graph',
                        figure=create_us_map(),
                        config={'displayModeBar': False},
                        style={
                            'background': 'white',
                            'border': f'1px solid {COLORS["border"]}',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'
                        }
                    )
                ]),
                
                # Right: Explore States Panel
                html.Div([
                    create_explore_states_panel()
                ])
                
            ], style={
                'display': 'grid',
                'gridTemplateColumns': '1fr 400px',  # Main map + Explore States sidebar
                'gap': '24px',
                'marginBottom': '24px'
            }),
            
            # County Map Container (hidden by default)
            html.Div(id='county-map-container', children=[], style={'marginTop': '24px'})
            
        ], style={'maxWidth': '1400px', 'margin': '0 auto'})
    ], style={'padding': '96px 40px', 'background': 'white'})

def create_comparison_section():
    """Enhanced: Comparison with side-by-side county maps"""
    return html.Div([
        html.Div([
            html.H2("Compare States", style={
                'fontSize': '36px',
                'fontWeight': '600',
                'marginBottom': '28px',
                'color': COLORS['text_primary'],
                'letterSpacing': '-0.015em'
            }),
            
            # Dropdowns
            html.Div([
                html.Div([
                    html.Label("State A", style={
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='compare-state-a',
                        options=[{'label': data['name'], 'value': abbr} for abbr, data in STATE_DATA.items()],
                        value='WI',
                        clearable=False,
                        style={'minWidth': '200px'}
                    )
                ], style={'flex': '1'}),
                
                html.Div([
                    html.Label("State B", style={
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='compare-state-b',
                        options=[{'label': data['name'], 'value': abbr} for abbr, data in STATE_DATA.items()],
                        value='NJ',
                        clearable=False,
                        style={'minWidth': '200px'}
                    )
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '32px'}),
            
            # Comparison cards
            html.Div(id='comparison-output'),
            
            # County maps container (side-by-side)
            html.Div(id='comparison-county-maps', style={'marginTop': '32px'})
            
        ], style={'maxWidth': '1400px', 'margin': '0 auto'})
    ], style={'padding': '80px 40px', 'background': 'white'})

def create_cta_section():
    return html.Div([html.Div([html.H2("Take Action for Universal School Meals", style={'fontSize': '40px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '20px', 'textAlign': 'center'}), html.P("Contact your state representatives to advocate for CEP expansion in your community", style={'fontSize': '18px', 'color': COLORS['text_secondary'], 'textAlign': 'center', 'marginBottom': '40px'}), html.Div([html.A("Find Your Representatives", href="#", style={'background': COLORS['teal'], 'color': 'white', 'padding': '16px 40px', 'borderRadius': '8px', 'textDecoration': 'none', 'fontSize': '16px', 'fontWeight': '600', 'display': 'inline-block'})], style={'textAlign': 'center'})], style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '80px 40px'})], style={'background': f'linear-gradient(135deg, {COLORS["off_white"]} 0%, {COLORS["light_gray"]} 100%)'})

def create_landing_page():
    """Enhanced landing page - CTA section removed"""
    return html.Div([
        create_hero_section(),
        create_insights_section(),
        create_map_section(),
        create_comparison_section(),
        # Version indicator (small footer)
        html.Div("v2026-05-05", style={'textAlign': 'center', 'padding': '20px', 'fontSize': '11px', 'color': '#999'})
    ])

def create_comparison_cards(state_a, state_b):
    data_a = STATE_DATA[state_a]
    data_b = STATE_DATA[state_b]
    return html.Div([
        html.Div([
            html.H3(data_a['name'], style={'fontSize': '24px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}),
            html.Div([
                html.Div([
                    html.Div("Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}),
                    html.Div(f"{data_a['coverage_pct']}%", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})
                ], style={'marginBottom': '16px'}),
                html.Div([
                    html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}),
                    html.Div(f"{data_a['students_in_cep']:,}", style={'fontSize': '24px', 'fontWeight': '600', 'color': COLORS['text_primary']})
                ])
            ])
        ], style={'background': 'white', 'padding': '32px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
        html.Div([
            html.H3(data_b['name'], style={'fontSize': '24px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}),
            html.Div([
                html.Div([
                    html.Div("Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}),
                    html.Div(f"{data_b['coverage_pct']}%", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})
                ], style={'marginBottom': '16px'}),
                html.Div([
                    html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}),
                    html.Div(f"{data_b['students_in_cep']:,}", style={'fontSize': '24px', 'fontWeight': '600', 'color': COLORS['text_primary']})
                ])
            ])
        ], style={'background': 'white', 'padding': '32px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px'})

# ====================
# STATE DETAIL PAGES (ENHANCED WITH CONSISTENCY FIX)
# ====================

def create_state_executives_section(state_abbr):
    """Executive names colored by party with circular portraits and branch grouping"""
    executives = STATE_EXECUTIVES.get(state_abbr, [])
    if not executives:
        return html.Div()
    
    # Helper function to get initials
    def get_initials(name):
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}"
        return name[0] if name else "?"
    
    # Helper to create portrait circle with initials
    def create_portrait(official):
        name_color = get_party_color(official['party'])
        border_color = name_color
        return html.Div(get_initials(official['name']), style={
            'width': '40px', 'height': '40px', 'borderRadius': '50%',
            'border': f'2px solid {border_color}', 
            'backgroundColor': COLORS['off_white'],
            'display': 'flex', 'alignItems': 'center', 
            'justifyContent': 'center',
            'fontSize': '14px', 'fontWeight': '600', 
            'color': name_color,
            'flexShrink': '0'
        })
    
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
    
    # Group by branch AND chamber
    executive_branch = [e for e in executives if e['branch'] == 'Executive']
    
    # Separate Senate and House based on title keywords
    senate_titles = ['Senate', 'Lt. Governor', 'Lieutenant Governor']
    legislative_branch = [e for e in executives if e['branch'] == 'Legislative']
    
    state_senate = [e for e in legislative_branch if any(keyword in e['title'] for keyword in senate_titles)]
    state_house = [e for e in legislative_branch if not any(keyword in e['title'] for keyword in senate_titles)]
    
    sections = []
    
    # Executive Branch Section
    if executive_branch:
        exec_cards = []
        for official in executive_branch:
            name_color = get_party_color(official['party'])
            card = html.Div([
                create_portrait(official),
                html.Div([
                    html.Div(official['name'], style={'fontSize': '16px', 'fontWeight': '600', 'color': name_color, 'marginBottom': '2px'}),
                    html.Div(official['title'], style={'fontSize': '13px', 'color': COLORS['text_secondary']})
                ], style={'marginLeft': '12px', 'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'center', 'padding': '16px', 'background': 'white', 
                      'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}'})
            exec_cards.append(card)
        
        sections.append(html.Div([
            html.H3("Executive Branch", style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 
                                                'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px'}),
            html.Div(exec_cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))', 'gap': '12px'})
        ], style={'marginBottom': '24px'}))
    
    # State Senate Section
    if state_senate:
        senate_cards = []
        for official in state_senate:
            name_color = get_party_color(official['party'])
            card = html.Div([
                create_portrait(official),
                html.Div([
                    html.Div(official['name'], style={'fontSize': '16px', 'fontWeight': '600', 'color': name_color, 'marginBottom': '2px'}),
                    html.Div(official['title'], style={'fontSize': '13px', 'color': COLORS['text_secondary']})
                ], style={'marginLeft': '12px', 'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'center', 'padding': '16px', 'background': 'white', 
                      'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}'})
            senate_cards.append(card)
        
        sections.append(html.Div([
            html.H3("State Senate", style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 
                                           'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px'}),
            html.Div(senate_cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))', 'gap': '12px'})
        ], style={'marginBottom': '24px'}))
    
    # State House/Assembly Section
    if state_house:
        house_cards = []
        for official in state_house:
            name_color = get_party_color(official['party'])
            card = html.Div([
                create_portrait(official),
                html.Div([
                    html.Div(official['name'], style={'fontSize': '16px', 'fontWeight': '600', 'color': name_color, 'marginBottom': '2px'}),
                    html.Div(official['title'], style={'fontSize': '13px', 'color': COLORS['text_secondary']})
                ], style={'marginLeft': '12px', 'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'center', 'padding': '16px', 'background': 'white', 
                      'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}'})
            house_cards.append(card)
        
        sections.append(html.Div([
            html.H3("State House/Assembly", style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 
                                                    'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px'}),
            html.Div(house_cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))', 'gap': '12px'})
        ]))
    
    return html.Div([
        html.Div([
            html.H2("State Leadership", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '20px'}),
            legend
        ] + sections, style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 40px 40px'})
    ], style={'background': COLORS['off_white'], 'borderBottom': f'1px solid {COLORS["border"]}'})

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
        'NJ': {'lat': 40.0, 'lon': -74.5},
        'VA': {'lat': 37.5, 'lon': -78.5}
    }
    center = state_centers.get(state_abbr, {'lat': 39, 'lon': -98})
    
    fig.update_geos(
        fitbounds="locations",  # Auto-fit to data
        visible=False,  # Hide background
        projection_type="albers usa",  # Better projection for US states
        center=center
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
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
                {'if': {'filter_query': '{Status} = "FULL CEP"'}, 'backgroundColor': '#e0f2fe'},  # Light sky blue rows
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"'}, 'backgroundColor': '#fef3c7'},  # Light yellow rows
                {'if': {'filter_query': '{Status} = "NO CEP"'}, 'backgroundColor': '#fce7f3'},  # Light pink rows
                # Status pills (on top of row colors) - NEW COLORS: Sky Blue, Green, Pink
                {'if': {'filter_query': '{Status} = "FULL CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#87CEEB', 'color': '#1a1a1a', 'fontWeight': '600', 
                    'fontSize': '14px', 'padding': '8px 16px', 'borderRadius': '20px',
                    'textAlign': 'center'}, 
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#fbbf24', 'color': '#ffffff', 'fontWeight': '600', 
                    'fontSize': '14px', 'padding': '8px 16px', 'borderRadius': '20px',
                    'textAlign': 'center'}, 
                {'if': {'filter_query': '{Status} = "NO CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#ec4899', 'color': '#ffffff', 'fontWeight': '600', 
                    'fontSize': '14px', 'padding': '8px 16px', 'borderRadius': '20px',
                    'textAlign': 'center'}
            ], 
            style_filter={'backgroundColor': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '4px', 'padding': '8px', 'fontSize': '14px'}
        )
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})

def create_county_color_legend():
    """Simple inline legend for county CEP status colors"""
    return html.Div([
        html.Div([
            html.Span('■', style={'color': COLORS['full_cep'], 'fontSize': '18px', 'marginRight': '6px'}),
            html.Span('Sky Blue = Full CEP', style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'inline-flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([
            html.Span('■', style={'color': COLORS['partial_cep'], 'fontSize': '18px', 'marginRight': '6px'}),
            html.Span('Yellow = Partial CEP', style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'inline-flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([
            html.Span('■', style={'color': COLORS['no_cep'], 'fontSize': '18px', 'marginRight': '6px'}),
            html.Span('Pink = No CEP', style={'fontSize': '14px', 'color': COLORS['text_secondary']})
        ], style={'display': 'inline-flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'padding': '16px', 'marginTop': '12px', 
              'background': COLORS['off_white'], 'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}'})

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
    elif state_abbr == 'VA':
        df = load_virginia_data()
        fips_dict = VA_FIPS
    else:
        df = pd.DataFrame({'County': ['Sample'], 'Population': [100000], 'Children_in_Poverty': [15000], 'School_Districts': [10], 'Eligible_Schools': [25], 'CEP_Schools': [10], 'Students_in_CEP': [5000], 'Status': ['PARTIAL CEP'], 'Coverage_Pct': [40], 'School_Gap': [15]})
        df['Status'] = df['Status'].apply(normalize_status)  # CONSISTENCY FIX
        df['Status_Numeric'] = df['Status'].apply(status_to_numeric)  # CONSISTENCY FIX
        fips_dict = {}
    
    return html.Div([
        html.Div([html.Div([html.A("← All States", href="/", style={'color': COLORS['teal'], 'textDecoration': 'none', 'fontSize': '15px', 'fontWeight': '500', 'marginBottom': '24px', 'display': 'inline-block'}), html.H1(state_data['name'], style={'fontSize': '56px', 'fontWeight': '600', 'letterSpacing': '-0.02em', 'color': COLORS['text_primary'], 'marginBottom': '12px'}), html.P(f"{state_data['coverage_pct']}% CEP Coverage", style={'fontSize': '21px', 'color': COLORS['text_secondary']})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '60px 40px'})], style={'background': COLORS['white']}), 
        create_state_executives_section(state_abbr), 
        html.Div([html.Div([html.Div([html.Div("CEP Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['coverage_pct']}%", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['students_in_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("In CEP schools", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Opportunity", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['children_without_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("Children without CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Schools", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['cep_schools']}/{state_data['eligible_schools']}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("CEP vs Eligible", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}), 
        (html.Div([html.Div([html.H2("County-Level Coverage", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}), html.Div([dcc.Graph(figure=create_county_map(df, fips_dict, state_abbr), config={'displayModeBar': False})], style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), create_county_color_legend()], style={'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}) if fips_dict else html.Div()), 
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

# NEW CALLBACKS FOR ENHANCED LANDING PAGE

@application.callback(
    [Output('state-detail-panel', 'children'),
     Output('county-map-container', 'children')],
    [Input('us-map-graph', 'clickData'),
     Input('state-search-dropdown', 'value')]
)
def update_state_selection(click_data, search_value):
    """Update detail panel and county map when state is clicked or searched"""
    ctx = dash.callback_context
    
    state_abbr = None
    
    # Check if triggered by search
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'state-search-dropdown.value':
        if search_value:
            state_abbr = search_value
    # Check if triggered by map click
    elif click_data and 'points' in click_data and len(click_data['points']) > 0:
        state_abbr = click_data['points'][0]['location']
    
    if not state_abbr:
        # No selection - show default
        return create_state_detail_panel(), []
    
    # Create detail panel
    detail_panel = create_state_detail_panel(state_abbr)
    
    # Create county map if state has data
    county_map_content = []
    if state_abbr in ['WI', 'NJ']:
        # Load county data
        if state_abbr == 'WI':
            df = load_wisconsin_data()
            fips_dict = WI_FIPS
        else:  # NJ
            df = load_new_jersey_data()
            fips_dict = NJ_FIPS
        
        state_name = STATE_DATA[state_abbr]['name']
        
        county_map_content = [
            html.Div([
                html.H3(f"{state_name} County Map", style={
                    'fontSize': '18px',
                    'fontWeight': '600',
                    'marginBottom': '16px',
                    'color': COLORS['text_primary']
                }),
                html.Div([
                    dcc.Graph(
                        figure=create_county_map(df, fips_dict, state_abbr),
                        config={'displayModeBar': False}
                    )
                ], style={
                    'background': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'border': f'1px solid {COLORS["border"]}'
                })
            ], style={
                'padding': '20px',
                'background': COLORS['off_white'],
                'borderRadius': '12px',
                'border': f'1px solid {COLORS["border"]}'
            })
        ]
    
    return detail_panel, county_map_content

@application.callback(
    Output('comparison-county-maps', 'children'),
    [Input('compare-state-a', 'value'),
     Input('compare-state-b', 'value')]
)
def update_comparison_county_maps(state_a, state_b):
    """Show side-by-side county maps in comparison section"""
    if not state_a or not state_b:
        return []
    
    maps = []
    
    for state_abbr in [state_a, state_b]:
        if state_abbr in ['WI', 'NJ', 'VA']:
            # Load county data
            if state_abbr == 'WI':
                df = load_wisconsin_data()
                fips_dict = WI_FIPS
            elif state_abbr == 'NJ':
                df = load_new_jersey_data()
                fips_dict = NJ_FIPS
            elif state_abbr == 'VA':
                df = load_virginia_data()
                fips_dict = VA_FIPS
            
            state_name = STATE_DATA[state_abbr]['name']
            
            maps.append(
                html.Div([
                    html.H4(f"{state_name} Counties", style={
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '12px',
                        'color': COLORS['text_primary']
                    }),
                    html.Div([
                        dcc.Graph(
                            figure=create_county_map(df, fips_dict, state_abbr),
                            config={'displayModeBar': False}
                        )
                    ], style={
                        'background': 'white',
                        'padding': '16px',
                        'borderRadius': '12px',
                        'border': f'1px solid {COLORS["border"]}'
                    })
                ])
            )
        else:
            # State without county data
            state_name = STATE_DATA[state_abbr]['name']
            maps.append(
                html.Div([
                    html.H4(f"{state_name} Counties", style={
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '12px',
                        'color': COLORS['text_primary']
                    }),
                    html.Div([
                        html.Div("County-level data not available", style={
                            'padding': '40px',
                            'textAlign': 'center',
                            'color': COLORS['text_secondary'],
                            'fontSize': '14px'
                        })
                    ], style={
                        'background': 'white',
                        'padding': '16px',
                        'borderRadius': '12px',
                        'border': f'1px solid {COLORS["border"]}',
                        'minHeight': '200px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center'
                    })
                ])
            )
    
    return html.Div(maps, style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',
        'gap': '24px'
    })

if __name__ == '__main__':
    application.run(debug=False, host='0.0.0.0', port=8000)

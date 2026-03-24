# CEP Policy Intelligence Platform - ENHANCED
# 4 Targeted Enhancements to Wisconsin Page:
# 1. Executive names colored by party (maroon/blue)
# 2. County map fixed to show correct Full/Partial/No CEP
# 3. Table filters clean (header-only)
# 4. Status badges highly visible

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import pandas as pd

application = dash.Dash(__name__, suppress_callback_exceptions=True)
server = application.server

# Enhanced Color System
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
    'republican_name': '#991b1b'  # Maroon
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
    """Normalize status - used by map, table, and summaries"""
    if not status_str:
        return 'NO CEP'
    status_upper = str(status_str).upper().strip()
    if 'FULL' in status_upper:
        return 'FULL CEP'
    elif 'PARTIAL' in status_upper:
        return 'PARTIAL CEP'
    else:
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
    """Convert status to numeric for map (0=No, 1=Partial, 2=Full)"""
    normalized = normalize_status(status)
    if normalized == 'FULL CEP':
        return 2
    elif normalized == 'PARTIAL CEP':
        return 1
    else:
        return 0

# ====================
# STATE EXECUTIVES DATA
# ====================

STATE_EXECUTIVES = {
    'WI': {
        'Governor': {'name': 'Tony Evers', 'party': 'Democrat'},
        'State Treasurer': {'name': 'John Leiber', 'party': 'Republican'},
        'Senate Finance Co-Chair': {'name': 'Howard Marklein', 'party': 'Republican'},
        'Assembly Finance Co-Chair': {'name': 'Mark Born', 'party': 'Republican'}
    }
}

# ====================
# WISCONSIN DATA
# ====================

def load_wisconsin_data():
    """Load Wisconsin county data - 72 counties, all 11 columns"""
    data = {
        'County': ['Milwaukee', 'Dane', 'Racine', 'Rock', 'Brown', 'Kenosha', 'Waukesha', 'Winnebago', 'La Crosse', 'Outagamie', 'Marathon', 'Sheboygan', 'Eau Claire', 'Walworth', 'Fond du Lac', 'Wood', 'Manitowoc', 'Dodge', 'Portage', 'Washington', 'Jefferson', 'Douglas', 'Chippewa', 'Sauk', 'Grant', 'Monroe', 'St. Croix', 'Shawano', 'Barron', 'Marinette', 'Waupaca', 'Clark', 'Dunn', 'Columbia', 'Polk', 'Oneida', 'Vernon', 'Juneau', 'Ozaukee', 'Oconto', 'Trempealeau', 'Sawyer', 'Jackson', 'Lincoln', 'Calumet', 'Green', 'Pierce', 'Waushara', 'Vilas', 'Langlade', 'Richland', 'Rusk', 'Bayfield', 'Taylor', 'Ashland', 'Crawford', 'Washburn', 'Adams', 'Burnett', 'Door', 'Green Lake', 'Price', 'Menominee', 'Marquette', 'Forest', 'Iowa', 'Lafayette', 'Kewaunee', 'Buffalo', 'Iron', 'Pepin', 'Florence'],
        'Population': [939489, 561504, 197727, 163687, 268740, 169151, 406978, 171730, 120784, 190705, 138013, 118034, 105710, 105230, 104154, 74207, 81359, 89396, 70377, 136761, 86148, 44295, 66297, 65763, 51938, 46274, 93536, 40881, 46711, 41872, 51812, 34659, 45440, 58490, 44977, 37845, 30714, 26718, 91503, 38965, 30760, 18074, 21145, 28415, 52442, 37093, 42212, 24520, 23047, 19491, 17304, 14188, 16220, 19913, 16027, 16113, 16623, 20654, 16526, 30066, 19018, 14054, 4255, 15592, 9179, 23709, 16611, 20563, 13317, 6137, 7318, 4558],
        'Children_in_Poverty': [84614, 17942, 13021, 12356, 10526, 9652, 8958, 8619, 7196, 7162, 6492, 5732, 5723, 4622, 4380, 4068, 3984, 3801, 3586, 3496, 3408, 3099, 3048, 3023, 2986, 2972, 2710, 2540, 2536, 2531, 2509, 2447, 2244, 2184, 2132, 2040, 2039, 1924, 1863, 1714, 1691, 1681, 1643, 1619, 1618, 1563, 1545, 1466, 1433, 1388, 1239, 1217, 1215, 1194, 1183, 1142, 1094, 1066, 1041, 1034, 964, 963, 942, 916, 913, 906, 903, 754, 716, 466, 398, 287],
        'School_Districts': [38, 30, 13, 9, 20, 13, 15, 12, 8, 14, 13, 14, 8, 14, 12, 7, 10, 14, 8, 10, 9, 5, 10, 8, 10, 7, 8, 9, 9, 9, 9, 9, 8, 9, 9, 7, 8, 6, 9, 7, 7, 4, 5, 4, 7, 7, 6, 5, 6, 4, 4, 4, 7, 4, 4, 5, 4, 3, 4, 5, 4, 4, 2, 4, 4, 5, 6, 4, 5, 2, 2, 1],
        'Eligible_Schools': [317, 60, 33, 32, 42, 41, 14, 25, 19, 29, 33, 32, 23, 18, 26, 19, 17, 24, 15, 9, 14, 11, 17, 13, 14, 21, 6, 12, 13, 16, 13, 14, 10, 9, 14, 13, 14, 14, 5, 9, 8, 6, 6, 6, 9, 8, 4, 7, 10, 8, 7, 5, 17, 6, 6, 9, 7, 6, 9, 6, 6, 6, 5, 7, 7, 5, 7, 6, 8, 3, 2, 3],
        'CEP_Schools': [305, 22, 29, 26, 28, 36, 1, 21, 14, 17, 8, 30, 2, 4, 5, 8, 14, 4, 5, 0, 0, 0, 0, 4, 4, 4, 0, 4, 0, 8, 2, 6, 3, 5, 8, 5, 5, 6, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 3, 8, 0, 6, 11, 0, 1, 0, 0, 9, 5, 0, 4, 3, 5, 3, 5, 2, 0, 0, 0, 1, 0, 0],
        'Students_in_CEP': [135942, 6704, 17554, 9859, 11118, 18629, 214, 11651, 3113, 6236, 1649, 11483, 268, 550, 971, 1473, 5941, 810, 1233, 0, 0, 0, 0, 592, 840, 416, 0, 707, 0, 1448, 454, 591, 233, 1233, 1107, 1523, 700, 706, 0, 0, 0, 403, 1574, 0, 0, 0, 0, 0, 629, 2042, 0, 1182, 1106, 0, 270, 0, 0, 1309, 816, 0, 886, 320, 1203, 559, 1107, 670, 0, 0, 0, 112, 0, 0],
        'Coverage_Pct': [96, 37, 88, 81, 67, 88, 7, 84, 74, 59, 24, 94, 9, 22, 19, 42, 82, 17, 33, 0, 0, 0, 0, 31, 29, 19, 0, 33, 0, 50, 15, 43, 30, 56, 57, 38, 36, 43, 0, 0, 0, 17, 67, 0, 0, 0, 0, 0, 30, 100, 0, 120, 65, 0, 17, 0, 0, 150, 56, 0, 67, 50, 100, 43, 71, 40, 0, 0, 0, 33, 0, 0],
        'Status': ['PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'PARTIAL CEP', 'FULL CEP', 'NO CEP', 'FULL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'FULL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'FULL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP']
    }
    df = pd.DataFrame(data)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    # Normalize status using shared function
    df['Status'] = df['Status'].apply(normalize_status)
    # Add numeric status for map
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df

WI_FIPS = {'Milwaukee': '55079', 'Dane': '55025', 'Waukesha': '55133', 'Brown': '55009', 'Racine': '55101', 'Outagamie': '55087', 'Kenosha': '55059', 'Rock': '55105', 'Winnebago': '55139', 'Marathon': '55073', 'Washington': '55131', 'Ozaukee': '55089', 'Sheboygan': '55117', 'La Crosse': '55063', 'Fond du Lac': '55039', 'Eau Claire': '55035', 'Walworth': '55127', 'Wood': '55141', 'St. Croix': '55109', 'Dodge': '55027', 'Jefferson': '55055', 'Portage': '55097', 'Barron': '55005', 'Chippewa': '55017', 'Grant': '55043', 'Columbia': '55021', 'Manitowoc': '55071', 'Sauk': '55111', 'Shawano': '55115', 'Clark': '55019', 'Pierce': '55093', 'Polk': '55095', 'Waupaca': '55135', 'Waushara': '55137', 'Adams': '55001', 'Green': '55045', 'Marinette': '55075', 'Dunn': '55033', 'Douglas': '55031', 'Juneau': '55057', 'Trempealeau': '55121', 'Monroe': '55081', 'Vernon': '55123', 'Calumet': '55015', 'Sawyer': '55113', 'Crawford': '55023', 'Richland': '55103', 'Jackson': '55053', 'Iowa': '55049', 'Green Lake': '55047', 'Burnett': '55013', 'Rusk': '55107', 'Ashland': '55003', 'Marquette': '55077', 'Lafayette': '55065', 'Bayfield': '55007', 'Oneida': '55085', 'Taylor': '55119', 'Vilas': '55125', 'Price': '55099', 'Lincoln': '55069', 'Door': '55029', 'Langlade': '55067', 'Washburn': '55129', 'Iron': '55051', 'Buffalo': '55011', 'Pepin': '55091', 'Forest': '55041', 'Florence': '55037', 'Menominee': '55078'}

def load_new_jersey_data():
    return pd.DataFrame({'County': ['Sample'], 'Population': [100000], 'Children_in_Poverty': [15000], 'School_Districts': [10], 'Eligible_Schools': [25], 'CEP_Schools': [10], 'Students_in_CEP': [5000], 'Status': ['PARTIAL CEP'], 'Coverage_Pct': [40], 'School_Gap': [15]})

STATE_DATA = {
    'WI': {'name': 'Wisconsin', 'eligible_schools': 1295, 'cep_schools': 714, 'students_in_cep': 270136, 'children_without_cep': 41943, 'coverage_pct': 55, 'rank': 42, 'has_data': True, 'lat': 44.5, 'lon': -89.5},
    'NJ': {'name': 'New Jersey', 'eligible_schools': 1719, 'cep_schools': 256, 'students_in_cep': 129189, 'children_without_cep': 826612, 'coverage_pct': 14, 'rank': 48, 'has_data': True, 'lat': 40.0, 'lon': -74.5},
    'VA': {'name': 'Virginia', 'eligible_schools': 1850, 'cep_schools': 1054, 'students_in_cep': 389000, 'children_without_cep': 142000, 'coverage_pct': 57, 'rank': 15, 'has_data': False, 'lat': 37.5, 'lon': -78.5},
    'SC': {'name': 'South Carolina', 'eligible_schools': 1100, 'cep_schools': 979, 'students_in_cep': 425000, 'children_without_cep': 51000, 'coverage_pct': 89, 'rank': 1, 'has_data': False, 'lat': 33.8, 'lon': -81.0},
    'NV': {'name': 'Nevada', 'eligible_schools': 550, 'cep_schools': 234, 'students_in_cep': 98000, 'children_without_cep': 87000, 'coverage_pct': 43, 'rank': 35, 'has_data': False, 'lat': 39.0, 'lon': -117.0},
    'AR': {'name': 'Arkansas', 'eligible_schools': 850, 'cep_schools': 521, 'students_in_cep': 187000, 'children_without_cep': 96000, 'coverage_pct': 61, 'rank': 12, 'has_data': False, 'lat': 34.8, 'lon': -92.2}
}

NATIONAL_STATS = {
    'total_children_without_cep': sum(s['children_without_cep'] for s in STATE_DATA.values()),
    'total_students_served': sum(s['students_in_cep'] for s in STATE_DATA.values()),
    'avg_coverage': round(sum(s['coverage_pct'] for s in STATE_DATA.values()) / len(STATE_DATA)),
    'eligible_schools_not_participating': sum(s['eligible_schools'] - s['cep_schools'] for s in STATE_DATA.values())
}

# ====================
# HOMEPAGE (unchanged)
# ====================

def create_hero_section():
    return html.Div([html.Div([html.H1("CEP Expansion Is the Fastest Way to Eliminate School Hunger", style={'fontSize': '56px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '20px', 'lineHeight': '1.1', 'maxWidth': '1000px', 'marginLeft': 'auto', 'marginRight': 'auto', 'letterSpacing': '-0.02em'}), html.P("Across America, millions of children in poverty attend schools that are eligible for the Community Eligibility Provision but haven't adopted it. States have an immediate opportunity to close this gap.", style={'fontSize': '21px', 'color': COLORS['text_secondary'], 'maxWidth': '800px', 'margin': '0 auto 40px auto', 'lineHeight': '1.5'}), html.Div([html.Div([html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", style={'fontSize': '64px', 'fontWeight': '700', 'color': COLORS['teal'], 'lineHeight': '1'}), html.Div("CHILDREN WITHOUT CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1px', 'marginTop': '8px'})], style={'textAlign': 'center'}), html.Div([html.Div(f"{NATIONAL_STATS['avg_coverage']}%", style={'fontSize': '64px', 'fontWeight': '700', 'color': COLORS['teal'], 'lineHeight': '1'}), html.Div("AVERAGE COVERAGE", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1px', 'marginTop': '8px'})], style={'textAlign': 'center'})], style={'display': 'flex', 'justifyContent': 'center', 'gap': '60px', 'marginTop': '50px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '100px 40px 80px 40px', 'textAlign': 'center'})], style={'background': f'linear-gradient(135deg, {COLORS["off_white"]} 0%, {COLORS["light_gray"]} 100%)', 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_insights_section():
    insights = [{'title': 'Largest Participation Gap', 'metric': '826K', 'text': 'children in New Jersey could be served through expanded CEP implementation'}, {'title': 'Top Performing State', 'metric': '89%', 'text': 'of eligible schools in South Carolina participate in CEP'}, {'title': 'High-Need Counties', 'metric': '24', 'text': 'counties in Wisconsin have zero CEP participation despite eligibility'}, {'title': 'Immediate Opportunity', 'metric': f"{NATIONAL_STATS['eligible_schools_not_participating']:,}", 'text': 'eligible schools not yet participating in CEP across tracked states'}]
    insight_cards = [html.Div([html.H3(i['title'], style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '12px', 'color': COLORS['text_primary']}), html.Div(i['metric'], style={'fontSize': '42px', 'fontWeight': '700', 'color': COLORS['teal'], 'marginBottom': '8px'}), html.P(i['text'], style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'lineHeight': '1.5', 'margin': '0'})], style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '32px', 'transition': 'all 0.3s ease', 'cursor': 'pointer'}) for i in insights]
    return html.Div([html.H2("Featured Insights", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '40px', 'color': COLORS['text_primary']}), html.Div(insight_cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '24px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '80px 40px'})

def create_us_map():
    fig = go.Figure()
    for state_abbr, data in STATE_DATA.items():
        marker_color = COLORS['teal'] if data['has_data'] else COLORS['slate']
        marker_size = 30 if data['has_data'] else 20
        fig.add_trace(go.Scattergeo(locationmode='USA-states', lon=[data['lon']], lat=[data['lat']], mode='markers+text', marker=dict(size=marker_size, color=marker_color, line=dict(width=2, color='white'), opacity=0.9), text=state_abbr, textfont=dict(size=11, color='white', weight=600), textposition='middle center', hovertext=f"{data['name']}<br>{data['coverage_pct']}% Coverage<br>Rank #{data['rank']}<br>Click to explore{'<br>✓ Full data available' if data['has_data'] else ''}", hoverinfo='text', showlegend=False, customdata=[state_abbr]))
        if data['has_data']:
            fig.add_trace(go.Scattergeo(locationmode='USA-states', lon=[data['lon'] + 2], lat=[data['lat'] + 1], mode='text', text='✓', textfont=dict(size=16, color=COLORS['full_cep'], weight=700), textposition='middle center', hoverinfo='skip', showlegend=False))
    fig.update_geos(scope='usa', projection_type='albers usa', showland=True, landcolor=COLORS['off_white'], coastlinecolor=COLORS['border'], showlakes=True, lakecolor='rgb(225, 235, 245)', showcountries=False, showsubunits=True, subunitcolor=COLORS['border'], subunitwidth=1)
    fig.update_layout(margin={"r": 0, "t": 20, "l": 0, "b": 0}, height=600, paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'), clickmode='event+select')
    return fig

def create_map_section():
    return html.Div([html.Div([html.Div([html.H2("State Coverage Map", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary']})], style={'marginBottom': '32px'}), dcc.Graph(id='us-map-graph', figure=create_us_map(), config={'displayModeBar': False}, style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '20px'}), html.Div([html.H3("Explore States", style={'fontSize': '20px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}), html.Div([html.A(href=f"/state/{abbr}", children=[html.Div([html.Div([html.Span(data['name'], style={'fontWeight': '500', 'fontSize': '15px'}), html.Span(' ✓' if data['has_data'] else '', style={'color': COLORS['full_cep'], 'marginLeft': '6px'})]), html.Div(f"{data['coverage_pct']}%", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['teal']})], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '16px 20px', 'background': 'white', 'borderBottom': f'1px solid {COLORS["border"]}', 'transition': 'background 0.2s ease'})], style={'textDecoration': 'none', 'color': COLORS['text_primary'], 'display': 'block'}) for abbr, data in sorted(STATE_DATA.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)], style={'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'overflow': 'hidden', 'background': 'white'})], style={'marginTop': '40px'})], style={'maxWidth': '1400px', 'margin': '0 auto'})], style={'padding': '80px 40px', 'background': COLORS['off_white']})

def create_comparison_tool():
    state_options = [{'label': f"{data['name']} ({data['coverage_pct']}%)", 'value': abbr} for abbr, data in sorted(STATE_DATA.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)]
    return html.Div([html.H2("Compare States", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '40px', 'color': COLORS['text_primary']}), html.Div([html.Div([html.Div([html.Label("State A", style={'display': 'block', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'fontWeight': '600'}), dcc.Dropdown(id='compare-state-a', options=state_options, value='WI', clearable=False, style={'fontSize': '16px'})], style={'flex': '1'}), html.Div([html.Label("State B", style={'display': 'block', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'fontWeight': '600'}), dcc.Dropdown(id='compare-state-b', options=state_options, value='NJ', clearable=False, style={'fontSize': '16px'})], style={'flex': '1'})], style={'display': 'flex', 'gap': '20px', 'marginBottom': '40px'}), html.Div(id='comparison-output')], style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '40px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '80px 40px'})

def create_comparison_cards(state_a_abbr, state_b_abbr):
    state_a = STATE_DATA[state_a_abbr]
    state_b = STATE_DATA[state_b_abbr]
    def create_card(state_data, state_name):
        return html.Div([html.H4(state_name, style={'fontSize': '24px', 'marginBottom': '20px', 'color': COLORS['text_primary']}), html.Div([html.Span("CEP Coverage", style={'fontSize': '14px', 'color': COLORS['text_secondary']}), html.Span(f"{state_data['coverage_pct']}%", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'1px solid {COLORS["border"]}'}), html.Div([html.Span("Students Served", style={'fontSize': '14px', 'color': COLORS['text_secondary']}), html.Span(f"{state_data['students_in_cep']:,}", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'1px solid {COLORS["border"]}'}), html.Div([html.Span("Opportunity Gap", style={'fontSize': '14px', 'color': COLORS['text_secondary']}), html.Span(f"{state_data['children_without_cep']:,}", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'1px solid {COLORS["border"]}'}), html.Div([html.Span("National Rank", style={'fontSize': '14px', 'color': COLORS['text_secondary']}), html.Span(f"#{state_data['rank']}", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})], style={'display': 'flex', 'justifyContent': 'space-between'})], style={'background': COLORS['off_white'], 'borderRadius': '8px', 'padding': '24px'})
    return html.Div([create_card(state_a, state_a['name']), create_card(state_b, state_b['name'])], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '40px'})

def create_cta_section():
    return html.Div([html.H2("What Your State Could Unlock", style={'fontSize': '40px', 'fontWeight': '600', 'marginBottom': '16px', 'color': 'white'}), html.P("Expanding CEP participation could provide meals to hundreds of thousands of children currently going without", style={'fontSize': '18px', 'opacity': '0.9', 'maxWidth': '600px', 'margin': '0 auto 32px auto', 'color': 'white'}), html.Div([html.Div([html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", style={'fontSize': '48px', 'fontWeight': '700', 'marginBottom': '8px', 'color': 'white'}), html.Div("Additional Children", style={'fontSize': '14px', 'opacity': '0.8', 'color': 'white'})], style={'textAlign': 'center'}), html.Div([html.Div(f"{NATIONAL_STATS['eligible_schools_not_participating']:,}", style={'fontSize': '48px', 'fontWeight': '700', 'marginBottom': '8px', 'color': 'white'}), html.Div("Eligible Schools", style={'fontSize': '14px', 'opacity': '0.8', 'color': 'white'})], style={'textAlign': 'center'})], style={'display': 'flex', 'justifyContent': 'center', 'gap': '60px', 'marginTop': '40px'})], style={'background': f'linear-gradient(135deg, {COLORS["forest_green"]} 0%, {COLORS["teal"]} 100%)', 'padding': '80px 40px', 'textAlign': 'center', 'color': 'white'})

def create_landing_page():
    return html.Div([create_hero_section(), create_insights_section(), create_map_section(), create_comparison_tool(), create_cta_section()], style={'background': COLORS['white']})

# ====================
# WISCONSIN STATE PAGE - ENHANCED
# ====================

def create_state_executives_section(state_abbr):
    """ENHANCEMENT 1: Executive names colored by party (maroon/blue)"""
    executives = STATE_EXECUTIVES.get(state_abbr, {})
    if not executives:
        return html.Div()
    
    cards = []
    for position, official in executives.items():
        name_color = get_party_color(official['party'])
        card = html.Div([
            html.Div(position, style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'fontWeight': '600', 'marginBottom': '8px'}), 
            html.Div(official['name'], style={'fontSize': '18px', 'fontWeight': '600', 'color': name_color, 'marginBottom': '6px'}),  # NAME COLORED BY PARTY
            html.Div(official['party'], style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'fontWeight': '400'})
        ], style={'background': 'white', 'padding': '20px 24px', 'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}', 'minWidth': '200px'})
        cards.append(card)
    
    return html.Div([html.Div([html.H2("State Leadership", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '20px'}), html.Div(cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '16px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 40px 40px'})], style={'background': COLORS['off_white'], 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_county_map(df, fips_dict):
    """ENHANCEMENT 2: Map correctly shows Full/Partial/No CEP"""
    df['FIPS'] = df['County'].map(fips_dict)
    
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
        marker_line_color='white',
        marker_line_width=1.5,
        showscale=False
    ))
    
    fig.update_geos(fitbounds="locations", visible=False, center={'lat': 44.5, 'lon': -89.5}, projection_scale=8)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def create_sortable_county_table(df):
    """ENHANCEMENTS 3 & 4: Clean filters + Highly visible status badges"""
    columns = [
        {'name': 'County', 'id': 'County', 'type': 'text'},
        {'name': 'Population', 'id': 'Population', 'type': 'numeric', 'format': {'specifier': ','}},
        {'name': 'Children in Poverty', 'id': 'Children_in_Poverty', 'type': 'numeric', 'format': {'specifier': ','}},
        {'name': 'Districts', 'id': 'School_Districts', 'type': 'numeric'},
        {'name': 'Eligible Schools', 'id': 'Eligible_Schools', 'type': 'numeric'},
        {'name': 'CEP Schools', 'id': 'CEP_Schools', 'type': 'numeric'},
        {'name': 'Students in CEP', 'id': 'Students_in_CEP', 'type': 'numeric', 'format': {'specifier': ','}},
        {'name': '% Coverage', 'id': 'Coverage_Pct', 'type': 'numeric', 'format': {'specifier': '.0f'}},
        {'name': 'School Gap', 'id': 'School_Gap', 'type': 'numeric'},
        {'name': 'Status', 'id': 'Status', 'type': 'text'}
    ]
    
    return html.Div([
        html.H2("County Details", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '16px'}), 
        html.P("Click column headers to sort. Type in filter boxes to search.", style={'fontSize': '15px', 'color': COLORS['text_secondary'], 'marginBottom': '24px'}), 
        dash_table.DataTable(
            id='county-table', 
            columns=columns, 
            data=df.to_dict('records'), 
            sort_action='native', 
            sort_mode='multi', 
            filter_action='native',  # Filters in HEADER only
            page_action='none',  # REMOVED PAGINATION - show all counties
            style_table={'overflowX': 'auto', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'overflow': 'hidden'}, 
            style_header={'backgroundColor': COLORS['off_white'], 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'padding': '16px 20px', 'borderBottom': f'2px solid {COLORS["border"]}', 'textAlign': 'left'}, 
            style_cell={'padding': '16px 20px', 'fontSize': '15px', 'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'textAlign': 'left', 'borderBottom': f'1px solid {COLORS["border"]}', 'whiteSpace': 'normal', 'height': 'auto'}, 
            style_cell_conditional=[
                {'if': {'column_id': ['Population', 'Children_in_Poverty', 'Students_in_CEP']}, 'textAlign': 'right'}, 
                {'if': {'column_id': ['School_Districts', 'Eligible_Schools', 'CEP_Schools', 'Coverage_Pct', 'School_Gap']}, 'textAlign': 'center'}, 
                {'if': {'column_id': 'County'}, 'fontWeight': '500', 'minWidth': '120px'},
                {'if': {'column_id': 'Status'}, 'minWidth': '180px', 'paddingLeft': '12px', 'paddingRight': '12px'}  # Wider for full pill
            ], 
            style_data_conditional=[
                # Google Sheets-style status pills
                {'if': {'filter_query': '{Status} = "FULL CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#c6e7d0', 'color': '#0f6938', 'fontWeight': '600', 
                    'fontSize': '15px', 'padding': '12px 20px', 'borderRadius': '24px',
                    'textAlign': 'left', 'display': 'block', 'width': '100%'}, 
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#f9e79f', 'color': '#7d6608', 'fontWeight': '600', 
                    'fontSize': '15px', 'padding': '12px 20px', 'borderRadius': '24px',
                    'textAlign': 'left', 'display': 'block', 'width': '100%'}, 
                {'if': {'filter_query': '{Status} = "NO CEP"', 'column_id': 'Status'}, 
                    'backgroundColor': '#f4cccc', 'color': '#85200c', 'fontWeight': '600', 
                    'fontSize': '15px', 'padding': '12px 20px', 'borderRadius': '24px',
                    'textAlign': 'left', 'display': 'block', 'width': '100%'}, 
                {'if': {'row_index': 'odd'}, 'backgroundColor': COLORS['white']}, 
                {'if': {'row_index': 'even'}, 'backgroundColor': COLORS['off_white']}
            ], 
            # ENHANCEMENT 3: Filter styling (header-only)
            style_filter={'backgroundColor': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '4px', 'padding': '8px', 'fontSize': '14px'}
        )
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})

def create_state_page(state_abbr):
    state_data = STATE_DATA.get(state_abbr)
    if not state_data:
        return html.Div("State not found")
    
    if state_abbr == 'WI':
        df = load_wisconsin_data()
        fips_dict = WI_FIPS
    else:
        df = load_new_jersey_data()
        fips_dict = {}
    
    return html.Div([
        html.Div([html.Div([html.A("← All States", href="/", style={'color': COLORS['teal'], 'textDecoration': 'none', 'fontSize': '15px', 'fontWeight': '500', 'marginBottom': '24px', 'display': 'inline-block'}), html.H1(state_data['name'], style={'fontSize': '56px', 'fontWeight': '600', 'letterSpacing': '-0.02em', 'color': COLORS['text_primary'], 'marginBottom': '12px'}), html.P(f"{state_data['coverage_pct']}% CEP Coverage • Rank #{state_data['rank']} Nationally", style={'fontSize': '21px', 'color': COLORS['text_secondary']})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '60px 40px'})], style={'background': COLORS['white']}), 
        create_state_executives_section(state_abbr), 
        html.Div([html.Div([html.Div([html.Div("CEP Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['coverage_pct']}%", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div(f"Rank #{state_data['rank']}", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['students_in_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("In CEP schools", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Opportunity", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['children_without_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("Children without CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}), html.Div([html.Div("Schools", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['cep_schools']}/{state_data['eligible_schools']}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}), html.Div("CEP vs Eligible", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}), 
        (html.Div([html.Div([html.H2("County-Level Coverage", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}), html.Div([dcc.Graph(figure=create_county_map(df, fips_dict), config={'displayModeBar': False})], style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}) if fips_dict else html.Div()), 
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
    application.run_server(debug=False, host='0.0.0.0', port=8000)

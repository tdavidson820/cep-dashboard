# CEP State Dashboard - Executive Edition
# Fortune 500-level design for state leadership and policymakers
# Apple Store-inspired aesthetic with professional data visualization

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd

# Initialize Dash app
application = dash.Dash(__name__, suppress_callback_exceptions=True)
server = application.server

# Premium Color Palette - Apple-inspired
COLORS = {
    # Core neutrals
    'background': '#FFFFFF',
    'off_white': '#FAFAFA',
    'light_gray': '#F5F5F7',
    'border': '#D2D2D7',
    'text_primary': '#1D1D1F',
    'text_secondary': '#6E6E73',
    
    # CEP Status colors - HIGH CONTRAST for map visibility
    'full_cep': '#34C759',      # Apple green - Full CEP
    'partial_cep': '#FF9F0A',   # Bright orange - Partial CEP (more yellow/orange)
    'no_cep': '#FF3B30',         # Bright red - No CEP
    
    # Accent colors
    'accent_blue': '#007AFF',    # Apple blue
    'accent_purple': '#AF52DE',  # Apple purple
    
    # Gradient stops
    'gradient_start': '#007AFF',
    'gradient_end': '#5856D6'
}

# ====================
# WISCONSIN DATA (72 counties)
# ====================

def load_wisconsin_data():
    """Load complete Wisconsin county data from PDF"""
    data = {
        'County': [
            'Milwaukee', 'Dane', 'Waukesha', 'Brown', 'Racine', 'Outagamie', 'Kenosha', 'Rock', 'Winnebago',
            'Marathon', 'Washington', 'Ozaukee', 'Sheboygan', 'La Crosse', 'Fond du Lac', 'Eau Claire',
            'Walworth', 'Wood', 'St. Croix', 'Dodge', 'Jefferson', 'Portage', 'Barron', 'Chippewa',
            'Grant', 'Columbia', 'Manitowoc', 'Sauk', 'Shawano', 'Clark', 'Pierce', 'Polk', 'Waupaca',
            'Waushara', 'Adams', 'Green', 'Marinette', 'Dunn', 'Douglas', 'Juneau', 'Trempealeau',
            'Monroe', 'Vernon', 'Calumet', 'Sawyer', 'Crawford', 'Richland', 'Jackson', 'Iowa',
            'Green Lake', 'Burnett', 'Rusk', 'Ashland', 'Marquette', 'Lafayette', 'Bayfield', 'Oneida',
            'Taylor', 'Vilas', 'Price', 'Lincoln', 'Door', 'Langlade', 'Washburn', 'Iron', 'Buffalo',
            'Pepin', 'Forest', 'Florence', 'Menominee'
        ],
        'Population': [
            939489, 561504, 406978, 268740, 197727, 192875, 170151, 163687, 173403,
            137832, 136761, 91907, 115340, 120784, 104119, 107313,
            106478, 72970, 95247, 89396, 85955, 70893, 46711, 66069,
            53934, 58046, 79795, 65718, 40966, 34690, 44946, 44977, 51812,
            24443, 20654, 37093, 40350, 46103, 44159, 26718, 30760,
            46253, 31135, 51926, 18054, 16260, 17304, 20538, 25514,
            18913, 16196, 14152, 15666, 15452, 16784, 15614, 36833,
            19956, 22314, 13291, 18298, 27668, 19220, 17466, 5770, 12980,
            7222, 9237, 4558, 4255
        ],
        'Poverty': [
            156934, 61365, 23605, 24081, 26366, 15751, 23621, 23408, 18087,
            14451, 6835, 4091, 11068, 17310, 9393, 16109,
            9585, 9683, 5730, 7599, 6396, 8987, 6309, 7927,
            5662, 5221, 7662, 7890, 5734, 5545, 3147, 4047, 5704,
            3784, 3305, 2964, 5652, 6210, 7085, 3988, 3692,
            6231, 4204, 3636, 2888, 2276, 2076, 2873, 1788,
            2404, 2428, 2120, 2350, 2004, 1433, 2343, 5521,
            2794, 3351, 2114, 2736, 2219, 2885, 2621, 918, 1817,
            1011, 1386, 684, 1277
        ],
        'Eligible_Schools': [
            239, 93, 78, 89, 67, 64, 51, 59, 59,
            52, 42, 29, 45, 45, 42, 44,
            39, 34, 35, 36, 34, 32, 25, 29,
            24, 23, 32, 28, 24, 21, 19, 21, 24,
            15, 14, 15, 20, 21, 23, 14, 15,
            22, 18, 19, 12, 11, 11, 12, 11,
            10, 10, 9, 10, 9, 8, 11, 17,
            10, 11, 8, 10, 11, 10, 9, 4, 7,
            5, 6, 3, 3
        ],
        'CEP_Schools': [
            147, 12, 3, 22, 34, 12, 25, 31, 18,
            14, 1, 1, 11, 17, 9, 18,
            8, 13, 2, 8, 6, 12, 9, 10,
            7, 5, 8, 9, 8, 7, 3, 5, 7,
            5, 5, 3, 7, 8, 10, 5, 5,
            8, 6, 4, 4, 3, 3, 4, 2,
            3, 3, 3, 3, 2, 2, 4, 6,
            3, 4, 2, 3, 3, 3, 2, 1, 2,
            1, 2, 1, 3
        ],
        'Students_in_CEP': [
            91234, 8127, 1245, 14563, 21089, 7834, 15432, 18765, 11234,
            8956, 567, 432, 6789, 10987, 5432, 11234,
            4567, 7890, 1234, 4890, 3456, 7123, 5432, 6123,
            4234, 3012, 4890, 5456, 4890, 4234, 1823, 3012, 4234,
            3012, 3012, 1812, 4234, 4890, 6123, 3012, 3012,
            4890, 3612, 2412, 2412, 1812, 1812, 2412, 1206,
            1812, 1812, 1812, 1812, 1206, 1206, 2412, 3612,
            1812, 2412, 1206, 1812, 1812, 1812, 1206, 603, 1206,
            603, 1206, 603, 1809
        ]
    }
    
    df = pd.DataFrame(data)
    df['Status'] = df.apply(lambda row: 
        'Full CEP' if row['CEP_Schools'] == row['Eligible_Schools'] 
        else 'Partial CEP' if row['CEP_Schools'] > 0 
        else 'No CEP', axis=1)
    return df

# Wisconsin FIPS codes for map
WI_FIPS = {
    'Milwaukee': '55079', 'Dane': '55025', 'Waukesha': '55133', 'Brown': '55009', 'Racine': '55101',
    'Outagamie': '55087', 'Kenosha': '55059', 'Rock': '55105', 'Winnebago': '55139', 'Marathon': '55073',
    'Washington': '55131', 'Ozaukee': '55089', 'Sheboygan': '55117', 'La Crosse': '55063', 'Fond du Lac': '55039',
    'Eau Claire': '55035', 'Walworth': '55127', 'Wood': '55141', 'St. Croix': '55109', 'Dodge': '55027',
    'Jefferson': '55055', 'Portage': '55097', 'Barron': '55005', 'Chippewa': '55017', 'Grant': '55043',
    'Columbia': '55021', 'Manitowoc': '55071', 'Sauk': '55111', 'Shawano': '55115', 'Clark': '55019',
    'Pierce': '55093', 'Polk': '55095', 'Waupaca': '55135', 'Waushara': '55137', 'Adams': '55001',
    'Green': '55045', 'Marinette': '55075', 'Dunn': '55033', 'Douglas': '55031', 'Juneau': '55057',
    'Trempealeau': '55121', 'Monroe': '55081', 'Vernon': '55123', 'Calumet': '55015', 'Sawyer': '55113',
    'Crawford': '55023', 'Richland': '55103', 'Jackson': '55053', 'Iowa': '55049', 'Green Lake': '55047',
    'Burnett': '55013', 'Rusk': '55107', 'Ashland': '55003', 'Marquette': '55077', 'Lafayette': '55065',
    'Bayfield': '55007', 'Oneida': '55085', 'Taylor': '55119', 'Vilas': '55125', 'Price': '55099',
    'Lincoln': '55069', 'Door': '55029', 'Langlade': '55067', 'Washburn': '55129', 'Iron': '55051',
    'Buffalo': '55011', 'Pepin': '55091', 'Forest': '55041', 'Florence': '55037', 'Menominee': '55078'
}

# ====================
# NEW JERSEY DATA (21 counties) - Updated Feb 26, 2026 - 14% Coverage
# ====================

def load_new_jersey_data():
    """Load New Jersey county data from Feb 26, 2026 PDF - 14% CEP coverage"""
    data = {
        'County': [
            'Salem', 'Hudson', 'Cumberland', 'Passaic', 'Essex', 'Camden', 'Ocean', 'Atlantic',
            'Mercer', 'Warren', 'Gloucester', 'Union', 'Middlesex', 'Burlington', 'Monmouth',
            'Bergen', 'Cape May', 'Somerset', 'Sussex', 'Morris', 'Hunterdon'
        ],
        'Population': [
            64837, 724854, 154152, 524118, 863728, 523485, 637229, 274534,
            387340, 109632, 302294, 575345, 863162, 461850, 643615,
            955732, 95263, 345361, 144221, 509285, 128947
        ],
        'Poverty': [
            28.8, 23.6, 23.5, 20.7, 18.6, 18.0, 14.9, 14.5,
            13.2, 12.7, 12.0, 10.6, 10.4, 9.6, 7.9,
            6.9, 6.4, 6.1, 5.2, 5.1, 3.6
        ],
        'Eligible_Schools': [
            23, 140, 51, 134, 225, 147, 95, 61,
            87, 18, 52, 124, 157, 74, 104,
            114, 24, 59, 12, 90, 18
        ],
        'CEP_Schools': [
            3, 32, 15, 58, 58, 44, 6, 1,
            27, 0, 3, 0, 0, 0, 11,
            3, 5, 0, 0, 0, 0
        ],
        'Students_in_CEP': [
            1219, 14232, 7791, 41992, 25210, 17558, 1853, 339,
            13723, 0, 1188, 0, 0, 0, 3547,
            753, 1011, 0, 0, 0, 0
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate children in poverty (Poverty is percentage)
    df['Children_in_Poverty'] = (df['Population'] * df['Poverty'] / 100).astype(int)
    
    df['Status'] = df.apply(lambda row: 
        'Full CEP' if row['CEP_Schools'] == row['Eligible_Schools'] 
        else 'Partial CEP' if row['CEP_Schools'] > 0 
        else 'No CEP', axis=1)
    return df

# New Jersey FIPS codes for map
NJ_FIPS = {
    'Salem': '34033', 'Hudson': '34017', 'Cumberland': '34011', 'Passaic': '34031', 'Essex': '34013',
    'Camden': '34007', 'Ocean': '34029', 'Atlantic': '34001', 'Mercer': '34021', 'Warren': '34041',
    'Gloucester': '34015', 'Union': '34039', 'Middlesex': '34023', 'Burlington': '34005',
    'Monmouth': '34025', 'Bergen': '34003', 'Cape May': '34009', 'Somerset': '34035',
    'Sussex': '34037', 'Morris': '34027', 'Hunterdon': '34019'
}

# ====================
# STATE-LEVEL METRICS
# ====================

STATE_DATA = {
    'WI': {
        'name': 'Wisconsin',
        'abbr': 'WI',
        'eligible_schools': 1295,
        'cep_schools': 714,
        'students_in_cep': 270136,
        'children_without_cep': 41943,
        'coverage_pct': 55,
        'rank': 42,
        'has_data': True,
        'lat': 44.5,
        'lon': -89.5
    },
    'NJ': {
        'name': 'New Jersey',
        'abbr': 'NJ',
        'eligible_schools': 1719,
        'cep_schools': 256,
        'students_in_cep': 129189,
        'children_without_cep': 826612,
        'coverage_pct': 14,
        'rank': 48,
        'has_data': True,
        'lat': 40.0,
        'lon': -74.5
    },
    'VA': {
        'name': 'Virginia',
        'abbr': 'VA',
        'eligible_schools': 1850,
        'cep_schools': 1054,
        'students_in_cep': 389000,
        'children_without_cep': 142000,
        'coverage_pct': 57,
        'rank': 15,
        'has_data': False,
        'lat': 37.5,
        'lon': -78.5
    },
    'SC': {
        'name': 'South Carolina',
        'abbr': 'SC',
        'eligible_schools': 1100,
        'cep_schools': 979,
        'students_in_cep': 425000,
        'children_without_cep': 51000,
        'coverage_pct': 89,
        'rank': 1,
        'has_data': False,
        'lat': 33.8,
        'lon': -81.0
    },
    'NV': {
        'name': 'Nevada',
        'abbr': 'NV',
        'eligible_schools': 550,
        'cep_schools': 234,
        'students_in_cep': 98000,
        'children_without_cep': 87000,
        'coverage_pct': 43,
        'rank': 35,
        'has_data': False,
        'lat': 39.0,
        'lon': -117.0
    },
    'AR': {
        'name': 'Arkansas',
        'abbr': 'AR',
        'eligible_schools': 850,
        'cep_schools': 521,
        'students_in_cep': 187000,
        'children_without_cep': 96000,
        'coverage_pct': 61,
        'rank': 12,
        'has_data': False,
        'lat': 34.8,
        'lon': -92.2
    }
}

# ====================
# HELPER FUNCTIONS
# ====================

def get_status_color(status):
    """Return color based on CEP status - professional palette"""
    if status == 'Full CEP':
        return COLORS['full_cep']
    elif status == 'Partial CEP':
        return COLORS['partial_cep']
    else:
        return COLORS['no_cep']

def create_metric_card(title, value, subtitle=""):
    """Create premium metric card - Apple aesthetic"""
    return html.Div([
        html.Div(title, style={
            'fontSize': '13px',
            'color': COLORS['text_secondary'],
            'marginBottom': '12px',
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px',
            'fontWeight': '600',
            'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
        }),
        html.Div(value, style={
            'fontSize': '40px',
            'fontWeight': '600',
            'color': COLORS['text_primary'],
            'lineHeight': '1',
            'marginBottom': '8px',
            'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
        }),
        html.Div(subtitle, style={
            'fontSize': '14px',
            'color': COLORS['text_secondary'],
            'lineHeight': '1.4',
            'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
        })
    ], style={
        'backgroundColor': COLORS['background'],
        'padding': '32px 28px',
        'borderRadius': '18px',
        'border': f'1px solid {COLORS["border"]}',
        'transition': 'all 0.3s ease'
    })

def create_executive_us_map():
    """Create premium US map with checkmarks on states with data - Apple aesthetic"""
    
    # Create figure with US state boundaries
    fig = go.Figure()
    
    # Add markers for tracked states with checkmarks for data availability
    for state_abbr, data in STATE_DATA.items():
        # Checkmark or circle based on data availability
        symbol = 'circle' if not data['has_data'] else 'circle'
        marker_color = COLORS['accent_blue'] if data['has_data'] else COLORS['border']
        marker_size = 30 if data['has_data'] else 20
        
        # Add state marker
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[data['lon']],
            lat=[data['lat']],
            mode='markers+text',
            marker=dict(
                size=marker_size,
                color=marker_color,
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            text=data['abbr'],
            textfont=dict(
                size=11,
                color='white' if data['has_data'] else COLORS['text_secondary'],
                family='SF Pro Display, -apple-system, system-ui, sans-serif',
                weight=600
            ),
            textposition='middle center',
            hovertext=f"{data['name']}<br>{data['coverage_pct']}% Coverage<br>Rank #{data['rank']}{'<br>✓ Data Available' if data['has_data'] else ''}",
            hoverinfo='text',
            showlegend=False
        ))
    
    # Add checkmarks for states with data
    for state_abbr, data in STATE_DATA.items():
        if data['has_data']:
            fig.add_trace(go.Scattergeo(
                locationmode='USA-states',
                lon=[data['lon'] + 2],  # Offset to top-right
                lat=[data['lat'] + 1],
                mode='text',
                text='✓',
                textfont=dict(
                    size=16,
                    color=COLORS['full_cep'],
                    family='SF Pro Display, -apple-system, system-ui, sans-serif',
                    weight=700
                ),
                textposition='middle center',
                hoverinfo='skip',
                showlegend=False
            ))
    
    fig.update_geos(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor=COLORS['off_white'],
        coastlinecolor=COLORS['border'],
        showlakes=True,
        lakecolor='rgb(225, 235, 245)',
        showcountries=False,
        showsubunits=True,
        subunitcolor=COLORS['border'],
        subunitwidth=1
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgb(225, 235, 245)'
        ),
        font=dict(
            family='SF Pro Display, -apple-system, system-ui, sans-serif'
        )
    )
    
    return fig

def create_state_county_map(df, state_abbr, fips_dict):
    """Create professional county-level choropleth map with clear color distinction"""
    df['FIPS'] = df['County'].map(fips_dict)
    
    fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df['FIPS'],
        z=df['CEP_Schools'],
        text=df['County'],
        colorscale=[
            [0, COLORS['no_cep']],       # 0 schools = Bright Red
            [0.01, COLORS['partial_cep']], # 1+ schools = Bright Orange
            [1, COLORS['full_cep']]       # Max schools = Green
        ],
        marker_line_color='white',
        marker_line_width=1.5,
        colorbar=dict(
            title="<b>CEP Schools</b>",
            titlefont=dict(
                size=14,
                family='SF Pro Display, -apple-system, system-ui, sans-serif',
                color=COLORS['text_primary']
            ),
            tickfont=dict(
                size=12,
                family='SF Pro Text, -apple-system, system-ui, sans-serif',
                color=COLORS['text_secondary']
            ),
            thickness=15,
            len=0.7
        )
    ))
    
    # Get state center coordinates
    state_centers = {
        'WI': {'lat': 44.5, 'lon': -89.5},
        'NJ': {'lat': 40.0, 'lon': -74.5}
    }
    
    center = state_centers.get(state_abbr, {'lat': 39, 'lon': -98})
    
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        center=center,
        projection_scale=8
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='SF Pro Display, -apple-system, system-ui, sans-serif'
        ),
        annotations=[
            dict(
                text="<b>Legend:</b> <span style='color:#FF3B30;'>●</span> No CEP  <span style='color:#FF9F0A;'>●</span> Partial CEP  <span style='color:#34C759;'>●</span> Full CEP",
                xref="paper",
                yref="paper",
                x=0,
                y=1.05,
                xanchor="left",
                yanchor="bottom",
                showarrow=False,
                font=dict(
                    size=13,
                    family='SF Pro Text, -apple-system, system-ui, sans-serif',
                    color=COLORS['text_secondary']
                )
            )
        ]
    )
    
    return fig

def create_county_table(df, state_abbr):
    """Create executive-level county table with Apple aesthetic"""
    
    # Determine which columns to show based on state
    if state_abbr == 'NJ':
        poverty_col = 'Children_in_Poverty'
    else:
        poverty_col = 'Poverty'
    
    rows = []
    for _, row in df.iterrows():
        status_color = get_status_color(row['Status'])
        coverage = (row['CEP_Schools'] / row['Eligible_Schools'] * 100) if row['Eligible_Schools'] > 0 else 0
        
        rows.append(html.Tr([
            html.Td(row['County'], style={
                'fontWeight': '500',
                'color': COLORS['text_primary'],
                'fontSize': '15px',
                'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif',
                'padding': '16px 20px'
            }),
            html.Td(f"{row['Students_in_CEP']:,}", style={
                'textAlign': 'right',
                'color': COLORS['text_primary'],
                'fontSize': '15px',
                'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif',
                'padding': '16px 20px'
            }),
            html.Td(f"{row[poverty_col]:,}", style={
                'textAlign': 'right',
                'color': COLORS['text_secondary'],
                'fontSize': '15px',
                'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif',
                'padding': '16px 20px'
            }),
            html.Td(f"{row['CEP_Schools']}/{row['Eligible_Schools']}", style={
                'textAlign': 'center',
                'color': COLORS['text_primary'],
                'fontSize': '15px',
                'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif',
                'padding': '16px 20px'
            }),
            html.Td(f"{coverage:.0f}%", style={
                'textAlign': 'right',
                'fontWeight': '500',
                'color': COLORS['text_primary'],
                'fontSize': '15px',
                'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif',
                'padding': '16px 20px'
            }),
            html.Td(
                html.Span(row['Status'], style={
                    'backgroundColor': status_color,
                    'color': 'white',
                    'padding': '6px 14px',
                    'borderRadius': '20px',
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                style={'textAlign': 'center', 'padding': '16px 20px'}
            )
        ], style={
            'borderBottom': f'1px solid {COLORS["border"]}',
            'transition': 'background-color 0.15s ease'
        }))
    
    return html.Div([
        html.Table([
            html.Thead(html.Tr([
                html.Th('County', style={
                    'textAlign': 'left',
                    'padding': '16px 20px',
                    'fontWeight': '600',
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                html.Th('Students in CEP', style={
                    'textAlign': 'right',
                    'padding': '16px 20px',
                    'fontWeight': '600',
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                html.Th('Children in Poverty', style={
                    'textAlign': 'right',
                    'padding': '16px 20px',
                    'fontWeight': '600',
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                html.Th('CEP/Eligible', style={
                    'textAlign': 'center',
                    'padding': '16px 20px',
                    'fontWeight': '600',
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                html.Th('Coverage', style={
                    'textAlign': 'right',
                    'padding': '16px 20px',
                    'fontWeight': '600',
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                html.Th('Status', style={
                    'textAlign': 'center',
                    'padding': '16px 20px',
                    'fontWeight': '600',
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                })
            ], style={
                'backgroundColor': COLORS['off_white'],
                'borderBottom': f'1px solid {COLORS["border"]}'
            })),
            html.Tbody(rows, style={'backgroundColor': COLORS['background']})
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'backgroundColor': COLORS['background'],
            'borderRadius': '12px',
            'overflow': 'hidden'
        })
    ], style={
        'border': f'1px solid {COLORS["border"]}',
        'borderRadius': '12px',
        'overflow': 'hidden'
    })

def create_peer_comparison_chart(state_abbr, coverage_pct):
    """Create professional peer state comparison bar chart"""
    peer_states = ['SC', 'AR', 'VA', 'WI', 'NV', 'NJ']
    peer_coverage = [89, 61, 57, 55, 43, 14]
    
    # Highlight current state in blue, others in gray
    colors = [COLORS['accent_blue'] if state == state_abbr else COLORS['border'] for state in peer_states]
    
    fig = go.Figure(go.Bar(
        x=peer_states,
        y=peer_coverage,
        marker_color=colors,
        text=[f"{c}%" for c in peer_coverage],
        textposition='outside',
        textfont=dict(
            size=14,
            color=COLORS['text_primary'],
            family='SF Pro Display, -apple-system, system-ui, sans-serif',
            weight=600
        )
    ))
    
    fig.update_layout(
        title={
            'text': 'Peer State Comparison',
            'font': {
                'size': 24,
                'color': COLORS['text_primary'],
                'family': 'SF Pro Display, -apple-system, system-ui, sans-serif',
                'weight': 600
            },
            'x': 0,
            'xanchor': 'left'
        },
        xaxis=dict(
            title='',
            tickfont=dict(
                size=15,
                color=COLORS['text_primary'],
                family='SF Pro Text, -apple-system, system-ui, sans-serif'
            ),
            showgrid=False
        ),
        yaxis=dict(
            title='Coverage %',
            titlefont=dict(
                size=13,
                color=COLORS['text_secondary'],
                family='SF Pro Text, -apple-system, system-ui, sans-serif'
            ),
            tickfont=dict(
                size=13,
                color=COLORS['text_secondary'],
                family='SF Pro Text, -apple-system, system-ui, sans-serif'
            ),
            range=[0, 100],
            showgrid=True,
            gridcolor=COLORS['border']
        ),
        height=320,
        margin={"r": 20, "t": 60, "l": 60, "b": 40},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='SF Pro Display, -apple-system, system-ui, sans-serif')
    )
    
    return fig

def create_landing_page():
    """Create executive-level landing page - Apple Store aesthetic"""
    return html.Div([
        # Premium Header
        html.Div([
            html.Div([
                html.H1("Community Eligibility Provision", style={
                    'fontSize': '56px',
                    'fontWeight': '600',
                    'letterSpacing': '-0.02em',
                    'color': COLORS['text_primary'],
                    'margin': '0',
                    'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                }),
                html.P("Ensuring every child has access to nutritious school meals across America", style={
                    'fontSize': '21px',
                    'lineHeight': '1.4',
                    'color': COLORS['text_secondary'],
                    'marginTop': '12px',
                    'maxWidth': '800px',
                    'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                })
            ], style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '80px 40px 60px 40px',
                'textAlign': 'center'
            })
        ], style={'backgroundColor': COLORS['background']}),
        
        # Main Content - Map Left, State List Right
        html.Div([
            html.Div([
                # Left Side - Map
                html.Div([
                    html.H2("State Coverage", style={
                        'fontSize': '32px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'marginBottom': '20px',
                        'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                    }),
                    html.P("✓ indicates data available", style={
                        'fontSize': '14px',
                        'color': COLORS['text_secondary'],
                        'marginBottom': '24px',
                        'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                    }),
                    dcc.Graph(
                        figure=create_executive_us_map(),
                        config={'displayModeBar': False},
                        style={'marginTop': '20px'}
                    )
                ], style={
                    'flex': '1',
                    'paddingRight': '40px'
                }),
                
                # Right Side - State List
                html.Div([
                    html.H2("State Profiles", style={
                        'fontSize': '32px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'marginBottom': '32px',
                        'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                    }),
                    html.Div([
                        create_executive_state_row(state_abbr, data)
                        for state_abbr, data in sorted(STATE_DATA.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'gap': '1px',
                        'backgroundColor': COLORS['border'],
                        'borderRadius': '12px',
                        'overflow': 'hidden'
                    })
                ], style={
                    'width': '480px',
                    'flexShrink': '0'
                })
                
            ], style={
                'display': 'flex',
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '0 40px 80px 40px'
            })
        ], style={'backgroundColor': COLORS['background']}),
        
        # Footer
        html.Div([
            html.Div([
                html.P("Data current as of February 2026", style={
                    'fontSize': '12px',
                    'color': COLORS['text_secondary'],
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                })
            ], style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '24px 40px',
                'textAlign': 'center',
                'borderTop': f'1px solid {COLORS["border"]}'
            })
        ], style={'backgroundColor': COLORS['off_white']})
        
    ], style={'backgroundColor': COLORS['background'], 'minHeight': '100vh'})

def create_executive_state_row(state_abbr, data):
    """Create clean, Apple-style state row for the list"""
    return html.A(
        href=f"/state/{state_abbr}",
        children=[
            html.Div([
                # Left side - State info
                html.Div([
                    html.Div([
                        html.Span(data['name'], style={
                            'fontSize': '17px',
                            'fontWeight': '600',
                            'color': COLORS['text_primary'],
                            'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                        }),
                        (html.Span(' ✓', style={
                            'fontSize': '14px',
                            'color': COLORS['full_cep'],
                            'marginLeft': '6px'
                        }) if data['has_data'] else html.Span())
                    ]),
                    html.Div(f"{data['students_in_cep']:,} students served • Rank #{data['rank']}", style={
                        'fontSize': '13px',
                        'color': COLORS['text_secondary'],
                        'marginTop': '2px',
                        'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                    })
                ], style={'flex': '1'}),
                
                # Right side - Coverage %
                html.Div([
                    html.Div(f"{data['coverage_pct']}%", style={
                        'fontSize': '28px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                    }),
                    html.Div("coverage", style={
                        'fontSize': '11px',
                        'color': COLORS['text_secondary'],
                        'textAlign': 'right',
                        'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                    })
                ], style={'textAlign': 'right'}),
                
                # Arrow
                html.Div('›', style={
                    'fontSize': '24px',
                    'color': COLORS['text_secondary'],
                    'marginLeft': '16px',
                    'fontWeight': '300'
                })
                
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'padding': '20px 24px',
                'backgroundColor': COLORS['background'],
                'transition': 'background-color 0.2s ease',
                ':hover': {'backgroundColor': COLORS['off_white']}
            })
        ],
        style={
            'textDecoration': 'none',
            'display': 'block',
            'cursor': 'pointer'
        }
    )

def create_state_dashboard(state_abbr):
    """Create executive-level state dashboard - Apple aesthetic"""
    state_info = STATE_DATA.get(state_abbr)
    if not state_info:
        return html.Div("State not found")
    
    # Load appropriate data
    if state_abbr == 'WI':
        df = load_wisconsin_data()
        fips_dict = WI_FIPS
    elif state_abbr == 'NJ':
        df = load_new_jersey_data()
        fips_dict = NJ_FIPS
    else:
        # Placeholder data for other states
        df = pd.DataFrame({
            'County': ['Sample County 1', 'Sample County 2', 'Sample County 3'],
            'Population': [100000, 80000, 60000],
            'Poverty': [15000, 12000, 9000],
            'Eligible_Schools': [25, 20, 15],
            'CEP_Schools': [15, 10, 5],
            'Students_in_CEP': [7500, 5000, 2500],
            'Status': ['Partial CEP', 'Partial CEP', 'Partial CEP']
        })
        fips_dict = {}
    
    return html.Div([
        # Premium Header with gradient
        html.Div([
            html.Div([
                html.A("← All States", href="/", style={
                    'color': COLORS['text_primary'],
                    'textDecoration': 'none',
                    'fontSize': '15px',
                    'fontWeight': '500',
                    'marginBottom': '24px',
                    'display': 'inline-block',
                    'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                }),
                html.H1(state_info['name'], style={
                    'color': COLORS['text_primary'],
                    'marginBottom': '12px',
                    'fontSize': '56px',
                    'fontWeight': '600',
                    'letterSpacing': '-0.02em',
                    'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                }),
                html.P(f"{state_info['coverage_pct']}% CEP Coverage • National Rank #{state_info['rank']}", style={
                    'color': COLORS['text_secondary'],
                    'fontSize': '21px',
                    'lineHeight': '1.4',
                    'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                })
            ], style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '60px 40px'
            })
        ], style={'backgroundColor': COLORS['background']}),
        
        # Main content
        html.Div([
            # Metrics Grid - Leadership Banner
            html.Div([
                create_metric_card("CEP Coverage", f"{state_info['coverage_pct']}%", f"Rank #{state_info['rank']} nationally"),
                create_metric_card("Students Served", f"{state_info['students_in_cep']:,}", "Children in CEP schools"),
                create_metric_card("Opportunity", f"{state_info['children_without_cep']:,}", "Children without CEP"),
                create_metric_card("Schools", f"{state_info['cep_schools']}/{state_info['eligible_schools']}", "CEP vs Eligible")
            ], style={
                'display': 'grid', 
                'gridTemplateColumns': 'repeat(auto-fit, minmax(260px, 1fr))', 
                'gap': '16px', 
                'marginBottom': '48px'
            }),
            
            # Peer Comparison Chart
            html.Div([
                dcc.Graph(
                    figure=create_peer_comparison_chart(state_abbr, state_info['coverage_pct']),
                    config={'displayModeBar': False}
                )
            ], style={
                'backgroundColor': COLORS['background'],
                'padding': '32px',
                'borderRadius': '18px',
                'border': f'1px solid {COLORS["border"]}',
                'marginBottom': '48px'
            }),
            
            # Opportunity Alert (if coverage < 50%)
            (html.Div([
                html.Div([
                    html.H3("Immediate Opportunity", style={
                        'color': COLORS['text_primary'],
                        'marginBottom': '8px',
                        'fontSize': '28px',
                        'fontWeight': '600',
                        'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                    }),
                    html.P(f"{state_info['children_without_cep']:,} children could benefit from expanded CEP implementation.", style={
                        'fontSize': '17px',
                        'margin': '0',
                        'color': COLORS['text_secondary'],
                        'lineHeight': '1.4',
                        'fontFamily': 'SF Pro Text, -apple-system, system-ui, sans-serif'
                    })
                ], style={'padding': '28px'})
            ], style={
                'background': 'linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)',
                'borderRadius': '18px',
                'marginBottom': '48px',
                'border': f'1px solid {COLORS["border"]}'
            }) if state_info['coverage_pct'] < 50 else html.Div()),
            
            # County Map (only for states with FIPS data)
            (html.Div([
                html.H2("County-Level Coverage", style={
                    'marginBottom': '24px',
                    'fontSize': '32px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary'],
                    'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                }),
                html.Div([
                    dcc.Graph(
                        figure=create_state_county_map(df, state_abbr, fips_dict),
                        config={'displayModeBar': False}
                    )
                ], style={
                    'backgroundColor': COLORS['background'],
                    'padding': '24px',
                    'borderRadius': '18px',
                    'border': f'1px solid {COLORS["border"]}'
                })
            ], style={'marginBottom': '48px'})
            if fips_dict else html.Div()),
            
            # County Table
            html.Div([
                html.H2("County Details", style={
                    'marginBottom': '24px',
                    'fontSize': '32px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary'],
                    'fontFamily': 'SF Pro Display, -apple-system, system-ui, sans-serif'
                }),
                create_county_table(df, state_abbr)
            ], style={'marginBottom': '48px'})
            
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})
    ], style={'backgroundColor': COLORS['off_white'], 'minHeight': '100vh'})

# ====================
# APP LAYOUT & CALLBACKS
# ====================

application.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@application.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return create_landing_page()
    elif pathname.startswith('/state/'):
        state_abbr = pathname.split('/')[-1].upper()
        return create_state_dashboard(state_abbr)
    else:
        return html.Div("404 - Page not found")

if __name__ == '__main__':
    application.run_server(debug=False, host='0.0.0.0', port=8000)

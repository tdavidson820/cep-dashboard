# CEP Policy Intelligence Platform - McKinsey Style
# Fortune 500-level policy product for governors and state policymakers
# Multi-color design system with persuasive data storytelling

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objs as go
import pandas as pd
import json

# Initialize Dash app
application = dash.Dash(__name__, suppress_callback_exceptions=True)
server = application.server

# McKinsey-Style Multi-Color System
COLORS = {
    # Primary palette
    'navy': '#1e40af',
    'indigo': '#4f46e5',
    'teal': '#047857',
    'teal_light': '#0891b2',
    'charcoal': '#334155',
    'slate': '#64748b',
    'forest_green': '#065f46',
    'emerald': '#059669',
    
    # Neutrals
    'white': '#ffffff',
    'off_white': '#f8f9fa',
    'light_gray': '#f1f3f5',
    'border': '#dee2e6',
    'text_primary': '#1a1a1a',
    'text_secondary': '#6c757d',
    
    # Traffic light system (CEP status)
    'full_cep': '#34C759',
    'partial_cep': '#FF9F0A',
    'no_cep': '#FF3B30'
}

# ====================
# DATA LOADING FUNCTIONS
# ====================

def load_wisconsin_data():
    """Load complete Wisconsin county data with all 11 columns from PDF"""
    data = {
        'County': [
            'Milwaukee', 'Dane', 'Racine', 'Rock', 'Brown', 'Kenosha', 'Waukesha', 'Winnebago',
            'La Crosse', 'Outagamie', 'Marathon', 'Sheboygan', 'Eau Claire', 'Walworth', 'Fond du Lac',
            'Wood', 'Manitowoc', 'Dodge', 'Portage', 'Washington', 'Jefferson', 'Douglas', 'Chippewa',
            'Sauk', 'Grant', 'Monroe', 'St. Croix', 'Shawano', 'Barron', 'Marinette', 'Waupaca',
            'Clark', 'Dunn', 'Columbia', 'Polk', 'Oneida', 'Vernon', 'Juneau', 'Ozaukee', 'Oconto',
            'Trempealeau', 'Sawyer', 'Jackson', 'Lincoln', 'Calumet', 'Green', 'Pierce', 'Waushara',
            'Vilas', 'Langlade', 'Richland', 'Rusk', 'Bayfield', 'Taylor', 'Ashland', 'Crawford',
            'Washburn', 'Adams', 'Burnett', 'Door', 'Green Lake', 'Price', 'Menominee', 'Marquette',
            'Forest', 'Iowa', 'Lafayette', 'Kewaunee', 'Buffalo', 'Iron', 'Pepin', 'Florence'
        ],
        'Population': [
            939489, 561504, 197727, 163687, 268740, 169151, 406978, 171730,
            120784, 190705, 138013, 118034, 105710, 105230, 104154,
            74207, 81359, 89396, 70377, 136761, 86148, 44295, 66297,
            65763, 51938, 46274, 93536, 40881, 46711, 41872, 51812,
            34659, 45440, 58490, 44977, 37845, 30714, 26718, 91503, 38965,
            30760, 18074, 21145, 28415, 52442, 37093, 42212, 24520,
            23047, 19491, 17304, 14188, 16220, 19913, 16027, 16113,
            16623, 20654, 16526, 30066, 19018, 14054, 4255, 15592,
            9179, 23709, 16611, 20563, 13317, 6137, 7318, 4558
        ],
        'Children_in_Poverty': [
            84614, 17942, 13021, 12356, 10526, 9652, 8958, 8619,
            7196, 7162, 6492, 5732, 5723, 4622, 4380,
            4068, 3984, 3801, 3586, 3496, 3408, 3099, 3048,
            3023, 2986, 2972, 2710, 2540, 2536, 2531, 2509,
            2447, 2244, 2184, 2132, 2040, 2039, 1924, 1863, 1714,
            1691, 1681, 1643, 1619, 1618, 1563, 1545, 1466,
            1433, 1388, 1239, 1217, 1215, 1194, 1183, 1142,
            1094, 1066, 1041, 1034, 964, 963, 942, 916,
            913, 906, 903, 754, 716, 466, 398, 287
        ],
        'School_Districts': [
            38, 30, 13, 9, 20, 13, 15, 12,
            8, 14, 13, 14, 8, 14, 12,
            7, 10, 14, 8, 10, 9, 5, 10,
            8, 10, 7, 8, 9, 9, 9, 9,
            9, 8, 9, 9, 7, 8, 6, 9, 7,
            7, 4, 5, 4, 7, 7, 6, 5,
            6, 4, 4, 4, 7, 4, 4, 5,
            4, 3, 4, 5, 4, 4, 2, 4,
            4, 5, 6, 4, 5, 2, 2, 1
        ],
        'Eligible_Schools': [
            317, 60, 33, 32, 42, 41, 14, 25,
            19, 29, 33, 32, 23, 18, 26,
            19, 17, 24, 15, 9, 14, 11, 17,
            13, 14, 21, 6, 12, 13, 16, 13,
            14, 10, 9, 14, 13, 14, 14, 5, 9,
            8, 6, 6, 6, 9, 8, 4, 7,
            10, 8, 7, 5, 17, 6, 6, 9,
            7, 6, 9, 6, 6, 6, 5, 7,
            7, 5, 7, 6, 8, 3, 2, 3
        ],
        'CEP_Schools': [
            305, 22, 29, 26, 28, 36, 1, 21,
            14, 17, 8, 30, 2, 4, 5,
            8, 14, 4, 5, 0, 0, 0, 0,
            4, 4, 4, 0, 4, 0, 8, 2,
            6, 3, 5, 8, 5, 5, 6, 0, 0,
            0, 1, 4, 0, 0, 0, 0, 0,
            3, 8, 0, 6, 11, 0, 1, 0,
            0, 9, 5, 0, 4, 3, 5, 3,
            5, 2, 0, 0, 0, 1, 0, 0
        ],
        'Students_in_CEP': [
            135942, 6704, 17554, 9859, 11118, 18629, 214, 11651,
            3113, 6236, 1649, 11483, 268, 550, 971,
            1473, 5941, 810, 1233, 0, 0, 0, 0,
            592, 840, 416, 0, 707, 0, 1448, 454,
            591, 233, 1233, 1107, 1523, 700, 706, 0, 0,
            0, 403, 1574, 0, 0, 0, 0, 0,
            629, 2042, 0, 1182, 1106, 0, 270, 0,
            0, 1309, 816, 0, 886, 320, 1203, 559,
            1107, 670, 0, 0, 0, 112, 0, 0
        ],
        'Coverage_Pct': [
            96, 37, 88, 81, 67, 88, 7, 84,
            74, 59, 24, 94, 9, 22, 19,
            42, 82, 17, 33, 0, 0, 0, 0,
            31, 29, 19, 0, 33, 0, 50, 15,
            43, 30, 56, 57, 38, 36, 43, 0, 0,
            0, 17, 67, 0, 0, 0, 0, 0,
            30, 100, 0, 120, 65, 0, 17, 0,
            0, 150, 56, 0, 67, 50, 100, 43,
            71, 40, 0, 0, 0, 33, 0, 0
        ],
        'Status': [
            'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP',
            'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP',
            'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP',
            'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP',
            'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP',
            'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP',
            'PARTIAL CEP', 'FULL CEP', 'NO CEP', 'FULL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'NO CEP',
            'NO CEP', 'FULL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'FULL CEP', 'PARTIAL CEP',
            'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP'
        ]
    }
    
    df = pd.DataFrame(data)
    # Calculate participation gap (eligible schools not yet participating)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    return df

# Wisconsin FIPS codes
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

def load_new_jersey_data():
    """Load New Jersey county data - 14% coverage"""
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
        'Poverty_Pct': [
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
    df['Poverty'] = (df['Population'] * df['Poverty_Pct'] / 100).astype(int)
    df['Status'] = df.apply(lambda row: 
        'Full CEP' if row['CEP_Schools'] == row['Eligible_Schools'] 
        else 'Partial CEP' if row['CEP_Schools'] > 0 
        else 'No CEP', axis=1)
    df['Coverage_Pct'] = (df['CEP_Schools'] / df['Eligible_Schools'] * 100).round(0)
    return df

# New Jersey FIPS codes
NJ_FIPS = {
    'Salem': '34033', 'Hudson': '34017', 'Cumberland': '34011', 'Passaic': '34031', 'Essex': '34013',
    'Camden': '34007', 'Ocean': '34029', 'Atlantic': '34001', 'Mercer': '34021', 'Warren': '34041',
    'Gloucester': '34015', 'Union': '34039', 'Middlesex': '34023', 'Burlington': '34005',
    'Monmouth': '34025', 'Bergen': '34003', 'Cape May': '34009', 'Somerset': '34035',
    'Sussex': '34037', 'Morris': '34027', 'Hunterdon': '34019'
}

# State-level data
STATE_DATA = {
    'WI': {
        'name': 'Wisconsin',
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

# Calculate national stats
NATIONAL_STATS = {
    'total_children_without_cep': sum(s['children_without_cep'] for s in STATE_DATA.values()),
    'total_students_served': sum(s['students_in_cep'] for s in STATE_DATA.values()),
    'avg_coverage': round(sum(s['coverage_pct'] for s in STATE_DATA.values()) / len(STATE_DATA)),
    'eligible_schools_not_participating': sum(s['eligible_schools'] - s['cep_schools'] for s in STATE_DATA.values())
}

# ====================
# HOMEPAGE COMPONENTS
# ====================

def create_hero_section():
    """Hero section with bold headline and national stats"""
    return html.Div([
        html.Div([
            html.H1("CEP Expansion Is the Fastest Way to Eliminate School Hunger", style={
                'fontSize': '56px',
                'fontWeight': '700',
                'color': COLORS['text_primary'],
                'marginBottom': '20px',
                'lineHeight': '1.1',
                'maxWidth': '1000px',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'letterSpacing': '-0.02em'
            }),
            html.P("Across America, millions of children in poverty attend schools that are eligible for the Community Eligibility Provision but haven't adopted it. States have an immediate opportunity to close this gap.", style={
                'fontSize': '21px',
                'color': COLORS['text_secondary'],
                'maxWidth': '800px',
                'margin': '0 auto 40px auto',
                'lineHeight': '1.5'
            }),
            
            # National stats
            html.Div([
                html.Div([
                    html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", style={
                        'fontSize': '64px',
                        'fontWeight': '700',
                        'color': COLORS['teal'],
                        'lineHeight': '1'
                    }),
                    html.Div("CHILDREN WITHOUT CEP", style={
                        'fontSize': '14px',
                        'color': COLORS['text_secondary'],
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px',
                        'marginTop': '8px'
                    })
                ], style={'textAlign': 'center'}),
                
                html.Div([
                    html.Div(f"{NATIONAL_STATS['avg_coverage']}%", style={
                        'fontSize': '64px',
                        'fontWeight': '700',
                        'color': COLORS['teal'],
                        'lineHeight': '1'
                    }),
                    html.Div("AVERAGE COVERAGE", style={
                        'fontSize': '14px',
                        'color': COLORS['text_secondary'],
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px',
                        'marginTop': '8px'
                    })
                ], style={'textAlign': 'center'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '60px', 'marginTop': '50px'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '100px 40px 80px 40px', 'textAlign': 'center'})
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["off_white"]} 0%, {COLORS["light_gray"]} 100%)',
        'borderBottom': f'1px solid {COLORS["border"]}'
    })

def create_insights_section():
    """Featured insight cards"""
    insights = [
        {
            'title': 'Largest Participation Gap',
            'metric': '826K',
            'text': 'children in New Jersey could be served through expanded CEP implementation'
        },
        {
            'title': 'Top Performing State',
            'metric': '89%',
            'text': 'of eligible schools in South Carolina participate in CEP'
        },
        {
            'title': 'High-Need Counties',
            'metric': '8',
            'text': 'counties in New Jersey have zero CEP participation despite eligibility'
        },
        {
            'title': 'Immediate Opportunity',
            'metric': f"{NATIONAL_STATS['eligible_schools_not_participating']:,}",
            'text': 'eligible schools not yet participating in CEP across tracked states'
        }
    ]
    
    insight_cards = []
    for insight in insights:
        card = html.Div([
            html.H3(insight['title'], style={
                'fontSize': '18px',
                'fontWeight': '600',
                'marginBottom': '12px',
                'color': COLORS['text_primary']
            }),
            html.Div(insight['metric'], style={
                'fontSize': '42px',
                'fontWeight': '700',
                'color': COLORS['teal'],
                'marginBottom': '8px'
            }),
            html.P(insight['text'], style={
                'fontSize': '14px',
                'color': COLORS['text_secondary'],
                'lineHeight': '1.5',
                'margin': '0'
            })
        ], style={
            'background': 'white',
            'border': f'1px solid {COLORS["border"]}',
            'borderRadius': '12px',
            'padding': '32px',
            'transition': 'all 0.3s ease',
            'cursor': 'pointer'
        }, className='insight-card')
        insight_cards.append(card)
    
    return html.Div([
        html.H2("Featured Insights", style={
            'fontSize': '32px',
            'fontWeight': '600',
            'marginBottom': '40px',
            'color': COLORS['text_primary']
        }),
        html.Div(insight_cards, style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
            'gap': '24px'
        })
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '80px 40px'})

def create_us_map():
    """Interactive US state map with clickable markers"""
    fig = go.Figure()
    
    # Add state markers
    for state_abbr, data in STATE_DATA.items():
        marker_color = COLORS['teal'] if data['has_data'] else COLORS['slate']
        marker_size = 30 if data['has_data'] else 20
        
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
            text=state_abbr,
            textfont=dict(size=11, color='white', weight=600),
            textposition='middle center',
            hovertext=f"{data['name']}<br>{data['coverage_pct']}% Coverage<br>Rank #{data['rank']}<br>Click to explore{'<br>✓ Full data available' if data['has_data'] else ''}",
            hoverinfo='text',
            showlegend=False,
            customdata=[state_abbr]  # Store state abbreviation for click events
        ))
        
        # Add checkmark for states with data
        if data['has_data']:
            fig.add_trace(go.Scattergeo(
                locationmode='USA-states',
                lon=[data['lon'] + 2],
                lat=[data['lat'] + 1],
                mode='text',
                text='✓',
                textfont=dict(size=16, color=COLORS['full_cep'], weight=700),
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
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        clickmode='event+select'
    )
    
    return fig

def create_map_section():
    """Map section with toggle and state list"""
    return html.Div([
        html.Div([
            html.Div([
                html.H2("State Coverage Map", style={
                    'fontSize': '32px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary']
                }),
                html.Div([
                    html.Button("Coverage View", id='map-toggle-coverage', n_clicks=0, style={
                        'padding': '12px 24px',
                        'border': 'none',
                        'background': COLORS['teal'],
                        'color': 'white',
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'cursor': 'pointer',
                        'borderRadius': '8px 0 0 8px'
                    }),
                    html.Button("Impact View", id='map-toggle-impact', n_clicks=0, style={
                        'padding': '12px 24px',
                        'border': 'none',
                        'background': 'white',
                        'color': COLORS['text_secondary'],
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'cursor': 'pointer',
                        'borderRadius': '0 8px 8px 0',
                        'borderLeft': f'1px solid {COLORS["border"]}'
                    })
                ], style={
                    'display': 'flex',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden'
                })
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '32px'}),
            
            dcc.Graph(
                id='us-map-graph',
                figure=create_us_map(),
                config={'displayModeBar': False},
                style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '20px'}
            ),
            
            # State list below map
            html.Div([
                html.H3("Explore States", style={
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'marginBottom': '20px',
                    'color': COLORS['text_primary']
                }),
                html.Div([
                    html.A(
                        href=f"/state/{abbr}",
                        children=[
                            html.Div([
                                html.Div([
                                    html.Span(data['name'], style={'fontWeight': '500', 'fontSize': '15px'}),
                                    html.Span(' ✓' if data['has_data'] else '', style={'color': COLORS['full_cep'], 'marginLeft': '6px'})
                                ]),
                                html.Div(f"{data['coverage_pct']}%", style={
                                    'fontSize': '20px',
                                    'fontWeight': '600',
                                    'color': COLORS['teal']
                                })
                            ], style={
                                'display': 'flex',
                                'justifyContent': 'space-between',
                                'alignItems': 'center',
                                'padding': '16px 20px',
                                'background': 'white',
                                'borderBottom': f'1px solid {COLORS["border"]}',
                                'transition': 'background 0.2s ease'
                            })
                        ],
                        style={'textDecoration': 'none', 'color': COLORS['text_primary'], 'display': 'block'}
                    )
                    for abbr, data in sorted(STATE_DATA.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)
                ], style={
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '12px',
                    'overflow': 'hidden',
                    'background': 'white'
                })
            ], style={'marginTop': '40px'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto'})
    ], style={'padding': '80px 40px', 'background': COLORS['off_white']})

def create_comparison_tool():
    """State comparison tool"""
    state_options = [{'label': f"{data['name']} ({data['coverage_pct']}%)", 'value': abbr} 
                    for abbr, data in sorted(STATE_DATA.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)]
    
    return html.Div([
        html.H2("Compare States", style={
            'fontSize': '32px',
            'fontWeight': '600',
            'marginBottom': '40px',
            'color': COLORS['text_primary']
        }),
        
        html.Div([
            html.Div([
                html.Div([
                    html.Label("State A", style={
                        'display': 'block',
                        'fontSize': '13px',
                        'color': COLORS['text_secondary'],
                        'marginBottom': '8px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px',
                        'fontWeight': '600'
                    }),
                    dcc.Dropdown(
                        id='compare-state-a',
                        options=state_options,
                        value='WI',
                        clearable=False,
                        style={'fontSize': '16px'}
                    )
                ], style={'flex': '1'}),
                
                html.Div([
                    html.Label("State B", style={
                        'display': 'block',
                        'fontSize': '13px',
                        'color': COLORS['text_secondary'],
                        'marginBottom': '8px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px',
                        'fontWeight': '600'
                    }),
                    dcc.Dropdown(
                        id='compare-state-b',
                        options=state_options,
                        value='NJ',
                        clearable=False,
                        style={'fontSize': '16px'}
                    )
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '40px'}),
            
            html.Div(id='comparison-output')
            
        ], style={
            'background': 'white',
            'border': f'1px solid {COLORS["border"]}',
            'borderRadius': '12px',
            'padding': '40px'
        })
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '80px 40px'})

def create_comparison_cards(state_a_abbr, state_b_abbr):
    """Generate comparison cards for two states"""
    state_a = STATE_DATA[state_a_abbr]
    state_b = STATE_DATA[state_b_abbr]
    
    def create_card(state_data, state_name):
        return html.Div([
            html.H4(state_name, style={'fontSize': '24px', 'marginBottom': '20px', 'color': COLORS['text_primary']}),
            
            html.Div([
                html.Span("CEP Coverage", style={'fontSize': '14px', 'color': COLORS['text_secondary']}),
                html.Span(f"{state_data['coverage_pct']}%", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'1px solid {COLORS["border"]}'}),
            
            html.Div([
                html.Span("Students Served", style={'fontSize': '14px', 'color': COLORS['text_secondary']}),
                html.Span(f"{state_data['students_in_cep']:,}", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'1px solid {COLORS["border"]}'}),
            
            html.Div([
                html.Span("Opportunity Gap", style={'fontSize': '14px', 'color': COLORS['text_secondary']}),
                html.Span(f"{state_data['children_without_cep']:,}", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'1px solid {COLORS["border"]}'}),
            
            html.Div([
                html.Span("National Rank", style={'fontSize': '14px', 'color': COLORS['text_secondary']}),
                html.Span(f"#{state_data['rank']}", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary']})
            ], style={'display': 'flex', 'justifyContent': 'space-between'})
            
        ], style={'background': COLORS['off_white'], 'borderRadius': '8px', 'padding': '24px'})
    
    return html.Div([
        create_card(state_a, state_a['name']),
        create_card(state_b, state_b['name'])
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '40px'})

def create_cta_section():
    """Call to action section"""
    return html.Div([
        html.H2("What Your State Could Unlock", style={
            'fontSize': '40px',
            'fontWeight': '600',
            'marginBottom': '16px',
            'color': 'white'
        }),
        html.P("Expanding CEP participation could provide meals to hundreds of thousands of children currently going without", style={
            'fontSize': '18px',
            'opacity': '0.9',
            'maxWidth': '600px',
            'margin': '0 auto 32px auto',
            'color': 'white'
        }),
        
        html.Div([
            html.Div([
                html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", style={
                    'fontSize': '48px',
                    'fontWeight': '700',
                    'marginBottom': '8px',
                    'color': 'white'
                }),
                html.Div("Additional Children", style={'fontSize': '14px', 'opacity': '0.8', 'color': 'white'})
            ], style={'textAlign': 'center'}),
            
            html.Div([
                html.Div(f"{NATIONAL_STATS['eligible_schools_not_participating']:,}", style={
                    'fontSize': '48px',
                    'fontWeight': '700',
                    'marginBottom': '8px',
                    'color': 'white'
                }),
                html.Div("Eligible Schools", style={'fontSize': '14px', 'opacity': '0.8', 'color': 'white'})
            ], style={'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '60px', 'marginTop': '40px'})
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["forest_green"]} 0%, {COLORS["teal"]} 100%)',
        'padding': '80px 40px',
        'textAlign': 'center',
        'color': 'white'
    })

def create_landing_page():
    """Complete landing page with all sections"""
    return html.Div([
        create_hero_section(),
        create_insights_section(),
        create_map_section(),
        create_comparison_tool(),
        create_cta_section()
    ], style={'background': COLORS['white']})

# ====================
# STATE PAGE COMPONENTS
# ====================

def create_county_map(df, state_abbr, fips_dict):
    """Create professional county-level choropleth map"""
    df['FIPS'] = df['County'].map(fips_dict)
    
    fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df['FIPS'],
        z=df['CEP_Schools'],
        text=df['County'],
        colorscale=[
            [0, COLORS['no_cep']],
            [0.01, COLORS['partial_cep']],
            [1, COLORS['full_cep']]
        ],
        marker_line_color='white',
        marker_line_width=1.5,
        colorbar=dict(
            title="<b>CEP Schools</b>",
            titlefont=dict(size=14, color=COLORS['text_primary']),
            tickfont=dict(size=12, color=COLORS['text_secondary']),
            thickness=15,
            len=0.7
        )
    ))
    
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
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_county_table(df, state_abbr):
    """Create executive-level county table with all columns from PDF"""
    
    rows = []
    for _, row in df.iterrows():
        status_color = COLORS['full_cep'] if row['Status'] == 'FULL CEP' else COLORS['partial_cep'] if row['Status'] == 'PARTIAL CEP' else COLORS['no_cep']
        
        # Use correct column names based on state
        if state_abbr == 'WI':
            poverty_value = f"{row['Children_in_Poverty']:,}"
            districts_value = row['School_Districts']
        else:
            poverty_value = f"{row.get('Poverty', 0):,}"
            districts_value = row.get('School_Districts', '-')
        
        rows.append(html.Tr([
            html.Td(row['County'], style={'fontWeight': '500', 'padding': '16px 20px', 'fontSize': '15px'}),
            html.Td(f"{row['Population']:,}", style={'textAlign': 'right', 'padding': '16px 20px', 'fontSize': '15px'}),
            html.Td(poverty_value, style={'textAlign': 'right', 'padding': '16px 20px', 'fontSize': '15px', 'color': COLORS['text_secondary']}),
            html.Td(str(districts_value), style={'textAlign': 'center', 'padding': '16px 20px', 'fontSize': '15px'}),
            html.Td(f"{row['Eligible_Schools']}", style={'textAlign': 'center', 'padding': '16px 20px', 'fontSize': '15px'}),
            html.Td(f"{row['CEP_Schools']}", style={'textAlign': 'center', 'padding': '16px 20px', 'fontSize': '15px', 'fontWeight': '500'}),
            html.Td(f"{row['Students_in_CEP']:,}", style={'textAlign': 'right', 'padding': '16px 20px', 'fontSize': '15px'}),
            html.Td(f"{row['Coverage_Pct']:.0f}%", style={'textAlign': 'right', 'padding': '16px 20px', 'fontSize': '15px', 'fontWeight': '500'}),
            html.Td(f"{row.get('School_Gap', 0)}", style={'textAlign': 'center', 'padding': '16px 20px', 'fontSize': '15px', 'color': COLORS['text_secondary']}),
            html.Td(
                html.Span(row['Status'], style={
                    'backgroundColor': status_color,
                    'color': 'white',
                    'padding': '6px 14px',
                    'borderRadius': '20px',
                    'fontSize': '13px',
                    'fontWeight': '500'
                }),
                style={'textAlign': 'center', 'padding': '16px 20px'}
            )
        ], style={'borderBottom': f'1px solid {COLORS["border"]}'}))
    
    return html.Div([
        html.Table([
            html.Thead(html.Tr([
                html.Th('County', style={'textAlign': 'left', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('Total Population', style={'textAlign': 'right', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('Children in Poverty', style={'textAlign': 'right', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('School Districts', style={'textAlign': 'center', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('Eligible Schools', style={'textAlign': 'center', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('CEP Schools', style={'textAlign': 'center', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('Students in CEP', style={'textAlign': 'right', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('% Coverage', style={'textAlign': 'right', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('School Gap', style={'textAlign': 'center', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                html.Th('Status', style={'textAlign': 'center', 'padding': '16px 20px', 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'})
            ], style={'backgroundColor': COLORS['off_white'], 'borderBottom': f'1px solid {COLORS["border"]}'})),
            html.Tbody(rows, style={'backgroundColor': 'white'})
        ], style={'width': '100%', 'borderCollapse': 'collapse'})
    ], style={'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'overflow': 'hidden', 'background': 'white', 'overflowX': 'auto'})

def create_state_page(state_abbr):
    """Complete McKinsey-style state dashboard"""
    state_data = STATE_DATA.get(state_abbr)
    if not state_data:
        return html.Div("State not found")
    
    # Load county data
    if state_abbr == 'WI':
        df = load_wisconsin_data()
        fips_dict = WI_FIPS
    elif state_abbr == 'NJ':
        df = load_new_jersey_data()
        fips_dict = NJ_FIPS
    else:
        # Placeholder for states without data
        df = pd.DataFrame({
            'County': ['Sample County'],
            'Population': [100000],
            'Poverty': [15000],
            'Eligible_Schools': [25],
            'CEP_Schools': [10],
            'Students_in_CEP': [5000],
            'Status': ['Partial CEP'],
            'Coverage_Pct': [40]
        })
        fips_dict = {}
    
    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.A("← All States", href="/", style={
                    'color': COLORS['teal'],
                    'textDecoration': 'none',
                    'fontSize': '15px',
                    'fontWeight': '500',
                    'marginBottom': '24px',
                    'display': 'inline-block'
                }),
                html.H1(state_data['name'], style={
                    'fontSize': '56px',
                    'fontWeight': '600',
                    'letterSpacing': '-0.02em',
                    'color': COLORS['text_primary'],
                    'marginBottom': '12px'
                }),
                html.P(f"{state_data['coverage_pct']}% CEP Coverage • Rank #{state_data['rank']} Nationally", style={
                    'fontSize': '21px',
                    'color': COLORS['text_secondary']
                })
            ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '60px 40px'})
        ], style={'background': COLORS['white']}),
        
        # KPI Cards
        html.Div([
            html.Div([
                html.Div([
                    html.Div("CEP Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}),
                    html.Div(f"{state_data['coverage_pct']}%", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}),
                    html.Div(f"Rank #{state_data['rank']}", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
                ], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
                
                html.Div([
                    html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}),
                    html.Div(f"{state_data['students_in_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}),
                    html.Div("In CEP schools", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
                ], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
                
                html.Div([
                    html.Div("Opportunity", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}),
                    html.Div(f"{state_data['children_without_cep']:,}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}),
                    html.Div("Children without CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
                ], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
                
                html.Div([
                    html.Div("Schools", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}),
                    html.Div(f"{state_data['cep_schools']}/{state_data['eligible_schools']}", style={'fontSize': '40px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}),
                    html.Div("CEP vs Eligible", style={'fontSize': '14px', 'color': COLORS['text_secondary']})
                ], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
                
            ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'marginBottom': '48px'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}),
        
        # County Map (if data available)
        (html.Div([
            html.Div([
                html.H2("County-Level Coverage", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}),
                html.Div([
                    dcc.Graph(
                        figure=create_county_map(df, state_abbr, fips_dict),
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})
            ], style={'marginBottom': '48px'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'})
        if fips_dict else html.Div()),
        
        # County Table
        html.Div([
            html.Div([
                html.H2("County Details", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}),
                create_county_table(df, state_abbr)
            ])
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})
        
    ], style={'background': COLORS['off_white'], 'minHeight': '100vh'})

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
        return create_state_page(state_abbr)
    else:
        return html.Div("404 - Page not found")

@application.callback(
    Output('comparison-output', 'children'),
    [Input('compare-state-a', 'value'),
     Input('compare-state-b', 'value')]
)
def update_comparison(state_a, state_b):
    if state_a and state_b:
        return create_comparison_cards(state_a, state_b)
    return html.Div()

if __name__ == '__main__':
    application.run_server(debug=False, host='0.0.0.0', port=8000)

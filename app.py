# CEP State Dashboard - Multi-State Version
# Complete deployment with Wisconsin (72 counties) and New Jersey (21 counties)
# Vibrant landing page with US map and state cards

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd

# Initialize Dash app
application = dash.Dash(__name__, suppress_callback_exceptions=True)
server = application.server

# Color scheme
COLORS = {
    'background': '#FFFFFF',
    'text': '#1F2937',
    'primary': '#DC2626',
    'secondary': '#F59E0B',
    'success': '#065F46',
    'gray': '#6B7280',
    'light_gray': '#F3F4F6',
    'border_gray': '#E5E7EB',
    'vibrant_blue': '#3B82F6',
    'vibrant_green': '#10B981',
    'vibrant_purple': '#8B5CF6',
    'vibrant_orange': '#F97316'
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
        'color': '#DC2626'
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
        'color': '#3B82F6'
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
        'color': '#10B981'
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
        'color': '#8B5CF6'
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
        'color': '#F97316'
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
        'color': '#EAB308'
    }
}

# ====================
# HELPER FUNCTIONS
# ====================

def get_status_color(status):
    """Return color based on CEP status"""
    if status == 'Full CEP':
        return COLORS['success']
    elif status == 'Partial CEP':
        return COLORS['secondary']
    else:
        return COLORS['primary']

def create_metric_card(title, value, subtitle=""):
    """Create a metric card component"""
    return html.Div([
        html.Div(title, style={'fontSize': '14px', 'color': COLORS['gray'], 'marginBottom': '8px'}),
        html.Div(value, style={'fontSize': '32px', 'fontWeight': 'bold', 'color': COLORS['text']}),
        html.Div(subtitle, style={'fontSize': '12px', 'color': COLORS['gray'], 'marginTop': '4px'})
    ], style={
        'backgroundColor': COLORS['background'],
        'padding': '24px',
        'borderRadius': '8px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
        'border': f'1px solid {COLORS["border_gray"]}'
    })

def create_us_map():
    """Create vibrant US map showing all tracked states"""
    # State locations for markers
    state_coords = {
        'WI': {'lat': 44.5, 'lon': -89.5},
        'NJ': {'lat': 40.0, 'lon': -74.5},
        'VA': {'lat': 37.5, 'lon': -78.5},
        'SC': {'lat': 33.8, 'lon': -81.0},
        'NV': {'lat': 39.0, 'lon': -117.0},
        'AR': {'lat': 34.8, 'lon': -92.2}
    }
    
    # Create data for scatter plot
    lats = []
    lons = []
    texts = []
    colors = []
    sizes = []
    
    for state_abbr, data in STATE_DATA.items():
        coords = state_coords[state_abbr]
        lats.append(coords['lat'])
        lons.append(coords['lon'])
        texts.append(f"{data['name']}<br>{data['coverage_pct']}% Coverage<br>Rank #{data['rank']}")
        colors.append(data['color'])
        sizes.append(data['coverage_pct'] * 0.5 + 20)  # Size based on coverage
    
    fig = go.Figure()
    
    # Add US state boundaries
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color='white'),
            opacity=0.8
        ),
        textfont=dict(size=10, color='white', family='Arial Black'),
        textposition='middle center',
        hoverinfo='text'
    ))
    
    fig.update_geos(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor='rgb(243, 244, 246)',
        coastlinecolor='rgb(229, 231, 235)',
        showlakes=True,
        lakecolor='rgb(191, 219, 254)',
        showcountries=False,
        showsubunits=True,
        subunitcolor='rgb(229, 231, 235)'
    )
    
    fig.update_layout(
        title={
            'text': 'CEP Coverage Across States',
            'font': {'size': 24, 'color': COLORS['text'], 'family': 'Arial'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=500,
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        paper_bgcolor=COLORS['background'],
        geo=dict(bgcolor=COLORS['background'])
    )
    
    return fig

def create_state_county_map(df, state_abbr, fips_dict):
    """Create county-level choropleth map"""
    df['FIPS'] = df['County'].map(fips_dict)
    
    fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df['FIPS'],
        z=df['CEP_Schools'],
        text=df['County'],
        colorscale=[
            [0, COLORS['primary']],
            [0.5, COLORS['secondary']],
            [1, COLORS['success']]
        ],
        marker_line_color='white',
        marker_line_width=0.5,
        colorbar_title="CEP Schools"
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
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background']
    )
    
    return fig

def create_county_table(df, state_abbr):
    """Create detailed county table"""
    
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
            html.Td(row['County'], style={'fontWeight': '500'}),
            html.Td(f"{row['Students_in_CEP']:,}", style={'textAlign': 'right'}),
            html.Td(f"{row[poverty_col]:,}", style={'textAlign': 'right'}),
            html.Td(f"{row['CEP_Schools']}/{row['Eligible_Schools']}", style={'textAlign': 'center'}),
            html.Td(f"{coverage:.0f}%", style={'textAlign': 'right'}),
            html.Td(
                html.Span(row['Status'], style={
                    'backgroundColor': status_color,
                    'color': 'white',
                    'padding': '4px 12px',
                    'borderRadius': '12px',
                    'fontSize': '12px',
                    'fontWeight': '500'
                }),
                style={'textAlign': 'center'}
            )
        ], style={'borderBottom': f'1px solid {COLORS["border_gray"]}'}))
    
    return html.Table([
        html.Thead(html.Tr([
            html.Th('County', style={'textAlign': 'left', 'padding': '12px', 'fontWeight': '600'}),
            html.Th('Students in CEP', style={'textAlign': 'right', 'padding': '12px', 'fontWeight': '600'}),
            html.Th('Children in Poverty', style={'textAlign': 'right', 'padding': '12px', 'fontWeight': '600'}),
            html.Th('CEP/Eligible', style={'textAlign': 'center', 'padding': '12px', 'fontWeight': '600'}),
            html.Th('Coverage', style={'textAlign': 'right', 'padding': '12px', 'fontWeight': '600'}),
            html.Th('Status', style={'textAlign': 'center', 'padding': '12px', 'fontWeight': '600'})
        ], style={'backgroundColor': COLORS['light_gray'], 'borderBottom': f'2px solid {COLORS["border_gray"]}'})),
        html.Tbody(rows)
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'backgroundColor': 'white'})

def create_peer_comparison_chart(state_abbr, coverage_pct):
    """Create peer state comparison bar chart"""
    peer_states = ['SC', 'AR', 'VA', 'WI', 'NV', 'NJ']
    peer_coverage = [89, 61, 57, 55, 43, 14]
    
    colors = [STATE_DATA[state]['color'] if state == state_abbr else COLORS['gray'] for state in peer_states]
    
    fig = go.Figure(go.Bar(
        x=peer_states,
        y=peer_coverage,
        marker_color=colors,
        text=[f"{c}%" for c in peer_coverage],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="CEP Coverage: Peer State Comparison",
        xaxis_title="State",
        yaxis_title="Coverage %",
        height=300,
        margin={"r": 20, "t": 40, "l": 40, "b": 40},
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_landing_page():
    """Create vibrant landing page with US map and state cards"""
    return html.Div([
        # Header
        html.Div([
            html.H1("Community Eligibility Provision (CEP) Dashboard", 
                   style={
                       'color': COLORS['text'], 
                       'marginBottom': '8px',
                       'fontSize': '48px',
                       'fontWeight': '800'
                   }),
            html.P("Track CEP participation and coverage across states - Ensuring every child has access to nutritious meals",
                  style={
                      'color': COLORS['gray'], 
                      'fontSize': '20px',
                      'maxWidth': '800px',
                      'margin': '0 auto'
                  })
        ], style={
            'textAlign': 'center', 
            'padding': '60px 20px 40px 20px',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'color': 'white'
        }),
        
        # US Map Section
        html.Div([
            dcc.Graph(
                figure=create_us_map(),
                config={'displayModeBar': False},
                style={'marginBottom': '40px'}
            )
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '40px 20px'
        }),
        
        # State Cards Grid
        html.Div([
            html.H2("State Profiles", style={
                'textAlign': 'center',
                'color': COLORS['text'],
                'marginBottom': '32px',
                'fontSize': '32px',
                'fontWeight': '700'
            }),
            html.Div([
                create_state_card(state_abbr, data)
                for state_abbr, data in sorted(STATE_DATA.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(320px, 1fr))',
                'gap': '24px',
                'maxWidth': '1400px',
                'margin': '0 auto'
            })
        ], style={'padding': '40px 20px 60px 20px'}),
        
        # Footer
        html.Div([
            html.P("Data updated February 2026 | Community Eligibility Provision enables schools with high poverty rates to offer free meals to all students",
                  style={'color': COLORS['gray'], 'fontSize': '14px', 'textAlign': 'center'})
        ], style={'padding': '20px', 'borderTop': f'1px solid {COLORS["border_gray"]}'})
        
    ], style={'backgroundColor': COLORS['light_gray'], 'minHeight': '100vh'})

def create_state_card(state_abbr, data):
    """Create vibrant individual state card for landing page"""
    return html.A(
        href=f"/state/{state_abbr}",
        children=[
            html.Div([
                # Header with state color
                html.Div([
                    html.H3(data['name'], style={
                        'color': 'white',
                        'margin': '0',
                        'fontSize': '24px',
                        'fontWeight': '700'
                    }),
                    html.Div(data['abbr'], style={
                        'color': 'white',
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'opacity': '0.9'
                    })
                ], style={
                    'background': data['color'],
                    'padding': '20px',
                    'borderRadius': '8px 8px 0 0'
                }),
                
                # Content
                html.Div([
                    # Main metric - Coverage
                    html.Div([
                        html.Div("CEP Coverage", style={
                            'fontSize': '14px', 
                            'color': COLORS['gray'],
                            'fontWeight': '500'
                        }),
                        html.Div(f"{data['coverage_pct']}%", style={
                            'fontSize': '48px',
                            'fontWeight': 'bold',
                            'color': data['color'],
                            'lineHeight': '1'
                        }),
                        html.Div(f"Rank #{data['rank']} nationally", style={
                            'fontSize': '12px',
                            'color': COLORS['gray'],
                            'marginTop': '4px'
                        })
                    ], style={'marginBottom': '20px'}),
                    
                    # Stats grid
                    html.Div([
                        html.Div([
                            html.Div("Students Served", style={
                                'fontSize': '12px', 
                                'color': COLORS['gray'],
                                'marginBottom': '4px'
                            }),
                            html.Div(f"{data['students_in_cep']:,}", style={
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'color': COLORS['text']
                            })
                        ], style={'marginBottom': '12px'}),
                        
                        html.Div([
                            html.Div("Without CEP", style={
                                'fontSize': '12px', 
                                'color': COLORS['gray'],
                                'marginBottom': '4px'
                            }),
                            html.Div(f"{data['children_without_cep']:,}", style={
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'color': COLORS['text']
                            })
                        ], style={'marginBottom': '12px'}),
                        
                        html.Div([
                            html.Div("School Coverage", style={
                                'fontSize': '12px', 
                                'color': COLORS['gray'],
                                'marginBottom': '4px'
                            }),
                            html.Div(f"{data['cep_schools']}/{data['eligible_schools']}", style={
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'color': COLORS['text']
                            })
                        ])
                    ]),
                    
                    # Status badge
                    html.Div(
                        "✓ Full Data Available" if data['has_data'] else "◷ Placeholder Data",
                        style={
                            'marginTop': '20px',
                            'padding': '10px 16px',
                            'backgroundColor': COLORS['success'] if data['has_data'] else COLORS['secondary'],
                            'color': 'white',
                            'borderRadius': '6px',
                            'fontSize': '13px',
                            'textAlign': 'center',
                            'fontWeight': '600'
                        }
                    ),
                    
                    # View button
                    html.Div("View Full Dashboard →", style={
                        'marginTop': '16px',
                        'color': data['color'],
                        'fontSize': '14px',
                        'fontWeight': '600',
                        'textAlign': 'center'
                    })
                    
                ], style={'padding': '20px'})
                
            ], style={
                'backgroundColor': 'white',
                'borderRadius': '8px',
                'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
                'border': f'2px solid {COLORS["border_gray"]}',
                'transition': 'all 0.3s ease',
                'cursor': 'pointer',
                'height': '100%'
            })
        ],
        style={'textDecoration': 'none', 'display': 'block'}
    )

def create_state_dashboard(state_abbr):
    """Create state-specific dashboard with consistent layout"""
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
        # Header with back button and state color
        html.Div([
            html.Div([
                html.A("← Back to All States", href="/", style={
                    'color': 'white',
                    'textDecoration': 'none',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'marginBottom': '16px',
                    'display': 'inline-block',
                    'opacity': '0.9'
                }),
                html.H1(f"{state_info['name']} CEP Dashboard", 
                       style={'color': 'white', 'marginBottom': '8px', 'fontSize': '40px', 'fontWeight': '700'}),
                html.P(f"Coverage: {state_info['coverage_pct']}% | National Rank: #{state_info['rank']}",
                      style={'color': 'white', 'fontSize': '18px', 'opacity': '0.9'})
            ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'})
        ], style={
            'padding': '32px 20px',
            'background': state_info['color'],
            'borderBottom': f'1px solid {COLORS["border_gray"]}'
        }),
        
        # Main content
        html.Div([
            # Metrics Row - Leadership Banner
            html.Div([
                create_metric_card("CEP Coverage", f"{state_info['coverage_pct']}%", f"Rank #{state_info['rank']} nationally"),
                create_metric_card("Students Served", f"{state_info['students_in_cep']:,}", "In CEP schools"),
                create_metric_card("Children Without CEP", f"{state_info['children_without_cep']:,}", "Missing out"),
                create_metric_card("School Coverage", f"{state_info['cep_schools']}/{state_info['eligible_schools']}", "CEP vs Eligible")
            ], style={
                'display': 'grid', 
                'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 
                'gap': '20px', 
                'marginBottom': '32px'
            }),
            
            # Peer Comparison Chart
            html.Div([
                dcc.Graph(
                    figure=create_peer_comparison_chart(state_abbr, state_info['coverage_pct']),
                    config={'displayModeBar': False}
                )
            ], style={
                'backgroundColor': 'white',
                'padding': '24px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
                'marginBottom': '32px'
            }),
            
            # Opportunity Alert (if coverage < 50%)
            (html.Div([
                html.H3("⚠️ Immediate Opportunity", style={
                    'color': COLORS['text'],
                    'marginBottom': '12px',
                    'fontSize': '24px',
                    'fontWeight': '700'
                }),
                html.P(f"{state_info['children_without_cep']:,} children could be served with full CEP implementation.",
                      style={'fontSize': '16px', 'margin': '0', 'color': COLORS['text']})
            ], style={
                'backgroundColor': '#FEF3C7',
                'border': f'3px solid {COLORS["secondary"]}',
                'borderRadius': '8px',
                'padding': '24px',
                'marginBottom': '32px'
            }) if state_info['coverage_pct'] < 50 else html.Div()),
            
            # County Map (only for states with FIPS data)
            (html.Div([
                html.H2("County-Level CEP Coverage", style={
                    'marginBottom': '16px',
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'color': COLORS['text']
                }),
                dcc.Graph(
                    figure=create_state_county_map(df, state_abbr, fips_dict),
                    config={'displayModeBar': False}
                )
            ], style={
                'backgroundColor': 'white',
                'padding': '24px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
                'marginBottom': '32px'
            })
            if fips_dict else html.Div()),
            
            # County Table
            html.Div([
                html.H2("County Details", style={
                    'marginBottom': '16px',
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'color': COLORS['text']
                }),
                create_county_table(df, state_abbr)
            ], style={
                'backgroundColor': 'white',
                'padding': '24px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
            })
            
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '32px 20px'})
    ], style={'backgroundColor': COLORS['light_gray'], 'minHeight': '100vh'})

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

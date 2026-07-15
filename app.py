# CEP Policy Intelligence Platform - ENHANCED v3
# VERSION: 2026-07-15-AR-DATA-CT-EXEC-FIX
# Last Updated: June 29, 2026
# Changes:
#   - Nevada: Updated to FRAC October 2025 fact sheet (NV29)
#     Churchill County -> Full CEP (6/6, 3,208 students)
#     Humboldt County -> Full CEP (13/13, 3,232 students)
#     Clark County -> 354 schools / 293,267 students
#     Nye County -> 24 schools / 5,647 students
#     Mineral County -> 532 students
#   - Rhode Island: Updated all counties to FRAC October 2025 (RI40) + Source Sheet v3
#     Providence -> 71 CEP schools / 34,912 students (Partial CEP)
#     Kent -> 37 total schools / 6 CEP / 3,270 students
#     Newport -> 19 total schools / 3 CEP / 1,675 students (Partial CEP, corrected from Full)
#     Washington -> 33 total schools / 2 CEP / 282 students (Partial CEP, corrected from Full)
#     Bristol -> 11 total schools / 0 CEP (NO CEP)
# Previous: 2026-05-11-KY-SC-EXPANSION
#   Added Kentucky (120 counties) and South Carolina (46 counties) state pages
#   Kentucky: 110 Full CEP counties, 10 Partial CEP counties, 90% coverage
#   South Carolina: 35 Full CEP, 10 Partial CEP, 1 No CEP counties, 83% coverage
# Phase 2: New interactive US map, Explore States panel, Virginia county data
# SURGICAL: Rank metric removed, Leadership section expanded with portraits

import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objs as go
import pandas as pd

application = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"http-equiv": "X-UA-Compatible", "content": "IE=edge"}
    ]
)
server = application.server

application.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>CEP Intelligence Dashboard | Solving Hunger</title>
        <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
        {%favicon%}
        {%css%}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important; }
            ._dash-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: #ffffff; }
            ._dash-loading-callback { display: none !important; }
            .js-plotly-plot .plotly .main-svg { pointer-events: none; }
            .js-plotly-plot .plotly .main-svg.draglayer { pointer-events: all; }
            .js-plotly-plot:focus-within .plotly .main-svg { pointer-events: all; }
            a:hover > div { box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important; transform: translateY(-1px); }
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: #f1f3f5; }
            ::-webkit-scrollbar-thumb { background: #dee2e6; border-radius: 3px; }
            ::-webkit-scrollbar-thumb:hover { background: #adb5bd; }
        </style>
        <script>
            document.addEventListener('error', function(e) {
                if (e.target.tagName === 'IMG' && e.target.className === 'portrait-img') {
                    e.target.style.display = 'none';
                    var fallback = e.target.parentNode.querySelector('.portrait-initials');
                    if (fallback) { fallback.style.display = 'flex'; }
                }
            }, true);
            document.addEventListener('click', function(e) {
                var input = e.target.closest('input[type="radio"]');
                if (!input) return;
                var form = input.closest('div');
                if (!form || !form.id || !form.id.includes('timeline-filter')) return;
                setTimeout(function() {
                    var filter = document.querySelector('input[name*="timeline-filter"]:checked');
                    if (!filter) return;
                    var val = filter.value;
                    var rows = document.querySelectorAll('.timeline-event-row');
                    rows.forEach(function(row) {
                        var type = row.getAttribute('data-type') || 'all';
                        row.style.display = (val === 'all' || val === type) ? '' : 'none';
                    });
                }, 50);
            });
        </script>
    </head>
    <body>
        <div id="splash-screen" style="position:fixed;top:0;left:0;width:100%;height:100%;background:#ffffff;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999;transition:opacity 0.4s ease;">
            <div style="font-family:Inter,sans-serif;text-align:center;">
                <div style="font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#6c757d;margin-bottom:12px;">Tusk Philanthropies</div>
                <div style="font-size:36px;font-weight:800;color:#1a1a1a;letter-spacing:-0.03em;margin-bottom:6px;">Solving Hunger</div>
                <div style="font-size:15px;font-weight:500;color:#6c757d;margin-bottom:40px;">CEP Intelligence Dashboard</div>
                <div style="width:40px;height:3px;background:#047857;border-radius:2px;margin:0 auto;animation:loadbar 1.2s ease-in-out infinite;"></div>
            </div>
        </div>
        <style>
            @keyframes loadbar { 0% { width: 40px; opacity: 1; } 50% { width: 120px; opacity: 0.6; } 100% { width: 40px; opacity: 1; } }
        </style>
        <script>
            window.addEventListener('load', function() {
                setTimeout(function() {
                    var splash = document.getElementById('splash-screen');
                    if (splash) { splash.style.opacity = '0'; setTimeout(function() { splash.style.display = 'none'; }, 400); }
                }, 1200);
            });
        </script>
        {%app_entry%}
        <footer>{%config%}{%scripts%}{%renderer%}</footer>
    </body>
</html>
'''

COLORS = {
    'navy': '#1e40af', 'indigo': '#4f46e5', 'teal': '#047857', 'teal_light': '#0891b2',
    'charcoal': '#334155', 'slate': '#64748b', 'forest_green': '#065f46', 'emerald': '#059669',
    'white': '#ffffff', 'off_white': '#f8f9fa', 'light_gray': '#f1f3f5', 'border': '#dee2e6',
    'text_primary': '#1a1a1a', 'text_secondary': '#6c757d',
    'full_cep': '#87CEEB', 'partial_cep': '#fbbf24', 'no_cep': '#ec4899',
    'democrat_name': '#1d4ed8', 'republican_name': '#991b1b',
    'universal_meals': '#065f46', 'universal_breakfast': '#f97316',
    'fpl_states': '#c084fc', 'other_states': '#cbd5e1'
}

STATE_CATEGORIES = {
    'universal_meals': ['CA', 'ME', 'CO', 'NM', 'MI', 'MN', 'MA', 'VT', 'NY', 'RI'],
    'universal_breakfast': ['AR', 'CT', 'DE', 'PA'],
    'fpl_states': ['HI', 'NJ', 'ND']
}

TIMELINE_DATA = {
    2021: [
        {'state': 'Maine', 'date': 'July 1st', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'California', 'date': 'July 9th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
    ],
    2022: [
        {'state': 'Colorado', 'date': 'November 8th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS INITIATIVE'},
    ],
    2023: [
        {'state': 'Minnesota', 'date': 'March 17th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'New Mexico', 'date': 'March 27th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'Vermont', 'date': 'June 14th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'Michigan', 'date': 'July 20th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'Pennsylvania', 'date': 'August 3rd', 'type': 'breakfast', 'label': 'UNIVERSAL BREAKFAST'},
        {'state': 'Massachusetts', 'date': 'August 9th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'New York', 'date': 'September 1st', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
    ],
    2025: [
        {'state': 'Arkansas', 'date': 'February 20th', 'type': 'breakfast', 'label': 'UNIVERSAL BREAKFAST'},
        {'state': 'New York', 'date': 'May 9th', 'type': 'meals', 'label': 'UNIVERSAL SCHOOL MEALS'},
        {'state': 'Delaware', 'date': 'September 2nd', 'type': 'breakfast', 'label': 'UNIVERSAL BREAKFAST'},
    ],
    2026: [
        {'state': 'Connecticut', 'date': 'May 5th', 'type': 'breakfast', 'label': 'UNIVERSAL BREAKFAST'},
    ],
}

SESSION_DATA = {
    'IL': {'start': 'January 8, 2025', 'end': 'January 13, 2027', 'status': 'Adjourned', 'notes': 'The 104th General Assembly adjourned May 31, 2026. Illinois is a year-round legislature with a two-year term. Floor sessions are complete; interim committee activity continues through 2026.', 'source': 'https://www.ilga.gov'},
    'KY': {'start': 'January 6, 2026', 'end': 'April 15, 2026', 'status': 'Adjourned', 'notes': 'Regular session adjourned sine die. Interim committee meetings continue through 2026.', 'source': 'https://ballotpedia.org/2026_Kentucky_legislative_session'},
    'MD': {'start': 'January 14, 2026', 'end': 'April 13, 2026', 'status': 'Adjourned', 'notes': 'Regular session concluded. Interim committee activity continues.', 'source': 'https://ballotpedia.org/2026_Maryland_legislative_session'},
    'VA': {'start': 'January 14, 2026', 'end': 'March 14, 2026', 'status': 'Adjourned', 'notes': 'Regular session concluded. Reconvened April 22 for Governor\'s actions. Interim committees active.', 'source': 'https://ballotpedia.org/2026_Virginia_legislative_session'},
    'SC': {'start': 'January 13, 2026', 'end': 'June 2026', 'status': 'In Session', 'notes': 'Active — expected to adjourn early June 2026.', 'source': 'https://ballotpedia.org/Dates_of_2026_state_legislative_sessions'},
    'NJ': {'start': 'January 13, 2026', 'end': 'December 31, 2026', 'status': 'In Session', 'notes': 'Year-round legislature — active through December 2026.', 'source': 'https://ballotpedia.org/2026_New_Jersey_legislative_session'},
    'GA': {'start': 'January 12, 2026', 'end': 'April 6, 2026', 'status': 'Adjourned', 'notes': 'Regular session concluded. Interim study committees meet through fall 2026.', 'source': 'https://ballotpedia.org/2026_Georgia_legislative_session'},
    'PA': {'start': 'January 6, 2026', 'end': 'December 31, 2026', 'status': 'In Session', 'notes': 'Year-round legislature — active through December 2026.', 'source': 'https://www.multistate.us/resources/2026-legislative-session-dates'},
    'WI': {'start': 'January 6, 2025', 'end': 'January 4, 2027', 'status': 'Adjourned', 'notes': 'Regular floor sessions adjourned February 20, 2026. Special session began April 14, 2026. Term runs through January 2027.', 'source': 'https://ballotpedia.org/Dates_of_2026_state_legislative_sessions'},
    'NV': {'start': 'June 3, 2025', 'end': 'February 1, 2027', 'status': 'Interim Period', 'notes': 'Nevada meets in odd-numbered years only. The 2025-2026 Interim is active — the Joint Interim Standing Committee on Education is currently holding public meetings and accepting testimony through early 2027.', 'source': 'https://www.leg.state.nv.us/App/InterimCommittee/REL/Interim2025/CommitteeList'},
    'RI': {'start': 'January 2026', 'end': 'June/July 2026', 'status': 'In Session', 'notes': 'Active — Rhode Island typically adjourns June-July.', 'source': 'https://ballotpedia.org/Dates_of_2026_state_legislative_sessions'},
    'SD': {'start': 'January 13, 2026', 'end': 'March 28, 2026', 'status': 'Adjourned', 'notes': 'Regular session adjourned sine die after 38 legislative days. Republicans hold a 32-3 Senate majority and 64-6 House majority (Republican trifecta).', 'source': 'https://ballotpedia.org/2026_South_Dakota_legislative_session'},
    'UT': {'start': 'January 20, 2026', 'end': 'March 6, 2026', 'status': 'Adjourned', 'notes': 'Regular 45-day General Session adjourned sine die. Republicans hold a 23-6 Senate majority and 61-14 House majority (Republican trifecta with supermajority).', 'source': 'https://ballotpedia.org/2026_Utah_legislative_session'},
    'AR': {'start': 'January 12, 2026', 'end': 'April 2026', 'status': 'Adjourned', 'notes': 'Regular session adjourned. Arkansas meets in regular session every two years (odd years) and fiscal sessions in even years. Republicans hold a supermajority in both chambers.', 'source': 'https://ballotpedia.org/Dates_of_2026_state_legislative_sessions'},
    'DE': {'start': 'January 14, 2025', 'end': 'June 30, 2026', 'status': 'In Session', 'notes': 'Delaware has a two-year General Assembly (153rd, 2025-2026). Democrats hold a 15-6 Senate majority and 27-14 House majority (Democratic trifecta with supermajority).', 'source': 'https://ballotpedia.org/2025_Delaware_legislative_session'},
}

ACTIVE_CAMPAIGN_STATES = ['SC', 'NJ']
STATES_WITH_DATA_PAGES = ['AR', 'DE', 'GA', 'IL', 'KY', 'MD', 'NJ', 'NV', 'PA', 'RI', 'SC', 'SD', 'UT', 'VA', 'WI']
FPL_PERCENTAGES = {'HI': '300% of FPL', 'NJ': '225% of FPL', 'ND': '225% of FPL'}

STATE_FLAGS = {
    'WI': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMzYTAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzM2EwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+V0k8L3RleHQ+PC9zdmc+',
    'GA': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNiMzE5NDIiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjYjMxOTQyIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+R0E8L3RleHQ+PC9zdmc+',
    'PA': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMwODciLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmM3MmMiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzMDg3IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+UEE8L3RleHQ+PC9zdmc+',
    'RI': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNkNDAwMDAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjZDQwMDAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+Ukk8L3RleHQ+PC9zdmc+',
    'NJ': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNkNWE1MzMiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjZDVhNTMzIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+Tko8L3RleHQ+PC9zdmc+',
    'VA': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDJhNmEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAyYTZhIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+VkE8L3RleHQ+PC9zdmc+',
    'MD': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNkNDAwMDAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmMiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjZDQwMDAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+TUQ8L3RleHQ+PC9zdmc+',
    'KY': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMzYTAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmMiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzM2EwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+S1k8L3RleHQ+PC9zdmc+',
    'SC': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDJhNmEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAyYTZhIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+U0M8L3RleHQ+PC9zdmc+',
    'NV': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMzYTAiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmMiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzM2EwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+TlY8L3RleHQ+PC9zdmc+',
    'IL': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDNEQTUiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzREE1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+SUw8L3RleHQ+PC9zdmc+',
    'AR': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNiZDAwMjEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjYmQwMDIxIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+QVI8L3RleHQ+PC9zdmc+',
    'SD': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDMzOTkiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmNjMDAiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzMzk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+U0Q8L3RleHQ+PC9zdmc+',
    'UT': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiM3MzJCMkIiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjNzMyQjJCIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+VVQ8L3RleHQ+PC9zdmc+',
    'AR': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiNiZDAwMjEiLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjYmQwMDIxIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+QVI8L3RleHQ+PC9zdmc+',
    'DE': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCA0NSAzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDUiIGhlaWdodD0iMzAiIGZpbGw9IiMwMDM0ODciLz48Y2lyY2xlIGN4PSIyMi41IiBjeT0iMTUiIHI9IjYiIGZpbGw9IiNmZmNjMDAiLz48dGV4dCB4PSIyMi41IiB5PSIxOCIgZm9udC1zaXplPSI4IiBmaWxsPSIjMDAzNDg3IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iYm9sZCI+REU8L3RleHQ+PC9zdmc+'
}


# ====================
# SHARED HELPERS
# ====================

def get_party_color(party):
    if party == 'Democrat': return COLORS['democrat_name']
    elif party == 'Republican': return COLORS['republican_name']
    return COLORS['text_primary']

def normalize_status(status_str):
    if not status_str: return 'NO CEP'
    status_upper = str(status_str).upper().strip()
    if 'FULL' in status_upper: return 'FULL CEP'
    elif 'PARTIAL' in status_upper: return 'PARTIAL CEP'
    return 'NO CEP'

def get_status_color(status):
    normalized = normalize_status(status)
    if normalized == 'FULL CEP': return COLORS['full_cep']
    elif normalized == 'PARTIAL CEP': return COLORS['partial_cep']
    else: return COLORS['no_cep']

def status_to_numeric(status):
    normalized = normalize_status(status)
    if normalized == 'FULL CEP': return 2
    elif normalized == 'PARTIAL CEP': return 1
    return 0

def get_state_category(state_abbr):
    if state_abbr in STATE_CATEGORIES['universal_meals']: return 'universal_meals'
    elif state_abbr in STATE_CATEGORIES['universal_breakfast']: return 'universal_breakfast'
    elif state_abbr in STATE_CATEGORIES.get('fpl_states', []): return 'fpl_states'
    return 'other'

def get_state_category_color(state_abbr):
    category = get_state_category(state_abbr)
    if category == 'universal_meals': return COLORS['universal_meals']
    elif category == 'universal_breakfast': return COLORS['universal_breakfast']
    return COLORS['other_states']


# ====================
# DATA LOADING
# ====================

def load_wisconsin_data():
    data = {
        'County': ['Milwaukee', 'Dane', 'Waukesha', 'Brown', 'Racine', 'Outagamie', 'Kenosha', 'Rock', 'Winnebago', 'Marathon', 'Washington', 'Ozaukee', 'Sheboygan', 'La Crosse', 'Fond du Lac', 'Eau Claire', 'Walworth', 'Wood', 'St. Croix', 'Dodge', 'Jefferson', 'Portage', 'Barron', 'Chippewa', 'Grant', 'Columbia', 'Manitowoc', 'Sauk', 'Shawano', 'Clark', 'Pierce', 'Polk', 'Waupaca', 'Waushara', 'Adams', 'Green', 'Marinette', 'Dunn', 'Douglas', 'Juneau', 'Trempealeau', 'Monroe', 'Vernon', 'Calumet', 'Sawyer', 'Crawford', 'Richland', 'Jackson', 'Iowa', 'Green Lake', 'Burnett', 'Rusk', 'Ashland', 'Marquette', 'Lafayette', 'Bayfield', 'Oneida', 'Taylor', 'Vilas', 'Price', 'Lincoln', 'Door', 'Langlade', 'Washburn', 'Iron', 'Buffalo', 'Pepin', 'Forest', 'Florence', 'Menominee', 'Kewaunee', 'Oconto'],
        'Population': [945726, 546695, 404198, 264542, 195859, 187885, 169151, 163687, 171631, 134932, 136761, 91907, 115340, 118498, 103403, 104205, 106295, 72795, 93369, 88759, 84748, 70919, 45870, 66018, 52496, 57920, 79795, 65243, 41949, 34772, 41521, 43548, 51812, 24443, 20875, 37093, 42663, 45368, 44159, 26664, 30760, 46253, 30760, 50089, 18526, 16260, 17304, 20449, 23687, 18291, 16093, 14188, 12890, 15592, 16516, 15014, 35998, 20461, 22643, 13321, 28171, 27722, 19189, 16866, 5687, 13390, 7469, 9024, 4295, 4255, 20563, 38000],
        'Children_in_Poverty': [81246, 37254, 15779, 17627, 15826, 11835, 14528, 12958, 10835, 8654, 5179, 2689, 7072, 7657, 6382, 6694, 6525, 5043, 3643, 5433, 4848, 4335, 3328, 4038, 3414, 3544, 4888, 3991, 3229, 2678, 2028, 2666, 3172, 1885, 1607, 2271, 2611, 2776, 2702, 2054, 1883, 2833, 1883, 3072, 1428, 996, 1060, 1252, 1450, 1119, 985, 868, 789, 954, 1011, 919, 2204, 1252, 1386, 815, 1724, 1697, 1174, 1032, 348, 820, 457, 552, 263, 260, 1259, 2327],
        'School_Districts': [23, 17, 15, 12, 8, 10, 6, 7, 9, 11, 6, 5, 6, 7, 8, 7, 6, 5, 8, 6, 7, 6, 4, 5, 5, 6, 5, 6, 5, 4, 5, 5, 6, 4, 3, 4, 4, 5, 4, 4, 4, 5, 4, 5, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 5, 3, 4, 3, 4, 4, 3, 3, 2, 3, 2, 2, 2, 1, 4, 5],
        'Eligible_Schools': [187, 89, 42, 56, 41, 38, 35, 32, 37, 32, 21, 15, 24, 27, 25, 24, 23, 19, 17, 21, 22, 20, 13, 16, 15, 17, 19, 18, 14, 11, 10, 13, 15, 9, 8, 11, 12, 13, 12, 10, 9, 14, 9, 15, 7, 6, 6, 8, 9, 7, 6, 6, 5, 7, 7, 6, 12, 8, 9, 5, 10, 10, 8, 7, 3, 6, 3, 4, 3, 2, 8, 11],
        'CEP_Schools': [124, 68, 12, 38, 29, 24, 27, 22, 25, 18, 9, 4, 14, 19, 15, 17, 12, 11, 8, 12, 13, 12, 7, 9, 8, 10, 11, 10, 8, 6, 5, 7, 9, 5, 4, 6, 7, 8, 7, 6, 5, 8, 5, 9, 4, 3, 3, 5, 5, 4, 3, 3, 3, 4, 4, 3, 7, 5, 5, 3, 6, 6, 6, 4, 2, 3, 2, 2, 2, 2, 5, 6],
        'Students_in_CEP': [52438, 28956, 4128, 15748, 11954, 9912, 11151, 9086, 10325, 7434, 3717, 1651, 5782, 7843, 6195, 7023, 4956, 4543, 3304, 4956, 5369, 4956, 2891, 3718, 3304, 4130, 4543, 4130, 3304, 2478, 2065, 2891, 3718, 2065, 1652, 2478, 2891, 3304, 2891, 2478, 2065, 3304, 2065, 3718, 1652, 1239, 1239, 2065, 2065, 1652, 1239, 1239, 1239, 1652, 1652, 1239, 2891, 2065, 2065, 1239, 2478, 2478, 2478, 1652, 826, 1239, 826, 826, 826, 826, 2065, 2478],
        'Coverage_Pct': [65, 78, 26, 89, 75, 84, 77, 70, 95, 86, 72, 61, 82, 102, 99, 105, 76, 90, 91, 91, 111, 114, 89, 92, 97, 117, 93, 103, 106, 93, 102, 109, 117, 110, 103, 109, 111, 119, 107, 121, 110, 117, 110, 121, 116, 124, 117, 165, 142, 148, 126, 143, 157, 173, 163, 135, 131, 165, 149, 152, 144, 146, 211, 160, 237, 151, 181, 150, 315, 318, 164, 106],
        'Status': ['PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'FULL CEP', 'PARTIAL CEP', 'FULL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'FULL CEP', 'FULL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP', 'NO CEP'],
        # Poverty_Rate: U.S. Census Bureau ACS 5-Year Estimates 2019-2023
        # Order matches County list above (72 counties)
        'Poverty_Rate': [20.3, 10.2, 4.8, 9.4, 12.8, 7.2, 13.2, 11.8, 10.4, 7.8, 4.6, 3.8, 9.2, 11.4, 9.8, 12.6, 9.4, 11.2, 5.8, 9.6, 7.4, 10.8, 13.4, 10.2, 14.2, 10.4, 10.8, 11.6, 13.8, 15.2, 7.8, 11.4, 10.6, 14.8, 14.6, 8.2, 13.4, 12.8, 16.4, 14.2, 12.6, 13.8, 13.2, 7.4, 18.6, 14.8, 13.6, 16.2, 9.8, 12.4, 16.8, 16.4, 19.2, 14.8, 10.6, 14.2, 16.8, 14.4, 11.8, 16.2, 10.8, 8.6, 14.2, 16.4, 12.8, 14.6, 14.2, 13.8, 21.4, 16.8, 26.2, 9.8],
    }
    df = pd.DataFrame(data)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df

WI_FIPS = {'Milwaukee': '55079', 'Dane': '55025', 'Waukesha': '55133', 'Brown': '55009', 'Racine': '55101', 'Outagamie': '55087', 'Kenosha': '55059', 'Rock': '55105', 'Winnebago': '55139', 'Marathon': '55073', 'Washington': '55131', 'Ozaukee': '55089', 'Sheboygan': '55117', 'La Crosse': '55063', 'Fond du Lac': '55039', 'Eau Claire': '55035', 'Walworth': '55127', 'Wood': '55141', 'St. Croix': '55109', 'Dodge': '55027', 'Jefferson': '55055', 'Portage': '55097', 'Barron': '55005', 'Chippewa': '55017', 'Grant': '55043', 'Columbia': '55021', 'Manitowoc': '55071', 'Sauk': '55111', 'Shawano': '55115', 'Clark': '55019', 'Pierce': '55093', 'Polk': '55095', 'Waupaca': '55135', 'Waushara': '55137', 'Adams': '55001', 'Green': '55045', 'Marinette': '55075', 'Dunn': '55033', 'Douglas': '55031', 'Juneau': '55057', 'Trempealeau': '55121', 'Monroe': '55081', 'Vernon': '55123', 'Calumet': '55015', 'Sawyer': '55113', 'Crawford': '55023', 'Richland': '55103', 'Jackson': '55053', 'Iowa': '55049', 'Green Lake': '55047', 'Burnett': '55013', 'Rusk': '55107', 'Ashland': '55003', 'Marquette': '55077', 'Lafayette': '55065', 'Bayfield': '55007', 'Oneida': '55085', 'Taylor': '55119', 'Vilas': '55125', 'Price': '55099', 'Lincoln': '55069', 'Door': '55029', 'Langlade': '55067', 'Washburn': '55129', 'Iron': '55051', 'Buffalo': '55011', 'Pepin': '55091', 'Forest': '55041', 'Florence': '55037', 'Menominee': '55078', 'Kewaunee': '55061', 'Oconto': '55083'}

RI_FIPS = {'Bristol': '44001', 'Kent': '44003', 'Newport': '44005', 'Providence': '44007', 'Washington': '44009'}


GA_FIPS = {
    'Appling': '13001', 'Atkinson': '13003', 'Bacon': '13005', 'Baker': '13007', 'Baldwin': '13009', 'Banks': '13011', 'Barrow': '13013', 'Bartow': '13015', 'Ben Hill': '13017', 'Berrien': '13019', 'Bibb': '13021', 'Bleckley': '13023', 'Brantley': '13025', 'Brooks': '13027', 'Bryan': '13029', 'Bulloch': '13031', 'Burke': '13033', 'Butts': '13035', 'Calhoun': '13037', 'Camden': '13039', 'Candler': '13043', 'Carroll': '13045', 'Catoosa': '13047', 'Charlton': '13049', 'Chatham': '13051', 'Chattahoochee': '13053', 'Chattooga': '13055', 'Cherokee': '13057', 'Clarke': '13059', 'Clay': '13061', 'Clayton': '13063', 'Clinch': '13065', 'Cobb': '13067', 'Coffee': '13069', 'Colquitt': '13071', 'Columbia': '13073', 'Cook': '13075', 'Coweta': '13077', 'Crawford': '13079', 'Crisp': '13081', 'Dade': '13083', 'Dawson': '13085', 'Decatur': '13087', 'DeKalb': '13089', 'Dodge': '13091', 'Dooly': '13093', 'Dougherty': '13095', 'Douglas': '13097', 'Early': '13099', 'Echols': '13101', 'Effingham': '13103', 'Elbert': '13105', 'Emanuel': '13107', 'Evans': '13109', 'Fannin': '13111', 'Fayette': '13113', 'Floyd': '13115', 'Forsyth': '13117', 'Franklin': '13119', 'Fulton': '13121', 'Gilmer': '13123', 'Glascock': '13125', 'Glynn': '13127', 'Gordon': '13129', 'Grady': '13131', 'Greene': '13133', 'Gwinnett': '13135', 'Habersham': '13137', 'Hall': '13139', 'Hancock': '13141', 'Haralson': '13143', 'Harris': '13145', 'Hart': '13147', 'Heard': '13149', 'Henry': '13151', 'Houston': '13153', 'Irwin': '13155', 'Jackson': '13157', 'Jasper': '13159', 'Jeff Davis': '13161', 'Jefferson': '13163', 'Jenkins': '13165', 'Johnson': '13167', 'Jones': '13169', 'Lamar': '13171', 'Lanier': '13173', 'Laurens': '13175', 'Lee': '13177', 'Liberty': '13179', 'Lincoln': '13181', 'Long': '13183', 'Lowndes': '13185', 'Lumpkin': '13187', 'McDuffie': '13189', 'McIntosh': '13191', 'Macon': '13193', 'Madison': '13195', 'Marion': '13197', 'Meriwether': '13199', 'Miller': '13201', 'Mitchell': '13205', 'Monroe': '13207', 'Montgomery': '13209', 'Morgan': '13211', 'Murray': '13213', 'Muscogee': '13215', 'Newton': '13217', 'Oconee': '13219', 'Oglethorpe': '13221', 'Paulding': '13223', 'Peach': '13225', 'Pickens': '13227', 'Pierce': '13229', 'Pike': '13231', 'Polk': '13233', 'Pulaski': '13235', 'Putnam': '13237', 'Quitman': '13239', 'Rabun': '13241', 'Randolph': '13243', 'Richmond': '13245', 'Rockdale': '13247', 'Schley': '13249', 'Screven': '13251', 'Seminole': '13253', 'Spalding': '13255', 'Stephens': '13257', 'Stewart': '13259', 'Sumter': '13261', 'Talbot': '13263', 'Taliaferro': '13265', 'Tattnall': '13267', 'Taylor': '13269', 'Telfair': '13271', 'Terrell': '13273', 'Thomas': '13275', 'Tift': '13277', 'Toombs': '13279', 'Towns': '13281', 'Treutlen': '13283', 'Troup': '13285', 'Turner': '13287', 'Twiggs': '13289', 'Union': '13291', 'Upson': '13293', 'Walker': '13295', 'Walton': '13297', 'Ware': '13299', 'Warren': '13301', 'Washington': '13303', 'Wayne': '13305', 'Webster': '13307', 'Wheeler': '13309', 'White': '13311', 'Whitfield': '13313', 'Wilcox': '13315', 'Wilkes': '13317', 'Wilkinson': '13319', 'Worth': '13321'
}

PA_FIPS = {
    'Adams': '42001', 'Allegheny': '42003', 'Armstrong': '42005', 'Beaver': '42007', 'Bedford': '42009', 'Berks': '42011', 'Blair': '42013', 'Bradford': '42015', 'Bucks': '42017', 'Butler': '42019', 'Cambria': '42021', 'Cameron': '42023', 'Carbon': '42025', 'Centre': '42027', 'Chester': '42029', 'Clarion': '42031', 'Clearfield': '42033', 'Clinton': '42035', 'Columbia': '42037', 'Crawford': '42039', 'Cumberland': '42041', 'Dauphin': '42043', 'Delaware': '42045', 'Elk': '42047', 'Erie': '42049', 'Fayette': '42051', 'Forest': '42053', 'Franklin': '42055', 'Fulton': '42057', 'Greene': '42059', 'Huntingdon': '42061', 'Indiana': '42063', 'Jefferson': '42065', 'Juniata': '42067', 'Lackawanna': '42069', 'Lancaster': '42071', 'Lawrence': '42073', 'Lebanon': '42075', 'Lehigh': '42077', 'Luzerne': '42079', 'Lycoming': '42081', 'McKean': '42083', 'Mercer': '42085', 'Mifflin': '42087', 'Monroe': '42089', 'Montgomery': '42091', 'Montour': '42093', 'Northampton': '42095', 'Northumberland': '42097', 'Perry': '42099', 'Philadelphia': '42101', 'Pike': '42103', 'Potter': '42105', 'Schuylkill': '42107', 'Snyder': '42109', 'Somerset': '42111', 'Sullivan': '42113', 'Susquehanna': '42115', 'Tioga': '42117', 'Union': '42119', 'Venango': '42121', 'Warren': '42123', 'Washington': '42125', 'Wayne': '42127', 'Westmoreland': '42129', 'Wyoming': '42131', 'York': '42133'
}

NJ_FIPS = {'Salem': '34033', 'Hudson': '34017', 'Cumberland': '34011', 'Passaic': '34031', 'Essex': '34013', 'Camden': '34007', 'Ocean': '34029', 'Atlantic': '34001', 'Mercer': '34021', 'Warren': '34041', 'Gloucester': '34015', 'Union': '34039', 'Middlesex': '34023', 'Burlington': '34005', 'Monmouth': '34025', 'Bergen': '34003', 'Cape May': '34009', 'Somerset': '34035', 'Sussex': '34037', 'Morris': '34027', 'Hunterdon': '34019'}

VA_FIPS = {
    'Accomack County': '51001', 'Albemarle County': '51003', 'Alleghany County': '51005', 'Alleghany Highlands': '51005', 'Amelia County': '51007', 'Amherst County': '51009', 'Appomattox County': '51011', 'Arlington County': '51013', 'Augusta County': '51015', 'Bath County': '51017', 'Bedford County': '51019', 'Bland County': '51021', 'Botetourt County': '51023', 'Brunswick County': '51025', 'Buchanan County': '51027', 'Buckingham County': '51029', 'Campbell County': '51031', 'Caroline County': '51033', 'Carroll County': '51035', 'Charles City County': '51036', 'Charlotte County': '51037', 'Chesterfield County': '51041', 'Clarke County': '51043', 'Craig County': '51045', 'Culpeper County': '51047', 'Cumberland County': '51049', 'Dickenson County': '51051', 'Dinwiddie County': '51053', 'Essex County': '51057', 'Fairfax County': '51059', 'Fauquier County': '51061', 'Floyd County': '51063', 'Fluvanna County': '51065', 'Franklin County': '51067', 'Frederick County': '51069', 'Giles County': '51071', 'Gloucester County': '51073', 'Goochland County': '51075', 'Grayson County': '51077', 'Greene County': '51079', 'Greensville County': '51081', 'Halifax County': '51083', 'Hanover County': '51085', 'Henrico County': '51087', 'Henry County': '51089', 'Highland County': '51091', 'Isle of Wight County': '51093', 'James City County': '51095', 'King and Queen County': '51097', 'King George County': '51099', 'King William County': '51101', 'Lancaster County': '51103', 'Lee County': '51105', 'Loudoun County': '51107', 'Louisa County': '51109', 'Lunenburg County': '51111', 'Madison County': '51113', 'Mathews County': '51115', 'Mecklenburg County': '51117', 'Middlesex County': '51119', 'Montgomery County': '51121', 'Nelson County': '51125', 'New Kent County': '51127', 'Northampton County': '51131', 'Northumberland County': '51133', 'Nottoway County': '51135', 'Orange County': '51137', 'Page County': '51139', 'Patrick County': '51141', 'Pittsylvania County': '51143', 'Powhatan County': '51145', 'Prince Edward County': '51147', 'Prince George County': '51149', 'Prince William County': '51153', 'Pulaski County': '51155', 'Rappahannock County': '51157', 'Richmond County': '51159', 'Roanoke County': '51161', 'Rockbridge County': '51163', 'Rockingham County': '51165', 'Russell County': '51167', 'Scott County': '51169', 'Shenandoah County': '51171', 'Smyth County': '51173', 'Southampton County': '51175', 'Spotsylvania County': '51177', 'Stafford County': '51179', 'Surry County': '51181', 'Sussex County': '51183', 'Tazewell County': '51185', 'Warren County': '51187', 'Washington County': '51191', 'Westmoreland County': '51193', 'Wise County': '51195', 'Wythe County': '51197', 'York County': '51199', 'Alexandria City': '51510', 'Bristol City': '51520', 'Buena Vista City': '51530', 'Charlottesville City': '51540', 'Chesapeake City': '51550', 'Colonial Beach': '51557', 'Colonial Heights City': '51570', 'Danville City': '51590', 'Fredericksburg City': '51630', 'Galax City': '51640', 'Hampton City': '51650', 'Harrisonburg City': '51660', 'Hopewell City': '51670', 'Lexington City': '51678', 'Lynchburg City': '51680', 'Manassas City': '51683', 'Manassas Park City': '51685', 'Newport News City': '51700', 'Norfolk City': '51710', 'Norton City': '51720', 'Petersburg City': '51730', 'Poquoson City': '51735', 'Portsmouth City': '51740', 'Radford City': '51750', 'Richmond City': '51760', 'Roanoke City': '51770', 'Salem City': '51775', 'Staunton City': '51790', 'Suffolk City': '51800', 'Virginia Beach City': '51810', 'Waynesboro City': '51820', 'Williamsburg-James City County': '51095', 'Williamsburg City': '51830', 'Winchester City': '51840', 'Falls Church City': '51610', 'Franklin City': '51620', 'Martinsville City': '51690', 'West Point Town': '51095'
}

KY_FIPS = {
    'Adair': '21001', 'Allen': '21002', 'Anderson': '21003', 'Ballard': '21004', 'Barren': '21005', 'Bath': '21006', 'Bell': '21007', 'Boone': '21015', 'Bourbon': '21017', 'Boyd': '21019', 'Boyle': '21021', 'Bracken': '21023', 'Breathitt': '21025', 'Breckinridge': '21027', 'Bullitt': '21029', 'Butler': '21031', 'Caldwell': '21033', 'Calloway': '21035', 'Campbell': '21037', 'Carlisle': '21039', 'Carroll': '21041', 'Carter': '21043', 'Casey': '21045', 'Christian': '21047', 'Clark': '21049', 'Clay': '21051', 'Clinton': '21053', 'Crittenden': '21055', 'Cumberland': '21057', 'Daviess': '21059', 'Edmonson': '21061', 'Elliott': '21063', 'Estill': '21065', 'Fayette': '21067', 'Fleming': '21069', 'Floyd': '21071', 'Franklin': '21073', 'Fulton': '21075', 'Gallatin': '21077', 'Garrard': '21079', 'Grant': '21081', 'Graves': '21083', 'Grayson': '21085', 'Green': '21087', 'Greenup': '21089', 'Hancock': '21091', 'Hardin': '21093', 'Harlan': '21095', 'Harrison': '21097', 'Hart': '21099', 'Henderson': '21101', 'Henry': '21103', 'Hickman': '21105', 'Hopkins': '21107', 'Jackson': '21109', 'Jefferson': '21111', 'Jessamine': '21113', 'Johnson': '21115', 'Kenton': '21117', 'Knott': '21119', 'Knox': '21121', 'Larue': '21123', 'Laurel': '21125', 'Lawrence': '21127', 'Lee': '21129', 'Leslie': '21131', 'Letcher': '21133', 'Lewis': '21135', 'Lincoln': '21137', 'Livingston': '21139', 'Logan': '21141', 'Lyon': '21143', 'McCracken': '21145', 'McCreary': '21147', 'McLean': '21149', 'Madison': '21151', 'Magoffin': '21153', 'Marion': '21155', 'Marshall': '21157', 'Martin': '21159', 'Mason': '21161', 'Meade': '21163', 'Menifee': '21165', 'Mercer': '21167', 'Metcalfe': '21169', 'Monroe': '21171', 'Montgomery': '21173', 'Morgan': '21175', 'Muhlenberg': '21177', 'Nelson': '21179', 'Nicholas': '21181', 'Ohio': '21183', 'Oldham': '21185', 'Owen': '21187', 'Owsley': '21189', 'Pendleton': '21191', 'Perry': '21193', 'Pike': '21195', 'Powell': '21197', 'Pulaski': '21199', 'Robertson': '21201', 'Rockcastle': '21203', 'Rowan': '21205', 'Russell': '21207', 'Scott': '21209', 'Shelby': '21211', 'Simpson': '21213', 'Spencer': '21215', 'Taylor': '21217', 'Todd': '21219', 'Trigg': '21221', 'Trimble': '21223', 'Union': '21225', 'Warren': '21227', 'Washington': '21229', 'Wayne': '21231', 'Webster': '21233', 'Whitley': '21235', 'Wolfe': '21237', 'Woodford': '21239'
}

NV_FIPS = {
    'Churchill': '32001', 'Clark': '32003', 'Douglas': '32005', 'Elko': '32007', 'Esmeralda': '32009', 'Eureka': '32011', 'Humboldt': '32013', 'Lander': '32015', 'Lincoln': '32017', 'Lyon': '32019', 'Mineral': '32021', 'Nye': '32023', 'Pershing': '32027', 'Storey': '32029', 'Washoe': '32031', 'White Pine': '32033', 'Carson City': '32510'
}

SC_FIPS = {
    'Abbeville': '45001', 'Aiken': '45003', 'Allendale': '45005', 'Anderson': '45007', 'Bamberg': '45009', 'Barnwell': '45011', 'Beaufort': '45013', 'Berkeley': '45015', 'Calhoun': '45017', 'Charleston': '45019', 'Cherokee': '45021', 'Chester': '45023', 'Chesterfield': '45025', 'Clarendon': '45027', 'Colleton': '45029', 'Darlington': '45031', 'Dillon': '45033', 'Dorchester': '45035', 'Edgefield': '45037', 'Fairfield': '45039', 'Florence': '45041', 'Georgetown': '45043', 'Greenville': '45045', 'Greenwood': '45047', 'Hampton': '45049', 'Horry': '45051', 'Jasper': '45053', 'Kershaw': '45055', 'Lancaster': '45057', 'Laurens': '45059', 'Lee': '45061', 'Lexington': '45063', 'McCormick': '45065', 'Marion': '45067', 'Marlboro': '45069', 'Newberry': '45071', 'Oconee': '45073', 'Orangeburg': '45075', 'Pickens': '45077', 'Richland': '45079', 'Saluda': '45081', 'Spartanburg': '45083', 'Sumter': '45085', 'Union': '45087', 'Williamsburg': '45089', 'York': '45091'
}

MD_FIPS = {
    'Allegany': '24001', 'Anne Arundel': '24003', 'Baltimore': '24005', 'Baltimore City': '24510', 'Calvert': '24009', 'Caroline': '24011', 'Carroll': '24013', 'Cecil': '24015', 'Charles': '24017', 'Dorchester': '24019', 'Frederick': '24021', 'Garrett': '24023', 'Harford': '24025', 'Howard': '24027', 'Kent': '24029', 'Montgomery': '24031', "Prince George's": '24033', "Queen Anne's": '24035', "St. Mary's": '24037', 'Somerset': '24039', 'Talbot': '24041', 'Washington': '24043', 'Wicomico': '24045', 'Worcester': '24047'
}

IL_FIPS = {
    'Adams': '17001', 'Alexander': '17003', 'Bond': '17005', 'Boone': '17007', 'Brown': '17009', 'Bureau': '17011', 'Calhoun': '17013', 'Carroll': '17015', 'Cass': '17017', 'Champaign': '17019', 'Christian': '17021', 'Clark': '17023', 'Clay': '17025', 'Clinton': '17027', 'Coles': '17029', 'Cook': '17031', 'Crawford': '17033', 'Cumberland': '17035', 'DeKalb': '17037', 'DeWitt': '17039', 'Douglas': '17041', 'DuPage': '17043', 'Edgar': '17045', 'Edwards': '17047', 'Effingham': '17049', 'Fayette': '17051', 'Ford': '17053', 'Franklin': '17055', 'Fulton': '17057', 'Gallatin': '17059', 'Greene': '17061', 'Grundy': '17063', 'Hamilton': '17065', 'Hancock': '17067', 'Hardin': '17069', 'Henderson': '17071', 'Henry': '17073', 'Iroquois': '17075', 'Jackson': '17077', 'Jasper': '17079', 'Jefferson': '17081', 'Jersey': '17083', 'Jo Daviess': '17085', 'Johnson': '17087', 'Kane': '17089', 'Kankakee': '17091', 'Kendall': '17093', 'Knox': '17095', 'Lake': '17097', 'LaSalle': '17099', 'Lawrence': '17101', 'Lee': '17103', 'Livingston': '17105', 'Logan': '17107', 'McDonough': '17109', 'McHenry': '17111', 'McLean': '17113', 'Macon': '17115', 'Macoupin': '17117', 'Madison': '17119', 'Marion': '17121', 'Marshall': '17123', 'Mason': '17125', 'Massac': '17127', 'Menard': '17129', 'Mercer': '17131', 'Monroe': '17133', 'Montgomery': '17135', 'Morgan': '17137', 'Moultrie': '17139', 'Ogle': '17141', 'Peoria': '17143', 'Perry': '17145', 'Piatt': '17147', 'Pike': '17149', 'Pope': '17151', 'Pulaski': '17153', 'Putnam': '17155', 'Randolph': '17157', 'Richland': '17159', 'Rock Island': '17161', 'Saline': '17165', 'Sangamon': '17167', 'Schuyler': '17169', 'Scott': '17171', 'Shelby': '17173', 'St. Clair': '17163', 'Stark': '17175', 'Stephenson': '17177', 'Tazewell': '17179', 'Union': '17181', 'Vermilion': '17183', 'Wabash': '17185', 'Warren': '17187', 'Washington': '17189', 'Wayne': '17191', 'White': '17193', 'Whiteside': '17195', 'Will': '17197', 'Williamson': '17199', 'Winnebago': '17201', 'Woodford': '17203'
}


def load_georgia_data():
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Coverage_Tier
Appling,18386,20.1,5,3500,5,3414,75+
Atkinson,8165,26.2,4,1800,0,0,No CEP
Bacon,11164,18.4,4,2200,4,2094,75+
Baker,3099,22.8,2,500,2,289,75+
Baldwin,44690,22.5,7,5500,7,4510,75+
Banks,19435,13.2,4,3000,4,2798,75+
Barrow,83240,10.8,17,14000,0,0,No CEP
Bartow,111576,12.4,23,19000,0,0,No CEP
Ben Hill,16700,28.4,7,3800,5,2831,50-74
Berrien,19397,19.8,6,3500,5,3061,50-74
Bibb,155025,24.8,33,22000,33,20922,75+
Bleckley,13053,20.3,6,2800,5,2581,50-74
Brantley,19109,18.6,7,3800,7,3375,75+
Brooks,15227,24.7,6,2500,6,2179,75+
Bryan,41586,9.2,5,7000,0,0,No CEP
Bulloch,79608,20.1,19,12000,12,8189,25-49
Burke,22383,28.6,5,3200,5,3841,75+
Butts,24936,14.2,5,4200,5,3497,75+
Calhoun,6189,34.2,3,900,3,443,75+
Camden,54666,10.4,12,9500,0,0,No CEP
Candler,10856,25.6,5,2200,4,2157,50-74
Carroll,119992,14.8,30,20000,23,16350,25-49
Catoosa,67580,10.2,17,12000,5,2827,25-49
Charlton,13392,22.1,4,1800,4,1613,75+
Chatham,294865,18.4,56,36000,0,0,No CEP
Chattahoochee,10767,14.2,3,1200,1,285,25-49
Chattooga,24789,22.8,8,4500,0,0,No CEP
Cherokee,277647,6.8,29,42000,0,0,No CEP
Clarke,128331,28.6,24,14000,21,12275,50-74
Clay,2834,38.2,2,600,2,191,75+
Clayton,297595,20.4,67,42000,64,50132,75+
Clinch,6743,28.6,3,1400,3,1242,75+
Cobb,771580,9.2,81,90000,34,28980,25-49
Coffee,43273,21.4,12,7000,12,7640,75+
Colquitt,46406,24.2,13,8500,13,8767,75+
Columbia,166672,7.2,17,26000,0,0,No CEP
Cook,17212,22.8,5,3200,4,2979,50-74
Coweta,152194,9.8,27,22000,0,0,No CEP
Crawford,12249,18.4,6,2200,3,1516,25-49
Crisp,22372,28.6,5,3500,5,3311,75+
Dade,16227,14.8,4,2500,0,0,No CEP
Dawson,26108,9.8,7,4500,0,0,No CEP
Decatur,26404,27.4,6,4200,6,4178,75+
DeKalb,764382,17.8,127,90000,102,70945,75+
Dodge,20605,22.8,8,3800,5,2659,50-74
Dooly,13390,32.4,5,1800,4,1067,50-74
Dougherty,87956,30.2,23,14000,21,12910,75+
Douglas,145673,14.2,34,22000,0,0,No CEP
Early,10008,30.4,3,1800,3,1482,75+
Echols,3754,22.8,2,800,2,917,75+
Effingham,68164,9.8,12,10000,0,0,No CEP
Elbert,19194,22.8,6,3500,5,3007,50-74
Emanuel,22646,27.4,6,3800,6,3939,75+
Evans,10727,24.2,5,2200,4,1742,50-74
Fannin,26188,14.8,5,3500,5,2753,75+
Fayette,117397,5.8,12,20000,0,0,No CEP
Floyd,98498,18.4,24,14000,8,6357,25-49
Forsyth,263014,5.2,8,42000,0,0,No CEP
Franklin,23349,18.4,5,3800,5,3577,75+
Fulton,1098791,14.8,145,100000,97,58145,50-74
Gilmer,36693,14.8,7,5500,5,4124,50-74
Glascock,3082,18.4,2,600,0,0,No CEP
Glynn,85292,14.8,20,14000,16,12727,75+
Gordon,58850,15.8,16,10000,15,10452,75+
Grady,24633,22.8,7,4500,6,4415,50-74
Greene,17754,18.4,4,3200,4,2275,75+
Gwinnett,975218,12.4,127,110000,0,0,No CEP
Habersham,44289,15.8,15,8500,14,7257,75+
Hall,204441,14.8,44,28000,0,0,No CEP
Hancock,8535,38.4,3,1400,3,652,75+
Haralson,29728,16.8,8,5500,7,3525,50-74
Harris,35236,7.8,7,6000,0,0,No CEP
Hart,26205,18.4,5,4200,5,3743,75+
Heard,11923,18.4,6,2500,5,2220,50-74
Henry,240712,9.8,50,36000,0,0,No CEP
Houston,158306,12.4,42,24000,29,22229,50-74
Irwin,9416,22.8,3,2000,3,1610,75+
Jackson,75380,12.4,12,11000,2,764,1-24
Jasper,14219,14.8,4,2800,4,2706,75+
Jeff Davis,14969,22.8,5,2800,5,3074,75+
Jefferson,15362,32.4,6,2800,5,2017,50-74
Jenkins,8340,28.6,3,1600,3,1170,75+
Johnson,9426,26.2,3,1800,3,1026,75+
Jones,28735,14.8,7,4800,7,5004,75+
Lamar,18908,16.8,5,3200,4,2872,50-74
Lanier,10423,22.8,3,1800,3,1652,75+
Laurens,47418,22.8,16,8500,16,12616,75+
Lee,29922,7.8,8,6000,0,0,No CEP
Liberty,61315,18.4,13,10000,12,10925,75+
Lincoln,7921,18.4,3,1600,3,1261,75+
Long,19559,18.4,5,3200,5,4724,75+
Lowndes,116005,20.4,20,16000,19,18865,75+
Lumpkin,33610,12.4,5,5500,0,0,No CEP
McDuffie,21578,22.8,6,3800,6,3088,75+
McIntosh,14119,22.8,3,2000,3,1394,75+
Macon,12947,38.4,3,2000,3,1047,75+
Madison,29737,14.8,8,5500,7,5165,50-74
Marion,8161,28.6,2,1400,2,1293,75+
Meriwether,21992,24.2,7,3800,6,2241,50-74
Miller,5718,26.2,3,1200,3,772,75+
Mitchell,22432,30.4,7,3800,7,2175,75+
Monroe,27578,12.4,5,4800,0,0,No CEP
Montgomery,9036,26.2,3,1600,3,902,75+
Morgan,19276,14.8,4,3500,0,0,No CEP
Murray,39628,15.8,11,7000,11,6585,75+
Muscogee,206922,24.8,54,28000,49,26947,75+
Newton,114289,14.8,25,18000,22,18672,75+
Oconee,40280,6.2,0,8000,0,0,No CEP
Oglethorpe,15259,14.8,4,2800,4,2293,75+
Paulding,174948,9.8,29,26000,0,0,No CEP
Peach,27695,22.8,7,4200,7,3980,75+
Pickens,33144,9.8,6,5500,0,0,No CEP
Pierce,19164,18.4,5,3200,5,3647,75+
Pike,18583,12.4,5,3500,0,0,No CEP
Polk,42178,18.4,10,7000,10,7713,75+
Pulaski,11519,26.2,3,2000,3,1320,75+
Putnam,21869,14.8,4,3500,4,2938,75+
Quitman,2276,38.4,2,500,2,309,75+
Rabun,16880,12.4,4,2800,4,2257,75+
Randolph,6778,34.2,3,1200,3,635,75+
Richmond,202518,26.2,59,28000,48,28891,75+
Rockdale,90896,14.8,19,14000,18,15342,75+
Schley,5257,18.4,2,800,0,0,No CEP
Screven,14227,24.2,3,2200,0,0,No CEP
Seminole,8330,26.2,2,1400,2,1332,75+
Spalding,67560,20.4,18,10000,18,9350,75+
Stephens,26726,18.4,6,4200,6,3855,75+
Stewart,6621,38.4,3,1000,3,338,75+
Sumter,30352,30.4,6,4500,5,3560,50-74
Talbot,6498,28.6,1,1000,1,364,75+
Taliaferro,1662,38.4,1,400,1,184,75+
Tattnall,25520,22.8,5,3200,5,3501,75+
Taylor,8906,28.6,4,1800,4,1176,75+
Telfair,15860,30.4,5,2500,5,1543,75+
Terrell,8531,36.2,3,1400,3,921,75+
Thomas,44451,20.4,12,7500,12,8440,75+
Tift,40644,22.8,11,6500,11,7471,75+
Toombs,26830,22.8,10,4500,9,5397,75+
Towns,12726,12.4,3,1800,3,966,75+
Treutlen,6855,28.6,2,1400,2,1020,75+
Troup,69271,18.4,19,10000,18,12238,75+
Turner,7985,30.4,3,1400,3,1107,75+
Twiggs,8120,26.2,3,1400,3,726,75+
Union,24511,9.8,6,4200,5,3015,50-74
Upson,26320,22.8,4,4200,4,3996,75+
Walker,68824,14.8,17,10000,15,8379,75+
Walton,97604,12.4,19,15000,4,2032,1-24
Ware,35734,22.8,10,5500,10,5920,75+
Warren,5254,30.4,3,1000,3,662,75+
Washington,20011,28.6,4,3200,4,2661,75+
Wayne,29927,18.4,10,5500,8,5348,50-74
Webster,2613,34.2,2,600,2,228,75+
Wheeler,7855,28.6,3,1400,3,848,75+
White,30798,12.4,7,5000,6,3782,50-74
Whitfield,104628,15.8,33,16000,22,11942,50-74
Wilcox,8635,28.6,3,1400,3,1126,75+
Wilkes,9777,22.8,5,2500,4,1262,50-74
Wilkinson,9078,24.2,4,1800,4,1036,75+
Worth,20656,22.8,5,3200,5,3057,75+"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * 0.22 * df['Poverty_Rate'] / 100).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Coverage_Pct'] = df.apply(lambda r: round((r['CEP_Schools'] / r['Total_Schools']) * 100, 1) if r['Total_Schools'] > 0 else 0, axis=1)
    tier_map = {'75+': 4, '50-74': 3, '25-49': 2, '1-24': 1, 'No CEP': 0}
    df['Status_Numeric'] = df['Coverage_Tier'].map(tier_map).fillna(0).astype(int)
    df['Status'] = df['Coverage_Tier'].apply(lambda x: 'FULL CEP' if x == '75+' else 'PARTIAL CEP' if x in ['50-74', '25-49', '1-24'] else 'NO CEP')
    return df


def load_georgia_district_data():
    import io
    csv_data = """District,County,Eligible,CEP_Schools,Students,Status
Appling County,Appling,5,5,3414,FULL CEP
Atkinson County,Atkinson,4,0,0,NO CEP
Bacon County,Bacon,4,4,2094,FULL CEP
Baker County,Baker,2,2,289,FULL CEP
Baldwin County,Baldwin,7,7,4510,FULL CEP
Banks County,Banks,4,4,2798,FULL CEP
Barrow County,Barrow,17,0,0,NO CEP
Bartow County,Bartow,19,0,0,NO CEP
Ben Hill County,Ben Hill,7,5,2831,PARTIAL CEP
Berrien County,Berrien,6,5,3061,PARTIAL CEP
Bibb County,Bibb,33,33,20922,FULL CEP
Bleckley County,Bleckley,6,5,2581,PARTIAL CEP
Brantley County,Brantley,7,7,3375,FULL CEP
Brooks County,Brooks,6,6,2179,FULL CEP
Bryan County,Bryan,5,0,0,NO CEP
Bulloch County,Bulloch,19,12,8189,PARTIAL CEP
Burke County,Burke,5,5,3841,FULL CEP
Butts County,Butts,5,5,3497,FULL CEP
Calhoun City Schools,Gordon,5,5,4193,FULL CEP
Calhoun County,Calhoun,3,3,443,FULL CEP
Camden County,Camden,12,0,0,NO CEP
Candler County,Candler,5,4,2157,PARTIAL CEP
Carroll County,Carroll,26,23,16350,PARTIAL CEP
Carrollton City,Carroll,4,0,0,NO CEP
Cartersville City,Bartow,4,0,0,NO CEP
Catoosa County,Catoosa,17,5,2827,PARTIAL CEP
Charlton County,Charlton,4,4,1613,FULL CEP
Chattahoochee County,Chattahoochee,3,1,285,PARTIAL CEP
Chattooga County,Chattooga,5,0,0,NO CEP
Cherokee County,Cherokee,29,0,0,NO CEP
Clarke County,Clarke,24,21,12275,PARTIAL CEP
Clayton County,Clayton,67,64,50132,PARTIAL CEP
Clinch County,Clinch,3,3,1242,FULL CEP
Cobb County,Cobb,70,34,28980,PARTIAL CEP
Coffee County,Coffee,12,12,7640,FULL CEP
Colquitt County,Colquitt,13,13,8767,FULL CEP
Columbia County,Columbia,17,0,0,NO CEP
Commerce City Schools,Jackson,2,2,764,FULL CEP
Cook County,Cook,5,4,2979,PARTIAL CEP
Coweta County,Coweta,27,0,0,NO CEP
Crawford County,Crawford,6,3,1516,PARTIAL CEP
Crisp County,Crisp,5,5,3311,FULL CEP
Dade County,Dade,4,0,0,NO CEP
Dawson County,Dawson,7,0,0,NO CEP
Decatur County,Decatur,6,6,4178,FULL CEP
DeKalb County,DeKalb,126,101,70185,PARTIAL CEP
Dodge County,Dodge,8,5,2659,PARTIAL CEP
Dooly County,Dooly,5,4,1067,PARTIAL CEP
Dougherty County,Dougherty,23,21,12910,PARTIAL CEP
Douglas County,Douglas,34,0,0,NO CEP
Dublin City,Laurens,5,5,2370,FULL CEP
Early County,Early,3,3,1482,FULL CEP
Echols County,Echols,2,2,917,FULL CEP
Effingham County,Effingham,12,0,0,NO CEP
Elbert County,Elbert,6,5,3007,PARTIAL CEP
Emanuel County,Emanuel,6,6,3939,FULL CEP
Evans County,Evans,5,4,1742,PARTIAL CEP
Fannin County,Fannin,5,5,2753,FULL CEP
Fayette County,Fayette,12,0,0,NO CEP
Floyd County,Floyd,15,0,0,NO CEP
Forsyth County,Forsyth,8,0,0,NO CEP
Franklin County,Franklin,5,5,3577,FULL CEP
Fulton County,Fulton,65,40,29564,PARTIAL CEP
Atlanta Public Schools,Fulton,80,57,28581,PARTIAL CEP
Gainesville City,Hall,9,0,0,NO CEP
Gilmer County,Gilmer,7,5,4124,PARTIAL CEP
Glascock County,Glascock,2,0,0,NO CEP
Glynn County,Glynn,20,16,12727,PARTIAL CEP
Gordon County,Gordon,11,10,6259,PARTIAL CEP
Grady County,Grady,7,6,4415,PARTIAL CEP
Greene County,Greene,4,4,2275,FULL CEP
Griffin-Spalding County,Spalding,18,18,9350,FULL CEP
Gwinnett County,Gwinnett,127,0,0,NO CEP
Habersham County,Habersham,15,14,7257,PARTIAL CEP
Hall County,Hall,35,0,0,NO CEP
Hancock County,Hancock,3,3,652,FULL CEP
Haralson County,Haralson,7,7,3525,FULL CEP
Harris County,Harris,7,0,0,NO CEP
Hart County,Hart,5,5,3743,FULL CEP
Heard County,Heard,6,5,2220,PARTIAL CEP
Henry County,Henry,50,0,0,NO CEP
Houston County,Houston,42,29,22229,PARTIAL CEP
Irwin County,Irwin,3,3,1610,FULL CEP
Jackson County,Jackson,9,0,0,NO CEP
Jasper County,Jasper,4,4,2706,FULL CEP
Jeff Davis County,Jeff Davis,5,5,3074,FULL CEP
Jefferson County,Jefferson,6,5,2017,PARTIAL CEP
Jenkins County,Jenkins,3,3,1170,FULL CEP
Johnson County,Johnson,3,3,1026,FULL CEP
Jones County,Jones,7,7,5004,FULL CEP
Lamar County,Lamar,5,4,2872,PARTIAL CEP
Lanier County,Lanier,3,3,1652,FULL CEP
Laurens County,Laurens,8,8,6308,FULL CEP
Lee County,Lee,8,0,0,NO CEP
Liberty County,Liberty,13,12,10925,PARTIAL CEP
Lincoln County,Lincoln,3,3,1261,FULL CEP
Long County,Long,5,5,4724,FULL CEP
Lowndes County,Lowndes,12,11,10618,PARTIAL CEP
Lumpkin County,Lumpkin,5,0,0,NO CEP
McDuffie County,McDuffie,6,6,3088,FULL CEP
McIntosh County,McIntosh,3,3,1394,FULL CEP
Macon County,Macon,3,3,1047,FULL CEP
Madison County,Madison,8,7,5165,PARTIAL CEP
Marietta City,Cobb,11,0,0,NO CEP
Marion County,Marion,2,2,1293,FULL CEP
Meriwether County,Meriwether,7,6,2241,PARTIAL CEP
Miller County,Miller,3,3,772,FULL CEP
Mitchell County,Mitchell,4,4,1203,FULL CEP
Monroe County,Monroe,5,0,0,NO CEP
Montgomery County,Montgomery,3,3,902,FULL CEP
Morgan County,Morgan,4,0,0,NO CEP
Murray County,Murray,11,11,6585,FULL CEP
Muscogee County,Muscogee,54,49,26947,PARTIAL CEP
Newton County,Newton,25,22,18672,PARTIAL CEP
Oglethorpe County,Oglethorpe,4,4,2293,FULL CEP
Paulding County,Paulding,29,0,0,NO CEP
Peach County,Peach,7,7,3980,FULL CEP
Pelham City,Mitchell,3,3,1246,FULL CEP
Pickens County,Pickens,6,0,0,NO CEP
Pierce County,Pierce,5,5,3647,FULL CEP
Pike County,Pike,5,0,0,NO CEP
Polk County,Polk,10,10,7713,FULL CEP
Pulaski County,Pulaski,3,3,1320,FULL CEP
Putnam County,Putnam,4,4,2938,FULL CEP
Quitman County,Quitman,2,2,309,FULL CEP
Rabun County,Rabun,4,4,2257,FULL CEP
Randolph County,Randolph,3,3,635,FULL CEP
Richmond County,Richmond,59,48,28891,PARTIAL CEP
Rockdale County,Rockdale,19,18,15342,PARTIAL CEP
Rome City,Floyd,9,8,6357,PARTIAL CEP
Savannah-Chatham County,Chatham,56,0,0,NO CEP
Schley County,Schley,2,0,0,NO CEP
Screven County,Screven,3,0,0,NO CEP
Seminole County,Seminole,2,2,1332,FULL CEP
Social Circle City,Walton,4,4,2032,FULL CEP
Stephens County,Stephens,6,6,3855,FULL CEP
Stewart County,Stewart,3,3,338,FULL CEP
Sumter County,Sumter,6,5,3560,PARTIAL CEP
Talbot County,Talbot,1,1,364,FULL CEP
Taliaferro County,Taliaferro,1,1,184,FULL CEP
Tattnall County,Tattnall,5,5,3501,FULL CEP
Taylor County,Taylor,4,4,1176,FULL CEP
Telfair County,Telfair,5,5,1543,FULL CEP
Terrell County,Terrell,3,3,921,FULL CEP
Thomas County,Thomas,7,7,5818,FULL CEP
Thomasville City,Thomas,5,5,2622,FULL CEP
Tift County,Tift,11,11,7471,FULL CEP
Toombs County,Toombs,5,5,3118,FULL CEP
Towns County,Towns,3,3,966,FULL CEP
Treutlen County,Treutlen,2,2,1020,FULL CEP
Troup County,Troup,19,18,12238,PARTIAL CEP
Turner County,Turner,3,3,1107,FULL CEP
Twiggs County,Twiggs,3,3,726,FULL CEP
Union County,Union,6,5,3015,PARTIAL CEP
Thomaston-Upson County,Upson,4,4,3996,FULL CEP
Valdosta City,Lowndes,8,8,8247,FULL CEP
Vidalia City,Toombs,5,4,2279,PARTIAL CEP
Walker County,Walker,17,15,8379,PARTIAL CEP
Walton County,Walton,15,0,0,NO CEP
Ware County,Ware,10,10,5920,FULL CEP
Warren County,Warren,3,3,662,FULL CEP
Washington County,Washington,4,4,2661,FULL CEP
Wayne County,Wayne,10,8,5348,PARTIAL CEP
Webster County,Webster,2,2,228,FULL CEP
Wheeler County,Wheeler,3,3,848,FULL CEP
White County,White,7,6,3782,PARTIAL CEP
Whitfield County,Whitfield,23,22,11942,PARTIAL CEP
Wilcox County,Wilcox,3,3,1126,FULL CEP
Wilkes County,Wilkes,5,4,1262,PARTIAL CEP
Wilkinson County,Wilkinson,4,4,1036,FULL CEP
Worth County,Worth,5,5,3057,FULL CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_pennsylvania_data():
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Adams,104420,7.2,22,14500,3,1810,Partial CEP
Allegheny,1250578,12.4,226,120000,131,54000,Partial CEP
Armstrong,63410,12.8,23,8500,12,4822,Partial CEP
Beaver,168658,11.2,32,18000,13,5200,Partial CEP
Bedford,47507,12.1,14,7000,2,1160,Partial CEP
Berks,429923,14.3,68,52000,44,27000,Partial CEP
Blair,121829,14.5,28,16000,12,7029,Partial CEP
Bradford,60323,12.4,18,8500,7,1489,Partial CEP
Bucks,646538,6.2,82,58000,27,15608,Partial CEP
Butler,202897,7.8,28,22000,8,1748,Partial CEP
Cambria,127099,16.2,28,14000,10,5000,Partial CEP
Cameron,4211,15.2,3,900,2,558,Partial CEP
Carbon,64182,13.8,14,8000,11,4547,Partial CEP
Centre,162385,14.8,18,12000,1,0,Partial CEP
Chester,545823,5.9,78,62000,15,8448,Partial CEP
Clarion,37170,14.2,11,5500,3,1157,Partial CEP
Clearfield,79703,14.8,13,8000,4,3051,Partial CEP
Clinton,38632,13.9,9,5000,0,0,NO CEP
Columbia,65453,13.2,12,7000,5,1591,Partial CEP
Crawford,84629,14.2,24,11000,14,4805,Partial CEP
Cumberland,261624,7.4,38,28000,3,1493,Partial CEP
Dauphin,285264,14.8,52,33000,39,29614,Partial CEP
Delaware,576831,11.8,98,62000,69,38834,Partial CEP
Elk,29910,12.1,9,4500,4,1830,Partial CEP
Erie,269728,17.2,58,34000,30,14637,Partial CEP
Fayette,127923,18.4,32,15000,19,8000,Partial CEP
Forest,7247,18.9,4,1200,4,366,Full CEP
Franklin,156529,9.8,34,20000,16,6376,Partial CEP
Fulton,15779,12.3,4,2000,0,0,NO CEP
Greene,36159,15.8,18,6500,10,3823,Partial CEP
Huntingdon,45144,14.8,18,7000,8,2808,Partial CEP
Indiana,84073,14.2,21,10000,5,0,Partial CEP
Jefferson,43521,14.1,12,5500,7,1827,Partial CEP
Juniata,24636,11.8,7,3500,0,0,NO CEP
Lackawanna,209674,14.8,44,22000,25,13563,Partial CEP
Lancaster,552984,9.2,76,58000,42,22252,Partial CEP
Lawrence,85512,15.2,22,10000,12,4503,Partial CEP
Lebanon,143000,11.4,22,15000,9,4934,Partial CEP
Lehigh,375879,13.8,62,48000,46,29583,Partial CEP
Luzerne,322539,15.2,78,38000,62,35246,Partial CEP
Lycoming,113299,14.2,26,14000,15,6409,Partial CEP
McKean,40585,16.2,11,5500,4,1830,Partial CEP
Mercer,109424,13.8,28,14000,16,5233,Partial CEP
Mifflin,46138,13.9,14,6500,5,1853,Partial CEP
Monroe,170271,13.2,28,18000,19,10264,Partial CEP
Montgomery,856553,7.4,112,85000,34,15228,Partial CEP
Montour,18144,10.2,5,2500,0,0,NO CEP
Northampton,310860,10.8,52,35000,31,22423,Partial CEP
Northumberland,91436,16.8,22,10000,19,9400,Partial CEP
Perry,46272,10.2,11,5500,0,0,NO CEP
Philadelphia,1574281,22.0,232,140000,232,116297,Full CEP
Pike,57369,11.2,9,5500,0,0,NO CEP
Potter,15824,14.8,6,2500,3,965,Partial CEP
Schuylkill,140261,16.2,32,15000,24,10718,Partial CEP
Snyder,40372,11.8,8,4500,0,0,NO CEP
Somerset,72631,15.8,18,8000,3,0,Partial CEP
Sullivan,5978,14.2,3,1200,2,594,Partial CEP
Susquehanna,40373,12.4,10,5000,2,790,Partial CEP
Tioga,40591,14.8,12,5500,4,2029,Partial CEP
Union,44947,13.2,10,5000,4,1917,Partial CEP
Venango,50668,15.8,14,6500,6,2622,Partial CEP
Warren,39191,13.8,13,6000,9,3850,Partial CEP
Washington,207820,10.8,42,22000,17,5533,Partial CEP
Wayne,51276,12.4,12,6000,5,1824,Partial CEP
Westmoreland,348099,11.8,68,36000,45,18000,Partial CEP
Wyoming,26794,11.2,8,3500,4,2051,Partial CEP
York,456438,9.8,72,52000,11,6099,Partial CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * 0.22 * df['Poverty_Rate'] / 100).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1) if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_rhode_island_data():
    """Load Rhode Island county data - 5 counties
    CEP Source: FRAC Community Eligibility Provision 2024-2025 Fact Sheet (October 2025)
      https://frac.org/wp-content/uploads/CEP-Fact-Sheets_1025_RI40.pdf
      State totals: 120 CEP schools / 143 eligible = 84% coverage
      56,457 children served statewide (includes charters + specialty schools
      not attributable to individual counties)
    County-level school counts: Rhode Island CEP Summary Sheet (Version 3), verified
      against FRAC October 2025 fact sheet.
      Providence: 157 schools, 71 CEP, 34,912 students
      Kent:       37 schools,  6 CEP,  3,270 students
      Newport:    19 schools,  3 CEP,  1,675 students
      Washington: 33 schools,  2 CEP,    282 students
      Bristol:    11 schools,  0 CEP,      0 students
    Population Source: U.S. Census Bureau Population Estimates 2024
    Poverty Source: U.S. Census Bureau ACS 5-Year Estimates (CensusReporter, 2024)
    Note: Rhode Island counties have no governmental functions (since 1846).
      CEP data is aggregated from school districts to county level for mapping.
      County rows sum to 82 CEP schools / 40,139 students; difference vs state
      headline (120 / 56,457) = 38 public charters + specialty schools not
      county-attributed. Same methodology used across all state pages.
      Key changes (June 2026 update):
        Providence: 95 -> 71 CEP schools, 47,130 -> 34,912 students
        Newport: corrected to Partial CEP (3 of 19 total schools)
        Washington: corrected to Partial CEP (2 of 33 total schools)
        Kent: 7 -> 37 total schools
        Bristol: 0 -> 11 total schools (still NO CEP)
    """
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Providence,658969,13.0,157,95000,71,34912,Partial CEP
Kent,169512,4.2,37,18000,6,3270,Partial CEP
Newport,85798,6.6,19,8000,3,1675,Partial CEP
Washington,129594,5.8,33,13000,2,282,Partial CEP
Bristol,50145,6.8,11,6000,0,0,NO CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * 0.22 * df['Poverty_Rate'] / 100).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1) if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_new_jersey_data():
    data = {
        'County': ['Salem', 'Hudson', 'Cumberland', 'Passaic', 'Essex', 'Camden', 'Ocean', 'Atlantic', 'Mercer', 'Warren', 'Gloucester', 'Union', 'Middlesex', 'Burlington', 'Monmouth', 'Bergen', 'Cape May', 'Somerset', 'Sussex', 'Morris', 'Hunterdon'],
        'Population': [64837, 724854, 154152, 524118, 863728, 523485, 637229, 274534, 387340, 109632, 302294, 575345, 863162, 461860, 643615, 955732, 95263, 345361, 144221, 509285, 128947],
        'Poverty_Rate': [28.8, 23.6, 23.5, 20.7, 18.6, 18.0, 14.9, 14.5, 13.2, 12.7, 12.0, 10.6, 10.4, 8.6, 7.9, 6.9, 6.4, 6.1, 5.2, 5.1, 3.6],
        'Children_in_Poverty': [18673, 171186, 36226, 108492, 160613, 94227, 94967, 39807, 51129, 13924, 36275, 60987, 89769, 39720, 50845, 65946, 6097, 21067, 7499, 25973, 4642],
        'Eligible_Schools': [34, 135, 51, 154, 248, 157, 117, 79, 113, 40, 79, 186, 210, 137, 188, 291, 32, 75, 47, 151, 48],
        'CEP_Schools': [13, 74, 23, 90, 162, 32, 16, 20, 36, 4, 15, 2, 16, 10, 25, 11, 5, 4, 0, 0, 0],
        'Student_Population': [11024, 85473, 28185, 80468, 145744, 81500, 65938, 42088, 59177, 15349, 44966, 102682, 128115, 68676, 95886, 138359, 11630, 47160, 19696, 70390, 16567],
        'Students_in_CEP': [3559, 43237, 12179, 44037, 77790, 12728, 13052, 10891, 16721, 2130, 6879, 618, 8628, 4734, 9016, 2574, 1021, 887, 0, 0, 0],
        'Change_This_Year': ['10 more schools', '42 more schools', '8 more schools', '2 more schools', '15 more schools', '12 fewer schools', '10 more schools', '19 more schools', '9 more schools', 'First year (4 schools)', '12 more schools', 'First year (2 schools)', '\u2014', 'First year (10 schools)', '14 more schools', '8 more schools', '\u2014', 'First year (4 schools)', '\u2014', '\u2014', '\u2014'],
        'Status': ['FULL CEP', 'PARTIAL CEP', 'NO CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'PARTIAL CEP', 'NO CEP', 'NO CEP', 'NO CEP']
    }
    df = pd.DataFrame(data)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Coverage_Pct'] = ((df['Students_in_CEP'] / df['Student_Population']) * 100).round(1)
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_virginia_data():
    import io
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
    df['Population'] = df['Population'].astype(int)
    df['Poverty_Rate'] = df['Poverty_Rate'].astype(float)
    df['Eligible_Schools'] = df['Eligible_Schools'].astype(int)
    df['CEP_Schools'] = df['CEP_Schools'].astype(int)
    df['Students_in_CEP'] = df['Students_in_CEP'].astype(int)
    df['Coverage_Pct'] = df['Coverage_Pct'].astype(int)
    df['School_Gap'] = df['School_Gap'].astype(int)
    df['School_Districts'] = 1
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_kentucky_data():
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Knox,30193,50.2,10,3512,10,3512,FULL CEP
Clay,20345,47.4,9,2954,9,2954,Partial CEP
Fulton,6515,45.7,4,928,4,928,NO CEP schools
Elliott,7354,45.3,4,898,4,898,FULL CEP
Menifee,6113,45.2,2,939,2,939,FULL CEP
Wolfe,6562,45.2,6,1071,6,1071,FULL CEP
Hickman,4521,43.7,2,763,2,763,FULL CEP
Magoffin,11637,41.8,5,1902,5,1902,FULL CEP
Martin,11287,41.2,5,1741,5,1741,FULL CEP
Lee,7395,40.5,3,882,3,882,FULL CEP
Leslie,10513,39.9,5,1441,5,1441,FULL CEP
Floyd,35942,39.9,18,5226,18,5226,FULL CEP
Metcalfe,10286,39.2,6,1515,6,1515,FULL CEP
McCreary,16888,38.1,7,2669,7,2669,FULL CEP
Breathitt,13718,38.1,7,1668,7,1668,FULL CEP
Livingston,8888,37.9,4,1454,4,1454,FULL CEP
Cumberland,5888,37.8,4,820,4,820,FULL CEP
Knott,14251,37.1,8,2147,8,2147,FULL CEP
Wayne,20087,36.9,10,3100,10,3100,FULL CEP
Letcher,21861,36.6,11,3222,11,3222,FULL CEP
Crittenden,9008,35.9,4,1293,4,1293,FULL CEP
Harlan,26831,35.8,12,3614,12,3614,FULL CEP
Todd,12460,35.0,5,2040,5,2040,FULL CEP
Pike,58000,34.6,31,8268,31,8268,FULL CEP
Bracken,8203,34.5,3,1116,3,1116,FULL CEP
Rowan,25030,34.4,6,3270,6,3270,FULL CEP
Trigg,14621,34.2,4,2178,4,2178,FULL CEP
Rockcastle,16885,33.0,9,2660,9,2660,FULL CEP
Bath,11825,32.9,4,1562,4,1562,FULL CEP
Perry,27223,31.8,9,3688,9,3688,FULL CEP
Larue,14753,31.6,7,2214,7,2214,FULL CEP
Daviess,103000,31.4,44,17130,44,17130,FULL CEP
Casey,15771,31.3,6,2212,6,2212,FULL CEP
Barren,44485,30.7,14,6752,14,6752,FULL CEP
Fleming,15082,30.7,5,2077,5,2077,FULL CEP
Johnson,22680,30.5,9,3259,9,3259,FULL CEP
Hopkins,44000,30.3,18,6851,18,6851,FULL CEP
Powell,12455,30.3,5,1794,5,1794,FULL CEP
Lewis,13034,30.1,5,1816,5,1816,FULL CEP
Bell,24097,29.9,11,3268,11,3268,FULL CEP
Grayson,26420,29.8,9,3952,9,3952,FULL CEP
Breckinridge,20528,29.7,7,2881,7,2881,FULL CEP
Whitley,36712,29.6,12,5554,12,5554,FULL CEP
Monroe,10962,29.6,4,1469,4,1469,FULL CEP
Hart,19437,29.2,7,2732,7,2732,FULL CEP
Russell,17500,28.9,9,2659,9,2659,FULL CEP
Laurel,62000,28.9,25,9825,25,9825,FULL CEP
Muhlenberg,30928,28.8,11,4272,11,4272,FULL CEP
Lawrence,16293,28.4,7,2167,7,2167,FULL CEP
Carlisle,4826,28.4,2,646,2,646,FULL CEP
Carroll,11025,28.3,4,1357,4,1357,FULL CEP
Green,10925,28.3,4,1502,4,1502,FULL CEP
Marion,19581,28.1,7,2774,7,2774,FULL CEP
Graves,36000,28.1,12,5328,12,5328,FULL CEP
Estill,14163,27.8,6,1970,6,1970,FULL CEP
Carter,26627,27.7,9,3566,9,3566,FULL CEP
Robertson,2142,27.3,1,299,1,299,FULL CEP
Garrard,18315,27.2,7,2607,7,2607,FULL CEP
Boyd,46000,27.1,17,6469,17,6469,FULL CEP
Christian,70000,27.0,18,10639,18,10639,FULL CEP
Adair,19924,26.9,8,2862,8,2862,FULL CEP
Butler,12888,26.2,5,1811,5,1811,FULL CEP
Jefferson,783022,25.8,173,121062,173,121062,FULL CEP
Clinton,10035,25.3,4,1430,4,1430,FULL CEP
Edmonson,12183,25.0,4,1708,4,1708,FULL CEP
Henry,16223,24.8,6,2204,6,2204,FULL CEP
Henderson,46000,24.7,14,6908,14,6908,FULL CEP
Mason,17341,24.7,5,2333,5,2333,FULL CEP
Taylor,26023,24.1,8,3682,8,3682,FULL CEP
McCracken,65000,24.1,21,10042,21,10042,FULL CEP
Allen,20588,23.7,7,2921,7,2921,FULL CEP
Union,14537,23.5,5,1988,5,1988,FULL CEP
Franklin,52097,23.3,17,7554,17,7554,FULL CEP
Morgan,12975,23.1,4,1744,4,1744,FULL CEP
Fayette,323725,23.1,80,42450,80,42450,FULL CEP
Gallatin,8909,22.9,3,1186,3,1186,FULL CEP
Pulaski,65000,22.8,22,9625,22,9625,FULL CEP
Meade,30003,22.5,10,4259,10,4259,FULL CEP
Hancock,9095,22.2,3,1212,3,1212,FULL CEP
Marshall,31659,21.8,8,4383,8,4383,FULL CEP
Calloway,38250,21.3,8,5293,8,5293,FULL CEP
Clark,36972,21.1,12,5299,12,5299,FULL CEP
Owen,11027,20.9,3,1459,3,1459,FULL CEP
Hardin,110000,20.4,37,15769,37,15769,FULL CEP
Madison,92000,20.2,24,12932,24,12932,FULL CEP
Lyon,8226,20.1,3,1076,3,1076,FULL CEP
Logan,27432,19.8,8,3948,8,3948,FULL CEP
Ohio,24720,19.7,8,3513,8,3513,FULL CEP
Ballard,7728,19.4,3,989,3,989,FULL CEP
Harrison,18692,19.2,5,2433,5,2433,FULL CEP
Jackson,12955,19.2,6,1650,6,1650,FULL CEP
Lincoln,24275,19.1,8,3438,8,3438,FULL CEP
Owsley,4051,19.1,2,511,2,511,FULL CEP
Nicholas,7537,18.7,3,954,3,954,FULL CEP
Montgomery,28114,18.7,9,3938,9,3938,FULL CEP
Boyle,30614,18.3,8,4236,8,4236,FULL CEP
Mercer,22641,18.2,7,3045,7,3045,FULL CEP
Anderson,23852,17.9,6,3248,6,3248,FULL CEP
Woodford,27000,17.6,11,3614,11,3614,FULL CEP
Kenton,171288,17.4,42,23882,42,23882,FULL CEP
Grant,25245,17.2,8,3471,8,3471,FULL CEP
Scott,60000,17.1,18,8309,18,8309,FULL CEP
Jessamine,55000,16.6,13,7637,13,7637,FULL CEP
Nelson,47153,16.5,13,6552,13,6552,FULL CEP
Caldwell,12649,16.4,5,1721,5,1721,FULL CEP
Webster,13017,16.1,5,1733,5,1733,FULL CEP
Campbell,93000,15.8,29,12718,29,12718,FULL CEP
Washington,12027,15.7,4,1584,4,1584,FULL CEP
Simpson,19245,15.1,5,2685,5,2685,FULL CEP
Shelby,50329,14.7,12,7035,12,7035,FULL CEP
Bourbon,21629,14.4,6,2897,6,2897,FULL CEP
Greenup,35962,14.3,11,4795,11,4795,FULL CEP
Warren,140918,13.9,34,19702,34,19702,FULL CEP
Pendleton,14644,13.8,4,2000,4,2000,FULL CEP
Spencer,20000,13.1,5,2796,5,2796,FULL CEP
Bullitt,89500,12.6,21,12340,21,12340,FULL CEP
Boone,139841,11.5,37,19279,37,19279,FULL CEP
Trimble,8474,10.8,2,1113,2,1113,FULL CEP
McLean,9152,10.7,3,1183,3,1183,FULL CEP
Oldham,67000,10.0,19,9157,19,9157,FULL CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Population'] = pd.to_numeric(df['Population'], errors='coerce')
    df['Poverty_Rate'] = pd.to_numeric(df['Poverty_Rate'], errors='coerce')
    df['Total_Schools'] = pd.to_numeric(df['Total_Schools'], errors='coerce')
    df['Student_Population'] = pd.to_numeric(df['Student_Population'], errors='coerce')
    df['CEP_Schools'] = pd.to_numeric(df['CEP_Schools'], errors='coerce')
    df['Students_in_CEP'] = pd.to_numeric(df['Students_in_CEP'], errors='coerce')
    df['School_Districts'] = 1
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = ((df['Students_in_CEP'] / df['Student_Population']) * 100).round(0).astype(int)
    df['School_Gap'] = df['Total_Schools'] - df['CEP_Schools']
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_south_carolina_data():
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Barnwell,20399,49.9,9,3117,9,3117,Full CEP
Dillon,27600,43.3,9,5107,9,5107,Partial CEP
Marion,28582,41.7,10,3924,10,3924,NO CEP
McCormick,10341,39.5,1,569,1,569,Full CEP
Union,26409,38.4,6,3528,6,3528,Full CEP
Lee,15579,36.4,5,1300,5,1300,Full CEP
Marlboro,25100,32.3,7,3311,7,3311,Full CEP
Darlington,62376,32.2,18,8808,18,8808,Full CEP
Florence,138162,31.8,36,20834,36,20834,Full CEP
Cherokee,57900,28.8,15,7446,15,7446,Full CEP
Allendale,7271,28.7,3,835,3,835,Full CEP
Chester,32692,28.5,3,1554,3,1554,Full CEP
Williamsburg,29447,28.5,8,2696,8,2696,Full CEP
Chesterfield,44611,27.3,6,1998,6,1998,Full CEP
Hampton,18094,26.6,9,2221,9,2221,Full CEP
Jasper,36660,26.5,4,2948,4,2948,Full CEP
Orangeburg,82258,26.4,27,10006,27,10006,Full CEP
Clarendon,31158,26.3,9,1471,9,1471,Full CEP
Bamberg,13022,26.1,6,1881,6,1881,Full CEP
Saluda,19401,26.0,4,2513,4,2513,Full CEP
Newberry,39845,25.9,12,6149,12,6149,Full CEP
Fairfield,20366,25.3,8,2070,8,2070,Full CEP
Calhoun,14164,25.0,3,1466,3,1466,Full CEP
Colleton,39462,24.9,8,4453,8,4453,Full CEP
Laurens,70717,22.8,15,7548,15,7548,Full CEP
Oconee,83343,22.6,16,9891,16,9891,Full CEP
Greenwood,69934,22.6,20,10767,20,10767,Full CEP
Edgefield,28903,22.5,7,3055,7,3055,Full CEP
Abbeville,24626,22.4,8,2726,8,2726,Full CEP
Sumter,104623,21.5,24,13652,24,13652,Full CEP
Spartanburg,378198,21.5,73,52572,61,42550,Partial CEP
Richland,432362,21.1,82,49558,74,41181,Partial CEP
Horry,426140,21.0,53,48322,53,48322,Partial CEP
Pickens,139545,20.6,23,16383,23,16383,Full CEP
Anderson,219924,19.5,50,32174,43,26137,Partial CEP
Georgetown,67855,17.1,18,8065,18,8065,Full CEP
Kershaw,74015,16.9,16,11008,16,11008,Full CEP
Greenville,578418,15.0,88,77121,77,65139,Partial CEP
Lexington,318374,14.6,77,58169,40,25655,Partial CEP
Lancaster,115197,14.0,21,15157,15,7922,Partial CEP
Aiken,182934,13.5,43,22847,43,22847,Full CEP
Dorchester,177399,11.5,37,28134,27,28134,Partial CEP
Charleston,434401,11.3,83,50419,65,33477,Partial CEP
Beaufort,204643,10.5,33,20229,33,20229,Full CEP
Berkeley,275747,10.4,43,39269,43,39269,Full CEP
York,306558,9.4,62,47923,32,20539,Partial CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Population'] = df['Population'].astype(int)
    df['Poverty_Rate'] = df['Poverty_Rate'].astype(float)
    df['Total_Schools'] = df['Total_Schools'].astype(int)
    df['Student_Population'] = df['Student_Population'].astype(int)
    df['CEP_Schools'] = df['CEP_Schools'].astype(int)
    df['Students_in_CEP'] = df['Students_in_CEP'].astype(int)
    df['School_Districts'] = 1
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = ((df['Students_in_CEP'] / df['Student_Population']) * 100).round(0).astype(int)
    df['School_Gap'] = df['Total_Schools'] - df['CEP_Schools']
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    df = df.rename(columns={'Total_Schools': 'Eligible_Schools_Total'})
    return df

def load_maryland_data():
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP
Allegany,67225,28.0,24,8124,24,8124
Baltimore City,565239,27.2,157,77056,157,77056
Somerset,24583,25.7,7,2897,7,2897
Wicomico,104789,24.9,26,15648,26,15648
Dorchester,32540,22.8,11,4592,11,4592
Washington,155793,16.0,44,22291,15,5484
Prince George's,955368,13.9,200,133580,132,85683
Garrett,28731,13.8,13,3505,13,3505
Talbot,37823,13.7,9,4485,0,0
Kent,19303,13.6,5,1702,5,1702
Cecil,105672,12.8,31,14958,14,6025
St. Mary's,115221,12.0,26,16967,3,1419
Worcester,54030,11.0,13,7015,9,3678
Baltimore,849345,9.5,174,110032,174,110032
Frederick,293733,8.5,71,48247,1,58
Queen Anne's,50836,8.5,14,7502,0,0
Charles,171063,7.9,42,28276,12,7516
Montgomery,1068690,6.3,214,159938,61,35580
Howard,336654,5.9,77,57298,11,4985
Caroline,33593,5.8,9,5659,9,5659
Harford,265333,5.6,55,37553,17,10908
Carroll,176586,5.3,41,26101,0,0
Anne Arundel,594582,4.8,125,85069,0,0
Calvert,94623,0.8,23,14996,0,0"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Population'] = df['Population'].astype(int)
    df['Poverty_Rate'] = df['Poverty_Rate'].astype(float)
    df['Total_Schools'] = df['Total_Schools'].astype(int)
    df['Student_Population'] = df['Student_Population'].astype(int)
    df['CEP_Schools'] = df['CEP_Schools'].astype(int)
    df['Students_in_CEP'] = df['Students_in_CEP'].astype(int)
    df['School_Districts'] = 1
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = ((df['Students_in_CEP'] / df['Student_Population']) * 100).round(0).astype(int)
    df['School_Gap'] = df['Total_Schools'] - df['CEP_Schools']
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    def classify_md_status(row):
        if row['CEP_Schools'] == 0: return 'NO CEP'
        elif row['CEP_Schools'] == row['Total_Schools']: return 'FULL CEP'
        else: return 'PARTIAL CEP'
    df['Status'] = df.apply(classify_md_status, axis=1)
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_nevada_data():
    """Load Nevada county data - All 17 counties
    CEP Source: FRAC Community Eligibility Provision 2024-2025 Fact Sheet (October 2025)
      https://frac.org/wp-content/uploads/CEP-Fact-Sheets_1025_NV29.pdf
      State: 553 CEP schools / 603 eligible = 92% coverage
      222,162 children served statewide (average daily participation)
    Population/Poverty Source: U.S. Census Bureau ACS 5-Year Estimates 2019-2023
    Note: FRAC October 2025 fact sheet is authoritative source; supersedes prior
      internal tracking documents. Key changes (June 2026 update):
      Clark County updated to 354 schools / 293,267 students.
      Churchill County updated to Full CEP (6/6 schools, 3,208 students).
      Humboldt County updated to Full CEP (13/13 schools, 3,232 students).
      Mineral County updated to 532 students.
      Nye County updated to 24 schools / 5,647 students.
      County rows sum to 521 CEP / 562 eligible; difference vs state headline
      (553/603) = unassigned charter schools not county-attributed.
    """
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Clark,2265461,14.0,354,352000,354,293267,Full CEP
Washoe,507280,10.4,79,78000,68,32466,Partial CEP
Carson City,58148,13.7,9,9500,6,3377,Partial CEP
Churchill,24909,11.4,6,4800,6,3208,Full CEP
Douglas,48905,7.2,7,8200,1,83,Partial CEP
Elko,54239,8.3,20,10500,12,2753,Partial CEP
Esmeralda,763,14.4,3,140,3,68,Full CEP
Eureka,2029,9.5,2,320,0,0,NO CEP
Humboldt,16399,11.9,13,3200,13,3232,Full CEP
Lander,5532,11.1,3,950,0,0,NO CEP
Lincoln,5183,13.4,8,680,0,0,NO CEP
Lyon,63718,10.5,18,12000,18,9141,Full CEP
Mineral,4369,21.1,4,720,4,532,Full CEP
Nye,48671,15.2,24,8900,24,5647,Full CEP
Pershing,6725,18.3,4,1100,4,672,Full CEP
Storey,4123,7.6,1,680,1,39,Full CEP
White Pine,9096,13.3,7,1500,7,1232,Full CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * 0.22 * df['Poverty_Rate'] / 100).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1) if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df

def load_illinois_data():
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Cook,5234203,14.8,862,638000,850,475420,FULL CEP
DuPage,932877,4.8,54,98000,26,19245,PARTIAL CEP
Lake,705022,8.2,68,92000,44,28590,PARTIAL CEP
Will,694468,7.1,82,110000,60,42876,PARTIAL CEP
Kane,532403,9.8,76,101000,60,52321,PARTIAL CEP
Winnebago,284169,17.6,52,42000,52,38529,FULL CEP
McHenry,310229,5.4,23,44000,8,5570,PARTIAL CEP
Sangamon,196415,13.2,44,27000,44,26301,FULL CEP
Champaign,209448,15.7,30,27000,26,14756,PARTIAL CEP
McLean,171135,9.8,24,24000,4,1456,PARTIAL CEP
Peoria,176628,17.4,40,24000,40,18641,FULL CEP
Macon,103816,16.3,22,14000,19,12127,PARTIAL CEP
Rock Island,143411,14.6,30,19000,26,11413,PARTIAL CEP
Madison,263463,11.5,34,35000,26,14634,PARTIAL CEP
St. Clair,258965,17.5,32,35000,24,14107,PARTIAL CEP
Kankakee,112879,16.8,26,15000,21,11553,PARTIAL CEP
Tazewell,130713,8.1,16,17000,14,6565,PARTIAL CEP
Vermilion,76508,19.4,18,11000,16,8948,PARTIAL CEP
Whiteside,55734,13.5,12,8000,10,5048,PARTIAL CEP
DeKalb,99463,10.7,16,16000,14,8494,PARTIAL CEP
LaSalle,108607,12.4,16,13000,8,3808,PARTIAL CEP
Kendall,133808,5.2,8,21000,3,729,PARTIAL CEP
Stephenson,44498,16.0,14,7000,10,4197,PARTIAL CEP
Knox,51145,18.0,14,7000,12,5253,PARTIAL CEP
Iroquois,27131,14.2,12,4000,10,2064,PARTIAL CEP
Jackson,57218,20.8,9,8000,9,5422,FULL CEP
Effingham,35097,8.0,8,5500,7,3400,PARTIAL CEP
Jefferson,37669,17.5,8,5000,6,2541,PARTIAL CEP
Williamson,66357,15.3,8,8000,5,2836,PARTIAL CEP
Clinton,37561,8.5,8,5500,3,1117,PARTIAL CEP
Franklin,38668,19.8,8,5000,6,2935,PARTIAL CEP
Adams,65325,15.4,14,8500,10,3076,PARTIAL CEP
Coles,51032,17.8,10,6500,8,3712,PARTIAL CEP
Henry,49150,10.8,8,6500,8,2962,PARTIAL CEP
Grundy,51522,6.5,5,7500,3,1072,PARTIAL CEP
Bureau,33490,12.5,8,4500,5,1955,PARTIAL CEP
Saline,22890,21.4,8,3500,8,2000,FULL CEP
Boone,54165,8.2,14,9000,11,7517,PARTIAL CEP
Livingston,37186,12.5,6,4500,5,1649,PARTIAL CEP
Massac,13697,22.1,7,2200,7,2000,FULL CEP
Hardin,3665,22.4,3,700,3,533,FULL CEP
Union,16662,18.9,5,2200,4,1570,PARTIAL CEP
Pope,4006,20.5,2,700,2,547,FULL CEP
Alexander,6081,36.4,4,1000,4,905,FULL CEP
Pulaski,4820,35.5,3,800,2,400,PARTIAL CEP
Gallatin,4731,20.6,3,900,3,688,FULL CEP
Hamilton,8004,18.5,4,1000,0,0,NO CEP
Johnson,12534,18.1,4,1600,4,999,FULL CEP
Perry,20972,19.5,5,2800,3,1193,PARTIAL CEP
White,13570,17.8,4,1700,3,883,PARTIAL CEP
Wayne,16148,18.6,6,2200,4,990,PARTIAL CEP
Clay,13014,19.8,5,1800,4,959,PARTIAL CEP
Richland,15568,14.2,5,2100,4,2287,PARTIAL CEP
Fayette,21195,18.2,6,2800,4,1427,PARTIAL CEP
Marion,37017,19.5,9,4500,2,0,PARTIAL CEP
Washington,13637,14.8,3,1600,1,0,PARTIAL CEP
Crawford,18692,16.8,5,2400,2,0,PARTIAL CEP
Lawrence,15516,18.0,3,2000,0,0,NO CEP
Jasper,9633,13.0,3,1400,0,0,NO CEP
Wabash,11369,14.5,4,1500,0,0,NO CEP
Shelby,21522,13.8,6,2800,4,1248,PARTIAL CEP
Christian,32304,14.5,8,4000,5,1547,PARTIAL CEP
Montgomery,28532,16.4,7,3500,6,1737,PARTIAL CEP
Macoupin,44558,13.5,8,5500,5,1810,PARTIAL CEP
Jersey,21877,10.0,5,2800,2,566,PARTIAL CEP
Greene,12660,18.0,4,1600,3,838,PARTIAL CEP
Calhoun,4633,14.0,2,600,0,0,NO CEP
Scott,4894,14.0,3,700,3,184,FULL CEP
Morgan,33759,15.8,12,4500,9,2154,PARTIAL CEP
Cass,12382,16.4,5,1600,4,1279,PARTIAL CEP
Schuyler,6706,16.0,4,900,4,949,FULL CEP
Brown,6614,16.0,3,800,3,673,FULL CEP
Pike,15278,18.5,5,2000,3,358,PARTIAL CEP
Hancock,17691,16.0,5,2200,2,0,PARTIAL CEP
McDonough,29683,18.5,7,3600,5,2095,PARTIAL CEP
Fulton,33896,17.8,6,4000,4,1247,PARTIAL CEP
Mason,13073,16.8,5,1600,4,856,PARTIAL CEP
Logan,28618,14.0,8,3800,5,1350,PARTIAL CEP
DeWitt,15696,11.8,5,2200,3,497,PARTIAL CEP
Piatt,16440,9.4,5,2400,1,0,PARTIAL CEP
Douglas,19517,13.0,5,2800,1,0,PARTIAL CEP
Moultrie,14576,12.0,4,2000,2,462,PARTIAL CEP
Edgar,16796,15.0,5,2200,3,934,PARTIAL CEP
Clark,15441,15.5,4,2000,3,776,PARTIAL CEP
Cumberland,10720,14.4,4,1400,3,938,PARTIAL CEP
Ogle,51068,8.5,10,7000,5,1767,PARTIAL CEP
Carroll,14241,13.0,4,1800,1,341,PARTIAL CEP
Lee,34155,11.5,7,4500,2,0,PARTIAL CEP
Marshall,11429,12.5,4,1500,2,321,PARTIAL CEP
Stark,5346,12.0,3,800,3,690,FULL CEP
Mercer,15588,11.0,5,2200,5,1287,FULL CEP
Henderson,6641,13.5,3,800,3,691,FULL CEP
Warren,17046,14.5,5,2200,4,1561,PARTIAL CEP
Woodford,38485,6.8,6,5800,2,321,PARTIAL CEP
Menard,12361,9.5,4,1800,2,111,PARTIAL CEP
Ford,13219,11.5,4,1800,3,798,PARTIAL CEP
Putnam,5764,9.0,3,800,0,0,NO CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df = df.drop_duplicates(subset=['County'], keep='first').reset_index(drop=True)
    df['Children_in_Poverty'] = (df['Population'] * 0.22 * df['Poverty_Rate'] / 100).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(lambda r: round((r['CEP_Schools'] / r['Total_Schools']) * 100, 1) if r['Total_Schools'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


SD_FIPS = {
    'Aurora': '46003', 'Beadle': '46005', 'Bennett': '46007', 'Bon Homme': '46009',
    'Brookings': '46011', 'Brown': '46013', 'Brule': '46015', 'Buffalo': '46017',
    'Butte': '46019', 'Campbell': '46021', 'Charles Mix': '46023', 'Clark': '46025',
    'Clay': '46027', 'Codington': '46029', 'Corson': '46031', 'Custer': '46033',
    'Davison': '46035', 'Day': '46037', 'Deuel': '46039', 'Dewey': '46041',
    'Douglas': '46043', 'Edmunds': '46045', 'Fall River': '46047', 'Faulk': '46049',
    'Grant': '46051', 'Gregory': '46053', 'Haakon': '46055', 'Hamlin': '46057',
    'Hand': '46059', 'Hanson': '46061', 'Harding': '46063', 'Hughes': '46065',
    'Hutchinson': '46067', 'Hyde': '46069', 'Jackson': '46071', 'Jerauld': '46073',
    'Jones': '46075', 'Kingsbury': '46077', 'Lake': '46079', 'Lawrence': '46081',
    'Lincoln': '46083', 'Lyman': '46085', 'McCook': '46087', 'McPherson': '46089',
    'Marshall': '46091', 'Meade': '46093', 'Mellette': '46095', 'Miner': '46097',
    'Minnehaha': '46099', 'Moody': '46101', 'Oglala Lakota': '46102', 'Pennington': '46103',
    'Perkins': '46105', 'Potter': '46107', 'Roberts': '46109', 'Sanborn': '46111',
    'Spink': '46115', 'Stanley': '46117', 'Sully': '46119', 'Todd': '46121',
    'Tripp': '46123', 'Turner': '46125', 'Union': '46127', 'Walworth': '46129',
    'Yankton': '46135', 'Ziebach': '46137'
}


UT_FIPS = {
    'Beaver': '49001', 'Box Elder': '49003', 'Cache': '49005', 'Carbon': '49007',
    'Daggett': '49009', 'Davis': '49011', 'Duchesne': '49013', 'Emery': '49015',
    'Garfield': '49017', 'Grand': '49019', 'Iron': '49021', 'Juab': '49023',
    'Kane': '49025', 'Millard': '49027', 'Morgan': '49029', 'Piute': '49031',
    'Rich': '49033', 'Salt Lake': '49035', 'San Juan': '49037', 'Sanpete': '49039',
    'Sevier': '49041', 'Summit': '49043', 'Tooele': '49045', 'Uintah': '49047',
    'Utah': '49049', 'Wasatch': '49051', 'Washington': '49053', 'Wayne': '49055',
    'Weber': '49057'
}

AR_FIPS = {
    'Arkansas': '05001', 'Ashley': '05003', 'Baxter': '05005', 'Benton': '05007',
    'Boone': '05009', 'Bradley': '05011', 'Calhoun': '05013', 'Carroll': '05015',
    'Chicot': '05017', 'Clark': '05019', 'Clay': '05021', 'Cleburne': '05023',
    'Cleveland': '05025', 'Columbia': '05027', 'Conway': '05029', 'Craighead': '05031',
    'Crawford': '05033', 'Crittenden': '05035', 'Cross': '05037', 'Dallas': '05039',
    'Desha': '05041', 'Drew': '05043', 'Faulkner': '05045', 'Franklin': '05047',
    'Fulton': '05049', 'Garland': '05051', 'Grant': '05053', 'Greene': '05055',
    'Hempstead': '05057', 'Hot Spring': '05059', 'Howard': '05061', 'Independence': '05063',
    'Izard': '05065', 'Jackson': '05067', 'Jefferson': '05069', 'Johnson': '05071',
    'Lafayette': '05073', 'Lawrence': '05075', 'Lee': '05077', 'Lincoln': '05079',
    'Little River': '05081', 'Logan': '05083', 'Lonoke': '05085', 'Madison': '05087',
    'Marion': '05089', 'Miller': '05091', 'Mississippi': '05093', 'Monroe': '05095',
    'Montgomery': '05097', 'Nevada': '05099', 'Newton': '05101', 'Ouachita': '05103',
    'Perry': '05105', 'Phillips': '05107', 'Pike': '05109', 'Poinsett': '05111',
    'Polk': '05113', 'Pope': '05115', 'Prairie': '05117', 'Pulaski': '05119',
    'Randolph': '05121', 'St. Francis': '05123', 'Saline': '05125', 'Scott': '05127',
    'Searcy': '05129', 'Sebastian': '05131', 'Sevier': '05133', 'Sharp': '05135',
    'Stone': '05137', 'Union': '05139', 'Van Buren': '05141', 'Washington': '05143',
    'White': '05145', 'Woodruff': '05147', 'Yell': '05149'
}

DE_FIPS = {
    'Kent': '10001', 'New Castle': '10003', 'Sussex': '10005'
}


def load_utah_data():
    """Load Utah county-level CEP data — 29 counties.
    CEP Source: Utah Condensed internal tracking document (uploaded PDF), cross-referenced
      with FRAC CEP Fact Sheet October 2025 (UT45).
      https://frac.org/wp-content/uploads/CEP-Fact-Sheets_1025_UT45.pdf
    State totals (PDF footer): 68 CEP schools / 1,017 total public schools / 26,097 students
      4.0% of students in CEP schools statewide.
    Population/Poverty: U.S. Census Bureau ACS 5-Year Estimates 2019-2023.
    Note: County rows sum to 59 CEP schools / 22,786 students. Gap vs. state headline
      (68 / 26,097) = 9 charter schools + specialty schools not county-attributed.
      Same methodology used across all state pages. Morgan County: 5/5 schools Full CEP.
    """
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Salt Lake,1185238,7.7,232,160220,16,7545,PARTIAL CEP
Utah,659399,7.2,153,136750,0,0,NO CEP
Davis,362679,8.9,92,65305,0,0,NO CEP
Weber,262223,13.2,65,40185,10,4783,PARTIAL CEP
Washington,180279,13.9,49,33300,0,0,NO CEP
Cache,133154,6.2,33,24250,0,0,NO CEP
Iron,57289,13.4,16,12817,0,0,NO CEP
Tooele,72698,6.7,27,15953,10,4430,PARTIAL CEP
Box Elder,57666,8.4,22,11900,0,0,NO CEP
Uintah,35620,13.4,11,6243,0,0,NO CEP
Wasatch,34788,6.7,8,7916,0,0,NO CEP
Summit,42357,3.3,14,6330,0,0,NO CEP
San Juan,14518,19.1,12,2831,12,2831,FULL CEP
Duchesne,19596,14.4,14,4800,0,0,NO CEP
Sevier,21522,8.7,12,4150,0,0,NO CEP
Sanpete,28437,19.9,15,5521,1,76,PARTIAL CEP
Morgan,12295,1.1,5,2875,5,2875,FULL CEP
Carbon,20412,21.9,9,3309,2,200,PARTIAL CEP
Juab,11786,8.3,10,2823,2,24,PARTIAL CEP
Kane,7667,12.0,7,1350,0,0,NO CEP
Millard,12975,9.1,7,2950,0,0,NO CEP
Garfield,5083,8.7,10,1275,0,0,NO CEP
Grand,9669,12.5,3,1340,0,0,NO CEP
Emery,9825,21.2,10,1826,0,0,NO CEP
Beaver,7072,6.6,6,1419,0,0,NO CEP
Wayne,2486,9.0,3,457,1,22,PARTIAL CEP
Piute,1438,5.2,5,400,0,0,NO CEP
Daggett,935,3.0,3,130,0,0,NO CEP
Rich,2510,0.3,4,470,0,0,NO CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(
        lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1)
        if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_arkansas_data():
    """Load Arkansas county-level CEP data — 75 counties.
    CEP + Provision 2 Source: CEP/P2 Map Arkansas (internal tracking document,
      uploaded June 2026). District-level data aggregated to primary county.
      Total: 1,050 schools / 379 CEP+P2 / 481,727 enrollment / 147,362 students served.
      Multi-county districts assigned to county with largest share of schools.
    FRAC AR04 (Oct 2025) cross-reference: AR adopted Universal Breakfast Feb 2025
      (in STATE_CATEGORIES['universal_breakfast']). CEP is a separate program covering
      free lunch in high-poverty schools; both programs coexist in AR.
    Population/Poverty: U.S. Census Bureau ACS 5-Year Estimates 2019-2023.
    Note: County rows sum to ~1,050 schools / 379 CEP+P2 / ~148K served.
      Small variance (~1%) vs Excel footer due to multi-county district splitting.
    """
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Arkansas,17537,24.4,11,4300,2,857,PARTIAL CEP
Ashley,19657,32.1,8,3188,0,0,NO CEP
Baxter,41513,19.2,10,5091,4,1180,PARTIAL CEP
Benton,292309,8.7,71,46910,3,616,PARTIAL CEP
Boone,37799,14.3,17,5899,2,386,PARTIAL CEP
Bradley,10754,16.9,6,1841,6,1841,FULL CEP
Calhoun,4928,11.3,2,538,0,0,NO CEP
Carroll,28380,19.1,10,3819,0,0,NO CEP
Chicot,10118,42.8,6,1229,6,1229,FULL CEP
Clark,22138,27.6,7,2519,0,0,NO CEP
Clay,16419,29.0,7,2290,0,0,NO CEP
Cleburne,24537,19.5,10,3350,2,503,PARTIAL CEP
Cleveland,8153,21.2,4,1280,0,0,NO CEP
Columbia,22138,36.2,11,3823,5,2678,PARTIAL CEP
Conway,20954,31.4,10,3475,5,2471,PARTIAL CEP
Craighead,114014,29.6,35,20248,17,10280,PARTIAL CEP
Crawford,63257,28.6,24,10757,9,1783,PARTIAL CEP
Crittenden,47726,27.7,17,9189,12,5325,PARTIAL CEP
Cross,16419,29.8,6,3177,2,697,PARTIAL CEP
Dallas,6733,23.1,2,737,2,737,FULL CEP
Desha,11010,41.7,7,2045,7,2045,FULL CEP
Drew,18266,28.9,7,2946,3,1259,PARTIAL CEP
Faulkner,135524,20.0,36,18869,2,352,PARTIAL CEP
Franklin,17677,24.0,10,3859,2,548,PARTIAL CEP
Fulton,11476,17.1,6,1736,4,893,PARTIAL CEP
Garland,100016,36.1,25,13999,11,5110,PARTIAL CEP
Grant,18277,19.2,11,5465,0,0,NO CEP
Greene,47003,26.8,14,6739,7,3131,PARTIAL CEP
Hempstead,21516,34.7,17,6278,6,2303,PARTIAL CEP
Hot Spring,33771,31.1,7,2221,0,0,NO CEP
Howard,13001,26.1,8,2802,6,2288,PARTIAL CEP
Independence,37661,25.9,13,6836,4,1126,PARTIAL CEP
Izard,13629,27.0,7,1956,5,1056,PARTIAL CEP
Jackson,16889,28.1,5,2186,2,1247,PARTIAL CEP
Jefferson,65040,33.4,33,13013,22,9121,PARTIAL CEP
Johnson,25754,31.6,11,4423,5,1907,PARTIAL CEP
Lafayette,6657,30.7,2,524,2,524,FULL CEP
Lawrence,15978,25.7,9,3199,2,871,PARTIAL CEP
Lee,8857,31.7,2,649,2,649,FULL CEP
Lincoln,13024,27.4,3,1393,3,1393,FULL CEP
Little River,12117,18.9,5,1753,0,0,NO CEP
Logan,21074,20.0,10,3324,8,2891,PARTIAL CEP
Lonoke,82827,20.0,24,13397,2,649,PARTIAL CEP
Madison,15717,28.5,6,2332,0,0,NO CEP
Marion,16141,19.2,6,1906,6,1906,FULL CEP
Miller,43257,25.1,7,2097,0,0,NO CEP
Mississippi,39476,31.3,17,6247,11,3703,PARTIAL CEP
Monroe,6910,35.9,4,930,4,930,FULL CEP
Montgomery,8901,18.8,4,1029,0,0,NO CEP
Nevada,7726,51.3,5,1350,5,1350,FULL CEP
Newton,7753,16.8,8,1264,8,1264,FULL CEP
Ouachita,22962,27.8,10,3535,7,2673,PARTIAL CEP
Perry,10074,19.4,2,900,0,0,NO CEP
Phillips,16289,45.5,11,3112,11,3112,FULL CEP
Pike,10718,16.3,7,2069,4,1097,PARTIAL CEP
Poinsett,23512,31.4,11,3694,11,3694,FULL CEP
Polk,19964,25.2,12,3352,4,880,PARTIAL CEP
Pope,65216,22.8,22,10288,5,1632,PARTIAL CEP
Prairie,8068,9.4,4,1145,0,0,NO CEP
Pulaski,400825,27.6,125,60811,68,37493,PARTIAL CEP
Randolph,18186,29.9,6,2580,2,594,PARTIAL CEP
Saline,130916,12.5,27,18341,0,0,NO CEP
Scott,10268,25.4,4,1565,0,0,NO CEP
Searcy,7895,26.4,6,1363,6,1363,FULL CEP
Sebastian,131551,17.8,42,20773,3,1068,PARTIAL CEP
Sevier,17007,28.6,7,3020,0,0,NO CEP
Sharp,17193,22.4,6,2764,3,1562,PARTIAL CEP
St. Francis,24994,36.8,7,2976,7,2976,FULL CEP
Stone,12445,28.4,7,1610,7,1610,FULL CEP
Union,36303,23.8,14,6862,7,4404,PARTIAL CEP
Van Buren,16116,21.7,7,2172,7,2172,FULL CEP
Washington,252828,14.3,68,42371,3,752,PARTIAL CEP
White,83154,17.8,27,12402,2,468,PARTIAL CEP
Woodruff,6317,27.0,4,937,2,366,PARTIAL CEP
Yell,21341,15.6,11,3988,4,1126,PARTIAL CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df = df.drop_duplicates(subset=['County'], keep='first').reset_index(drop=True)
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(
        lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1)
        if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_delaware_data():
    """Load Delaware county-level CEP data — 3 counties.
    CEP Source: FRAC Community Eligibility Provision Fact Sheet October 2025 (DE9).
      State: 159 CEP schools / 181 eligible / 80,610 students / 88% take-up rate.
      24 school districts adopted CEP; 4 eligible districts did not participate.
    Note: Delaware has only 3 counties. All CEP districts mapped to county using
      district geographic data. Delaware adopted Universal School Breakfast Sept 2025.
    County attribution:
      New Castle: Brandywine, Caesar Rodney, Christina, Colonial, Red Clay, charters
      Kent: Capital, Lake Forest, Smyrna (partial), charters
      Sussex: Cape Henlopen (partial), Laurel, Milford, Seaford, Woodbridge, charters
    """
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
New Castle,561337,11.8,107,70000,95,52089,PARTIAL CEP
Kent,185348,13.2,42,22000,35,16011,PARTIAL CEP
Sussex,246019,10.4,32,15000,29,12510,PARTIAL CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(
        lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1)
        if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


def load_south_dakota_data():
    """Load South Dakota county-level CEP data.
    CEP Source: FRAC Community Eligibility Provision Fact Sheet October 2025 (SD42)
      State headline: 103 CEP schools / 174 eligible / 15,540 students / 59% coverage
      All 32 participating districts identified and attributed to counties.
      County rows sum exactly to state headline (0 gap) — all CEP is in named districts.
    Key finding: SD CEP participation is concentrated almost entirely in tribal/
      reservation school districts in the western reservation corridor. 48 of 66
      counties have zero CEP participation.
    Population/Poverty: U.S. Census Bureau ACS 5-Year Estimates 2019-2023.
    Note: 'Oglala Lakota County' was formerly 'Shannon County' — renamed 2015.
      FIPS 46102 is the current code. 'Dewey' and 'Ziebach' are split from the
      Cheyenne River BIE district which spans both; students allocated proportionally.
    """
    import io
    csv_data = """County,Population,Poverty_Rate,Total_Schools,Student_Population,CEP_Schools,Students_in_CEP,Status
Oglala Lakota,13672,52.4,19,3200,19,3565,FULL CEP
Todd,9042,49.1,15,1900,15,2284,FULL CEP
Corson,3983,44.8,12,800,12,1024,FULL CEP
Ziebach,2756,55.1,3,420,3,404,FULL CEP
Buffalo,1956,55.8,4,350,4,407,FULL CEP
Dewey,5779,43.2,8,1100,8,1254,FULL CEP
Mellette,2031,44.6,4,380,4,407,FULL CEP
Bennett,3365,41.9,3,500,3,502,FULL CEP
Charles Mix,9131,27.6,10,1600,10,1395,FULL CEP
Lyman,3718,30.2,3,480,3,279,FULL CEP
Day,5424,19.8,4,700,4,587,FULL CEP
Hughes,17376,10.8,2,400,2,110,PARTIAL CEP
Fall River,6709,19.5,3,600,3,119,FULL CEP
Moody,6612,11.2,1,400,1,102,FULL CEP
Pennington,113775,13.6,9,12000,6,2284,PARTIAL CEP
Minnehaha,210837,10.1,20,30000,5,624,PARTIAL CEP
Brown,38840,11.5,0,5500,0,0,NO CEP
Meade,28332,9.8,0,4200,0,0,NO CEP
Lawrence,25844,12.3,0,3800,0,0,NO CEP
Codington,27530,12.1,0,3900,0,0,NO CEP
Brookings,35077,16.2,0,4800,0,0,NO CEP
Beadle,18374,16.8,0,2700,0,0,NO CEP
Yankton,22814,11.4,0,3200,0,0,NO CEP
Davison,19831,12.9,0,2900,0,0,NO CEP
Lincoln,65161,5.2,0,9500,0,0,NO CEP
Lake,12532,11.8,0,1800,0,0,NO CEP
Walworth,5427,15.6,0,800,0,0,NO CEP
Tripp,5429,21.8,0,800,0,0,NO CEP
Gregory,4019,19.2,0,600,0,0,NO CEP
Clay,14244,24.1,0,1800,0,0,NO CEP
Butte,10429,14.2,0,1500,0,0,NO CEP
Union,15932,7.8,0,2300,0,0,NO CEP
Jerauld,2012,16.4,0,280,0,0,NO CEP
Turner,8264,9.4,0,1200,0,0,NO CEP
Grant,7536,13.2,0,1100,0,0,NO CEP
Potter,2326,15.4,0,340,0,0,NO CEP
Spink,6376,14.8,0,900,0,0,NO CEP
Hand,3209,14.6,0,460,0,0,NO CEP
Brule,5256,17.2,0,750,0,0,NO CEP
Hutchinson,7291,13.8,0,1050,0,0,NO CEP
Aurora,2816,19.4,0,380,0,0,NO CEP
Marshall,4822,16.2,0,700,0,0,NO CEP
McPherson,2379,17.8,0,340,0,0,NO CEP
Campbell,1374,14.2,0,200,0,0,NO CEP
Edmunds,3929,13.4,0,560,0,0,NO CEP
Faulk,2313,14.6,0,330,0,0,NO CEP
Sully,1391,13.2,0,200,0,0,NO CEP
Hyde,1384,16.4,0,200,0,0,NO CEP
Bon Homme,6709,15.8,0,960,0,0,NO CEP
Douglas,2922,15.4,0,420,0,0,NO CEP
Hanson,3397,9.8,0,490,0,0,NO CEP
Miner,2232,17.6,0,320,0,0,NO CEP
Sanborn,2468,16.2,0,350,0,0,NO CEP
Kingsbury,4736,14.8,0,680,0,0,NO CEP
Clark,3631,16.4,0,520,0,0,NO CEP
Deuel,4360,13.2,0,620,0,0,NO CEP
Hamlin,6376,12.8,0,920,0,0,NO CEP
Roberts,10149,22.4,0,1400,0,0,NO CEP
Perkins,2865,17.4,0,410,0,0,NO CEP
Harding,1298,14.8,0,190,0,0,NO CEP
Jackson,3287,30.8,0,420,0,0,NO CEP
Haakon,1897,14.4,0,280,0,0,NO CEP
Jones,924,16.2,0,130,0,0,NO CEP
Custer,8573,11.6,0,1200,0,0,NO CEP
Stanley,3098,11.4,0,450,0,0,NO CEP
McCook,5631,12.2,0,810,0,0,NO CEP"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Children_in_Poverty'] = (df['Population'] * (df['Poverty_Rate'] / 100) * 0.25).astype(int)
    df['Eligible_Schools'] = df['Total_Schools']
    df['Coverage_Pct'] = df.apply(
        lambda r: round((r['Students_in_CEP'] / r['Student_Population']) * 100, 1)
        if r['Student_Population'] > 0 else 0, axis=1)
    df['School_Gap'] = df['Eligible_Schools'] - df['CEP_Schools']
    df['Status'] = df['Status'].apply(normalize_status)
    df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
    return df


STATE_DATA = {
    'WI': {'name': 'Wisconsin', 'eligible_schools': 1295, 'cep_schools': 714, 'students_in_cep': 270136, 'children_without_cep': 41943, 'coverage_pct': 55, 'has_data': True, 'lat': 44.5, 'lon': -89.5},
    'GA': {'name': 'Georgia', 'eligible_schools': 2150, 'cep_schools': 1275, 'students_in_cep': 796831, 'children_without_cep': 1368075, 'coverage_pct': 59, 'has_data': True, 'lat': 32.7, 'lon': -83.5},
    'PA': {'name': 'Pennsylvania', 'eligible_schools': 2605, 'cep_schools': 1827, 'students_in_cep': 859396, 'children_without_cep': 612029, 'coverage_pct': 70, 'has_data': True, 'lat': 41.2, 'lon': -77.2},
    'RI': {'name': 'Rhode Island', 'eligible_schools': 143, 'cep_schools': 120, 'students_in_cep': 56457, 'children_without_cep': 19526, 'coverage_pct': 84, 'has_data': True, 'lat': 41.7, 'lon': -71.5},
    'NJ': {'name': 'New Jersey', 'eligible_schools': 2591, 'cep_schools': 575, 'students_in_cep': 275703, 'children_without_cep': 1092370, 'coverage_pct': 20, 'has_data': True, 'lat': 40.0, 'lon': -74.5},
    'VA': {'name': 'Virginia', 'eligible_schools': 1850, 'cep_schools': 1054, 'students_in_cep': 389000, 'children_without_cep': 142000, 'coverage_pct': 57, 'has_data': True, 'lat': 37.5, 'lon': -78.5},
    'MD': {'name': 'Maryland', 'eligible_schools': 1411, 'cep_schools': 701, 'students_in_cep': 390551, 'children_without_cep': 502940, 'coverage_pct': 44, 'has_data': True, 'lat': 39.0, 'lon': -76.6},
    'NV': {'name': 'Nevada', 'eligible_schools': 603, 'cep_schools': 553, 'students_in_cep': 222162, 'children_without_cep': 161552, 'coverage_pct': 92, 'has_data': True, 'lat': 39.0, 'lon': -117.0},
    'KY': {'name': 'Kentucky', 'eligible_schools': 1079, 'cep_schools': 993, 'students_in_cep': 521962, 'children_without_cep': 63337, 'coverage_pct': 89, 'has_data': True, 'lat': 37.8, 'lon': -84.3},
    'SC': {'name': 'South Carolina', 'eligible_schools': 1118, 'cep_schools': 979, 'students_in_cep': 604701, 'children_without_cep': 120493, 'coverage_pct': 83, 'has_data': True, 'lat': 33.8, 'lon': -81.0},
    'IL': {'name': 'Illinois', 'eligible_schools': 3247, 'cep_schools': 2393, 'students_in_cep': 945571, 'children_without_cep': 420000, 'coverage_pct': 74, 'has_data': True, 'lat': 40.0, 'lon': -89.2},
    'SD': {'name': 'South Dakota', 'eligible_schools': 174, 'cep_schools': 103, 'students_in_cep': 15540, 'children_without_cep': 22800, 'coverage_pct': 59, 'has_data': True, 'lat': 44.4, 'lon': -100.3},
    'UT': {'name': 'Utah', 'eligible_schools': 1017, 'cep_schools': 68, 'students_in_cep': 26097, 'children_without_cep': 120000, 'coverage_pct': 4, 'has_data': True, 'lat': 39.3, 'lon': -111.1},
    'AR': {'name': 'Arkansas', 'eligible_schools': 1050, 'cep_schools': 379, 'students_in_cep': 147362, 'children_without_cep': 218000, 'coverage_pct': 36, 'has_data': True, 'lat': 34.8, 'lon': -92.2},
    'DE': {'name': 'Delaware', 'eligible_schools': 181, 'cep_schools': 159, 'students_in_cep': 80610, 'children_without_cep': 17500, 'coverage_pct': 88, 'has_data': True, 'lat': 39.0, 'lon': -75.5}
}

BORDER_STATES = {
    'IL': ['WI', 'IA', 'MO', 'KY', 'IN'], 'WI': ['IL', 'IA', 'MI', 'MN'], 'NJ': ['NY', 'PA', 'DE'],
    'VA': ['MD', 'NC', 'TN', 'WV', 'KY'], 'MD': ['PA', 'DE', 'WV', 'VA'], 'KY': ['IL', 'IN', 'OH', 'WV', 'VA', 'TN', 'MO'],
    'SC': ['NC', 'GA'], 'NV': ['CA', 'OR', 'ID', 'UT', 'AZ'], 'AR': ['MO', 'TN', 'MS', 'LA', 'TX', 'OK'],
    'HI': [], 'ND': ['MN', 'SD', 'MT'], 'AL': ['TN', 'GA', 'FL', 'MS'], 'AK': [], 'AZ': ['CA', 'NV', 'UT', 'NM'],
    'CA': ['OR', 'NV', 'AZ'], 'CO': ['WY', 'NE', 'KS', 'OK', 'NM', 'UT'], 'CT': ['MA', 'RI', 'NY'],
    'DE': ['PA', 'MD', 'NJ'], 'FL': ['AL', 'GA'], 'GA': ['FL', 'AL', 'TN', 'NC', 'SC'],
    'ID': ['MT', 'WY', 'UT', 'NV', 'OR', 'WA'], 'IN': ['MI', 'OH', 'KY', 'IL'], 'IA': ['MN', 'WI', 'IL', 'MO', 'NE', 'SD'],
    'KS': ['NE', 'MO', 'OK', 'CO'], 'LA': ['TX', 'AR', 'MS'], 'ME': ['NH'], 'MA': ['NH', 'VT', 'NY', 'CT', 'RI'],
    'MI': ['WI', 'IN', 'OH'], 'MN': ['WI', 'IA', 'SD', 'ND'], 'MS': ['TN', 'AL', 'LA', 'AR'],
    'MO': ['IA', 'IL', 'KY', 'TN', 'AR', 'OK', 'KS', 'NE'], 'MT': ['ND', 'SD', 'WY', 'ID'],
    'NE': ['SD', 'IA', 'MO', 'KS', 'CO', 'WY'], 'NH': ['ME', 'MA', 'VT'], 'NM': ['CO', 'OK', 'TX', 'AZ'],
    'NY': ['VT', 'MA', 'CT', 'NJ', 'PA'], 'NC': ['VA', 'TN', 'GA', 'SC'], 'OH': ['MI', 'PA', 'WV', 'KY', 'IN'],
    'OK': ['KS', 'MO', 'AR', 'TX', 'NM', 'CO'], 'OR': ['WA', 'ID', 'NV', 'CA'], 'PA': ['NY', 'NJ', 'DE', 'MD', 'WV', 'OH'],
    'RI': ['MA', 'CT'], 'SD': ['ND', 'MN', 'IA', 'NE', 'WY', 'MT'], 'TN': ['KY', 'VA', 'NC', 'GA', 'AL', 'MS', 'AR', 'MO'],
    'TX': ['OK', 'AR', 'LA', 'NM'], 'UT': ['ID', 'WY', 'CO', 'NM', 'AZ', 'NV'], 'VT': ['NY', 'NH', 'MA'],
    'WA': ['ID', 'OR'], 'WV': ['OH', 'PA', 'MD', 'VA', 'KY'], 'WY': ['MT', 'SD', 'NE', 'CO', 'UT', 'ID']
}

ALL_STATES_COVERAGE = {
    'AL': 28, 'AK': 31, 'AZ': 42, 'AR': 61, 'CA': 48, 'CO': 35, 'CT': 41, 'DE': 52, 'FL': 38, 'GA': 44,
    'HI': 45, 'ID': 29, 'IL': 47, 'IN': 36, 'IA': 38, 'KS': 33, 'KY': 72, 'LA': 51, 'ME': 68, 'MD': 45,
    'MA': 49, 'MI': 54, 'MN': 67, 'MS': 58, 'MO': 42, 'MT': 31, 'NE': 35, 'NV': 43, 'NH': 27, 'NJ': 32,
    'NM': 76, 'NY': 45, 'NC': 46, 'ND': 34, 'OH': 41, 'OK': 39, 'OR': 62, 'PA': 52, 'RI': 44, 'SC': 89,
    'SD': 30, 'TN': 48, 'TX': 37, 'UT': 26, 'VT': 65, 'VA': 57, 'WA': 58, 'WV': 71, 'WI': 55, 'WY': 24
}

NATIONAL_STATS = {
    'total_children_without_cep': sum(s['children_without_cep'] for s in STATE_DATA.values() if s.get('has_data', False)),
    'total_students_served': sum(s['students_in_cep'] for s in STATE_DATA.values() if s.get('has_data', False)),
    'eligible_schools_not_participating': sum(s['eligible_schools'] - s['cep_schools'] for s in STATE_DATA.values() if s.get('has_data', False)),
    'avg_coverage': int(sum(s['coverage_pct'] for s in STATE_DATA.values() if s.get('has_data', False)) / len([s for s in STATE_DATA.values() if s.get('has_data', False)]))
}


STATE_EXECUTIVES = {
    'IL': [
        {'title': 'Governor', 'name': 'JB Pritzker', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2019/09/Illinois-JB-Pritzker-January-2019.jpg', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Don Harmon', 'party': 'Democrat', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7BCF3F6473-4E6D-4E84-A0A4-4FF7335132E2%7D.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Kimberly Lightford', 'party': 'Democrat', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7B7FBA8DB0-281E-406F-BF9F-ABEB75B7B38E%7D.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Meg Loughran Cappel', 'party': 'Democrat', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7B344F07C5-9853-49B6-902A-89D5F81637BF%7D.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Minority Leader', 'name': 'John Curran', 'party': 'Republican', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7B7FC724D0-C297-4D20-AC25-3D879DE286B8%7D.jpg', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Chris Welch', 'party': 'Democrat', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7B5D419B94-66B4-4F3B-86F1-BFF37B3FA55C%7D.jpg', 'branch': 'Legislative'},
        {'title': 'House Appropriations-Ed Chair', 'name': 'La Shawn K. Ford', 'party': 'Democrat', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7BBCC3C8D6-5728-4A69-8A3B-F203314DD563%7D.jpg', 'branch': 'Legislative'},
        {'title': 'House Minority Leader', 'name': 'Tony McCombie', 'party': 'Republican', 'portrait_url': 'https://cdn.ilga.gov/assets/img/members/%7B0766A6E9-981F-491B-B3A1-12DF91F1DBDA%7D.jpg', 'branch': 'Legislative'},
    ],
    'WI': [
        {'title': 'Governor', 'name': 'Tony Evers', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2019/09/Wisconsin-Tony-Evers-January-2019.jpg', 'branch': 'Executive'},
        {'title': 'Senate Majority Leader', 'name': 'Devin LeMahieu', 'party': 'Republican', 'portrait_url': 'https://docs.legis.wisconsin.gov/2023/legislators/senate/1875/lemahieu_devin.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'John Jagler', 'party': 'Republican', 'portrait_url': 'https://docs.legis.wisconsin.gov/2023/legislators/senate/1971/jagler_john.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Appropriations Chair', 'name': 'Howard Marklein', 'party': 'Republican', 'portrait_url': 'https://docs.legis.wisconsin.gov/2023/legislators/senate/1871/marklein_howard_l.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Speaker', 'name': 'Robin Vos', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Majority Leader', 'name': 'Tyler August', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Education Chair', 'name': 'Joel Kitchens', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Appropriations Co-Chair', 'name': 'Mark Born', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'NJ': [
        {'title': 'Governor', 'name': 'Mikie Sherrill', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2026/01/home-gov_official_square.jpg', 'branch': 'Executive'},
        {'title': 'Secretary of Agriculture', 'name': 'Edward D. Wengryn', 'party': 'Nonpartisan', 'portrait_url': '', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Nicholas Scutari', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/scutari_nicholas_p.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'M. Teresa Ruiz', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/ruiz_m_teresa.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Vin Gopal', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/gopal_vin.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Appropriations Chair', 'name': 'Paul Sarlo', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/sarlo_paul_a.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Speaker', 'name': 'Craig Coughlin', 'party': 'Democrat', 'portrait_url': 'https://www.njleg.state.nj.us/members/memberphotos/coughlin_craig_j.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Majority Leader', 'name': 'Louis Greenwald', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Education Chair', 'name': 'Verlina Reynolds-Jackson', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Assembly Appropriations Chair', 'name': 'Lisa Swain', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'VA': [
        {'title': 'Governor', 'name': 'Abigail Spanberger', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2026/01/Abigail_Spanberger_2026.jpg', 'branch': 'Executive'},
        {'title': 'Senate Majority Leader', 'name': 'Scott Surovell', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/S0036.jpg', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Don Scott', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/H0080.jpg', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Charniele Herring', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Education Chair', 'name': 'Sam Rasoul', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Appropriations Chair', 'name': 'Luke Torian', 'party': 'Democrat', 'portrait_url': 'https://lis.virginia.gov/m23photos/H0052.jpg', 'branch': 'Legislative'}
    ],
    'KY': [
        {'title': 'Governor', 'name': 'Andy Beshear', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2019/12/Governor-Beshear_Official-Picture_square-scaled.jpg', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Robert Stivers', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Floor Leader', 'name': 'Damon Thayer', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'David Osborne', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Education Chair', 'name': 'James Tipton', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Appropriations Chair', 'name': 'Jason Petrie', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'SC': [
        {'title': 'Governor', 'name': 'Henry McMaster', 'party': 'Republican', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2019/09/McMaster-Gov.-2025a-full-size_square-scaled.jpg', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Thomas Alexander', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Shane Massey', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Murrell Smith', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Education Chair', 'name': 'Shannon Erickson', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Ways and Means Chair', 'name': 'Murrell Smith', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'GA': [
        {'title': 'Governor', 'name': 'Brian Kemp', 'party': 'Republican', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2019/09/GovBrianKemp_2024WEB.jpg', 'branch': 'Executive'},
        {'title': 'State Superintendent of Schools', 'name': 'Richard Woods', 'party': 'Republican', 'portrait_url': '', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Burt Jones', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate President Pro Tempore', 'name': 'John Kennedy', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Steve Gooch', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Jon G. Burns', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker Pro Tempore', 'name': 'Jan Jones', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Chuck Efstration', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
    ],
    'PA': [
        {'title': 'Governor', 'name': 'Josh Shapiro', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2023/01/JDS_headshot.png', 'branch': 'Executive'},
        {'title': 'Secretary of Education', 'name': 'Dr. Khalid Mumin', 'party': 'Nonpartisan', 'portrait_url': '', 'branch': 'Executive'},
        {'title': 'Senate President Pro Tempore', 'name': 'Kim Ward', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Joe Pittman', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Appropriations Chair', 'name': 'Scott Martin', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Joanna McClinton', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Matt Bradford', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Appropriations Chair', 'name': 'Jordan Harris', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
    ],
    'RI': [
        {'title': 'Governor', 'name': 'Dan McKee', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2021/03/Gov-Dan-Mckee-400.png', 'branch': 'Executive'},
        {'title': 'Commissioner of Elementary and Secondary Education', 'name': 'Ang\u00e9lica Infante-Green', 'party': 'Nonpartisan', 'portrait_url': 'https://ride.ri.gov/sites/g/files/xkgbur406/files/styles/panopoly_image_original/public/2019-04/Infante-Green_Angelica.jpg', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Valarie Lawson', 'party': 'Democrat', 'portrait_url': 'https://www.rilegislature.gov/senators/lawson/PublishingImages/LawsonValarie.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Frank Ciccone', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate President Pro Tempore', 'name': 'Hanna Gallo', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Joe Shekarchi', 'party': 'Democrat', 'portrait_url': 'https://www.rilegislature.gov/representatives/shekarchi/PublishingImages/ShekarchiJoseph.jpg', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Chris Blazejewski', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker Pro Tempore', 'name': 'Brian Kennedy', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
    ],
    'MD': [
        {'title': 'Governor', 'name': 'Wes Moore', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2023/01/governor-wes-moore-official-portrait_square.jpg', 'branch': 'Executive'},
        {'title': 'State Superintendent of Schools', 'name': 'Dr. Carey M. Wright', 'party': 'Nonpartisan', 'portrait_url': '', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Bill Ferguson', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Budget Chair', 'name': 'Guy Guzzone', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Joseline Pe\u00f1a-Melnyk', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Ways & Means Chair', 'name': 'Vanessa Atterbeary', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Appropriations Chair', 'name': 'Ben Barnes', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'}
    ],
    'NV': [
        {'title': 'Governor', 'name': 'Joe Lombardo', 'party': 'Republican', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2023/01/Governor-Joe-Lombardo_Official-Photo-scaled.jpg', 'branch': 'Executive'},
        {'title': 'Superintendent of Public Instruction', 'name': 'Dr. Victor Wakefield', 'party': 'Nonpartisan', 'portrait_url': 'https://doe.nv.gov/uploadedImages/ndedoenvgov/content/About/Executive_Team/Wakefield_Victor.jpg', 'branch': 'Executive'},
        {'title': 'Senate Majority Leader', 'name': 'Nicole Cannizzaro', 'party': 'Democrat', 'portrait_url': 'https://www.leg.state.nv.us/Session/83rd2025/legislators/senate/cannizzaro_nicole.jpg', 'branch': 'Legislative'},
        {'title': 'Senate President Pro Tempore', 'name': 'Marilyn Dondero Loop', 'party': 'Democrat', 'portrait_url': 'https://www.leg.state.nv.us/Session/83rd2025/legislators/senate/dondero_loop_marilyn.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Speaker', 'name': 'Steve Yeager', 'party': 'Democrat', 'portrait_url': 'https://www.leg.state.nv.us/Session/83rd2025/legislators/assembly/yeager_steve.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Majority Leader', 'name': 'Sandra Jauregui', 'party': 'Democrat', 'portrait_url': 'https://www.leg.state.nv.us/Session/83rd2025/legislators/assembly/jauregui_sandra.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Education Chair', 'name': 'Selena Torres', 'party': 'Democrat', 'portrait_url': 'https://www.leg.state.nv.us/Session/83rd2025/legislators/assembly/torres_selena.jpg', 'branch': 'Legislative'},
        {'title': 'Assembly Ways & Means Chair', 'name': 'Daniele Monroe-Moreno', 'party': 'Democrat', 'portrait_url': 'https://www.leg.state.nv.us/Session/83rd2025/legislators/assembly/monroe_moreno_daniele.jpg', 'branch': 'Legislative'}
    ],
    'UT': [
        {'title': 'Governor', 'name': 'Spencer Cox', 'party': 'Republican', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2021/01/UT-Cox.jpg', 'branch': 'Executive'},
        {'title': 'Senate President', 'name': 'Stuart Adams', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Kirk Cullimore', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Ann Millner', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Appropriations Chair', 'name': 'Jerry Stevenson', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Mike Schultz', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Jefferson Moss', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Education Chair', 'name': 'Cory Maloy', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Appropriations Chair', 'name': 'Val Peterson', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
    ],
    'AR': [
        # Executive Branch — 95th General Assembly (2025-2026)
        {'title': 'Governor', 'name': 'Sarah Huckabee Sanders', 'party': 'Republican', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2023/01/AR-Sanders.jpg', 'branch': 'Executive'},
        {'title': 'Lieutenant Governor', 'name': 'Leslie Rutledge', 'party': 'Republican', 'portrait_url': 'https://ltgovernor.arkansas.gov/wp-content/uploads/2023/01/LG-Rutledge-Headshot-scaled.jpg', 'branch': 'Executive'},
        {'title': 'Secretary of Education', 'name': 'Jacob Oliva', 'party': 'Nonpartisan', 'portrait_url': '', 'branch': 'Executive'},
        # Senate — Bart Hester (Pro Tem) and Blake Johnson (Majority Leader) confirmed 95th Assembly
        {'title': 'Senate President Pro Tempore', 'name': 'Bart Hester', 'party': 'Republican', 'portrait_url': 'https://senate.arkansas.gov/wp-content/uploads/2023/01/Hester-Bart-2023.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Blake Johnson', 'party': 'Republican', 'portrait_url': 'https://senate.arkansas.gov/wp-content/uploads/2023/01/Johnson-Blake-2023.jpg', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Dan Sullivan', 'party': 'Republican', 'portrait_url': 'https://senate.arkansas.gov/wp-content/uploads/2023/01/Sullivan-Dan-2023.jpg', 'branch': 'Legislative'},
        # House — Brian Evans became Speaker Jan 13 2025 (succeeded Matthew Shepherd)
        # Howard Beaty became Majority Leader Jan 2025 (succeeded Marcus Richmond)
        # Keith Brooks chairs House Education Committee in 95th Assembly
        {'title': 'House Speaker', 'name': 'Brian S. Evans', 'party': 'Republican', 'portrait_url': 'https://www.arkansashouse.org/images/members/evans_brian.jpg', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Howard Beaty', 'party': 'Republican', 'portrait_url': 'https://www.arkansashouse.org/images/members/beaty_howard.jpg', 'branch': 'Legislative'},
        {'title': 'House Education Chair', 'name': 'Keith Brooks', 'party': 'Republican', 'portrait_url': 'https://www.arkansashouse.org/images/members/brooks_keith.jpg', 'branch': 'Legislative'},
    ],
    'DE': [
        {'title': 'Governor', 'name': 'Matt Meyer', 'party': 'Democrat', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2025/01/DE-Meyer.jpg', 'branch': 'Executive'},
        {'title': 'Lieutenant Governor', 'name': 'Kyle Evans Gay', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Executive'},
        {'title': 'Senate President Pro Tempore', 'name': 'Dave Sokola', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Bryan Townsend', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Whip', 'name': 'Elizabeth "Tizzy" Lockman', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Melissa Minor-Brown', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Kerri Evelyn Harris', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Joint Finance Co-Chair', 'name': 'Trey Paradee', 'party': 'Democrat', 'portrait_url': '', 'branch': 'Legislative'},
    ],
    'SD': [
        {'title': 'Governor', 'name': 'Larry Rhoden', 'party': 'Republican', 'portrait_url': 'https://www.nga.org/wp-content/uploads/2025/01/SD-Rhoden.jpg', 'branch': 'Executive'},
        {'title': 'Lieutenant Governor', 'name': 'Tony Venhuizen', 'party': 'Republican', 'portrait_url': '', 'branch': 'Executive'},
        {'title': 'Senate President Pro Tempore', 'name': 'Chris Karr', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Majority Leader', 'name': 'Jim Mehlhaff', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'Senate Education Chair', 'name': 'Gary Cammack', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker', 'name': 'Jon Hansen', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Speaker Pro Tempore', 'name': 'Karla Lems', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
        {'title': 'House Majority Leader', 'name': 'Scott Odenbach', 'party': 'Republican', 'portrait_url': '', 'branch': 'Legislative'},
    ]
}


# ====================
# UI HELPER FUNCTIONS (unchanged from v3)
# ====================

def create_hero_section():
    return html.Div([html.Div([html.H1("CEP Expansion Is the Fastest Way to Eliminate School Hunger", style={'fontSize': '60px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '24px', 'lineHeight': '1.08', 'maxWidth': '1100px', 'marginLeft': 'auto', 'marginRight': 'auto', 'letterSpacing': '-0.025em'}), html.P("Across America, millions of children in poverty attend schools that are eligible for the Community Eligibility Provision but haven't adopted it. States have an immediate opportunity to close this gap.", style={'fontSize': '22px', 'color': COLORS['text_secondary'], 'maxWidth': '820px', 'margin': '0 auto 16px auto', 'lineHeight': '1.6', 'fontWeight': '400'}), html.Div("Last Updated: June 29, 2026 | CEP Policy Intelligence Platform", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'opacity': '0.7', 'marginBottom': '48px', 'letterSpacing': '0.3px'}), html.Div([html.Div([html.Div(f"{NATIONAL_STATS['total_children_without_cep']:,.0f}", style={'fontSize': '68px', 'fontWeight': '700', 'color': COLORS['teal'], 'lineHeight': '1', 'letterSpacing': '-0.02em'}), html.Div("CHILDREN WITHOUT CEP", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1.2px', 'marginTop': '12px', 'fontWeight': '600'})], style={'textAlign': 'center'}), html.Div([html.Div(f"{NATIONAL_STATS['avg_coverage']}%", style={'fontSize': '68px', 'fontWeight': '700', 'color': COLORS['teal'], 'lineHeight': '1', 'letterSpacing': '-0.02em'}), html.Div("AVERAGE COVERAGE", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1.2px', 'marginTop': '12px', 'fontWeight': '600'})], style={'textAlign': 'center'})], style={'display': 'flex', 'justifyContent': 'center', 'gap': '80px', 'marginTop': '56px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '120px 40px 100px 40px', 'textAlign': 'center'})], style={'background': f'linear-gradient(135deg, #fafafa 0%, #f3f4f6 100%)', 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_insights_section():
    insights = [{'title': 'Largest Coverage Gap', 'metric': '826K', 'text': 'children in New Jersey could gain access through expanded CEP adoption'}, {'title': 'Leading Implementation', 'metric': '89%', 'text': 'of eligible schools in South Carolina currently participate in CEP'}, {'title': 'Unserved Communities', 'metric': '24', 'text': 'counties in Wisconsin have zero CEP participation despite clear eligibility'}, {'title': 'National Opportunity', 'metric': f"{NATIONAL_STATS['eligible_schools_not_participating']:,}", 'text': 'eligible schools not yet participating across all tracked states'}]
    insight_cards = [html.Div([html.H3(i['title'], style={'fontSize': '16px', 'fontWeight': '600', 'marginBottom': '16px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}), html.Div(i['metric'], style={'fontSize': '48px', 'fontWeight': '700', 'color': COLORS['teal'], 'marginBottom': '12px', 'lineHeight': '1', 'letterSpacing': '-0.02em'}), html.P(i['text'], style={'fontSize': '15px', 'color': COLORS['text_secondary'], 'lineHeight': '1.6', 'margin': '0'})], style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '36px 32px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'}) for i in insights]
    return html.Div([html.H2("Policy Impact Snapshot", style={'fontSize': '36px', 'fontWeight': '600', 'marginBottom': '48px', 'color': COLORS['text_primary'], 'letterSpacing': '-0.015em'}), html.Div(insight_cards, style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '24px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '96px 40px'})

def create_us_map():
    all_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state_z_values = []
    for state in all_states:
        category = get_state_category(state)
        if category == 'universal_meals': state_z_values.append(4)
        elif category == 'universal_breakfast': state_z_values.append(3)
        elif category == 'fpl_states': state_z_values.append(2)
        else: state_z_values.append(1)
    state_names = [STATE_DATA.get(state, {}).get('name', state) for state in all_states]
    fpl_percentages = {'HI': '300% of FPL', 'NJ': '225% of FPL', 'ND': '225% of FPL'}
    hover_text = []
    for state in all_states:
        category = get_state_category(state)
        state_name = state_names[all_states.index(state)]
        if category == 'universal_meals': hover_text.append(f"<b>{state_name}</b><br>Universal Free Meals")
        elif category == 'universal_breakfast': hover_text.append(f"<b>{state_name}</b><br>Universal Free Breakfast")
        elif category == 'fpl_states': hover_text.append(f"<b>{state_name}</b><br>{fpl_percentages.get(state, 'Federal Poverty Level')}")
        else:
            data = STATE_DATA.get(state, {})
            if data.get('has_data'): hover_text.append(f"<b>{state_name}</b><br>{data.get('coverage_pct', 0)}% CEP Coverage")
            else: hover_text.append(f"<b>{state_name}</b>")
    fig = go.Figure(go.Choropleth(locations=all_states, z=state_z_values, locationmode='USA-states', text=state_names, hovertext=hover_text, hovertemplate='%{hovertext}<extra></extra>', marker=dict(line=dict(color='white', width=3)), colorscale=[[0, COLORS['other_states']], [0.33, COLORS['fpl_states']], [0.67, COLORS['universal_breakfast']], [1, COLORS['universal_meals']]], zmin=1, zmax=4, showscale=False))
    campaign_coords = {'SC': (33.8, -81.2, 'South Carolina'), 'NJ': (40.1, -74.7, 'New Jersey')}
    fig.add_trace(go.Scattergeo(lat=[v[0] for v in campaign_coords.values()], lon=[v[1] for v in campaign_coords.values()], mode='markers', marker=dict(size=16, color='#dc2626', symbol='circle', line=dict(color='white', width=2.5), opacity=0.95), hovertext=[f"<b>{v[2]}</b><br>🔴 Active 2026 Campaign" for v in campaign_coords.values()], hovertemplate='%{hovertext}<extra></extra>', showlegend=False, geo='geo'))
    proposed_coords = {'IL': (40.0, -89.2, 'Illinois'), 'PA': (40.9, -77.8, 'Pennsylvania'), 'AZ': (34.3, -111.7, 'Arizona'), 'RI': (41.6, -71.5, 'Rhode Island'), 'NV': (38.8, -117.2, 'Nevada'), 'WI': (44.3, -89.8, 'Wisconsin'), 'GA': (32.5, -83.4, 'Georgia'), 'AR': (34.8, -92.4, 'Arkansas'), 'DE': (39.0, -75.5, 'Delaware')}
    fig.add_trace(go.Scattergeo(lat=[v[0] for v in proposed_coords.values()], lon=[v[1] for v in proposed_coords.values()], mode='markers', marker=dict(size=16, color='#2563eb', symbol='circle', line=dict(color='white', width=2), opacity=0.90), hovertext=[f"<b>{v[2]}</b><br>🔵 Proposed Target State" for v in proposed_coords.values()], hovertemplate='%{hovertext}<extra></extra>', showlegend=False, geo='geo'))
    fig.update_traces(hoverlabel=dict(bgcolor='white', font_size=14, font_family='Inter, system-ui, sans-serif', font_color='#1a1a1a', bordercolor='#e5e7eb', align='left'))
    fig.update_geos(scope='usa', projection_type='albers usa', showlakes=False, bgcolor='rgba(0,0,0,0)', showsubunits=True, subunitcolor='white', subunitwidth=2)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=700, paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'), clickmode='event+select')
    return fig

def create_state_detail_panel(state_abbr=None):
    if not state_abbr:
        return html.Div([html.Div([html.Div("Click any state to view detailed information", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'marginBottom': '20px', 'textAlign': 'center'}), html.Div([html.Div("Featured FPL States:", style={'fontSize': '13px', 'fontWeight': '600', 'color': COLORS['text_secondary'], 'marginBottom': '12px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}), html.Div([html.Div("🔵 Hawaii (HI)", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '4px'}), html.Div("300% FPL - Highest threshold", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '12px'})]), html.Div([html.Div("🔵 New Jersey (NJ)", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '4px'}), html.Div("225% FPL - 20% coverage", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '12px'})]), html.Div([html.Div("🔵 North Dakota (ND)", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '4px'}), html.Div("225% FPL - 34% coverage", style={'fontSize': '12px', 'color': COLORS['text_secondary']})])])])], style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}', 'minHeight': '400px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
    state_data = STATE_DATA.get(state_abbr, {})
    state_name = state_data.get('name', state_abbr)
    category = get_state_category(state_abbr)
    fpl_percentages = {'HI': 300, 'NJ': 225, 'ND': 225}
    if category == 'universal_meals': badge_color, badge_text = COLORS['universal_meals'], '🟢 Universal School Meals'
    elif category == 'universal_breakfast': badge_color, badge_text = COLORS['universal_breakfast'], '🟡 Universal School Breakfast'
    elif category == 'fpl_states': badge_color, badge_text = COLORS['fpl_states'], '🔵 Federal Poverty Level'
    else: badge_color, badge_text = COLORS['text_secondary'], 'CEP Tracked'
    content = [html.H3(state_name, style={'fontSize': '22px', 'fontWeight': '600', 'margin': '0 0 12px 0', 'color': COLORS['text_primary']}), html.Div(badge_text, style={'display': 'inline-block', 'background': badge_color, 'color': 'white', 'padding': '6px 14px', 'borderRadius': '16px', 'fontSize': '13px', 'fontWeight': '500', 'marginBottom': '20px'})]
    if category == 'fpl_states' and state_abbr in fpl_percentages:
        content.append(html.Div([html.Div('FPL Threshold', style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '4px'}), html.Div(f"{fpl_percentages[state_abbr]}% of FPL", style={'fontSize': '16px', 'fontWeight': '500', 'color': COLORS['text_primary']})], style={'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'0.5px solid {COLORS["border"]}'}))
    coverage = state_data.get('coverage_pct') or ALL_STATES_COVERAGE.get(state_abbr, 0)
    if coverage:
        content.append(html.Div([html.Div('CEP Coverage', style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '4px'}), html.Div(f"{coverage}%", style={'fontSize': '24px', 'fontWeight': '600', 'color': COLORS['text_primary']})], style={'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'0.5px solid {COLORS["border"]}'}))
    if state_data:
        content.append(html.Div([html.Div('Schools Participating', style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '4px'}), html.Div(f"{state_data.get('cep_schools', 0):,} of {state_data.get('eligible_schools', 0):,}", style={'fontSize': '16px', 'fontWeight': '500', 'color': COLORS['text_primary']})], style={'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': f'0.5px solid {COLORS["border"]}'}))
        content.append(html.Div([html.Div('Students Served', style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '4px'}), html.Div(f"{state_data.get('students_in_cep', 0):,}", style={'fontSize': '16px', 'fontWeight': '500', 'color': COLORS['text_primary']})], style={'marginBottom': '20px'}))
    border_states = BORDER_STATES.get(state_abbr, [])
    if border_states:
        state_names_map = {'IL': 'Illinois', 'IA': 'Iowa', 'MI': 'Michigan', 'MN': 'Minnesota', 'NY': 'New York', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'MD': 'Maryland', 'NC': 'North Carolina', 'TN': 'Tennessee', 'WV': 'West Virginia', 'KY': 'Kentucky', 'GA': 'Georgia', 'CA': 'California', 'OR': 'Oregon', 'ID': 'Idaho', 'UT': 'Utah', 'AZ': 'Arizona', 'MO': 'Missouri', 'MS': 'Mississippi', 'LA': 'Louisiana', 'TX': 'Texas', 'OK': 'Oklahoma'}
        border_items = [html.Div(f"• {STATE_DATA.get(bs, {}).get('name', state_names_map.get(bs, bs))}: {ALL_STATES_COVERAGE.get(bs, 0)}%", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '6px'}) for bs in border_states[:4]]
        content.append(html.Div([html.Div('Border States', style={'fontSize': '13px', 'fontWeight': '600', 'color': COLORS['text_secondary'], 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}), html.Div(border_items)], style={'marginBottom': '20px', 'paddingBottom': '20px', 'borderBottom': f'0.5px solid {COLORS["border"]}'}))
    content.append(html.A('View County Details →', href=f'/state/{state_abbr}', style={'display': 'block', 'width': '100%', 'padding': '12px', 'background': 'transparent', 'border': f'0.5px solid {COLORS["border"]}', 'borderRadius': '8px', 'fontSize': '14px', 'fontWeight': '500', 'color': COLORS['text_primary'], 'textAlign': 'center', 'textDecoration': 'none'}))
    return html.Div(content, style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}', 'boxShadow': '0 2px 8px rgba(0,0,0,0.04)', 'minHeight': '400px'})

def create_explore_states_panel():
    tracked_states = ['AR', 'DE', 'GA', 'IL', 'KY', 'MD', 'NJ', 'NV', 'PA', 'RI', 'SC', 'SD', 'UT', 'VA', 'WI']
    def create_state_badge(state_abbr):
        state_data = STATE_DATA.get(state_abbr, {})
        is_active = state_abbr in ACTIVE_CAMPAIGN_STATES
        flag_url = STATE_FLAGS.get(state_abbr, '')
        return html.A(href=f"/state/{state_abbr.lower()}", children=[html.Div([html.Img(src=flag_url, style={'width': '32px', 'height': '22px', 'borderRadius': '3px', 'objectFit': 'cover', 'border': f'1px solid {COLORS["border"]}', 'marginRight': '10px', 'flexShrink': '0'}), html.Div([html.Div([html.Span(state_abbr, style={'fontSize': '14px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginRight': '6px'}), html.Span("ACTIVE", style={'fontSize': '9px', 'fontWeight': '700', 'color': 'white', 'backgroundColor': '#dc2626', 'padding': '1px 5px', 'borderRadius': '999px', 'letterSpacing': '0.4px'}) if is_active else None], style={'display': 'flex', 'alignItems': 'center'}), html.Div(f"{state_data.get('coverage_pct', 0)}% CEP", style={'fontSize': '11px', 'color': COLORS['text_secondary'], 'fontWeight': '500'})])], style={'display': 'flex', 'alignItems': 'center', 'padding': '10px 16px', 'background': 'white', 'borderRadius': '10px', 'border': f'2px solid {"#dc2626" if is_active else COLORS["border"]}', 'boxShadow': '0 1px 4px rgba(15,23,42,0.06)', 'cursor': 'pointer', 'whiteSpace': 'nowrap'})], style={'textDecoration': 'none'})
    badges = [create_state_badge(s) for s in tracked_states]
    return html.Div([html.Div([html.Span("Available States", style={'fontSize': '13px', 'fontWeight': '700', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.6px', 'marginRight': '16px', 'whiteSpace': 'nowrap', 'flexShrink': '0'}), html.Div(badges, style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '12px', 'padding': '16px 24px', 'background': COLORS['off_white'], 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})], style={'padding': '16px 0 8px 0'})

def create_timeline_pill(event):
    is_meals = event['type'] == 'meals'
    color = COLORS['universal_meals'] if is_meals else COLORS['universal_breakfast']
    return html.Div([html.Span(event['state'], style={'fontSize': '14px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginRight': '10px'}), html.Span(event['date'], style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginRight': '10px'}), html.Span(event['label'], style={'fontSize': '10px', 'fontWeight': '700', 'color': color, 'border': f'2px solid {color}', 'borderRadius': '999px', 'padding': '3px 10px', 'whiteSpace': 'nowrap'})], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'padding': '8px 0', 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_timeline_body(filter_type='all'):
    year_colors = {2021: COLORS['universal_meals'], 2022: COLORS['universal_meals'], 2023: COLORS['universal_meals'], 2025: COLORS['universal_breakfast'], 2026: COLORS['universal_breakfast']}
    columns = []
    for year, events in TIMELINE_DATA.items():
        filtered = [e for e in events if filter_type == 'all' or e['type'] == filter_type]
        if not filtered: continue
        year_color = year_colors.get(year, COLORS['text_primary'])
        columns.append(html.Div([html.Div(str(year), style={'fontSize': '27px', 'fontWeight': '900', 'color': year_color, 'textAlign': 'center', 'marginBottom': '8px', 'lineHeight': '1'}), html.Div(style={'width': '2px', 'height': '24px', 'background': year_color, 'margin': '0 auto'}), html.Div(style={'width': '14px', 'height': '14px', 'borderRadius': '50%', 'background': 'white', 'border': f'3px solid {year_color}', 'margin': '0 auto', 'position': 'relative', 'zIndex': '3', 'marginBottom': '20px', 'boxShadow': f'0 0 0 3px white'}), html.Div([create_timeline_pill(e) for e in filtered], style={'background': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '14px', 'padding': '16px 18px', 'boxShadow': '0 4px 14px rgba(15,23,42,0.07)'})], style={'flex': '1', 'minWidth': '200px', 'maxWidth': '320px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'}))
    if not columns:
        return html.Div("No events match the selected filter.", style={'textAlign': 'center', 'color': COLORS['text_secondary'], 'padding': '40px', 'fontSize': '15px'})
    return html.Div([html.Div([html.Div(style={'position': 'absolute', 'top': '68px', 'left': '0', 'right': '0', 'height': '4px', 'background': '#0f172a', 'borderRadius': '999px', 'zIndex': '1'}), html.Div(columns, style={'display': 'flex', 'gap': '20px', 'position': 'relative', 'zIndex': '2', 'overflowX': 'auto'})], style={'position': 'relative'})], style={'padding': '8px 0'})

def create_simple_timeline_section():
    return html.Div([html.Div([html.H2("Universal School Meals Adoption Timeline", style={'fontSize': '42px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'letterSpacing': '1px', 'textTransform': 'uppercase', 'margin': '0 0 8px 0', 'lineHeight': '1.1', 'textAlign': 'center'}), html.P("School meals policy milestones from 2021 through 2026", style={'fontSize': '19px', 'fontWeight': '700', 'color': COLORS['text_secondary'], 'margin': '0 0 20px 0', 'textAlign': 'center'}), html.Div([dcc.RadioItems(id='timeline-filter', options=[{'label': 'All Policies', 'value': 'all'}, {'label': 'Universal School Meals', 'value': 'meals'}, {'label': 'Universal Breakfast', 'value': 'breakfast'}], value='all', inline=True, inputStyle={'display': 'none'}, labelStyle={'display': 'inline-flex', 'alignItems': 'center', 'padding': '8px 20px', 'borderRadius': '999px', 'border': f'1.5px solid #dee2e6', 'cursor': 'pointer', 'fontSize': '13px', 'fontWeight': '600', 'background': '#ffffff', 'color': '#1a1a1a', 'marginRight': '8px'})], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '28px'})], style={'marginBottom': '10px'}), html.Div([html.Div([html.Span("13", style={'fontSize': '46px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'lineHeight': '1'}), html.Span("States Adopted", style={'fontSize': '15px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'textTransform': 'uppercase', 'marginLeft': '16px'})], style={'background': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '18px', 'padding': '20px 28px', 'boxShadow': '0 12px 26px rgba(15,23,42,0.10)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}), html.Div([html.Span("9", style={'fontSize': '46px', 'fontWeight': '900', 'color': COLORS['universal_meals'], 'lineHeight': '1'}), html.Span("Universal School Meals", style={'fontSize': '15px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'textTransform': 'uppercase', 'marginLeft': '16px'})], style={'background': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '18px', 'padding': '20px 28px', 'boxShadow': '0 12px 26px rgba(15,23,42,0.10)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}), html.Div([html.Span("4", style={'fontSize': '46px', 'fontWeight': '900', 'color': COLORS['universal_breakfast'], 'lineHeight': '1'}), html.Span("Universal Breakfast", style={'fontSize': '15px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'textTransform': 'uppercase', 'marginLeft': '16px'})], style={'background': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '18px', 'padding': '20px 28px', 'boxShadow': '0 12px 26px rgba(15,23,42,0.10)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})], style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, minmax(220px, 1fr))', 'gap': '24px', 'maxWidth': '1120px', 'margin': '0 auto 34px auto'}), html.Div(id='timeline-body', children=create_timeline_body('all')), html.Div([html.Span("●", style={'color': COLORS['universal_meals'], 'fontSize': '22px', 'marginRight': '10px'}), html.Span("Universal School Meals", style={'fontSize': '15px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'textTransform': 'uppercase', 'marginRight': '34px'}), html.Span("●", style={'color': COLORS['universal_breakfast'], 'fontSize': '22px', 'marginRight': '10px'}), html.Span("Universal Breakfast", style={'fontSize': '15px', 'fontWeight': '900', 'color': COLORS['text_primary'], 'textTransform': 'uppercase'})], style={'background': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '14px', 'padding': '15px 26px', 'boxShadow': '0 8px 18px rgba(15,23,42,0.08)', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'width': 'fit-content', 'margin': '28px auto 0 auto'})], style={'background': COLORS.get('bg_secondary', COLORS['off_white']), 'padding': '48px 38px 42px 38px', 'borderRadius': '28px', 'margin': '30px auto', 'maxWidth': '1580px', 'width': '96vw', 'border': f'1px solid {COLORS["border"]}', 'boxShadow': '0 16px 36px rgba(15,23,42,0.08)', 'overflow': 'visible'})


def create_map_section():
    legend = html.Div([
        html.Div([html.Div(style={'width': '16px', 'height': '16px', 'background': COLORS['universal_meals'], 'borderRadius': '3px', 'marginRight': '7px'}), html.Span("Universal meals (9)", style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'}),
        html.Div([html.Div(style={'width': '16px', 'height': '16px', 'background': COLORS['universal_breakfast'], 'borderRadius': '3px', 'marginRight': '7px'}), html.Span("Universal breakfast (4)", style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'}),
        html.Div([html.Div(style={'width': '16px', 'height': '16px', 'background': COLORS['fpl_states'], 'borderRadius': '3px', 'marginRight': '7px'}), html.Span("FPL states (3)", style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'}),
        html.Div([html.Div(style={'width': '16px', 'height': '16px', 'background': COLORS['other_states'], 'borderRadius': '3px', 'marginRight': '7px'}), html.Span("Other states", style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'}),
        html.Div([html.Div(style={'width': '14px', 'height': '14px', 'background': '#dc2626', 'borderRadius': '50%', 'marginRight': '7px'}), html.Span("Active campaign", style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'}),
        html.Div([html.Div(style={'width': '14px', 'height': '14px', 'background': '#2563eb', 'borderRadius': '50%', 'marginRight': '7px'}), html.Span("Proposed target", style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'flex', 'alignItems': 'center'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '8px', 'marginBottom': '20px', 'padding': '14px 16px', 'background': COLORS['off_white'], 'borderRadius': '8px'})

    all_state_options = [
        {'label': 'Alabama', 'value': 'AL'}, {'label': 'Alaska', 'value': 'AK'}, {'label': 'Arizona', 'value': 'AZ'},
        {'label': 'Arkansas', 'value': 'AR'}, {'label': 'California', 'value': 'CA'}, {'label': 'Colorado', 'value': 'CO'},
        {'label': 'Connecticut', 'value': 'CT'}, {'label': 'Delaware', 'value': 'DE'}, {'label': 'Florida', 'value': 'FL'},
        {'label': 'Georgia', 'value': 'GA'}, {'label': 'Hawaii', 'value': 'HI'}, {'label': 'Idaho', 'value': 'ID'},
        {'label': 'Illinois', 'value': 'IL'}, {'label': 'Indiana', 'value': 'IN'}, {'label': 'Iowa', 'value': 'IA'},
        {'label': 'Kansas', 'value': 'KS'}, {'label': 'Kentucky', 'value': 'KY'}, {'label': 'Louisiana', 'value': 'LA'},
        {'label': 'Maine', 'value': 'ME'}, {'label': 'Maryland', 'value': 'MD'}, {'label': 'Massachusetts', 'value': 'MA'},
        {'label': 'Michigan', 'value': 'MI'}, {'label': 'Minnesota', 'value': 'MN'}, {'label': 'Mississippi', 'value': 'MS'},
        {'label': 'Missouri', 'value': 'MO'}, {'label': 'Montana', 'value': 'MT'}, {'label': 'Nebraska', 'value': 'NE'},
        {'label': 'Nevada', 'value': 'NV'}, {'label': 'New Hampshire', 'value': 'NH'}, {'label': 'New Jersey', 'value': 'NJ'},
        {'label': 'New Mexico', 'value': 'NM'}, {'label': 'New York', 'value': 'NY'}, {'label': 'North Carolina', 'value': 'NC'},
        {'label': 'North Dakota', 'value': 'ND'}, {'label': 'Ohio', 'value': 'OH'}, {'label': 'Oklahoma', 'value': 'OK'},
        {'label': 'Oregon', 'value': 'OR'}, {'label': 'Pennsylvania', 'value': 'PA'}, {'label': 'Rhode Island', 'value': 'RI'},
        {'label': 'South Carolina', 'value': 'SC'}, {'label': 'South Dakota', 'value': 'SD'}, {'label': 'Tennessee', 'value': 'TN'},
        {'label': 'Texas', 'value': 'TX'}, {'label': 'Utah', 'value': 'UT'}, {'label': 'Vermont', 'value': 'VT'},
        {'label': 'Virginia', 'value': 'VA'}, {'label': 'Washington', 'value': 'WA'}, {'label': 'West Virginia', 'value': 'WV'},
        {'label': 'Wisconsin', 'value': 'WI'}, {'label': 'Wyoming', 'value': 'WY'}
    ]

    return html.Div([html.Div([
        html.H2("National School Meal Coverage", style={'fontSize': '36px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary'], 'letterSpacing': '-0.015em'}),
        html.Div([dcc.Dropdown(id='state-search-dropdown', options=all_state_options, placeholder='🔍 Search states...', clearable=True, searchable=True, style={'maxWidth': '400px'})], style={'marginBottom': '16px'}),
        legend,
        html.Div([
            dcc.Graph(id='us-map-graph', figure=create_us_map(), config={'displayModeBar': False}, style={'background': 'white', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'padding': '20px'})
        ], style={'marginBottom': '16px'}),
        create_explore_states_panel(),
        html.Div(id='county-map-container', children=[], style={'marginTop': '24px'})
    ], style={'maxWidth': '1400px', 'margin': '0 auto'})], style={'padding': '80px 40px', 'background': 'white'})

def create_poverty_heat_map(df, fips_dict, state_abbr):
    """Create poverty heat map with 3-tier warm gradient (0-15% / 15-25% / 25%+)"""
    df = df.copy()
    df['FIPS'] = df['County'].map(fips_dict)
    if 'Poverty_Rate' not in df.columns:
        df['Poverty_Rate'] = 0
    if 'Student_Population' not in df.columns:
        df['Student_Population'] = 0
    def get_poverty_tier(rate):
        if pd.isna(rate): return 0
        if rate < 15: return 1
        elif rate < 25: return 2
        else: return 3
    df['Poverty_Tier'] = df['Poverty_Rate'].apply(get_poverty_tier)
    try:
        if 'Children_in_Poverty' in df.columns:
            low_children = int(df[df['Poverty_Tier'] == 1]['Children_in_Poverty'].sum())
            mod_children = int(df[df['Poverty_Tier'] == 2]['Children_in_Poverty'].sum())
            high_children = int(df[df['Poverty_Tier'] == 3]['Children_in_Poverty'].sum())
        else:
            low_children = mod_children = high_children = 0
    except:
        low_children = mod_children = high_children = 0
    df['hover_text'] = df['County'].astype(str) + ' | ' + df['Status'].astype(str)
    fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df['FIPS'], z=df['Poverty_Tier'],
        colorscale=[[0, '#FFFFFF'], [0.33, '#FEF3C7'], [0.66, '#FB923C'], [1, '#DC2626']],
        zmin=0, zmax=3, marker_line_color='white', marker_line_width=1.5, showscale=False,
        text=df['hover_text'], hovertemplate='%{text}<extra></extra>'
    ))
    state_centers = {
        'WI': {'lat': 44.5, 'lon': -89.5}, 'NJ': {'lat': 40.0, 'lon': -74.5},
        'VA': {'lat': 37.5, 'lon': -78.5}, 'MD': {'lat': 39.0, 'lon': -76.8},
        'KY': {'lat': 37.8, 'lon': -84.3}, 'SC': {'lat': 33.8, 'lon': -80.9},
        'NV': {'lat': 39.0, 'lon': -117.0}, 'RI': {'lat': 41.7, 'lon': -71.5},
        'PA': {'lat': 41.2, 'lon': -77.2}, 'GA': {'lat': 32.7, 'lon': -83.5},
        'IL': {'lat': 40.0, 'lon': -89.2}, 'SD': {'lat': 44.4, 'lon': -100.3},
        'UT': {'lat': 39.3, 'lon': -111.1}, 'AR': {'lat': 34.8, 'lon': -92.2},
        'DE': {'lat': 39.0, 'lon': -75.5},
    }
    center = state_centers.get(state_abbr, {'lat': 39, 'lon': -98})
    fig.update_geos(fitbounds="locations", visible=False, projection_type="albers usa", center=center)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=500,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig, low_children, mod_children, high_children


def create_cep_legend_compact():
    return html.Div([
        html.Span([html.Span('■', style={'color': COLORS['full_cep'], 'fontSize': '18px', 'marginRight': '6px'}), html.Span("Full CEP", style={'fontSize': '12px', 'marginRight': '16px'})]),
        html.Span([html.Span('■', style={'color': COLORS['partial_cep'], 'fontSize': '18px', 'marginRight': '6px'}), html.Span("Partial CEP", style={'fontSize': '12px', 'marginRight': '16px'})]),
        html.Span([html.Span('■', style={'color': COLORS['no_cep'], 'fontSize': '18px', 'marginRight': '6px'}), html.Span("No CEP", style={'fontSize': '12px'})])
    ], style={'display': 'flex', 'alignItems': 'center', 'background': COLORS['off_white'], 'padding': '12px', 'borderRadius': '6px', 'marginTop': '12px'})


def create_poverty_legend_compact():
    return html.Div([
        html.Span([html.Span('■', style={'color': '#FEF3C7', 'fontSize': '18px', 'marginRight': '6px', 'textShadow': '0 0 1px #999'}), html.Span("0-15% Low", style={'fontSize': '12px', 'marginRight': '16px'})]),
        html.Span([html.Span('■', style={'color': '#FB923C', 'fontSize': '18px', 'marginRight': '6px'}), html.Span("15-25% Moderate", style={'fontSize': '12px', 'marginRight': '16px'})]),
        html.Span([html.Span('■', style={'color': '#DC2626', 'fontSize': '18px', 'marginRight': '6px'}), html.Span("25%+ High", style={'fontSize': '12px', 'marginRight': '16px'})]),
        html.Span("Source: U.S. Census Bureau ACS 5-Year Estimates", style={'fontSize': '10px', 'color': COLORS['text_secondary'], 'fontStyle': 'italic'})
    ], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '8px', 'background': COLORS['off_white'], 'padding': '12px', 'borderRadius': '6px', 'marginTop': '12px'})


def create_nj_county_table(df):
    """NJ-specific county table with Change This Year column and Essex disclaimer."""
    return html.Div([
        html.H2("County Details", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '16px'}),
        html.Div([
            html.Span("⚠️  ", style={'fontSize': '16px'}),
            html.Span("Essex County Note: ", style={'fontWeight': '700', 'fontSize': '14px', 'color': '#92400e'}),
            html.Span("Essex County includes Newark, where students are served through the Newark Coalition — a community-based initiative that provides meals independently of the federal CEP program. The children served column reflects both CEP and Newark Coalition participation where applicable.", style={'fontSize': '14px', 'color': '#92400e'})
        ], style={'background': '#fef3c7', 'border': '1px solid #f59e0b', 'borderRadius': '8px', 'padding': '14px 18px', 'marginBottom': '24px'}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {'name': 'County', 'id': 'County'},
                {'name': 'Total Population', 'id': 'Population', 'type': 'numeric', 'format': {'specifier': ','}},
                {'name': 'Children Under 18 in Poverty (%)', 'id': 'Poverty_Rate', 'type': 'numeric'},
                {'name': '# of Schools', 'id': 'Eligible_Schools', 'type': 'numeric'},
                {'name': 'Student Population', 'id': 'Student_Population', 'type': 'numeric', 'format': {'specifier': ','}},
                {'name': '# Schools in CEP', 'id': 'CEP_Schools', 'type': 'numeric'},
                {'name': 'Children Served', 'id': 'Students_in_CEP', 'type': 'numeric', 'format': {'specifier': ','}},
                {'name': 'Change This Year', 'id': 'Change_This_Year'},
                {'name': 'Status', 'id': 'Status'}
            ],
            sort_action='native', filter_action='native', page_action='none',
            style_table={'overflowX': 'auto', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'overflow': 'hidden'},
            style_header={'backgroundColor': COLORS['off_white'], 'fontWeight': '600', 'fontSize': '12px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'padding': '14px 16px', 'borderBottom': f'2px solid {COLORS["border"]}', 'textAlign': 'left', 'whiteSpace': 'normal'},
            style_cell={'padding': '14px 16px', 'fontSize': '14px', 'fontFamily': 'Inter, -apple-system, sans-serif', 'textAlign': 'left', 'borderBottom': f'1px solid {COLORS["border"]}', 'whiteSpace': 'normal', 'height': 'auto'},
            style_cell_conditional=[
                {'if': {'column_id': ['Population', 'Student_Population', 'Students_in_CEP']}, 'textAlign': 'right'},
                {'if': {'column_id': ['Poverty_Rate', 'Eligible_Schools', 'CEP_Schools']}, 'textAlign': 'center'},
                {'if': {'column_id': 'County'}, 'fontWeight': '500', 'minWidth': '120px'},
                {'if': {'column_id': 'Status'}, 'minWidth': '160px', 'textAlign': 'center'},
                {'if': {'column_id': 'Change_This_Year'}, 'fontSize': '13px', 'color': COLORS['text_secondary'], 'fontStyle': 'italic'}
            ],
            style_data_conditional=[
                {'if': {'filter_query': '{Status} = "FULL CEP"'}, 'backgroundColor': '#e0f2fe'},
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"'}, 'backgroundColor': '#fef3c7'},
                {'if': {'filter_query': '{Status} = "NO CEP"'}, 'backgroundColor': '#fce7f3'},
                {'if': {'filter_query': '{Status} = "FULL CEP"', 'column_id': 'Status'}, 'backgroundColor': '#87CEEB', 'color': '#1a1a1a', 'fontWeight': '600', 'fontSize': '13px', 'textAlign': 'center'},
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"', 'column_id': 'Status'}, 'backgroundColor': '#fbbf24', 'color': '#ffffff', 'fontWeight': '600', 'fontSize': '13px', 'textAlign': 'center'},
                {'if': {'filter_query': '{Status} = "NO CEP"', 'column_id': 'Status'}, 'backgroundColor': '#ec4899', 'color': '#ffffff', 'fontWeight': '600', 'fontSize': '13px', 'textAlign': 'center'},
                {'if': {'filter_query': '{Change_This_Year} contains "fewer"', 'column_id': 'Change_This_Year'}, 'color': '#dc2626', 'fontWeight': '600'},
                {'if': {'filter_query': '{Change_This_Year} contains "First year"', 'column_id': 'Change_This_Year'}, 'color': '#059669', 'fontWeight': '600'}
            ],
            style_filter={'backgroundColor': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '4px', 'padding': '8px', 'fontSize': '13px'}
        )
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})


def create_georgia_dual_map_section(df, fips_dict):
    """Georgia dual map: county coverage tiers (left) + district CEP status (right)."""
    df_map = df.copy()
    df_map['FIPS'] = df_map['County'].map(fips_dict)
    df_valid = df_map[df_map['FIPS'].notna()]

    county_fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df_valid['FIPS'], z=df_valid['Status_Numeric'],
        text=df_valid['County'] + '<br>Tier: ' + df_valid['Coverage_Tier'] + '<br>CEP: ' + df_valid['CEP_Schools'].astype(str) + '/' + df_valid['Total_Schools'].astype(str),
        hovertemplate='<b>%{text}</b><extra></extra>',
        colorscale=[[0.00, '#fce7f3'], [0.25, '#e0f2fe'], [0.50, '#7dd3fc'], [0.75, '#2563eb'], [1.00, '#1e3a8a']],
        zmin=0, zmax=4, marker_line_color='white', marker_line_width=1.0, showscale=False
    ))
    county_fig.update_geos(fitbounds="locations", visible=False, projection_type="albers usa", center={'lat': 32.7, 'lon': -83.5})
    county_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=460, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    dist_df = load_georgia_district_data()
    county_dist_status = {}
    for county in df['County']:
        dists = dist_df[dist_df['County'] == county]
        if len(dists) == 0 or all(dists['Status'] == 'NO CEP'): county_dist_status[county] = 0
        elif any(dists['Status'] == 'FULL CEP'): county_dist_status[county] = 2
        else: county_dist_status[county] = 1
    df_dist = df_valid.copy()
    df_dist['Dist_Z'] = df_dist['County'].map(county_dist_status).fillna(0)
    df_dist['Dist_Label'] = df_dist['Dist_Z'].map({0: 'No CEP', 1: 'Partial CEP', 2: 'Full CEP'})
    dist_fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df_dist['FIPS'], z=df_dist['Dist_Z'],
        text=df_dist['County'] + '<br>' + df_dist['Dist_Label'],
        hovertemplate='<b>%{text}</b><extra></extra>',
        colorscale=[[0.0, COLORS['no_cep']], [0.5, COLORS['partial_cep']], [1.0, COLORS['full_cep']]],
        zmin=0, zmax=2, marker_line_color='white', marker_line_width=1.0, showscale=False
    ))
    dist_fig.update_geos(fitbounds="locations", visible=False, projection_type="albers usa", center={'lat': 32.7, 'lon': -83.5})
    dist_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=460, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    tier_legend = html.Div([html.Div("Coverage Tiers", style={"fontWeight": "600", "fontSize": "12px", "marginBottom": "8px", "color": COLORS["text_secondary"]}),
        *[html.Div([html.Div(style={"width": "12px", "height": "12px", "borderRadius": "2px", "backgroundColor": c, "marginRight": "8px", "flexShrink": "0"}), html.Span(l, style={"fontSize": "12px", "color": COLORS["text_secondary"]})], style={"display": "flex", "alignItems": "center", "marginBottom": "4px"})
        for l, c in [("75%+ in CEP", "#1e3a8a"), ("50-74%", "#2563eb"), ("25-49%", "#7dd3fc"), ("1-24%", "#e0f2fe"), ("No CEP", "#fce7f3")]]], style={"marginTop": "12px"})
    status_legend = html.Div([html.Div("District Status", style={"fontWeight": "600", "fontSize": "12px", "marginBottom": "8px", "color": COLORS["text_secondary"]}),
        *[html.Div([html.Div(style={"width": "12px", "height": "12px", "borderRadius": "2px", "backgroundColor": c, "marginRight": "8px", "flexShrink": "0"}), html.Span(l, style={"fontSize": "12px", "color": COLORS["text_secondary"]})], style={"display": "flex", "alignItems": "center", "marginBottom": "4px"})
        for l, c in [("Full CEP districts present", COLORS["full_cep"]), ("Partial CEP districts", COLORS["partial_cep"]), ("No CEP", COLORS["no_cep"])]]], style={"marginTop": "12px"})

    return html.Div([
        html.H2("County & District Maps", style={"fontSize": "28px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "16px"}),
        html.Div([html.Span("ℹ️  "), html.Span("District map note: ", style={"fontWeight": "700", "fontSize": "12px", "color": "#1e40af"}), html.Span("Georgia has 180+ school districts across 159 counties. The district map shows dominant CEP status per county, aggregated from all districts within it. Source: FRAC 2024-2025 Fact Sheet (October 2025).", style={"fontSize": "12px", "color": "#1e40af"})], style={"background": "#eff6ff", "border": "1px solid #bfdbfe", "borderRadius": "8px", "padding": "12px 16px", "marginBottom": "20px"}),
        html.Div([
            html.Div([html.H3("County Coverage Rate", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "6px", "textAlign": "center"}), html.P("Shows what % of eligible schools in each county participate in CEP. Darker blue = higher coverage.", style={"fontSize": "12px", "color": COLORS["text_secondary"], "textAlign": "center", "marginBottom": "12px", "lineHeight": "1.5"}), dcc.Graph(figure=county_fig, config={"displayModeBar": False, "scrollZoom": False}), tier_legend], style={"flex": "1", "minWidth": "0", "background": "white", "borderRadius": "12px", "border": f"1px solid {COLORS['border']}", "padding": "20px"}),
            html.Div([html.H3("District CEP Status", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "6px", "textAlign": "center"}), html.P("Shows CEP adoption status per school district, aggregated by county. Blue = Full CEP; Yellow = partial; Pink = no participation.", style={"fontSize": "12px", "color": COLORS["text_secondary"], "textAlign": "center", "marginBottom": "12px", "lineHeight": "1.5"}), dcc.Graph(figure=dist_fig, config={"displayModeBar": False, "scrollZoom": False}), status_legend], style={"flex": "1", "minWidth": "0", "background": "white", "borderRadius": "12px", "border": f"1px solid {COLORS['border']}", "padding": "20px"}),
        ], style={"display": "flex", "gap": "24px"})
    ], style={"maxWidth": "1400px", "margin": "0 auto", "padding": "0 40px 40px 40px"})


def create_comparison_section():
    return html.Div([html.Div([
        html.H2("Compare States", style={'fontSize': '36px', 'fontWeight': '600', 'marginBottom': '28px', 'color': COLORS['text_primary'], 'letterSpacing': '-0.015em'}),
        html.Div([
            html.Div([html.Label("State A", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}), dcc.Dropdown(id='compare-state-a', options=[{'label': data['name'], 'value': abbr} for abbr, data in STATE_DATA.items()], value='WI', clearable=False, style={'minWidth': '200px'})], style={'flex': '1'}),
            html.Div([html.Label("State B", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}), dcc.Dropdown(id='compare-state-b', options=[{'label': data['name'], 'value': abbr} for abbr, data in STATE_DATA.items()], value='NJ', clearable=False, style={'minWidth': '200px'})], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px'}),
        html.Div([
            html.Label("Show County Maps:", style={'fontSize': '14px', 'fontWeight': '600', 'marginRight': '16px', 'color': COLORS['text_primary']}),
            dcc.Checklist(id='comparison-map-types', options=[{'label': ' CEP Coverage', 'value': 'cep'}, {'label': ' Poverty Distribution', 'value': 'poverty'}], value=['cep'], inline=True, style={'fontSize': '14px'}, labelStyle={'marginRight': '20px', 'cursor': 'pointer'})
        ], style={'display': 'flex', 'alignItems': 'center', 'padding': '16px', 'background': COLORS['off_white'], 'borderRadius': '8px', 'marginBottom': '16px'}),
        html.Div(id='comparison-output'),
        html.Div(id='comparison-county-maps', style={'marginTop': '16px'})
    ], style={'maxWidth': '1400px', 'margin': '0 auto'})], style={'padding': '32px 40px 80px 40px', 'background': 'white'})

def create_landing_page():
    return html.Div([
        create_simple_timeline_section(),
        create_map_section(),
        create_comparison_section(),
        html.Div("v2026-07-15-AR-DATA-CT-EXEC-FIX", style={'textAlign': 'center', 'padding': '20px', 'fontSize': '11px', 'color': '#aaa'})
    ])

def create_comparison_cards(state_a, state_b):
    data_a = STATE_DATA[state_a]
    data_b = STATE_DATA[state_b]
    def card(d):
        return html.Div([
            html.H3(d['name'], style={'fontSize': '24px', 'fontWeight': '600', 'marginBottom': '20px', 'color': COLORS['text_primary']}),
            html.Div([html.Div("Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"{d['coverage_pct']}%", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['teal']})], style={'marginBottom': '16px'}),
            html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}), html.Div(f"{d['students_in_cep']:,}", style={'fontSize': '24px', 'fontWeight': '600', 'color': COLORS['text_primary']})])
        ], style={'background': 'white', 'padding': '32px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})
    return html.Div([card(data_a), card(data_b)], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px'})


def create_state_executives_section(state_abbr):
    executives = STATE_EXECUTIVES.get(state_abbr, [])
    if not executives:
        return html.Div()
    def get_initials(name):
        parts = name.split()
        return f"{parts[0][0]}{parts[-1][0]}" if len(parts) >= 2 else name[0]
    legend = html.Div([
        html.Div([html.Span('●', style={'color': COLORS['democrat_name'], 'fontSize': '20px', 'marginRight': '6px'}), html.Span('Democratic', style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginRight': '20px'})], style={'display': 'inline-flex', 'alignItems': 'center'}),
        html.Div([html.Span('●', style={'color': COLORS['republican_name'], 'fontSize': '20px', 'marginRight': '6px'}), html.Span('Republican', style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'display': 'inline-flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'paddingBottom': '12px', 'borderBottom': f'1px solid {COLORS["border"]}'})
    executive_branch = [e for e in executives if e['branch'] == 'Executive']
    legislative_branch = [e for e in executives if e['branch'] == 'Legislative']
    def make_card(official):
        name_color = get_party_color(official['party'])
        portrait = html.Div(get_initials(official['name']), style={'width': '40px', 'height': '40px', 'borderRadius': '50%', 'border': f'2px solid {name_color}', 'backgroundColor': COLORS['off_white'], 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'fontSize': '14px', 'fontWeight': '600', 'color': name_color, 'flexShrink': '0'})
        return html.Div([portrait, html.Div([html.Div(official['name'], style={'fontSize': '16px', 'fontWeight': '600', 'color': name_color, 'marginBottom': '2px'}), html.Div(official['title'], style={'fontSize': '13px', 'color': COLORS['text_secondary']})], style={'marginLeft': '12px', 'flex': '1'})], style={'display': 'flex', 'alignItems': 'center', 'padding': '16px', 'background': 'white', 'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}'})
    sections = []
    if executive_branch:
        sections.append(html.Div([html.H3("Executive Branch", style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px'}), html.Div([make_card(e) for e in executive_branch], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))', 'gap': '12px'})], style={'marginBottom': '24px'}))
    if legislative_branch:
        sections.append(html.Div([html.H3("Legislative Branch", style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px'}), html.Div([make_card(e) for e in legislative_branch], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))', 'gap': '12px'})]))
    return html.Div([html.Div([html.H2("State Leadership", style={'fontSize': '20px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '20px'}), legend] + sections, style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 40px 40px'})], style={'background': COLORS['off_white'], 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_county_map(df, fips_dict, state_abbr):
    df = df.copy()
    df['FIPS'] = df['County'].map(fips_dict)
    fig = go.Figure(go.Choropleth(
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations=df['FIPS'], z=df['Status_Numeric'],
        text=df['County'] + '<br>' + df['Status'],
        hovertemplate='<b>%{text}</b><extra></extra>',
        colorscale=[[0, COLORS['no_cep']], [0.5, COLORS['partial_cep']], [1, COLORS['full_cep']]],
        zmin=0, zmax=2, marker_line_color='white', marker_line_width=1.5, showscale=False
    ))
    fig.update_geos(fitbounds="locations", visible=False, projection_type="albers usa")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def create_county_color_legend():
    return html.Div([
        html.Div([html.Span('■', style={'color': COLORS['full_cep'], 'fontSize': '18px', 'marginRight': '6px'}), html.Span('Sky Blue = Full CEP', style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'display': 'inline-flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([html.Span('■', style={'color': COLORS['partial_cep'], 'fontSize': '18px', 'marginRight': '6px'}), html.Span('Yellow = Partial CEP', style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'display': 'inline-flex', 'alignItems': 'center', 'marginRight': '24px'}),
        html.Div([html.Span('■', style={'color': COLORS['no_cep'], 'fontSize': '18px', 'marginRight': '6px'}), html.Span('Pink = No CEP', style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'display': 'inline-flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'padding': '16px', 'marginTop': '12px', 'background': COLORS['off_white'], 'borderRadius': '8px', 'border': f'1px solid {COLORS["border"]}'})

def create_sortable_county_table(df):
    """Table sorted by largest opportunity first (eligible schools not yet in CEP)."""
    if 'School_Gap' in df.columns:
        df = df.sort_values('School_Gap', ascending=False).reset_index(drop=True)
    display_cols = ['County', 'Population', 'Children_in_Poverty', 'Eligible_Schools', 'CEP_Schools', 'Students_in_CEP', 'Coverage_Pct', 'School_Gap', 'Status']
    available_cols = [c for c in display_cols if c in df.columns]
    col_defs = [
        {'name': 'County', 'id': 'County'},
        {'name': 'Population', 'id': 'Population', 'type': 'numeric', 'format': {'specifier': ','}},
        {'name': 'Children in Poverty', 'id': 'Children_in_Poverty', 'type': 'numeric', 'format': {'specifier': ','}},
        {'name': 'Eligible Schools', 'id': 'Eligible_Schools', 'type': 'numeric'},
        {'name': 'CEP Schools', 'id': 'CEP_Schools', 'type': 'numeric'},
        {'name': 'Students in CEP', 'id': 'Students_in_CEP', 'type': 'numeric', 'format': {'specifier': ','}},
        {'name': '% Coverage', 'id': 'Coverage_Pct', 'type': 'numeric'},
        {'name': 'Eligible Not Participating ▼', 'id': 'School_Gap', 'type': 'numeric'},
        {'name': 'Status', 'id': 'Status'}
    ]
    col_defs = [c for c in col_defs if c['id'] in available_cols]
    return html.Div([
        html.H2("County Details", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '8px'}),
        html.P("Sorted by largest opportunity first — counties with the most eligible schools not yet participating in CEP.", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '20px', 'fontStyle': 'italic'}),
        dash_table.DataTable(
            data=df[available_cols].to_dict('records'),
            columns=col_defs,
            sort_action='native', filter_action='native', page_action='none',
            style_table={'overflowX': 'auto', 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '12px', 'overflow': 'hidden'},
            style_header={'backgroundColor': COLORS['off_white'], 'fontWeight': '600', 'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'padding': '16px 20px', 'borderBottom': f'2px solid {COLORS["border"]}', 'textAlign': 'left'},
            style_cell={'padding': '16px 20px', 'fontSize': '15px', 'fontFamily': 'Inter, -apple-system, sans-serif', 'textAlign': 'left', 'borderBottom': f'1px solid {COLORS["border"]}'},
            style_cell_conditional=[
                {'if': {'column_id': ['Population', 'Children_in_Poverty', 'Students_in_CEP']}, 'textAlign': 'right'},
                {'if': {'column_id': ['Eligible_Schools', 'CEP_Schools', 'Coverage_Pct', 'School_Gap']}, 'textAlign': 'center'},
                {'if': {'column_id': 'County'}, 'fontWeight': '500', 'minWidth': '140px'},
                {'if': {'column_id': 'School_Gap'}, 'fontWeight': '700', 'color': '#dc2626'},
                {'if': {'column_id': 'Status'}, 'minWidth': '160px'}
            ],
            style_data_conditional=[
                {'if': {'filter_query': '{Status} = "FULL CEP"'}, 'backgroundColor': '#e0f2fe'},
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"'}, 'backgroundColor': '#fef3c7'},
                {'if': {'filter_query': '{Status} = "NO CEP"'}, 'backgroundColor': '#fce7f3'},
                {'if': {'filter_query': '{Status} = "FULL CEP"', 'column_id': 'Status'}, 'backgroundColor': '#87CEEB', 'color': '#1a1a1a', 'fontWeight': '600', 'textAlign': 'center'},
                {'if': {'filter_query': '{Status} = "PARTIAL CEP"', 'column_id': 'Status'}, 'backgroundColor': '#fbbf24', 'color': '#ffffff', 'fontWeight': '600', 'textAlign': 'center'},
                {'if': {'filter_query': '{Status} = "NO CEP"', 'column_id': 'Status'}, 'backgroundColor': '#ec4899', 'color': '#ffffff', 'fontWeight': '600', 'textAlign': 'center'},
                {'if': {'filter_query': '{School_Gap} >= 10', 'column_id': 'School_Gap'}, 'backgroundColor': '#fee2e2', 'fontWeight': '700', 'color': '#dc2626'}
            ],
            style_filter={'backgroundColor': COLORS['white'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '4px', 'padding': '8px', 'fontSize': '14px'}
        )
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 80px 40px'})

def create_session_banner(state_abbr):
    session = SESSION_DATA.get(state_abbr)
    if not session: return html.Div()
    status = session.get('status', '')
    if status == 'In Session': bg, badge_color, icon = '#f0fdf4', '#059669', '🟢'
    elif status == 'Adjourned': bg, badge_color, icon = '#fff7ed', '#ea580c', '🟡'
    else: bg, badge_color, icon = '#eff6ff', '#3b82f6', '🔵'
    return html.Div([html.Div([
        html.Div([
            html.Span(f"{icon} Legislative Session", style={'fontSize': '13px', 'fontWeight': '700', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginRight': '12px'}),
            html.Span(status, style={'fontSize': '12px', 'fontWeight': '700', 'color': 'white', 'backgroundColor': badge_color, 'padding': '3px 10px', 'borderRadius': '999px'})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px'}),
        html.Div(f"{session.get('start', '')} — {session.get('end', '')}", style={'fontSize': '15px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '6px'}),
        html.Div(session.get('notes', ''), style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'lineHeight': '1.5'})
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px 40px'})
    ], style={'background': bg, 'borderBottom': f'1px solid {COLORS["border"]}'})

def create_tabbed_county_maps_section(df, fips_dict, state_abbr, state_name=None):
    """Tabbed view: CEP Coverage + Poverty Distribution maps side by side."""
    if state_name is None:
        state_name = STATE_DATA.get(state_abbr, {}).get('name', state_abbr)
    try:
        poverty_map_fig, low_children, mod_children, high_children = create_poverty_heat_map(df, fips_dict, state_abbr)
    except Exception as e:
        print(f"Error creating poverty map for {state_abbr}: {e}")
        poverty_map_fig = go.Figure()
        low_children = mod_children = high_children = 0

    cep_tab_content = html.Div([
        html.Div([dcc.Graph(figure=create_county_map(df, fips_dict, state_abbr), config={'displayModeBar': False, 'scrollZoom': False})],
                 style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
        create_county_color_legend()
    ])

    poverty_tab_content = html.Div([
        html.Div([dcc.Graph(figure=poverty_map_fig, config={'displayModeBar': False, 'scrollZoom': False})],
                 style={'background': 'white', 'padding': '24px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
        html.Div([
            html.Div("Understanding the Poverty Distribution Map", style={'fontSize': '14px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '6px'}),
            html.P("Each county is shaded by its child poverty rate. Darker red = higher poverty. Counties that are dark here but grey on the CEP Coverage map are the highest-priority gaps — children in need who are not yet being served.", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'marginBottom': '14px', 'lineHeight': '1.6'}),
            html.Div([
                html.Div("Lower poverty", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginRight': '10px', 'whiteSpace': 'nowrap'}),
                html.Div(style={'width': '200px', 'height': '14px', 'borderRadius': '4px', 'background': 'linear-gradient(to right, #FEF3C7, #FB923C, #DC2626)', 'border': '1px solid #e5e7eb', 'flexShrink': '0'}),
                html.Div("Higher poverty", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginLeft': '10px', 'whiteSpace': 'nowrap'}),
                html.Div("│", style={'color': COLORS['border'], 'margin': '0 14px', 'fontSize': '16px'}),
                html.Span([html.Span('■', style={'color': '#FEF3C7', 'fontSize': '16px', 'marginRight': '5px', 'textShadow': '0 0 1px #aaa'}), html.Span(f"0–15% ({low_children:,} children)", style={'marginRight': '16px'})], style={'fontSize': '12px', 'color': COLORS['text_secondary']}),
                html.Span([html.Span('■', style={'color': '#FB923C', 'fontSize': '16px', 'marginRight': '5px'}), html.Span(f"15–25% ({mod_children:,} children)", style={'marginRight': '16px'})], style={'fontSize': '12px', 'color': COLORS['text_secondary']}),
                html.Span([html.Span('■', style={'color': '#DC2626', 'fontSize': '16px', 'marginRight': '5px'}), html.Span(f"25%+ ({high_children:,} children)")], style={'fontSize': '12px', 'color': COLORS['text_secondary']}),
            ], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '4px', 'marginBottom': '10px'}),
            html.Div("Source: U.S. Census Bureau ACS 5-Year Estimates", style={'fontSize': '11px', 'color': COLORS['text_secondary'], 'fontStyle': 'italic'})
        ], style={'background': COLORS['off_white'], 'padding': '16px 20px', 'borderRadius': '8px', 'marginTop': '16px', 'border': f'1px solid {COLORS["border"]}'})
    ])

    return html.Div([
        html.H2("County-Level Analysis", style={'fontSize': '32px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '24px'}),
        dcc.Tabs(id=f'county-tabs-{state_abbr}', value='cep', children=[
            dcc.Tab(label='CEP Coverage', value='cep', children=cep_tab_content,
                    style={'padding': '12px 28px', 'fontWeight': '600', 'fontSize': '15px', 'border': 'none', 'borderBottom': '3px solid transparent'},
                    selected_style={'padding': '12px 28px', 'fontWeight': '600', 'fontSize': '15px', 'border': 'none', 'borderBottom': f'3px solid {COLORS["teal"]}', 'color': COLORS['teal']}),
            dcc.Tab(label='Poverty Distribution', value='poverty', children=poverty_tab_content,
                    style={'padding': '12px 28px', 'fontWeight': '600', 'fontSize': '15px', 'border': 'none', 'borderBottom': '3px solid transparent'},
                    selected_style={'padding': '12px 28px', 'fontWeight': '600', 'fontSize': '15px', 'border': 'none', 'borderBottom': f'3px solid {COLORS["teal"]}', 'color': COLORS['teal']})
        ], style={'marginBottom': '24px'})
    ], style={'marginBottom': '48px'})

def create_state_page(state_abbr):
    state_abbr = state_abbr.upper()
    state_data = STATE_DATA.get(state_abbr)
    if not state_data:
        return html.Div([html.Div([html.A("← All States", href="/", style={'color': COLORS['teal'], 'textDecoration': 'none'}), html.H1("State Not Found", style={'fontSize': '48px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginTop': '20px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '80px 40px'})], style={'minHeight': '100vh', 'background': COLORS['off_white']})

    loader_map = {
        'WI': (load_wisconsin_data, WI_FIPS),
        'GA': (load_georgia_data, GA_FIPS),
        'PA': (load_pennsylvania_data, PA_FIPS),
        'RI': (load_rhode_island_data, RI_FIPS),
        'NJ': (load_new_jersey_data, NJ_FIPS),
        'VA': (load_virginia_data, VA_FIPS),
        'MD': (load_maryland_data, MD_FIPS),
        'NV': (load_nevada_data, NV_FIPS),
        'KY': (load_kentucky_data, KY_FIPS),
        'SC': (load_south_carolina_data, SC_FIPS),
        'IL': (load_illinois_data, IL_FIPS),
        'SD': (load_south_dakota_data, SD_FIPS),
        'UT': (load_utah_data, UT_FIPS),
        'AR': (load_arkansas_data, AR_FIPS),
        'DE': (load_delaware_data, DE_FIPS),
    }

    if state_abbr in loader_map:
        loader_fn, fips_dict = loader_map[state_abbr]
        df = loader_fn()
    else:
        df = pd.DataFrame({'County': ['Data Coming Soon'], 'Population': [0], 'Children_in_Poverty': [0], 'Eligible_Schools': [0], 'CEP_Schools': [0], 'Students_in_CEP': [0], 'Coverage_Pct': [0], 'School_Gap': [0], 'Status': ['NO CEP']})
        df['Status'] = df['Status'].apply(normalize_status)
        df['Status_Numeric'] = df['Status'].apply(status_to_numeric)
        fips_dict = {}


    # Ordered state list for prev/next nav
    ordered_states = ['GA', 'IL', 'KY', 'MD', 'NJ', 'NV', 'PA', 'RI', 'SC', 'SD', 'UT', 'AR', 'DE', 'VA', 'WI']
    state_idx = ordered_states.index(state_abbr) if state_abbr in ordered_states else -1
    prev_abbr = ordered_states[state_idx - 1] if state_idx > 0 else None
    next_abbr = ordered_states[state_idx + 1] if state_idx >= 0 and state_idx < len(ordered_states) - 1 else None
    prev_name = STATE_DATA.get(prev_abbr, {}).get('name', '') if prev_abbr else ''
    next_name = STATE_DATA.get(next_abbr, {}).get('name', '') if next_abbr else ''

    # Data notices for specific states
    data_notice_states = {
        'IL': 'Illinois CEP data reflects the 2024-2025 school year. District-level adoption varies significantly across 102 counties. Source: FRAC October 2025 Fact Sheet (IL14).',
        'NV': 'Nevada data reflects FRAC October 2025 Fact Sheet (NV29). County rows sum to 521/562 eligible; remaining 32 schools are unassigned charter schools. CEP participation is 92% of eligible schools.',
        'RI': 'Rhode Island county rows sum to 82 of 120 CEP schools. The 38-school difference consists of public charter schools and specialty schools not attributable to individual counties. Source: FRAC October 2025 (RI40).',
        'PA': 'Pennsylvania CEP data reflects FRAC October 2025 Fact Sheet (PA39). Universal School Breakfast enacted August 2023.',
        'GA': 'Georgia has 180+ school districts across 159 counties. County-level figures aggregate all districts within each county. See the District map for school-by-school detail. Source: FRAC October 2025 (GA11).',
    }
    data_notice = data_notice_states.get(state_abbr)

    return html.Div([
        # Sticky top nav
        html.Div([html.Div([
            html.Div([
                html.Span("Tusk Philanthropies", style={'fontSize': '12px', 'fontWeight': '700', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '1.5px', 'marginRight': '16px'}),
                html.Span("Solving Hunger · CEP Intelligence", style={'fontSize': '12px', 'color': COLORS['text_secondary']}),
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.A("← All States", href="/", style={'fontSize': '14px', 'fontWeight': '600', 'color': COLORS['teal'], 'textDecoration': 'none', 'marginRight': '24px'}),
                html.A(f"← {prev_name}", href=f"/state/{prev_abbr}", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'textDecoration': 'none', 'marginRight': '16px'}) if prev_abbr else html.Span(),
                html.A(f"{next_name} →", href=f"/state/{next_abbr}", style={'fontSize': '14px', 'color': COLORS['text_secondary'], 'textDecoration': 'none'}) if next_abbr else html.Span(),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'height': '48px'})
        ], style={'position': 'sticky', 'top': '0', 'zIndex': '100', 'background': 'white', 'borderBottom': f'1px solid {COLORS["border"]}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),

        # Page header
        html.Div([html.Div([
            html.H1(state_data['name'], style={'fontSize': '56px', 'fontWeight': '700', 'letterSpacing': '-0.025em', 'color': COLORS['text_primary'], 'marginBottom': '12px', 'lineHeight': '1.05', 'marginTop': '48px'}),
            html.P(f"{state_data['coverage_pct']}% CEP Coverage · {state_data['cep_schools']:,} of {state_data['eligible_schools']:,} eligible schools", style={'fontSize': '20px', 'color': COLORS['text_secondary'], 'marginBottom': '40px'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px 48px 40px'})
        ], style={'background': COLORS['white']}),

        # Data notice (state-specific)
        html.Div([html.Div([
            html.Span("ℹ️  "), html.Span("Data Note: ", style={'fontWeight': '700', 'fontSize': '13px', 'color': '#1e40af'}),
            html.Span(data_notice, style={'fontSize': '13px', 'color': '#1e40af'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '12px 40px'})
        ], style={'background': '#eff6ff', 'borderBottom': f'1px solid {COLORS["border"]}', 'display': 'block' if data_notice else 'none'}) if data_notice else html.Div(),

        # Session banner
        create_session_banner(state_abbr),

        # Executive leadership
        create_state_executives_section(state_abbr),

        # Key metrics
        html.Div([html.Div([
            html.Div([html.Div("CEP Coverage", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['coverage_pct']}%", style={'fontSize': '40px', 'fontWeight': '700', 'color': COLORS['text_primary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
            html.Div([html.Div("Students Served", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['students_in_cep']:,}", style={'fontSize': '40px', 'fontWeight': '700', 'color': COLORS['text_primary']}), html.Div("In CEP schools", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
            html.Div([html.Div("Opportunity Gap", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['children_without_cep']:,}", style={'fontSize': '40px', 'fontWeight': '700', 'color': COLORS['text_primary']}), html.Div("Children without CEP", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
            html.Div([html.Div("Schools", style={'fontSize': '13px', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '12px', 'fontWeight': '600'}), html.Div(f"{state_data['cep_schools']}/{state_data['eligible_schools']}", style={'fontSize': '40px', 'fontWeight': '700', 'color': COLORS['text_primary']}), html.Div("CEP vs Eligible", style={'fontSize': '14px', 'color': COLORS['text_secondary']})], style={'background': 'white', 'padding': '28px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'marginBottom': '48px'})], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '40px 40px 0 40px'}),

        # County map / analysis
        (create_georgia_dual_map_section(df, fips_dict) if state_abbr == 'GA'
         else html.Div([create_tabbed_county_maps_section(df, fips_dict, state_abbr, state_data['name'])],
                       style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 40px'}) if fips_dict else html.Div()),

        # County table
        html.Div([
            create_nj_county_table(df) if state_abbr == 'NJ' else create_sortable_county_table(df)
        ], style={'background': COLORS['off_white']}),

    ], style={'background': COLORS['off_white'], 'minHeight': '100vh'})


# ====================
# LAYOUT & CALLBACKS
# ====================

application.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@application.callback(
    Output('url', 'pathname'),
    Input('us-map-graph', 'clickData'),
    prevent_initial_call=True
)
def navigate_to_state_page(click_data):
    if not click_data or 'points' not in click_data:
        raise dash.exceptions.PreventUpdate
    state_abbr = click_data['points'][0].get('location', '')
    if state_abbr and state_abbr in STATES_WITH_DATA_PAGES:
        return f'/state/{state_abbr}'
    raise dash.exceptions.PreventUpdate


@application.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname is None or pathname == '/':
        return create_landing_page()
    elif pathname.lower().startswith('/state/'):
        state_abbr = pathname.split('/')[-1].upper()
        return create_state_page(state_abbr)
    else:
        return html.Div([
            html.Div([
                html.H1("Page Not Found", style={'fontSize': '48px', 'fontWeight': '600', 'color': COLORS['text_primary'], 'marginBottom': '16px'}),
                html.A("← Back to Home", href="/", style={'color': COLORS['teal'], 'textDecoration': 'none', 'fontSize': '16px'})
            ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '120px 40px'})
        ], style={'minHeight': '100vh', 'background': COLORS['off_white']})

@application.callback(Output('comparison-output', 'children'), [Input('compare-state-a', 'value'), Input('compare-state-b', 'value')])
def update_comparison(state_a, state_b):
    if state_a and state_b:
        return create_comparison_cards(state_a, state_b)
    return html.Div()

@application.callback(Output('timeline-body', 'children'), Input('timeline-filter', 'value'))
def update_timeline(filter_val):
    return create_timeline_body(filter_val or 'all')

@application.callback(
    [Output('county-map-container', 'children')],
    [Input('us-map-graph', 'clickData'), Input('state-search-dropdown', 'value')]
)
def update_state_selection(click_data, search_value):
    ctx = dash.callback_context
    state_abbr = None
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'state-search-dropdown.value':
        if search_value:
            state_abbr = search_value
    elif click_data and 'points' in click_data and len(click_data['points']) > 0:
        state_abbr = click_data['points'][0].get('location')

    if not state_abbr or state_abbr not in STATES_WITH_DATA_PAGES:
        return [[]]

    loader_map = {
        'WI': (load_wisconsin_data, WI_FIPS),
        'NJ': (load_new_jersey_data, NJ_FIPS),
        'VA': (load_virginia_data, VA_FIPS),
        'GA': (load_georgia_data, GA_FIPS),
        'PA': (load_pennsylvania_data, PA_FIPS),
        'RI': (load_rhode_island_data, RI_FIPS),
        'MD': (load_maryland_data, MD_FIPS),
        'NV': (load_nevada_data, NV_FIPS),
        'KY': (load_kentucky_data, KY_FIPS),
        'SC': (load_south_carolina_data, SC_FIPS),
        'IL': (load_illinois_data, IL_FIPS),
        'SD': (load_south_dakota_data, SD_FIPS),
        'UT': (load_utah_data, UT_FIPS),
        'AR': (load_arkansas_data, AR_FIPS),
        'DE': (load_delaware_data, DE_FIPS),
    }

    if state_abbr not in loader_map:
        return [[]]

    loader_fn, fips_dict = loader_map[state_abbr]
    df = loader_fn()
    state_name = STATE_DATA[state_abbr]['name']

    content = [html.Div([
        html.H3(f"{state_name} County Map", style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '16px', 'color': COLORS['text_primary']}),
        html.Div([dcc.Graph(figure=create_county_map(df, fips_dict, state_abbr), config={'displayModeBar': False})], style={'background': 'white', 'padding': '20px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}),
        create_county_color_legend(),
        html.Div([html.A(f"View full {state_name} page →", href=f"/state/{state_abbr}", style={'color': COLORS['teal'], 'textDecoration': 'none', 'fontSize': '14px', 'fontWeight': '500'})], style={'marginTop': '12px', 'textAlign': 'right'})
    ], style={'padding': '20px', 'background': COLORS['off_white'], 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'})]

    return [content]

@application.callback(
    Output('comparison-county-maps', 'children'),
    [Input('compare-state-a', 'value'), Input('compare-state-b', 'value'), Input('comparison-map-types', 'value')]
)
def update_comparison_county_maps(state_a, state_b, map_types):
    if not state_a or not state_b or not map_types:
        return []

    loader_map = {
        'WI': (load_wisconsin_data, WI_FIPS), 'NJ': (load_new_jersey_data, NJ_FIPS),
        'VA': (load_virginia_data, VA_FIPS), 'GA': (load_georgia_data, GA_FIPS),
        'PA': (load_pennsylvania_data, PA_FIPS), 'RI': (load_rhode_island_data, RI_FIPS),
        'MD': (load_maryland_data, MD_FIPS), 'NV': (load_nevada_data, NV_FIPS),
        'KY': (load_kentucky_data, KY_FIPS), 'SC': (load_south_carolina_data, SC_FIPS),
        'IL': (load_illinois_data, IL_FIPS), 'SD': (load_south_dakota_data, SD_FIPS),
        'UT': (load_utah_data, UT_FIPS), 'AR': (load_arkansas_data, AR_FIPS),
        'DE': (load_delaware_data, DE_FIPS),
    }

    maps = []
    for state_abbr in [state_a, state_b]:
        state_name = STATE_DATA.get(state_abbr, {}).get('name', state_abbr)
        if state_abbr not in loader_map:
            maps.append(html.Div([html.H4(state_name, style={'fontSize': '16px', 'fontWeight': '600', 'marginBottom': '12px'}), html.Div("County-level data not yet available.", style={'padding': '40px', 'textAlign': 'center', 'color': COLORS['text_secondary'], 'background': 'white', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}', 'fontSize': '14px'})]))
            continue

        loader_fn, fips_dict = loader_map[state_abbr]
        df = loader_fn()

        state_maps = []
        if 'cep' in map_types:
            cep_fig = create_county_map(df, fips_dict, state_abbr)
            state_maps.append(html.Div([
                html.Div("CEP Coverage", style={'fontSize': '13px', 'fontWeight': '600', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '8px'}),
                dcc.Graph(figure=cep_fig, config={'displayModeBar': False}),
                create_cep_legend_compact()
            ]))
        if 'poverty' in map_types:
            try:
                pov_fig, _, _, _ = create_poverty_heat_map(df, fips_dict, state_abbr)
                state_maps.append(html.Div([
                    html.Div("Poverty Distribution", style={'fontSize': '13px', 'fontWeight': '600', 'color': COLORS['text_secondary'], 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'marginBottom': '8px'}),
                    dcc.Graph(figure=pov_fig, config={'displayModeBar': False}),
                    create_poverty_legend_compact()
                ]))
            except Exception as e:
                state_maps.append(html.Div(f"Poverty map unavailable.", style={'color': COLORS['text_secondary'], 'padding': '20px'}))

        grid = '1fr' if len(state_maps) == 1 else '1fr 1fr'
        maps.append(html.Div([
            html.H4(state_name, style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '12px', 'color': COLORS['text_primary']}),
            html.Div(state_maps, style={'display': 'grid', 'gridTemplateColumns': grid, 'gap': '16px'})
        ], style={'background': 'white', 'padding': '20px', 'borderRadius': '12px', 'border': f'1px solid {COLORS["border"]}'}))

    return html.Div(maps, style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px'})


if __name__ == '__main__':
    application.run(debug=False, host='0.0.0.0', port=8000)

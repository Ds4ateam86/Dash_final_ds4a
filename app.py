#libraries
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc


#from callbacks import register_callbacks


request_path_prefix = "/"

# Dash instance declaration
app = dash.Dash(__name__, plugins=[dl.plugins.pages], requests_pathname_prefix=request_path_prefix, external_stylesheets=[dbc.themes.DARKLY],)


#Top menu, items get from all pages registered with plugin.pages
navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink( "Home Page", href=request_path_prefix)),
    dbc.DropdownMenu(
        [

            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Subjects",
    ),
    dbc.NavItem(dbc.NavLink("Team", href='team')),
    ],
    brand="DS4A Project - Analysis of illegal crops and their relationship to Colombian laws passed by Congress  -Team 86",
    color="primary",
    dark=True,
    className="mb-2",
)

#Main layout
app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
    ],
    className="dbc",
    fluid=True,
)

# Call to external function to register all callbacks
#register_callbacks(app)


# This call will be used with Gunicorn server
server = app.server


# Testing server, don't use in production, host
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)
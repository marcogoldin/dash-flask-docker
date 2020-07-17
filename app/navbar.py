import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():

	navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Dash Home", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="",
        ),
    ],
    color="primary",
    dark=True,
	)

	return navbar
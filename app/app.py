######################################
# Caleb Sellinger
# 44-630 Continuous Intelligence
# Dr. Case
# 12-5-2024
######################################

#####################
# Imports
#####################

import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins
from pathlib import Path

# Load dataset into program
df = palmerpenguins.load_penguins()

css_file = Path(__file__).parent / "styles.css"
ui.include_css(css_file)

# Page options for Shiny
ui.page_opts(title="Penguins dashboard", fillable=True)

#################
# Sidebar
#################

with ui.sidebar(title="Filter controls"):
    # Slider component, ID, display title, min value, max value, default value
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Checkbox, ID, Display title, choices, default selected choices
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # .hr method used to separate elements with a line
    ui.hr()
    # Header, size 6
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    # .a method used to insert link
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

########################
# Main Content (Body)
########################

# Grid-like layout, wraps a 1d sequence of UI elements into a 2d grid
with ui.layout_column_wrap(fill=False):
    # An opinionated box designed for displaying a title, value, and any other child components
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    # For Bootstrap components, general purpose container for grouping related UI elements
    with ui.card(full_screen=True):
        # Header for card component
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            # DataGrid holds data and options for spreadsheet view of a data frame
            return render.DataGrid(filtered_df()[cols], filters=True)

# Reactive Calc funtion for filtering data
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

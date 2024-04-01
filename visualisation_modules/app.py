from utility_modules.constants import APP
from visualisation_modules import visualisations


def run_app():
    visualisations.HistogramVisualisationModule.create_component()
    APP.run_server(debug=True)
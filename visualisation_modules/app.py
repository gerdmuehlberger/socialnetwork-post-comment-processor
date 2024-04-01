from utility_modules.constants import APP
from visualisation_modules import visualisations

def run_app(dataframe):
    visualisations.BarChartVisualisationModule.create_component(dataframe=dataframe,
                                                                x_axis=dataframe["sentiment_label"].unique(),
                                                                y_axis=dataframe["sentiment_label"].value_counts())
    
    APP.run_server(debug=True)
import pandas as pd
from data_processing_components import get_bridge_road_data, add_intersections, add_traffic

if __name__ == "__main__":
    # merge road and bridge data in the right format
    data = get_bridge_road_data(pd.read_csv("../data/raw/_roads3.csv"),
                                pd.read_excel(
                                    '../data/raw/BMMS_overview.xlsx', engine='openpyxl'),
                                ['N1', 'N2'],
                                "N",
                                25)

    # add the intersections at the right places
    data = add_intersections(data)

    # add the traffic data
    data = add_traffic(data,
                            "../data/raw/traffic/")

    # save data
    data.to_csv("../data/processed/N1_N2_plus_sideroads.csv", index=None)

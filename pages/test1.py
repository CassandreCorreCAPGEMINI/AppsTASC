from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode
import pandas as pd
import streamlit as st

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')


gb = GridOptionsBuilder.from_dataframe(df)
# enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=False)
gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
gridOptions = gb.build()

response = AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )

st.text("Test data shape:"+str(df.shape))
dtf = pd.DataFrame(response["selected_rows"])
st.subheader("Filtered data will appear below 👇 ")
st.text("")
st.dataframe(dtf)
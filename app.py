#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   tasc.py
@Time    :   2025/03/25 11:11
@Author  :   Akhli RIOUFFREYT
@Version :   1.0
@Contact :   akhli.riouffreyt@capgemini.com
"""

# here put the import lib

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(page_title="TASC Welcome page",page_icon="random",layout="wide")
    st.image("TASC-orange-horizontal-logo.png",width=500)

    st.write("# Welcome to Project TASC! ")

    st.sidebar.success("Select an app above.")

    st.markdown(
        """
       
        ** 👈 Select an app from the sidebar** to see some examples
      
        - This app "Generative AI for contract management" is an easy-to-use interface built with Streamlit.
        - Our app is using Capgemini Generative Engine. 
    """
    )

    with st.expander("ℹ️ - About this app", expanded=True):

        st.write(
        """
Solution:     
-   Contract Drafting 
-   Contract Extract  
-   Contract Compare
-   Contract Inconsistencies
-   Contract Terms Search

Benefits:
-   Generative AI  can significantly reduce the time required to process contracts.
-   Reducing their reliance on legal professionals for routine work, lowering overall legal costs.

	    """
    )


if __name__ == "__main__":
    run()

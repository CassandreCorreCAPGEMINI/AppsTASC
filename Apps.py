# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(page_title="TASC Weolcome page",page_icon="random",layout="wide")
    st.image("TASC-orange-horizontal-logo.png",width=500)

    st.write("# Welcome to Project TASC! ")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Comment optimiser des processus logistiques et d’achats par les techniques d’IA et de Blockchain

        ** 👈 Select a demo from the sidebar** to see some examples
      
        ### ​​Objectifs
        - Concevoir une solution BC pour traiter, sécuriser et gerer les données multi-partenaires, de façon à proteger les clients des risques fournisseurs.​
        - Proposer les solutions IA pour aider les membres d”une SC dans leurs taches de classification d’incidents, d’analyse de données fournisseurs. ​
        - Concevoir une solution pour transformer automatiquement des contrats en code Blockchain dits “Smart Legal Contrats”, connectés aux données des SI de la supply chain.​---
        - Concevoir un systeme logistique responsable fondé sur des technologies 4.0​
        
    """
    )


if __name__ == "__main__":
    run()

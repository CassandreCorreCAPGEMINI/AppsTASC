#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Pody.py
@Time    :   2022/07/12 11:13:03
@Author  :   Xin HUANG 
@Version :   1.0
@Contact :   xin.huang@altran.com
'''

# here put the import lib



import streamlit as st

from streamlit_agraph import agraph, Node, Edge, Config

config = Config(width=1000, 
                height=500, 
                # **kwargs
                ) 

entity = st.text_input(label='Searched Entity',value="Baimtec Material")


if st.button(label="submit"): 

    nodes = []
    edges = []
    nodes.append( Node(id="Baimtec Material", 
                   label="Baimtec Material", 
                   size=25, 
                   shape="circular") 
            ) # includes **kwargs
    nodes.append( Node(id="Airbus",
                   label="Airbus",
                   size=25,
                   shape="circular") 
            )
    edges.append( Edge(source="Baimtec Material", 
                   label="suplier of", 
                   target="Airbus", 
                   # **kwargs
                   ) 
            ) 
    nodes.append( Node(id="MEU",
                   label="MEU list",
                   size=25,
                   shape="circular") 
            )

    edges.append( Edge(source="Baimtec Material", 
                   label="in", 
                   target="MEU", 
                   # **kwargs
                   ) 
            ) 
    nodes.append( Node(id="China",
                   label="China",
                   size=25,
                   shape="circular") 
            )
    edges.append( Edge(source="Baimtec Material", 
                   label="locate in", 
                   target="China", 
                   # **kwargs
                   ) 
            ) 

    nodes.append( Node(id="Titanium_Pump_Casting",
                   label="United States Titanium Pump Casting",
                   size=25,
                   shape="circular") 
            )

    edges.append( Edge(source="Baimtec Material", 
                   label="has product", 
                   target="Titanium_Pump_Casting", 
                   # **kwargs
                   ) 
            ) 
    nodes.append( Node(id="U.S. Titanium Industry Inc.",
                   label="U.S. Titanium Industry Inc.",
                   size=25,
                   shape="circular") 
            )
    edges.append( Edge(source="U.S. Titanium Industry Inc.", 
                   label="has product", 
                   target="Titanium_Pump_Casting", 
                   # **kwargs
                   ) 
            ) 
    nodes.append( Node(id="All Metal Sales, Inc",
                   label="All Metal Sales, Inc",
                   size=25,
                   shape="circular") 
            )
    edges.append( Edge(source="All Metal Sales, Inc", 
                   label="has product", 
                   target="Titanium_Pump_Casting", 
                   # **kwargs
                   ) 
            ) 
    edges.append( Edge(source="Titanium_Pump_Casting", 
                   label="part of", 
                   target="A320", 
                   # **kwargs
                   ) 
            ) 
    nodes.append( Node(id="A320",
                   label="A320",
                   size=25,
                   shape="circular") 
            )
    edges.append( Edge(source="Airbus", 
                   label="has product", 
                   target="A320", 
                   # **kwargs
                   ) 
            ) 

    return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

# Currently not workin since update to agraph 2.0 - work in progress
# from rdflib import Graph
# from streamlit_agraph import TripleStore, agraph

# graph = Graph()
# graph.parse("http://www.w3.org/People/Berners-Lee/card")
# print("length of graph",len(graph))
# store = TripleStore()

# for subj, pred, obj in graph:
#     # print(subj, pred, obj)
#     store.add_triple(subj, pred, obj, "")
    
# return_value = agraph(list(store.getNodes()), list(store.getEdges()), config)
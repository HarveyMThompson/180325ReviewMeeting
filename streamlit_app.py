# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:00:05 2024

@author: harveythompson
"""

import streamlit as st

financial_page = st.Page("v4st_financial_CMTscco2.py", title="Financial cost (£)")
emissions_page = st.Page("v4st_CO2eq_CMTscco2.py",title="Emissions (kg CO2eq)")

pg = st.navigation([financial_page, emissions_page])
pg.run()
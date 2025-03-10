# Program to calculate quantities relevent to LCA assessment of cooling methods
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import streamlit as st

############################
# scCO2 system parameters
############################

# Carry out CO2 equivalent and financial calculations
def scco2_financial_calcs():

    machhrs_per_yr = st.session_state.machhrs_per_yr
    scco2_elec_pump_power  = st.session_state.scco2_elec_pump_power # kW
    scco2_elec_per_yr = machhrs_per_yr*scco2_elec_pump_power   # kWh
    scco2_flow_rate = st.session_state.scco2_flow_rate    # kg/hr
    scco2_per_yr = scco2_flow_rate*machhrs_per_yr    # kg/yr
    scco2_air_per_yr = st.session_state.scco2_air_flow_rate*machhrs_per_yr      # m^3/yr
    scco2_elec_air_per_yr = scco2_air_per_yr*CI_elecp   # kWh/yr
     
    #########################
    # Financial Calcs
    #########################
    cost_elecs = scco2_elec_per_yr*st.session_state.cost_elec_per_kWh
    cost_c = scco2_per_yr*st.session_state.cost_CO2_per_kg
    cost_elecp = scco2_elec_air_per_yr*st.session_state.cost_elec_per_kWh
    cost_mql =  st.session_state.mql_per_yr*st.session_state.cost_mql_per_ltr

    # costs for tools
    tool_life_hrs = st.session_state.tool_life_mins/60.0
    ntools = machhrs_per_yr/tool_life_hrs
    cost_tool = ntools*st.session_state.cost_tool
    cost_mec = cost_elecs + cost_c + cost_elecp + cost_mql + cost_tool

    # operator costs
    cost_operator = st.session_state.hrly_op_cost*machhrs_per_yr
    cost_mec_with_operator = cost_mec + cost_operator
    
    # create calcs dictionary
    calcs = dict()
    st.session_state.cost_elecs=cost_elecs
    st.session_state.cost_c=cost_c
    st.session_state.cost_elecp=cost_elecp
    st.session_state.cost_mql=cost_mql
    st.session_state.cost_mec=cost_mec
    st.session_state.cost_tool=cost_tool
    st.session_state.cost_mec_with_operator = cost_mec_with_operator

    return

# end emulsion_calcs

# plotting financial costs barchart
def plot_scco2_financial_barchart():
    
    cost_elecs = st.session_state.cost_elecs
    cost_c = st.session_state.cost_c
    cost_elecp = st.session_state.cost_elecp
    cost_mec = st.session_state.cost_mec
    cost_mql = st.session_state.cost_mql
    cost_tool = st.session_state.cost_tool

    species = (
        "Costs (£) from scco2 cooling (excluding operator costs)",
    )
    weight_counts = {
        "Electricity": np.array([cost_elecs+cost_elecp,0]),
        "Nozzle CO2": np.array([cost_c,0]),
        "MQL": np.array([cost_mql,0]),
        "Tools": np.array([cost_tool,0]),
    }
    width = 0.2

    fig, ax = plt.subplots(figsize=(4,5))
    bottom = np.zeros(2)

    for boolean, weight_count in weight_counts.items():
        p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
        bottom += weight_count

    ax.set_title("Costs (£) from scCO2 cooling (excluding operators)")
    ax.legend(loc="center")
    ax.set_ylabel('Costs (£)')

    return plt

# end plot_barchart

##############
# Main program
##############
# Add heading and introductory text
st.set_page_config(layout='wide')

st.title("ScCO2 + MQL financial cost")
st.markdown("---")

tab1, tab2 = st.tabs(["Financial cost calculator", "Financial cost bar chart"])

# Cost calculator tab
with tab1:
    
    # Create the input slides - Row 1
    row1 = st.columns([1,1,1])

    #  Total Annual machining Hours
    default_value = 2000.0
    st.session_state.machhrs_per_yr = default_value
    machhrs_per_yr = row1[0].slider("Annual Machining Hours", 1000.00, 2000.00, default_value)
    st.session_state.machhrs_per_yr = machhrs_per_yr

    #  Hourly Operator Cost
    default_value = 60.0
    st.session_state.hrly_op_cost = default_value
    hrly_op_cost = row1[1].slider("Hourly Operator Cost (£)", 20.00, 100.00, default_value)
    st.session_state.hrly_op_cost = hrly_op_cost

    #  CO2 Cost (£/kg)
    default_value = 1.00
    st.session_state.cost_CO2_per_kg = default_value
    cost_CO2_per_kg = row1[2].slider("CO2 Cost (£/kg)", 0.50, 2.00, default_value)
    st.session_state.cost_CO2_per_kg = cost_CO2_per_kg

    # Create the input slides - Row 2
    row2 = st.columns([1,1,1])

    #  Nozzle diameter (mm)
    default_value = 0.3
    st.session_state.d_nozzle = default_value
    d_nozzle = row2[0].slider("Nozzle diameter (mm)", 0.1, 0.5, default_value)
    st.session_state.d_nozzle = d_nozzle
    st.session_state.scco2_flow_rate = 132.66*(d_nozzle**1.7057)  # kg/hr
    st.session_state.scco2_air_flow_rate = 42.399*(d_nozzle**0.9672)   # m^3/hr

    #  Tool Cost
    default_value = 12.0
    st.session_state.cost_tool = default_value
    cost_tool = row2[1].slider("Tool Cost (£)", 10.0, 40.00, default_value)
    st.session_state.cost_tool = cost_tool

    #  Tool Life (mins)
    default_value = 60.0
    st.session_state.tool_life_mins = default_value
    tool_life_mins = row2[2].slider("Tool Life (mins)", 30.0, 120.00, default_value)
    st.session_state.tool_life_mins = tool_life_mins

    # Create the input slides - Row 3
    row3 = st.columns([1,1,1])

    #  MQL cost (£/litre)
    default_value = 17.5
    st.session_state.cost_mql_per_ltr = default_value
    cost_mql_per_ltr = row3[0].slider("MQL cost (£/litre)", 10.0, 30.00, default_value)
    st.session_state.cost_mql_per_ltr = cost_mql_per_ltr

    #  MQL consumption (l/yr)
    default_value = 80.0
    st.session_state.mql_per_yr = default_value
    mql_per_yr = row3[1].slider("MQL consumption (l/yr)", 50.0, 100.0, default_value)
    st.session_state.mql_per_yr = mql_per_yr

    #  Electricity cost £/kWh
    default_value = 0.21
    st.session_state.cost_elec_per_kWh = default_value
    cost_elec_per_kWh = row3[2].slider("Electricity cost (£/kWh)", 0.2, 0.4, default_value)
    st.session_state.cost_elec_per_kWh = cost_elec_per_kWh

    # Create the input slides - Row 4
    row4 = st.columns([1,1,1])

    #  Pneumatic air volume energy conversion factor m^3/kWh
    default_value = 0.11
    st.session_state.CI_elecp = default_value
    CI_elecp = row4[0].slider("Pneumatic air energy factor (kWh/m3)", 0.1, 0.2, default_value)
    st.session_state.CI_elecp = CI_elecp

    #  Electric pumping power kW
    default_value = 0.311
    st.session_state.scco2_elec_pump_power = default_value
    scco2_elec_pump_power = row4[1].slider("Electrical pumping power (kW)", 0.2, 0.4, default_value)
    st.session_state.scco2_elec_pump_power = scco2_elec_pump_power

    # Carry out financial cost calculations
    calcs = scco2_financial_calcs()
    output_str = "Annual financial cost = £{0:.2f}".format(st.session_state.cost_mec_with_operator)
    st.write(output_str)

# Financial cost bar chart tab
with tab2: 
    plt = plot_scco2_financial_barchart() 
    st.pyplot(plt)


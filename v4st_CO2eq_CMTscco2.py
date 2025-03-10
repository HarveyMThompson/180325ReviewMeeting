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

# Carry out CO2 equivalent calculations
def scco2_CO2eq_calcs():

    scco2_CEfactor = st.session_state.scco2_CEfactor
    CI_elecs = st.session_state.CI_elecs
    CI_elecp = st.session_state.CI_elecp
    machhrs_per_yr = st.session_state.machhrs_per_yr
    scco2_elec_pump_power  = st.session_state.scco2_elec_pump_power # kW
    scco2_elec_per_yr = machhrs_per_yr*scco2_elec_pump_power   # kWh
    scco2_flow_rate = st.session_state.scco2_flow_rate    # kg/hr
    scco2_per_yr = scco2_flow_rate*machhrs_per_yr    # kg/yr
    scco2_air_per_yr = st.session_state.scco2_air_flow_rate*machhrs_per_yr      # m^3/yr
    scco2_elec_air_per_yr = scco2_air_per_yr*CI_elecp   # kWh/yr

    #########
    # CElecs
    #########
    CE_elecs = scco2_elec_per_yr*CI_elecs    # kg CO2
    
    ######
    # CEc
    ######
    CE_c = scco2_per_yr*scco2_CEfactor

    ######
    # CE_elecp
    ######
    CE_elecp = scco2_elec_air_per_yr*CI_elecs    # kg CO2/yr

    # Embedded carbon in consumed tools
    CE_embedded_tool =st.session_state.CE_embedded_tool
    tool_life_mins = st.session_state.tool_life_mins
    tool_life_hrs = tool_life_mins/60.0
    ntools = machhrs_per_yr/tool_life_hrs
    CE_tool = ntools*CE_embedded_tool

    # total CE emissions
    CE_mec = CE_elecs + CE_c + CE_elecp + CE_tool

    st.session_state.CE_elecs=CE_elecs
    st.session_state.CE_c=CE_c
    st.session_state.CE_elecp=CE_elecp
    st.session_state.CE_mec=CE_mec
    st.session_state.CE_tool=CE_tool

    return

# end emulsion_calcs

# plotting CO2 eq barchart
def plot_scco2_CO2eq_barchart():
    
    CE_elecs = st.session_state.CE_elecs
    CE_c = st.session_state.CE_c
    CE_elecp = st.session_state.CE_elecp
    CE_mec = st.session_state.CE_mec
    CE_tool = st.session_state.CE_tool

    species = (
        "CE emissions (kg) from scco2 cooling",
    )
    weight_counts = {
        "Electricity": np.array([CE_elecs+CE_elecp,0]),
        "Nozzle CO2": np.array([CE_c,0]),
        "Tools": np.array([CE_tool,0]),
    }
    width = 0.2

    fig, ax = plt.subplots(figsize=(2.3,2.3))
    bottom = np.zeros(2)

    for boolean, weight_count in weight_counts.items():
        p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
        bottom += weight_count

    ax.set_title("CO2eq emissions (kg)")
    ax.legend(loc="center")
    ax.set_ylabel('Annual CO2eq emissions (kg)')

    return plt


##############
# Main program
##############
# Add heading and introductory text
st.set_page_config(layout='wide')

st.title("ScCO2 + MQL emissions")
st.markdown("---")

tab1, tab2 = st.tabs(["CO2eq cost calculator", "CO2eq cost bar chart"])

# Cost calculator tab
with tab1:
    
    # Create the input slides - Row 1
    row1 = st.columns([1,1,1])

    #  Total Annual machining Hours
    default_value = 2000.0
    st.session_state.machhrs_per_yr = default_value
    machhrs_per_yr = row1[0].slider("Annual machining hours", 1000.00, 2000.00, default_value)
    st.session_state.machhrs_per_yr = machhrs_per_yr
    
    #  Supercritical CO2 CO2eq Cost (kg/kg)
    default_value = 1.00
    st.session_state.scco2_CEfactor = default_value
    scco2_CEfactor = row1[1].slider("Supercritical Ce2 CO2eq factor (kg/kg)", 0.50, 2.00, default_value)
    st.session_state.scco2_CEfactor = scco2_CEfactor

    #  Nozzle diameter (mm)
    default_value = 0.3
    st.session_state.d_nozzle = default_value
    d_nozzle = row1[2].slider("Nozzle diameter (mm)", 0.1, 0.5, default_value)
    st.session_state.d_nozzle = d_nozzle
    st.session_state.scco2_flow_rate = 132.66*(d_nozzle**1.7057)  # kg/hr
    st.session_state.scco2_air_flow_rate = 42.399*(d_nozzle**0.9672)   # m^3/hr

    # Create the input slides - Row 2
    row2 = st.columns([1,1,1])

    #  Electrical pumping power kW
    default_value = 0.311
    st.session_state.scco2_elec_pump_power = default_value
    scco2_elec_pump_power = row2[0].slider("Electrical pumping power (kW)", 0.2, 0.4, default_value)
    st.session_state.scco2_elec_pump_power = scco2_elec_pump_power

    #  Pneumatic air volume energy conversion factor m^3/kWh
    default_value = 0.11
    st.session_state.CI_elecp = default_value
    CI_elecp = row2[1].slider("Pneumatic air energy factor (kWh/m3)", 0.1, 0.2, default_value)
    st.session_state.CI_elecp = CI_elecp

    #  Carbon Intensity of Electricity
    default_value = 0.149
    CI_elecs = row2[2].slider("Carbon Intensity of electricity (kg CO2eq/kWh)", 0.1, 0.5, default_value)
    st.session_state.CI_elecs = CI_elecs
      
    # Create the input slides - Row 3
    row3 = st.columns([1,1,1])

    #  Tool Life (mins)
    default_value = 60.0
    st.session_state.tool_life_mins = default_value
    tool_life_mins = row3[0].slider("Tool life (mins)", 30.0, 120.00, default_value)
    st.session_state.tool_life_mins = tool_life_mins

    #  Embedded CO2eq carbon in tools kg/kg
    default_value = 0.24
    st.session_state.CE_embedded_tool = default_value
    CE_embedded_tool = row3[1].slider("Embedded tool carbon (kg/kg)", 0.1, 0.5, default_value)
    st.session_state.CE_embedded_tool = CE_embedded_tool

    # Carry out financial cost calculations
    calcs = scco2_CO2eq_calcs()
    output_str = "Annual emissions: {0:.2f}".format(st.session_state.CE_mec)+"kg CO2eq"
    st.write(output_str)

# Financial cost bar chart tab
with tab2: 
    plt = plot_scco2_CO2eq_barchart() 
    st.pyplot(plt)


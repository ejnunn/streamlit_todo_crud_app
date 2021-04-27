import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
import csv
import os


HTML_BANNER = """
	<div style="background-color:#464e5f;padding:10px;border-radius:10px">
	<h1 style="color:white;text-align:center;">MES Placard Generator</h1>
	<p style="color:white;text-align:center;">Built with Streamlit</p>
	</div>
	"""

@st.cache(show_spinner=False)
def load_data(path):
	return pd.read_csv(path)

def main():
	stc.html(HTML_BANNER)

	wo_data = load_data('workorders.csv')
	
	
	form_column_names = ['ctrl_point_id', 'energy_type', 'magnitude', 'subsystem', 'lockout_proced', 'verify_proced']

	menu = ["Work Order", "Manual"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Work Order":
		workorder = st.text_input('Work Order Number', '')
		curr_wo = wo_data.loc[wo_data['workorder'] == workorder]
		st.write("Work Order Details", curr_wo)

		filename = 'data/{}_energy_sources.csv'.format(workorder)
		if os.path.exists(filename):
			energy_sources_df = pd.read_csv(filename)
		else:
			energy_sources_df = pd.DataFrame(columns=form_column_names)

		if st.button('Restart MES Placard'):
			energy_sources_df = pd.DataFrame(columns=form_column_names)
			energy_sources_df.to_csv(filename, index=False)

		st.subheader("Add Energy Sources")
		col1,col2 = st.beta_columns(2)
		
		with col1:
			energy_type = st.selectbox("Energy Source Type", ["Electrical", "Hydraulic", 'Water', 'Air Pressure', 'Vacuum', 'Chemical', 'Gravitational'])

		with col2:
			ctrl_point_id = ENERGY_ABREVS[energy_type] + str(len(energy_sources_df.loc[energy_sources_df['energy_type'] == energy_type])+1)
			magnitude = ''
			subsystem = st.text_input("Subsystem (Leave blank if N/A)", "")
			lockout_proced = ''
			verify_proced = ''
			if energy_type == "Electrical":
				device = st.selectbox("Device",["Disconnect","Circuit Breaker","Plug/Cord"])
				magnitude = st.selectbox('Voltage', ['120V', '240V', '480V'])


				lockout_proced = LOCKOUT_PROCEDURES[energy_type][device].replace('_', magnitude)
				verify_proced = VERIFY_PROCEDURES[energy_type][device].replace('_', magnitude)
	
		if st.button("Add Energy Source"):
			energy_source_dict = {'ctrl_point_id':ctrl_point_id, 'energy_type':energy_type, 'magnitude':magnitude, 'subsystem':subsystem, 'lockout_proced':lockout_proced, 'verify_proced':verify_proced}
			energy_sources_df.loc[len(energy_sources_df)] = energy_source_dict
			energy_sources_df.to_csv(filename, index=False)
		st.write(energy_sources_df)







	elif choice == "Manual":
		asset_name = st.text_input('Asset Name', '')
		cmms_equipment_id = st.text_input('CMMS Equipment #', '')
		property_id = st.text_input('Boeing Property ID', '')
		equipment_manufacturer = st.text_input('Equipment Manufacturer', '')
		equipment_model = st.text_input('Equipment Model', '')
		location_building = st.text_input('Building', '')
		location_floor = st.text_input('Floor', '')
		location_column = st.text_input('Column', '')




LOCKOUT_PROCEDURES = {'Electrical':{'Disconnect': 'Place disconnect switch in the off position and apply multiple lockout device, tag and personal padlock. Shuts off electrical power to the _ circuits.',
									'Circuit Breaker':'At _ power distribution panel, place circuit breaker in the off position and apply multiple lockout device, tag and personal padlock. Shuts off electrical power to the circuit.',
									'Plug/Cord': 'Remove plug from receptable or connector and maintain physical control to prevent re-energization. If improactical to maintain control of plug, apply plug lockout device, multiple lockout device, tag and personal padlock.'
									}
					}

VERIFY_PROCEDURES = {'Electrical':{'Disconnect': 'Test the _ electrical circuits and indicators powered by this disconnect switch. They should not turn on and no action should occur. Attempt to start or operate the equipment.',
									'Circuit Breaker': 'Test the _ electrical circuits powered by this circuit breaker with test equipment to ensure no electrical power. The circuits and indicators must not turn on and action must not occur.',
									'Plug/Cord': 'Attempt to start or operate the equipment that is powered by this cord. The electrical circuits and indicators must not turn on and action must not occur.'
									}
					}

ENERGY_ABREVS = {'Electrical':'E',
					'Hydraulic':'H',
					'Air Pressure':'P',
					'Gas':'G',
					'Chemical':'C',
					'Steam': 'S',
					'Hot Water':'T',
					'Other':'X'}



if __name__ == '__main__':
	main()


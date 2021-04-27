import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
import csv
import os

# Data Viz Pkgs
import plotly.express as px 


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
	
	


	menu = ["Work Order", "Manual"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()

	if choice == "Work Order":
		workorder = st.text_input('Work Order Number', '')
		curr_wo = wo_data.loc[wo_data['workorder'] == workorder]
		st.write("Work Order Details", curr_wo)
		asset_name = curr_wo['asset_name']

		filename = 'data/{}_energy_sources.csv'.format(workorder)
		if os.path.exists(filename):
			energy_sources_df = pd.read_csv(filename)
		else:
			column_names = ['ctrl_point_id', 'magnitude', 'subsystem', 'lockout_proced', 'verify_proced']
			energy_sources_df = pd.DataFrame(columns=column_names)


		st.subheader("Add Energy Sources")
		col1,col2 = st.beta_columns(2)
		
		with col1:
			energy_type = st.selectbox("Energy Source Type", ["Electrical", "Hydraulic", 'Water', 'Air', 'Vacuum', 'Chemical', 'Gravitational'])

		with col2:
			subsystem = st.text_input("Subsystem (Leave blank if N/A)", "")
			if energy_type == "Electrical":
				device = st.selectbox("Device",["Disconnect","Circuit Breaker","Plug/Cord"])
				magnitude = st.selectbox('Voltage', ['120V', '240V', '480V'])
		
				# Standard inputs for each energy control point
				ctrl_point_id = len(energy_sources_df)+1
				lockout_proced = "Lockout Procedure"
				verify_proced = "Verification Procedure"
		
		if st.button("Add Energy Source"):
			energy_source_dict = {'ctrl_point_id':ctrl_point_id, 'magnitude':magnitude, 'subsystem':subsystem, 'lockout_proced':lockout_proced, 'verify_proced':verify_proced}
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

	elif choice == "Read":
		# st.subheader("View Items")
		with st.beta_expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		with st.beta_expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='index',values='Status')
			st.plotly_chart(p1,use_container_width=True)


	elif choice == "Update":
		st.subheader("Edit Items")
		with st.beta_expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.beta_columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated ::{} ::To {}".format(task,new_task))

			with st.beta_expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.beta_expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.beta_expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

	else:
		st.subheader("About ToDo List App")
		st.info("Built with Streamlit")
		st.info("Jesus Saves @JCharisTech")
		st.text("Jesse E.Agbe(JCharis)")


if __name__ == '__main__':
	main()


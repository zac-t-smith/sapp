%%writefile app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize or load data
try:
    data = pd.read_csv("restoration_data.csv")
except FileNotFoundError:
    data = pd.DataFrame(columns=[
        "Job Name", "Project Manager", "Project Start Date", "Project End Date", "Insurance Carrier", "SCA Signature Date",
        "Lead Technician", "Technician Name", "Lead ID", "Lead Status", "Lead Date", "Referral Source", 
        "Type of Lead", "Leads Converted to Signed Job", "Cost of Lead", "Source of Lead", 
        "Revenue", "Direct Job Costs", "Overhead Costs", "CapEx", "Payments Made to Vendors or Staff", 
        "Material or Subcontractor Costs", "Outstanding Customer Payments", "Technician Hrs on Job", 
        "Billable Tech Hours", "Billable Lead Tech Hours", "Billable PM Hours on Job", "EQ Used on Job", 
        "Days EQ on a Job"
    ])

# App UI
st.title("Restoration Business Tracking App")
st.sidebar.title("Navigation")
tabs = st.sidebar.radio("Go to", ["Data Entry Form", "Analytics Dashboard"])

if tabs == "Data Entry Form":
    st.header("Data Entry Form")
    
    # Job Details
    st.subheader("Job Details")
    job_name = st.text_input("Job Name")
    project_manager = st.text_input("Project Manager")
    start_date = st.date_input("Project Start Date")
    end_date = st.date_input("Project End Date")
    insurance_carrier = st.text_input("Insurance Carrier")
    sca_signature_date = st.date_input("SCA Signature Date")
    lead_technician = st.text_input("Lead Technician")
    technician_name = st.text_input("Technician Name")
    
    # Leads
    st.subheader("Leads")
    lead_id = st.text_input("Lead ID")
    lead_status = st.selectbox("Lead Status", ["Pending", "Converted", "Lost"])
    lead_date = st.date_input("Lead Date")
    referral_source = st.text_input("Referral Source")
    type_of_lead = st.text_input("Type of Lead")
    leads_converted = st.number_input("Leads Converted to Signed Job", min_value=0, step=1)
    cost_of_lead = st.number_input("Cost of Lead ($)", min_value=0.0, step=0.01)
    source_of_lead = st.text_input("Source of Lead")
    
    # Financials
    st.subheader("Financials")
    revenue = st.number_input("Revenue ($)", min_value=0.0, step=100.0)
    direct_job_costs = st.number_input("Direct Job Costs ($)", min_value=0.0, step=100.0)
    overhead_costs = st.number_input("Overhead Costs ($)", min_value=0.0, step=100.0)
    capex = st.number_input("CapEx: New Inventory; Vehicles or EQ ($)", min_value=0.0, step=100.0)
    payments_to_vendors = st.number_input("Payments Made to Vendors or Staff ($)", min_value=0.0, step=100.0)
    material_costs = st.number_input("Material or Subcontractor Costs ($)", min_value=0.0, step=100.0)
    outstanding_payments = st.number_input("Outstanding Customer Payments ($)", min_value=0.0, step=100.0)
    ar = st.number_input("Accounts Receivable (AR) ($)", min_value=0.0, step=100.0)
    ap = st.number_input("Accounts Payable (AP) ($)", min_value=0.0, step=100.0)
    inventory_cost = st.number_input("Inventory Cost ($)", min_value=0.0, step=100.0)
    seasonality_indicator = st.selectbox("Seasonality Indicator", ["None", "Hurricane Season", "Winter Storm"])
    debt_amount = st.number_input("Debt Amounts ($)", min_value=0.0, step=100.0)
    total_hours = st.number_input("Total Available Hours", min_value=0, step=1)
    
    # Field Team
    st.subheader("Field Team")
    technician_hrs = st.number_input("Technician Hrs on Job", min_value=0, step=1)
    billable_tech_hrs = st.number_input("Billable Tech Hours", min_value=0, step=1)
    billable_lead_hrs = st.number_input("Billable Lead Tech Hours", min_value=0, step=1)
    billable_pm_hrs = st.number_input("Billable PM Hours on Job", min_value=0, step=1)
    eq_used = st.text_input("EQ Used on Job")
    eq_days = st.number_input("Days EQ on a Job", min_value=0, step=1)

    
    # Submit Button
    if st.button("Submit"):
        new_entry = {
            "Job Name": job_name,
            "Project Manager": project_manager,
            "Project Start Date": start_date,
            "Project End Date": end_date,
            "Insurance Carrier": insurance_carrier,
            "SCA Signature Date": sca_signature_date,
            "Lead Technician": lead_technician,
            "Technician Name": technician_name,
            "Lead ID": lead_id,
            "Lead Status": lead_status,
            "Lead Date": lead_date,
            "Referral Source": referral_source,
            "Type of Lead": type_of_lead,
            "Leads Converted to Signed Job": leads_converted,
            "Cost of Lead": cost_of_lead,
            "Source of Lead": source_of_lead,
            "Revenue": revenue,
            "Direct Job Costs": direct_job_costs,
            "Overhead Costs": overhead_costs,
            "CapEx": capex,
            "Payments Made to Vendors or Staff": payments_to_vendors,
            "Material or Subcontractor Costs": material_costs,
            "Outstanding Customer Payments": outstanding_payments,
            "Technician Hrs on Job": technician_hrs,
            "Billable Tech Hours": billable_tech_hrs,
            "Billable Lead Tech Hours": billable_lead_hrs,
            "Billable PM Hours on Job": billable_pm_hrs,
            "EQ Used on Job": eq_used,
            "Days EQ on a Job": eq_days
        }
        data = data.append(new_entry, ignore_index=True)
        data.to_csv("restoration_data.csv", index=False)
        st.success("Entry submitted successfully!")

elif tabs == "Analytics Dashboard":
    st.header("Analytics Dashboard")
    if not data.empty:
        # Summary Stats
        st.subheader("Summary Statistics")
        st.write(data.describe())
        
        # Revenue vs Costs
        st.subheader("Revenue vs Direct Costs")
        fig, ax = plt.subplots()
        ax.bar(data["Job Name"], data["Revenue"], label="Revenue")
        ax.bar(data["Job Name"], data["Direct Job Costs"], label="Direct Costs", alpha=0.7)
        ax.set_xticklabels(data["Job Name"], rotation=45, ha="right")
        ax.legend()
        st.pyplot(fig)
    if not data.empty:
        st.subheader("Cash Conversion Cycle (CCC)")
        
        days_in_period = 30  # Adjust based on your tracking period
        data['DSO'] = (data['Accounts Receivable (AR)'] / data['Revenue']) * days_in_period
        data['DPO'] = (data['Accounts Payable (AP)'] / data['Direct Job Costs']) * days_in_period
        data['DIO'] = (data['Inventory Cost'] / data['Direct Job Costs']) * days_in_period
        data['CCC'] = data['DSO'] + data['DIO'] - data['DPO']
        
        st.metric("Average DSO", f"{data['DSO'].mean():.2f} days")
        st.metric("Average DPO", f"{data['DPO'].mean():.2f} days")
        st.metric("Average DIO", f"{data['DIO'].mean():.2f} days")
        st.metric("Average CCC", f"{data['CCC'].mean():.2f} days")

        st.subheader("Rolling Cash Flow Forecasts")
        data['Projected Cash Flow'] = data['Revenue'] - data['Direct Job Costs'] - data['Overhead Costs']
        st.line_chart(data[['Revenue', 'Projected Cash Flow']])

        st.subheader("Break-even Cash Flow Analysis")
        data['Break-even Revenue'] = data['Direct Job Costs'] + data['Overhead Costs']
        st.bar_chart(data[['Revenue', 'Break-even Revenue']])

        st.subheader("Variance Analysis")
        if 'Budgeted Revenue' in data.columns:
            data['Variance'] = data['Revenue'] - data['Budgeted Revenue']
            st.bar_chart(data[['Variance']])

        st.subheader("ROIC per Project")
        data['ROIC'] = (data['Revenue'] - data['Direct Job Costs'] - data['Overhead Costs']) / (data['CapEx'] + data['Overhead Costs'])
        st.metric("Average ROIC", f"{data['ROIC'].mean():.2f}")

        st.subheader("Employee Utilization Rate")
        data['Utilization Rate (%)'] = (data['Billable Tech Hours'] / data['Total Available Hours']) * 100
        st.metric("Average Utilization Rate", f"{data['Utilization Rate (%)'].mean():.2f}%")


    else:
        st.warning("No budgeted values available.")



        else:
            st.warning("No data available for analysis.")


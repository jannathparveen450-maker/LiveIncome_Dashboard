#importing required libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import time

#STREAMLIT PAGE CONFIGURATION
#setting page title,icon and layout
st.set_page_config(
      page_title="Income Live Dashboard",
      page_icon="💰",
      layout="wide"
)

#Dashboard title
st.title("💸LIVE INCOME DATA MONITORING APP")


#LOAD DATASET
df = pd.read_csv("income_data.csv")


#FILTER SECTION
# Dropdown menu to select a job
job_filter = st.selectbox(
      "Choose a job",
      df["occupation"].unique()
)

#filter dataset based on occupation
df = df[df["occupation"]==job_filter].copy()


#PLACEHOLDER FOR LIVE UPDATING
#st.empty() creates an empty container that can be updated repeatedly
place_holder = st.empty()


#LIVE DASHBOARD LOOP
#loop runs for 300 seconds to simulate live data updates
for duration in range(300):
      #generate fake live data
      df["new_age"] = df["age"] * np.random.randint(1,4,size=len(df))
      df["hpw_new"] = df["hours-per-week"] * np.random.randint(1,4,size= len(df))

      #KPI CALCULATIONS
      #Avg age calculation:
      avg_age = np.mean(df["new_age"])


      #count married individuals(adding random number to simulate variation)
      count_married = int(df[df["marital-status"]=="Married-civ-spouse"]["marital-status"]
                      .count()
                      + np.random.randint(5,30)
                      )
                    

      #Avg working hours per week
      hpw = np.mean(df["hpw_new"])


      #DASHBOARD LAYOUT
      with place_holder.container():
            # container() allows multiple Streamlit elements to be grouped
            # inside the placeholder so they can update together in the loop

            #KPI METRICS SECTION
            #creating 3 columns for kpi cards
            kpi1,kpi2,kpi3 = st.columns(3)

            #KPI 1: Average age
            kpi1.metric(
                  label="Average Age",
                  value=round(avg_age),
                  delta=round(avg_age) - 10 #just a demo value
                  )
            #KPI 2: Married Count
            kpi2.metric(
                  label="Married Count",
                  value=count_married,
                  delta=count_married + 10
                  )
            #KPI 3: Working hours per week
            kpi3.metric(
                  label="Working Hours/Week",
                  value=round(hpw),
                  delta=round(hpw)-2
                  )


            #CHARTS SECTION
            #create two columns for charts
            figCol1, figCol2 = st.columns(2)

            #chart1: Age vs Marital status
            with figCol1:
                  st.markdown("### Age vs Marital Status")

                  fig = px.density_heatmap(
                  data_frame= df,
                  x= "marital-status",
                  y= "new_age"
                  )

                  fig.update_layout(
                        xaxis_title = "Marital Status",
                        yaxis_title = "Age"
                        )

                  st.plotly_chart(fig, use_container_width=True)


            #chart2: Age distribution
            with figCol2:
                  st.markdown("### Age Distribution")

                  fig2 = px.histogram(
                        df,
                        x="new_age"
                        )

                  fig2.update_layout(
                        xaxis_title = "Age"
                        )

                  st.plotly_chart(fig2, use_container_width=True)

            #DATA TABLE SECTION
            st.markdown("### Data View As Per Selection")

            #Display filtered dataset
            st.dataframe(df)

      #Pause for 1 second before refreshing dashboard
      time.sleep(1)      







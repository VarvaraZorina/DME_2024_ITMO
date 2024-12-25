import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_connection import get_data_from_db  

st.set_page_config(layout="wide")

data = get_data_from_db()

def plot_pie_chart(df):
    event_counts = df['event_name'].value_counts().reset_index()
    event_counts.columns = ['Event_Name', 'Count']
    
    fig = px.pie(event_counts, 
                 values='Count', 
                 names='Event_Name', 
                 title='Распределение погодных явлений',
                 color='Event_Name',
                 color_discrete_sequence=px.colors.sequential.Viridis)
    
    return fig

def plot_average_intensity_by_district(df, event_name):
    event_df = df[df['event_name'] == event_name]
    avg_intensity_by_district = event_df.groupby('federal_district')['event_intensity'].mean().reset_index()
    
    fig = px.bar(avg_intensity_by_district, 
                 x='federal_district', 
                 y='event_intensity', 
                 title=f'Средняя интенсивность "{event_name}" по федеральным округам',
                 labels={'event_intensity': 'Средняя интенсивность', 'federal_district': 'Федеральный округ'},
                 text='event_intensity',
                 color='event_intensity',
                 color_continuous_scale=px.colors.sequential.Viridis)
    
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_event_distribution_by_district(df, selected_district):
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['year'] = df['start_date'].dt.year

    event_counts = df[df['federal_district'] == selected_district].groupby(['year']).size().reset_index(name='event_count')

    fig = px.bar(event_counts, 
                 x='year', 
                 y='event_count', 
                 title=f'Распределение погодных явлений по годам для {selected_district}',
                 labels={'year': 'Год', 'event_count': 'Количество явлений'},
                 color='event_count',
                 color_continuous_scale=px.colors.sequential.Viridis)
    
    fig.update_layout(xaxis_tickangle=-45)
    return fig

st.title('Анализ частоты и интенсивности погодных явлений, ведущих к экономическим потерям в различных регионах РФ')

st.subheader('Данные')
col1, col2 = st.columns([3, 1])  

with col1:
    col11, col12, col13 = col1.columns([1, 1, 1])
    selected_event_name = col11.selectbox('Погодное явление:', options=data['event_name'].unique())
    selected_region = col12.selectbox('Регион:', options=data['region'].unique())
    selected_federal_district = col13.selectbox('Федеральный округ:', options=data['federal_district'].unique())

    filtered_data = data[
        (data['event_name'] == selected_event_name) &
        (data['region'] == selected_region) &
        (data['federal_district'] == selected_federal_district)
    ]

    st.dataframe(filtered_data, use_container_width=True, hide_index=True)  

with col2:
    st.subheader('Круговая диаграмма')
    pie_chart = plot_pie_chart(data)
    st.plotly_chart(pie_chart)

col1, col2 = st.columns(2)

with col1:
    event_names = data['event_name'].unique()
    selected_event = st.selectbox('Выберите погодное явление:', event_names)

    fig_intensity = plot_average_intensity_by_district(data, selected_event)
    st.plotly_chart(fig_intensity)

with col2:
    federal_districts = data['federal_district'].unique()
    selected_district = st.selectbox('Выберите федеральный округ:', federal_districts)

    fig_distribution = plot_event_distribution_by_district(data, selected_district)
    st.plotly_chart(fig_distribution)

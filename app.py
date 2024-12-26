import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from database.db_connection import get_data_from_db  


def plot_average_intensity_by_territory(df, event_name, territory):
    event_df = df[df['event_name'] == event_name]
    avg_intensity_by_district = event_df.groupby(territory)['event_intensity'].mean().reset_index()

    if territory == "federal_district":
        territory_label = "Федеральный округ"
    elif territory == "region":
        territory_label = "Регион"
    
    fig = px.bar(avg_intensity_by_district, 
                 x=territory, 
                 y='event_intensity', 
                 title=f'Средняя интенсивность "{event_name}"',
                 labels={'event_intensity': 'Средняя интенсивность', territory: territory_label},
                 text='event_intensity',
                 color='event_intensity',
                 color_continuous_scale=px.colors.sequential.Viridis)
    
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_event_distribution_by_territory(df, selected_territory, territory):
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['year'] = df['start_date'].dt.year

    if territory == "federal_district":
        event_counts = df[df['federal_district'] == selected_territory].groupby(['year']).size().reset_index(name='event_count')
    elif territory == "region":
        event_counts = df[df['region'] == selected_territory].groupby(['year']).size().reset_index(name='event_count')

    fig = px.bar(event_counts, 
                 x='year', 
                 y='event_count', 
                 title=f'Распределение погодных явлений по годам для {selected_territory}',
                 labels={'year': 'Год', 'event_count': 'Количество явлений'},
                 color='event_count',
                 color_continuous_scale=px.colors.sequential.Viridis)
    
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_ring_chart(df, selected_territory, territory):
    if territory == "federal_district":
        district_data = df[df['federal_district'] == selected_territory]
    elif territory == "region":
        district_data = df[df['region'] == selected_territory]

    grouped_data = district_data.groupby('event_name', as_index=False).agg({'event_intensity': 'sum'})

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=grouped_data['event_name'],
        values=grouped_data['event_intensity'],
        hole=0.4,  
        marker=dict(colors=px.colors.qualitative.Plotly),  
        textinfo='none',  
    ))

    fig.update_layout(
        title=f'Кольцевая диаграмма по погодным явлениям в "{selected_territory}"',
        annotations=[dict(text='Явления', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    return fig

st.set_page_config(layout="wide")

data = get_data_from_db()

with st.sidebar:
    selected = option_menu("Навигация", 
                           ["Общие показатели", 'Федеральные округа', 'Регионы'], 
                           icons=['house', 'geo-alt', 'bar-chart'], 
                           menu_icon="cast", 
                           default_index=0)

    st.markdown('Работа выполнена студентами:<br /> - Рум Роман (@rmx2n),<br /> - Дарья Арестова (@bendinini),<br /> - Алена Анциферова (@Alenants)', unsafe_allow_html=True)

if selected == "Общие показатели": 
    st.title('Анализ частоты и интенсивности погодных явлений, ведущих к экономическим потерям в различных регионах РФ')
    st.divider()
    st.header("Общие показатели")
    
    col1, col2 = st.columns([1,1])

    event_names = data['event_name'].unique()
    selected_event = col1.selectbox("Выберите событие:", event_names)

    data['start_date'] = pd.to_datetime(data['start_date'], errors='coerce')
    data['end_date'] = pd.to_datetime(data['end_date'], errors='coerce')
    years = data['start_date'].dt.year.unique()
    selected_year = col2.selectbox("Выберите год:", years)

    filtered_data = data[(data['event_name'] == selected_event) & (data['start_date'].dt.year == selected_year)]

    if not filtered_data.empty:
        max_intensity = filtered_data['event_intensity'].max()
        min_intensity = filtered_data['event_intensity'].min()
        max_duration = filtered_data['duration'].max()
        min_duration = filtered_data['duration'].min()


        col1.markdown(f"**Интенсивность MAX**<br /><span style='font-size:48px; color:#ff4b4b; margin-bottom: 10px; text-align: center;'>{max_intensity}</span>", unsafe_allow_html=True)
        col1.markdown(f"**Интенсивность MIN**<br /><span style='font-size:48px; color:#ff4b4b; margin-bottom: 10px; text-align: center;'>{min_intensity}</span>", unsafe_allow_html=True)
        
        col2.markdown(f"**Продолжительность MAX**<br /><span style='font-size:48px; color:#ff4b4b; margin-bottom: 10px; text-align: center;'>{max_duration}</span>", unsafe_allow_html=True)        
        col2.markdown(f"**Продолжительность MIN**<br /><span style='font-size:48px; color:#ff4b4b; margin-bottom: 10px; text-align: center;'>{min_duration}</span>", unsafe_allow_html=True)        
    else:
        st.write("Нет данных для выбранного события и года.")

    fig = px.scatter(
        filtered_data,
        x='duration',
        y='event_intensity',
        size='event_intensity', 
        color='region',  
        hover_name='event_name',
        title=f'Интенсивность vs Продолжительность для {selected_event} в {selected_year}',
        labels={'duration': 'Продолжительность', 'event_intensity': 'Интенсивность', 'region': 'Регион'},
        size_max=60  
    )
    
    st.plotly_chart(fig) 

elif selected == "Федеральные округа": 
    st.title('Анализ частоты и интенсивности погодных явлений, ведущих к экономическим потерям в различных регионах РФ')
    st.divider()
    st.header("Федеральные округа")

    col1, col2 = st.columns([1,1])
    event_names = data['event_name'].unique()
    selected_event = col1.selectbox('Выберите погодное явление:', event_names)

    fig_intensity = plot_average_intensity_by_territory(data, selected_event, "federal_district")
    col1.plotly_chart(fig_intensity)
    filtered_data = data.drop(columns=['region', 'duration'])
    filtered_data = filtered_data.sort_values(by='start_date', ascending=False)
    filtered_data['start_date'] = pd.to_datetime(filtered_data['start_date'])
    filtered_data['start_date'] = filtered_data['start_date'].dt.strftime('%Y-%m-%d')
    filtered_data = filtered_data.rename(columns={
        'federal_district': 'Федеральный округ',
        'event_name': 'Погодное явление',
        'event_intensity': 'Интенсивность',
        'start_date': 'Дата начала',
        'end_date': 'Дата окончания'
    })
    filtered_data = filtered_data[['Федеральный округ', 'Погодное явление', 'Интенсивность', 'Дата начала', 'Дата окончания']]
    col2.dataframe(filtered_data, hide_index=True)

    federal_districts = data['federal_district'].unique()
    selected_district = st.selectbox('Выберите федеральный округ:', federal_districts)

    col1, col2 = st.columns([1,1])
    fig_distribution1 = plot_event_distribution_by_territory(data, selected_district, "federal_district")
    col1.plotly_chart(fig_distribution1)
    fig_distribution2 = plot_ring_chart(data, selected_district, "federal_district")
    col2.plotly_chart(fig_distribution2)


elif selected == "Регионы": 
    st.title('Анализ частоты и интенсивности погодных явлений, ведущих к экономическим потерям в различных регионах РФ')
    st.divider()
    st.header("Регионы")

    col1, col2 = st.columns([1,1])
    event_names = data['event_name'].unique()
    selected_event = col1.selectbox('Выберите погодное явление:', event_names)

    fig_intensity = plot_average_intensity_by_territory(data, selected_event, "region")
    col1.plotly_chart(fig_intensity)
    filtered_data = data.drop(columns=['federal_district', 'duration'])
    filtered_data = filtered_data.sort_values(by='start_date', ascending=False)
    filtered_data['start_date'] = pd.to_datetime(filtered_data['start_date'])
    filtered_data['start_date'] = filtered_data['start_date'].dt.strftime('%Y-%m-%d')
    filtered_data = filtered_data.rename(columns={
        'region': 'Регион',
        'event_name': 'Погодное явление',
        'event_intensity': 'Интенсивность',
        'start_date': 'Дата начала',
        'end_date': 'Дата окончания'
    })
    filtered_data = filtered_data[['Регион', 'Погодное явление', 'Интенсивность', 'Дата начала', 'Дата окончания']]
    col2.dataframe(filtered_data, hide_index=True)

    region = data['region'].unique()
    selected_district = st.selectbox('Выберите регион:', region)

    col1, col2 = st.columns([1,1])
    fig_distribution1 = plot_event_distribution_by_territory(data, selected_district, "region")
    col1.plotly_chart(fig_distribution1)
    fig_distribution2 = plot_ring_chart(data, selected_district, "region")
    col2.plotly_chart(fig_distribution2)
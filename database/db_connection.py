import pandas as pd
from sqlalchemy import create_engine

def get_data_from_db():
    user = 'postgres' 
    password = 'postgres'  
    host = 'localhost'  
    port = '5433'  
    database = 'pg_db'  

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    
    engine = create_engine(connection_string)

    query = """
        SELECT 
            w.start_date,
            w.end_date,
            e.event_name,
            w.event_intensity,
            r.region_name AS region,
            w.duration,
            r.federal_district
        FROM 
            normalized_weather_events w
        JOIN 
            weather_events_types e ON w.event_id = e.event_id
        JOIN 
            weather_regions r ON r.region_name = (SELECT region_name FROM weather_regions WHERE region_name = r.region_name)
    """
    
    df = pd.read_sql(query, engine)

    return df




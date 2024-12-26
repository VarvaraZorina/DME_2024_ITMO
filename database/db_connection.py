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
            r.federal_district,
            (w.end_date - w.start_date) AS duration
        FROM 
            normalized_weather_events w
        JOIN 
            weather_events_types e ON w.event_id = e.event_id
        JOIN 
            weather_regions r ON w.region_id = r.region_id; 
    """
    
    df = pd.read_sql(query, engine)

    return df




from sqlConnect import connection_url;
import pandas as pd;

from sqlalchemy import create_engine;

# Create the engine
engine = create_engine(connection_url)

# Query the database and convert to DataFrame
query_jobs = "SELECT * FROM jobs"
query_services = "SELECT * FROM services"


df_jobs = pd.read_sql(query_jobs, engine)
df_services = pd.read_sql(query_services, engine)


print(df_jobs);
print(df_services);



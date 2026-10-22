import pandas as pd 
import pymysql
from sqlalchemy import create_engine, text
df = pd.read_csv(r"D:\Vscode\Project_3\Job_placement_cleaneddata.csv")
print("CSV loaded successfully!")
print("Original shape:", df.shape)
df.columns = df.columns.str.strip()
duplicate_columns = df.columns[df.columns.str.lower().duplicated()]

try:

    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="prakash0510",
        database="firstprojectdb",
        cursorclass=pymysql.cursors.DictCursor

    )
    print("\n  connected to Mysql sucessfully")

except Exception as e:

    print("\n connection failed",e)
engine = create_engine("mysql+pymysql://root:prakash0510@localhost/firstprojectdb")

try:

    with engine.connect() as conn:
        print("SQLALchemy connection sucessful")

except Exception as e:

    print("SQLALchemy connection failed ",e)

df.columns = df.columns.str.strip()
seen = set()
columns_to_keep = []
for col in df.columns:
    col_lower = col.lower()
    if col_lower not in seen:
        seen.add(col_lower)
        columns_to_keep.append(col)
df = df[columns_to_keep]
print("Final columns:", df.columns.tolist())
print("Number of columns:", len(df.columns))
print("Duplicate check:", df.columns.str.lower().duplicated().any())
try:
    df.to_sql(
        name="job_placement",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Data inserted successfully!")

    with engine.connect() as connection:
     result = connection.execute(
        text("SELECT * FROM job_placement LIMIT 5")
    )

    for row in result:
        print(row)

except Exception as e:
    print("Database operation failed:", e)



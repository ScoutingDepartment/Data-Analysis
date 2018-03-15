from processor.csv_to_database import *
from processor.database import get_connection

from sqlalchemy.types import *

table = get_entries_table()

conn = get_connection()

table.to_sql(name="RAW_ENTRIES",
             con=conn,
             if_exists="replace",
             dtype={"Match": Integer,
                    "Team": Integer,
                    "Name": String,
                    "StartTime": Integer,
                    "Board": Integer,
                    "Data": String,
                    "Comments": String
                    })
conn.close()

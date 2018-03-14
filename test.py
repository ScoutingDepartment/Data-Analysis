
import numpy as np

import pandas as pd
from processor.database import get_connection


conn = get_connection()

df = pd.read_sql("SELECT * FROM RAW_ENTRIES", conn)

print(df)



# df = DataFrame(np.random.rand(10, 10))
#
# df.to_sql("RAW_ENTRIES", get_connection())


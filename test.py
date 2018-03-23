# write_unique()

import numpy as np
import pandas as pd

a = pd.Series(np.arange(120))
b = pd.Series(np.arange(0, 100, 3))

# print(a)
# print(b)
print(a.isin(b))

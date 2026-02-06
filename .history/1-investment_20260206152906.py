import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 模拟价格
np.random.seed(42)
returns = np.random.normal(0.001, 0.01, 252)
price = 100 * (1 + returns).cumprod()

df = pd.DataFrame({
    "price": price,
    "return": returns
})

print("平均收益:", df["return"].mean())
print("波动率:", df["return"].std())

plt.hist(df["return"], bins=50)
plt.title("Daily Return Distribution")
plt.show()
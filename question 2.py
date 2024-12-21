import yfinance as yf
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

STOCK = "RELIANCE.NS"
data = yf.download(STOCK, start="2022-01-01", end="2024-12-14")
closing_prices = data["Close"].dropna()

mean_price = closing_prices.mean()
std_dev = closing_prices.std()
sample_size = len(closing_prices)
meantry = 2500

t_score = (mean_price - meantry) / (std_dev / np.sqrt(sample_size))
z_score = (mean_price - meantry) / std_dev
confidence_level = 0.95
alpha = 1 - confidence_level
critical_value = stats.t.ppf(1 - alpha / 2, df=sample_size - 1)  # t critical value
margin_of_error = critical_value * (std_dev / np.sqrt(sample_size))
confidence_interval = (mean_price - margin_of_error, mean_price + margin_of_error)

plt.figure(figsize=(12, 6))
sns.histplot(
    closing_prices,
    kde=True,
    stat="density",
    color="blue",
    bins=30,
    label="Daily Closing Prices",
)
x = np.linspace(closing_prices.min(), closing_prices.max(), 500)
normal_pdf = stats.norm.pdf(x, float(mean_price.item()), float(std_dev.item()))
plt.plot(x, normal_pdf, "r", label="Normal Distribution", linewidth=2)

plt.title("Probability Distribution of Daily Closing Prices for Reliance (RELIANCE.NS)")
plt.xlabel("Closing Price")
plt.ylabel("Density")
plt.legend()
plt.show()


print(f"Mean: {mean_price.item()}")
print(f"Standard Deviation: {std_dev.item()}")
print(f"Sample Size: {sample_size}")

print(f"T-score: {t_score.item()}")
print(f"Z-score: {z_score.item()}")

print(
    f"{confidence_level*100}% CI: {confidence_interval[0].item()} to {confidence_interval[1].item()}"
)

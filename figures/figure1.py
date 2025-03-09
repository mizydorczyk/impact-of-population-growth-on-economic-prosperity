import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker

def main():
    income_or_consumption_data = pd.read_csv('assets/world_bank_property_and_inequality.csv')
    gross_domestic_product_data = pd.read_csv('assets/world_bank_gdp_constant_usd_2021.csv')

    chosen_year = '2020'

    gdp_data = gross_domestic_product_data[['Country Code', chosen_year]].rename(
        columns={chosen_year: 'GDP'}
    ).dropna()

    income_data = income_or_consumption_data[income_or_consumption_data['reporting_year'] == int(chosen_year)]

    merged_data = pd.merge(
        income_data, 
        gdp_data, 
        left_on='country_code',
        right_on='Country Code'
    )

    if merged_data.empty:
        print(f"No overlapping data for the year {chosen_year}.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(merged_data['GDP'], merged_data['mean'], alpha=0.7)

    x = merged_data['GDP']
    y = merged_data['mean']
    coeffs = np.polyfit(x, y, 1)
    regression_line = np.poly1d(coeffs)

    x_line = np.linspace(x.min(), x.max(), 500)
    y_line = regression_line(x_line)
    ax.plot(x_line, y_line, alpha=1)

    y_pred = regression_line(x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    print(r_squared)

    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d\$'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d\$'))

    plt.xlabel('PKB na osobę')
    plt.ylabel('Dzienna konsumpcja lub dochód na osobę')
    ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
    ax.grid(True, linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
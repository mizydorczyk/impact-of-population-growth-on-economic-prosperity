from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    population_growth_rate = pd.read_csv('assets/un_population_growth_rate.csv')
    gdp_per_capita = pd.read_csv('assets/world_bank_gdp_constant_usd_2021.csv')
    population_size = pd.read_csv('assets/un_population_size.csv')

    chosen_year = '2019'

    gdp_per_capita = gdp_per_capita[['Country Name', chosen_year]].rename(
        columns={chosen_year: 'GDP per capita'}
    ).dropna()

    population_size = population_size[population_size['Time'] == int(chosen_year)]
    population_size = population_size[['Location', 'Value']].rename(columns={'Value': 'Population'})

    population_growth_rate['Value'] = pd.to_numeric(population_growth_rate['Value'])
    population_growth_rate = population_growth_rate.dropna(subset=['Value'])
    population_growth_rate['Time'] = population_growth_rate['Time'].astype(int)
    population_growth_rate = population_growth_rate[(population_growth_rate['Time'] >= 1990) & (population_growth_rate['Time'] <= 2019)]

    avg_population_growth = population_growth_rate.groupby('Location')['Value'].mean().reset_index()
    avg_population_growth = avg_population_growth.rename(columns={'Value': 'Avg Population Growth'})

    merged = pd.merge(
        avg_population_growth,
        gdp_per_capita,
        left_on='Location',
        right_on='Country Name'
    )
    merged = pd.merge(
        merged,
        population_size,
        on='Location'
    )

    if merged.empty:
        print(f"No overlapping data for the year {chosen_year}.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    x = merged['Avg Population Growth']
    y = merged['GDP per capita']
    sizes = merged['Population'] / (1e6*0.4)

    ax.scatter(x, y, s=sizes, alpha=0.7)
    
    ax.set_yscale('log')
    ax.set_yticks([2000, 5000, 10000, 20000, 50000, 100000])
    ax.set_xticks([-1, 0, 1, 2, 3, 4, 5])
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d\$'))
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))

    plt.ylabel('PKB na osobę')
    plt.xlabel('Średnia zmiana populacji')
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

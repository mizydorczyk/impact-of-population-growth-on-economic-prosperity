from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    population_growth_rate = pd.read_csv('assets/un_population_growth_rate.csv')
    gdp_per_capita_growth_rate = pd.read_csv('assets/world_bank_gdp_per_capita_growth_rate.csv')
    population_size = pd.read_csv('assets/un_population_size.csv')

    population_size['Value'] = pd.to_numeric(population_size['Value'])
    population_growth_rate['Value'] = pd.to_numeric(population_growth_rate['Value'])

    population_size = population_size[(population_size['Time'] >= 1990) & (population_size['Time'] <= 2019)]

    avg_population_size = population_size.groupby('Location')['Value'].mean().reset_index()
    avg_population_size = avg_population_size.rename(columns={'Value': 'Avg Population'})

    population_growth_rate = population_growth_rate.dropna(subset=['Value'])
    population_growth_rate['Time'] = population_growth_rate['Time'].astype(int)
    population_growth_rate = population_growth_rate[(population_growth_rate['Time'] >= 1990) & (population_growth_rate['Time'] <= 2019)]

    avg_population_growth = population_growth_rate.groupby('Location')['Value'].mean().reset_index()
    avg_population_growth = avg_population_growth.rename(columns={'Value': 'Avg Population Growth'})

    gdp_per_capita_growth_rate = gdp_per_capita_growth_rate.dropna(subset=['Country Name'])
    gdp_per_capita_growth_rate = gdp_per_capita_growth_rate.melt(
        id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], 
        var_name='Year', 
        value_name='GDP Growth'
    )
    gdp_per_capita_growth_rate['Year'] = pd.to_numeric(gdp_per_capita_growth_rate['Year'])
    gdp_per_capita_growth_rate['GDP Growth'] = pd.to_numeric(gdp_per_capita_growth_rate['GDP Growth'])
    gdp_per_capita_growth_rate = gdp_per_capita_growth_rate.dropna(subset=['Year', 'GDP Growth'])
    gdp_per_capita_growth_rate = gdp_per_capita_growth_rate[(gdp_per_capita_growth_rate['Year'] >= 1990) & (gdp_per_capita_growth_rate['Year'] <= 2019)]

    avg_gdp_per_capita_growth = gdp_per_capita_growth_rate.groupby('Country Name')['GDP Growth'].mean().reset_index()
    avg_gdp_per_capita_growth = avg_gdp_per_capita_growth.rename(columns={'GDP Growth': 'Avg GDP Growth'})

    merged = pd.merge(
        avg_population_growth,
        avg_gdp_per_capita_growth,
        left_on='Location',
        right_on='Country Name'
    )
    merged = pd.merge(
        merged,
        avg_population_size,
        on='Location'
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    x = merged['Avg Population Growth']
    y = merged['Avg GDP Growth']
    sizes = merged['Avg Population'] / (1e6 * 0.6)

    ax.scatter(x, y, s=sizes, alpha=0.7)

    ax.set_xticks([-1, 0, 1, 2, 3, 4, 5])
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))

    plt.ylabel('Średnia zmiana PKB na osobę')
    plt.xlabel('Średnia zmiana populacji')
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

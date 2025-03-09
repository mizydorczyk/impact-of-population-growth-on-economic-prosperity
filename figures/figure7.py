from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    gdp_per_capita_growth_rate = pd.read_csv('assets/world_bank_gdp_per_capita_growth_rate.csv')
    human_capital_index = pd.read_csv('assets/world_bank_human_capital_index.csv')
    population_size = pd.read_csv('assets/un_population_size.csv')

    population_size['Value'] = pd.to_numeric(population_size['Value'])
    population_size = population_size[(population_size['Time'] >= 1990) & (population_size['Time'] <= 2019)]

    avg_population_size = population_size.groupby('Location')['Value'].mean().reset_index()
    avg_population_size = avg_population_size.rename(columns={'Value': 'Avg Population'})

    human_capital_index = human_capital_index.dropna(subset=['Country Name'])
    human_capital_index = human_capital_index[human_capital_index['Indicator Code'] == 'HD.HCI.LAYS']
    human_capital_index = human_capital_index.melt(
        id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], 
        var_name='Year', 
        value_name='Years in School'
    )
    human_capital_index['Year'] = pd.to_numeric(human_capital_index['Year'])
    human_capital_index['Years in School'] = pd.to_numeric(human_capital_index['Years in School'])
    years_in_schools = human_capital_index.dropna(subset=['Year', 'Years in School'])
    years_in_schools = years_in_schools[(years_in_schools['Year'] >= 1990) & (years_in_schools['Year'] <= 2019)]

    avg_years_in_schools = years_in_schools.groupby('Country Name')['Years in School'].mean().reset_index()
    avg_years_in_schools = avg_years_in_schools.rename(columns={'Years in School': 'Avg Years in School'})

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
        avg_years_in_schools,
        avg_gdp_per_capita_growth,
        left_on='Country Name',
        right_on='Country Name'
    )
    merged = pd.merge(
        merged,
        avg_population_size,
        left_on='Country Name',
        right_on='Location'
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    x = merged['Avg Years in School'] 
    y = merged['Avg GDP Growth']
    sizes = merged['Avg Population'] / (1e6 * 0.6)

    ax.scatter(x, y, s=sizes, alpha=0.7)

    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d lat'))

    plt.xlabel('Średnia liczba lat edukacji')
    plt.ylabel('Średnia zmiana PKB na osobę')
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

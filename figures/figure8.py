from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    population_growth_rate = pd.read_csv('assets/un_population_growth_rate.csv')
    human_capital_index = pd.read_csv('assets/world_bank_human_capital_index.csv')
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

    merged = pd.merge(
        avg_population_growth,
        avg_years_in_schools,
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
    y = merged['Avg Years in School']
    sizes = merged['Avg Population'] / (1e6 * 0.6)

    ax.scatter(x, y, s=sizes, alpha=0.7)

    ax.set_xticks([-1, 0, 1, 2, 3, 4, 5])
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d lat'))
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))

    plt.ylabel('Średnia liczba lat edukacji')
    plt.xlabel('Średnia zmiana populacji')
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

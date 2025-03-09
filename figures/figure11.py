from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    population_growth_rate = pd.read_csv('assets/un_population_growth_rate.csv')
    productivity = pd.read_csv('assets/penn_world_table.csv')

    population_growth_rate['Value'] = pd.to_numeric(population_growth_rate['Value'])

    population_growth_rate = population_growth_rate.dropna(subset=['Value'])
    population_growth_rate['Time'] = population_growth_rate['Time'].astype(int)
    population_growth_rate = population_growth_rate[(population_growth_rate['Time'] >= 1990) & (population_growth_rate['Time'] <= 2019)]

    avg_population_growth = population_growth_rate.groupby('Location')['Value'].mean().reset_index()
    avg_population_growth = avg_population_growth.rename(columns={'Value': 'Avg Population Growth'})

    productivity['rtfpna'] = pd.to_numeric(productivity['rtfpna'], errors='coerce')
    productivity = productivity[['country', 'year', 'rtfpna']]

    productivity = productivity.sort_values(by=['country', 'year'])
    productivity['rtfpna_change'] = productivity.groupby('country')['rtfpna'].diff()
    productivity['rtfpna_percent_change'] = productivity.groupby('country')['rtfpna'].pct_change() * 100

    productivity = productivity[(productivity['year'] >= 1990) & (productivity['year'] <= 2019)]

    avg_productivity_change = productivity.groupby('country')['rtfpna_percent_change'].mean().reset_index()
    avg_productivity_change = avg_productivity_change.rename(columns={'rtfpna_percent_change': 'Avg RTFPNA Change'})

    merged = pd.merge(
        avg_population_growth,
        avg_productivity_change,
        left_on='Location',
        right_on='country'
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    x = merged['Avg Population Growth']
    y = merged['Avg RTFPNA Change']

    ax.scatter(x, y, alpha=0.7)

    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))

    plt.ylabel('Średnia zmiana współczynnika całkowitej produktywności')
    plt.xlabel('Średnia zmiana populacji')
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

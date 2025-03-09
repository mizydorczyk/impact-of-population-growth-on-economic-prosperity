from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    life_expentancy_at_birth = pd.read_csv('assets/un_life_expectancy_at_birth.csv')
    gdp_per_capita = pd.read_csv('assets/world_bank_gdp_constant_usd_2021.csv')

    chosen_year = '2021'

    gdp_per_capita = gdp_per_capita[['Country Name', chosen_year]].rename(
        columns={chosen_year: 'GDP per capita'}
    ).dropna()

    life_expentancy_at_birth = life_expentancy_at_birth[life_expentancy_at_birth['Year(s)'] == int(chosen_year)]
    life_expentancy_at_birth['Value'] = pd.to_numeric(life_expentancy_at_birth['Value'])

    merged = pd.merge(
        life_expentancy_at_birth, 
        gdp_per_capita, 
        left_on='Country or Area',
        right_on='Country Name'
    )

    if merged.empty:
        print(f"No overlapping data for the year {chosen_year}.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    x = merged['GDP per capita']
    y = merged['Value']

    ax.scatter(x, y, alpha=0.7)
    
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d lat'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d\$'))

    plt.xlabel('PKB na osobę')
    plt.ylabel('Przewidywana długosc życia w roku 0')
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
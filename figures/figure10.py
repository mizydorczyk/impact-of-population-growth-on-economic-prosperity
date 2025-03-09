from matplotlib import ticker
import pandas as pd
import matplotlib.pyplot as plt

def main():
    data = pd.read_csv('assets/penn_world_table.csv')
    data['ctfp'] = pd.to_numeric(data['ctfp'], errors='coerce')
    data['pop'] = pd.to_numeric(data['pop'], errors='coerce')
    data['cgdpo'] = pd.to_numeric(data['cgdpo'], errors='coerce')

    chosen_year = 2019

    data_year = data[data['year'] == chosen_year]
    data_year = data_year.dropna(subset=['ctfp', 'cgdpo', 'pop'])
    data_year = data_year[data_year['pop'] != 0]

    if data_year.empty:
        print(f"No valid data available for year {chosen_year}")
        return
    
    fig, ax = plt.subplots(figsize=(8, 5))

    x = (data_year['cgdpo'] / data_year['pop'])  
    y = data_year['ctfp'] 
    sizes = data_year['pop'] * 0.6

    ax.set_xscale('log')
    ax.set_xticks([2000, 5000, 10000, 20000, 50000, 100000])
    ax.set_xticklabels([2000, 5000, 10000, 20000, 50000, 100000])

    ax.scatter(x, y, s=sizes, alpha=0.7)

    plt.xlabel('PKB na osobę')
    plt.ylabel('Współczynnik całkowitej produktywności')

    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d\$'))

    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
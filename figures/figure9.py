import pandas as pd
import matplotlib.pyplot as plt

def main():
    data = pd.read_csv('assets/penn_world_table.csv')

    data['year'] = pd.to_numeric(data['year'], errors='coerce')
    data['rtfpna'] = pd.to_numeric(data['rtfpna'], errors='coerce')

    developed_countries = ['Australia', 'Austria', 'Belgium', 'Canada', 'Denmark', 'Korea, Rep.', 'Finland', 'France', 'Germany', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Luxembourg', 'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom', 'United States']

    data = data[data['country'].isin(developed_countries)]

    data = data.dropna(subset=['year', 'rtfpna'])

    if data.empty:
        print("No valid data available for plotting.")
        return

    data_by_year = data.groupby('year')['rtfpna'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data_by_year['year'], data_by_year['rtfpna'], linestyle='-')

    plt.xlabel('Lata')
    plt.ylabel('Średni współczynnik całkowitej produktywności')

    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

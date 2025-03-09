from matplotlib import pyplot as plt, ticker
import pandas as pd

def main():
    data = pd.read_csv('assets/penn_world_table.csv')

    data['avh'] = pd.to_numeric(data['avh'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    data['pop'] = pd.to_numeric(data['pop'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    data['cgdpo'] = pd.to_numeric(data['cgdpo'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    
    developed_countries = ['Australia', 'Austria', 'Belgium', 'Canada', 'Denmark', 'Korea, Rep.', 'Finland', 'France', 'Germany', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Luxembourg', 'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom', 'United States']
    data = data[data['country'].isin(developed_countries)]

    data = data.dropna(subset=['avh', 'cgdpo', 'pop'])
    data = data[data['pop'] != 0]

    if data.empty:
        print("No valid data available for the specified range.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    data['gdp_per_capita'] = data['cgdpo'] / data['pop']
    avg_trace = data.groupby('year')[['gdp_per_capita', 'avh']].mean()

    std_dev = data.groupby('year')[['gdp_per_capita', 'avh']].std()

    ax.plot(avg_trace['gdp_per_capita'], avg_trace['avh'])

    ax.fill_between(avg_trace['gdp_per_capita'], 
                    avg_trace['avh'] - std_dev['avh'], 
                    avg_trace['avh'] + std_dev['avh'], alpha=0.1)
    
    for i, year in enumerate(avg_trace.index):
        if year % 5 == 0 and year != 1950 and year != 2010 and year != 1975:
            ax.plot(avg_trace['gdp_per_capita'].iloc[i], 
                    avg_trace['avh'].iloc[i], 
                    'o', color='#1f77b4', markersize=3)
            
            ax.text(avg_trace['gdp_per_capita'].iloc[i] + 50, 
                    avg_trace['avh'].iloc[i] + 10, 
                    str(year), 
                    fontsize=11, ha='left', va='bottom')
        if year == 2010:
            ax.plot(avg_trace['gdp_per_capita'].iloc[i], 
                    avg_trace['avh'].iloc[i], 
                    'o', color='#1f77b4', markersize=3)
            
            ax.text(avg_trace['gdp_per_capita'].iloc[i] - 2300, 
                    avg_trace['avh'].iloc[i] - 50, 
                    str(year), 
                    fontsize=11, ha='left', va='bottom')
        if year == 1975:
            ax.plot(avg_trace['gdp_per_capita'].iloc[i], 
                    avg_trace['avh'].iloc[i], 
                    'o', color='#1f77b4', markersize=3)
            
            ax.text(avg_trace['gdp_per_capita'].iloc[i] + 350, 
                    avg_trace['avh'].iloc[i] + 5, 
                    str(year), 
                    fontsize=11, ha='left', va='bottom')

    plt.xlabel('Średnie PKB na osobę')
    plt.ylabel('Średnia liczba przepracowanych godzin w roku')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d godz.'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d\$'))
    ax.set_xlim(avg_trace['gdp_per_capita'].min(), avg_trace['gdp_per_capita'].max())
    ax.grid(True, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

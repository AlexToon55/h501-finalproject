
import pandas as pd

class MoodAnalysis:
    KEEP_COLS = ['Fav genre','BPM','Anxiety','Depression','Insomnia','OCD','Music effects']

    def __init__(self, csv_path='data/mxmh_survey_results.csv'):
        self.csv_path = csv_path
        self.df = None
        self.df_clean = None

    # --- data ---
    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)
        cols = [c for c in self.KEEP_COLS if c in df.columns]
        df = df[cols].copy()
        for c in ['Anxiety','Depression','Insomnia','OCD','BPM']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')
        self.df = df
        return df

    def clean(self) -> pd.DataFrame:
        if self.df is None:
            self.load()
        df = self.df.copy()
        if 'BPM' in df.columns:
            df['BPM'] = df['BPM'].where(df['BPM'].between(40, 240))
            df.loc[df['BPM'].eq(0), 'BPM'] = pd.NA
        self.df_clean = df
        return df




    # --- analyses for stretch goal ---
    # I chose to use the spearman correlation approach for this. 
    ## Spearman analysis, or Spearman's rank correlation analysis, is a non-parametric statistical test that measures the strength and direction of the monotonic (consistently increasing or decreasing) relationship between two ranked variables. 
    ## It assesses how well the rank order of one variable corresponds to the rank order of another variable, making it useful for data that doesn't meet the linearity or normality assumptions of Pearson correlation, such as ordinal data or data with outliers
    def spearman_bpm_vs_scales(self) -> pd.DataFrame:
        df = self.df_clean if self.df_clean is not None else self.clean()
        measures = [m for m in ['Anxiety','Depression','Insomnia','OCD'] if m in df.columns]
        rows = []
        for m in measures:
            sub = df[['BPM', m]].dropna()
            rho = sub.corr(method='spearman').loc['BPM', m] if not sub.empty else float('nan')
            rows.append({'measure': m, 'n': len(sub), 'spearman_rho': round(float(rho), 3)})
        return pd.DataFrame(rows)


    # Imrove table function - this function creates a table that ranks music genres based on the percentage of respondents who reported an "Improved" mood after listening to music in that genre.
    # The table includes the rank, favorite genre, percentage of respondents reporting improved mood, and the number of respondents for each genre.
    # The function filters out genres with fewer than a specified minimum number of respondents to ensure statistical significance.

    def improve_table(self, min_n: int = 30) -> pd.DataFrame:
        df = self.df_clean if self.df_clean is not None else self.clean()
        g = df[['Fav genre','Music effects']].dropna()
        g = g[g['Music effects'].isin(['Improve','No effect','Worsen'])].copy()
        keep = g['Fav genre'].value_counts()
        g = g[g['Fav genre'].isin(keep[keep >= min_n].index)]
        counts = (g.groupby(['Fav genre','Music effects']).size().reset_index(name='n'))
        counts['percent'] = counts['n'] / counts.groupby('Fav genre')['n'].transform('sum')
        recs = (counts[counts['Music effects']=='Improve']
                    .sort_values('percent', ascending=False)
                    .rename(columns={'percent':'improve_pct'}))
        recs['rank'] = range(1, len(recs)+1)
        return recs[['rank','Fav genre','improve_pct','n']]

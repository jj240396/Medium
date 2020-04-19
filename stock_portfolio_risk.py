

#df - table containing the historical stock prices for the past 10 years.
#df_weights - dict containing the weightage of each stock in the portfolio

#converting the df_weights dict to dataframe
weightage = pd.DataFrame.from_dict(df_weights)
weightage = weightage.transpose()
weightage.columns = ['weightage']
np.sum(weightage['weightage'])
weightage.reset_index(inplace=True)
weightage.columns = ['stock','weights']

#calculating the annual return 
df = df.groupby(['stock','year']).agg(
{
    'avg':'mean'
})
df['prev_avg'] = df.groupby(['stock'])['avg'].shift(1)
df.reset_index(inplace=True)
df.dropna(inplace=True)
df['return'] = (df['avg'] - df['prev_avg'])/df['prev_avg']

#calculating the weighted annual return
df = df.merge(weightage,on='stock')
df['weighted_return'] = df['return']*df['weights']

#pivoting the table to get the covariance matrix and calculate the portfolio standard deviation
df_pivot = df.pivot('year', 'stock', 'weighted_return') 
df_pivot.reset_index(inplace=True)
cov_matrix = df_pivot.cov()

for i in range(len(cov_matrix)):
    for j in range(len(cov_matrix.columns)):
        if i != j:
            cov_matrix.iloc[i,j] = 2*cov_matrix.iloc[i,j]
            
portfolio_std_deviation = np.sqrt(np.sum(cov_matrix.sum(axis=0)))

#calculating the expected portfolio return
df_mean = df.groupby(['stock']).agg(
{
    'return':'mean'
})
df_mean.columns = ['expected_return']
df_std = df.groupby(['stock']).agg(
{
    'return':'std'
})
df_std.columns = ['standard_deviation']
df_stats = df_mean.merge(df_std,on='stock')
df_stats.reset_index(inplace=True)
df_stats = df_stats.merge(weightage,on='stock')
df_stats['expected_return_weighted'] = df_stats['expected_return']*df_stats['weights']

expected_portolio_return = np.sum(df_stats['expected_return_weighted'])

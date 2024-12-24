import pandas as pd

df = pd.read_csv('products.csv', encoding='utf-8')
df = df.fillna(0)
df = df.drop_duplicates()
df = df.drop(index=16)
df.to_csv('filtered.csv', index=False)

f_df = pd.read_csv('filtered.csv')

f_df = f_df.rename(columns={'feedback': 'reviews'})

columns_to_process = ['reviews', 'new_price', 'old_price']


for column in columns_to_process:
    f_df[column] = f_df[column].replace(' ', '', regex=True).astype(int)

try:
    f_df['rate'] = f_df['rate'].replace(' ', '', regex=True).astype(float)
except:
    f_df['rate'] = f_df['rate']


f_df['discount'] = (f_df['old_price'] - f_df['new_price']).apply(lambda x: 0 if x < 0 else x)
col = f_df.pop('discount')
f_df.insert(2, col.name, col)

f_df['discount_percentage'] = (f_df['discount'] / f_df['old_price'] * 100).round(1)
col = f_df.pop('discount_percentage')
f_df.insert(3, col.name, col)

f_df.head()

# print(f_df.nlargest(5, 'reviews'))

def reports():
    report = (
        f'Amout of goods: {f_df.shape[0]}\n',
        f'Avarage price with discount: {f_df["new_price"].mean()}\n',
        f'Avarage price without discount: {f_df["old_price"].mean().__round__(1)}\n',
        f'Max price with discount: {f_df["new_price"].max()}\n',
        '\n',
        'The most expensive products with discount:\n',
        f'{f_df.nlargest(5, "new_price")}\n',
        '\n',
        f'Max price without discount: {f_df["old_price"].max()}\n',
        '\n',
        'The most expensive products without discount:\n',
        f'{f_df.nlargest(5, "old_price")}\n',
        '\n',
        f'Min price with discount: {f_df["new_price"].min()}\n',
        f'Min price without discount: {f_df["old_price"].min()}\n',
        f'Max reviews: {f_df["reviews"].max()}\n',
        f'Min reviews: {f_df["reviews"].min()}\n',
        f'Avarage reviews: {f_df["reviews"].mean()}\n',
        '\n'
        'If we calculate that the number of reviews equals the number of sales.\n Then the most popular products are:\n',
        f'{f_df.nlargest(5, "reviews")}\n',
        '\n'
        f'Max discount: {f_df["discount"].max()}\n',
        f'Max discount percentage: {f_df["discount_percentage"].max()}\n',
        f'Min discount: {f_df["discount"].min()}\n',
        f'Min discount percentage: {f_df["discount_percentage"].min()}\n',
        f'Average discount: {f_df["discount"].mean().__round__(2)}\n',
        f'Average discount percentage: {f_df["discount_percentage"].mean().__round__(2)}\n',
        '\n'
        'The most favorable products based on the amount of discount:\n',
        f'{f_df.nlargest(5, "discount")}\n',
        '\n'
        'The most favorable products based on the percentage of discount:\n',
        f'{f_df.nlargest(5, "discount_percentage")}\n',
        '\n'
        'How many what ratings among the products:\n',
        f'{f_df["rate"].value_counts()}\n',
        '\n'
        'Top 5 products with the best ratings:\n',
        f'{f_df[f_df['rate'] == '5.0'].head()}\n',
        )
    return report

print(f_df.head())

report = reports()

with open('report.txt', 'w', encoding='utf-8') as file:
        for line in report:
            file.write(line)

f_df.to_csv('filtered.csv', index=False)


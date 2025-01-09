import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# stats dosyası doluysa çalıştırmana gerek yok. bir kez çalıştırılması yeterlidir, istatistik görsellerini kaydetmeye yarar.

data = pd.read_csv('car-price-dataset.csv')
data['Fiyat'] = data['Fiyat'] / 1e6 # fiyatı milyon cinsine çevirme
data['Kilometre'] = data['Kilometre'] / 1e4 # kilometreyi bin cinsine çevirme

# 1 - marka bazında ortalama fiyatın hesaplanması
brand_avg_price = data.groupby('Marka')['Fiyat'].mean().sort_values(ascending=False)

plt.figure(figsize=(14, 8))
sns.barplot(x=brand_avg_price.values, y=brand_avg_price.index, palette='viridis')
plt.title('Marka ve Ortalama Fiyat Dağılımı')
plt.xlabel('Ortalama Fiyat (Milyon TL)')
plt.ylabel('Marka')
plt.savefig('static/stats/stat1.png')


# 2 - kilometre bazında fiyat ilişkisi
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Kilometre', y='Fiyat', data=data)
plt.title('Kilometre ve Fiyat İlişkisi')
plt.xlabel('Kilometre (Bin)')
plt.ylabel('Fiyat (Milyon TL)')
plt.savefig('static/stats/stat2.png')

# 3 - kilometre ve yıl ilişkisi
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Yıl', y='Kilometre', data=data)
plt.title('Yıl ve Kilometre Dağılımı')
plt.xlabel('Yıl')
plt.ylabel('Kilometre (Bin)')
plt.savefig('static/stats/stat3.png')


# 4 - marka bazında araç dağılımı
plt.figure(figsize=(12, 8))
brand_counts = data['Marka'].value_counts()
sns.barplot(x=brand_counts.index, y=brand_counts.values)
plt.xticks(rotation=90)
plt.title('Marka Bazında Araç Sayısı')
plt.xlabel('Marka')
plt.ylabel('Araç Sayısı')
plt.savefig('static/stats/stat4.png')


# 5 - yakıt tipine göre araç dağılımı
plt.figure(figsize=(12, 8))
fuel_counts = data['YakıtTipi'].value_counts()
sns.barplot(x=fuel_counts.index, y=fuel_counts.values)
plt.title('Yakıt Tipine Göre Araç Dağılımı')
plt.xlabel('Yakıt Tipi')
plt.ylabel('Araç Sayısı')
plt.savefig('static/stats/stat5.png')


# 6 - araç yaşı ve fiyat ilişkisi
data['Yaş'] = 2024 - data['Yıl']

plt.figure(figsize=(14, 8))
sns.scatterplot(x='Yaş', y='Fiyat', data=data, hue='YakıtTipi', palette='Set1', alpha=0.6)
plt.title('Araç Yaşı ve Fiyat İlişkisi')
plt.xlabel('Araç Yaşı')
plt.ylabel('Fiyat (Milyon TL)')
plt.legend(title='Yakıt Tipi')
plt.grid(True)
plt.savefig('static/stats/stat6.png')

# 7 - yıl bazında ortalama fiyatı hesapla
filtered_data = data[data['Yıl'] >= 1980]

year_avg_price = filtered_data.groupby('Yıl')['Fiyat'].mean()

plt.figure(figsize=(14, 8))
sns.lineplot(x=year_avg_price.index, y=year_avg_price.values, marker='o', color='b')
plt.title('Yıl ve Ortalama Fiyat Değişimi (1980 sonrası)')
plt.xlabel('Yıl')
plt.ylabel('Ortalama Fiyat (Milyon TL)')
plt.grid(True)
plt.savefig('static/stats/stat7.png')

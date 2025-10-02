"""
Alcohol Consumption & Impact Dashboard
Author: Gautam
Date: 2025-09-29

This project was created for my personal portfolio and learning purposes only.
Please do not copy, redistribute, or use this code without my explicit permission.
"""

# --- Import required libraries ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap
import os

# --- Generate synthetic data for 10 years ---
np.random.seed(42)
years = np.arange(2016, 2026)
wine_shops = np.random.randint(100, 300, size=len(years))
consumers = np.random.randint(5000, 10000, size=len(years))
deaths = np.random.randint(100, 500, size=len(years))
age_18_30 = np.random.randint(2000, 4000, size=len(years))
age_31_50 = np.random.randint(1500, 3000, size=len(years))
age_51_plus = consumers - (age_18_30 + age_31_50)

# --- Create DataFrame ---
data = pd.DataFrame({
    'Year': years,
    'Wine_Shops': wine_shops,
    'Consumers': consumers,
    'Deaths': deaths,
    'Age_18_30': age_18_30,
    'Age_31_50': age_31_50,
    'Age_51_plus': age_51_plus
})

print("\nPreview of the data:")
print(data.head())

# --- Visualization Setup ---
sns.set_theme(style="whitegrid")
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# --- Load and Insert Background Image (Blended Full Canvas) ---
bg_path = 'consuming alchol.jpg'  # Ensure this image is in the same directory
if os.path.exists(bg_path):
    bg_img = mpimg.imread(bg_path)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig_bg_ax = fig.add_axes([0, 0, 1, 1], zorder=0)
    fig_bg_ax.imshow(bg_img, aspect='auto', extent=[0, 1, 0, 1], alpha=0.2)
    fig_bg_ax.axis('off')
else:
    print(f"⚠️ Background image '{bg_path}' not found. Proceeding without it.")

# --- Bar Chart ---
bar_width = 0.25
x = np.arange(len(years))
axs[0, 0].bar(x - bar_width, data['Wine_Shops'], width=bar_width, label='Wine Shops', color='#8B0000', zorder=2)
axs[0, 0].bar(x, data['Consumers'], width=bar_width, label='Consumers', color='#B22222', zorder=2)
axs[0, 0].bar(x + bar_width, data['Deaths'], width=bar_width, label='Deaths', color='#FF6347', zorder=2)
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(data['Year'])
axs[0, 0].set_title('Alcohol Trends Over Years')
axs[0, 0].legend()

# --- Line Chart ---
axs[0, 1].plot(data['Year'], data['Consumers'], marker='o', label='Consumers', color='#B22222', linewidth=2, zorder=2)
axs[0, 1].plot(data['Year'], data['Deaths'], marker='s', label='Deaths', color='#FF6347', linewidth=2, zorder=2)
axs[0, 1].set_title('Consumption vs Deaths Trend')
axs[0, 1].legend()

# --- Pie Chart ---
last_year = data.iloc[-1]
pie_labels = ['18-30', '31-50', '51+']
pie_sizes = [last_year['Age_18_30'], last_year['Age_31_50'], last_year['Age_51_plus']]
axs[1, 0].pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', startangle=140,
              colors=['#CD5C5C', '#F08080', "#FA7272"])
axs[1, 0].set_title(f"{last_year['Year']} Age-wise Consumption")

# --- Heatmap ---
corr = data[['Wine_Shops', 'Consumers', 'Deaths']].corr()
sns.heatmap(corr, annot=True, cmap='Reds', ax=axs[1, 1], cbar=True)
axs[1, 1].set_title('Correlation Heatmap')

# --- Main Title ---
plt.suptitle('Alcohol Consumption, Wine Shops & Deaths Analysis (2016–2025)', fontsize=18, fontweight='bold', color='#2F4F4F')

# --- Layout ---
plt.tight_layout(rect=[0, 0, 1, 0.96])

# --- Summary Box ---
best_year = data.loc[data['Consumers'].idxmax(), 'Year']
worst_year = data.loc[data['Deaths'].idxmax(), 'Year']
note_text = (
    f"Highest Consumption Year: {best_year} ({data['Consumers'].max()} consumers)\n"
    f"Highest Deaths Year: {worst_year} ({data['Deaths'].max()} deaths)"
)
plt.gcf().text(0.02, 0.01, note_text, fontsize=9, color='#2F4F4F', ha='left', va='bottom', fontweight='bold')

# --- Footer ---
plt.gcf().text(0.5, -0.04, 'Thank you for viewing this dashboard!\nCreated by Gautam | 2025',
              fontsize=11, color='#8B0000', ha='center', va='top',
              bbox=dict(facecolor='#f2e9e4', edgecolor='#8B0000', boxstyle='round,pad=0.5'))

# --- Highlights ---
best_idx = data['Consumers'].idxmax()
worst_idx = data['Deaths'].idxmax()
axs[0, 1].annotate('Peak Consumption',
                   xy=(data['Year'][best_idx], data['Consumers'][best_idx]),
                   xytext=(data['Year'][best_idx], data['Consumers'][best_idx]+500),
                   arrowprops=dict(facecolor='green', shrink=0.05),
                   fontsize=10, color='green', fontweight='bold')
axs[0, 1].annotate('Peak Deaths',
                   xy=(data['Year'][worst_idx], data['Deaths'][worst_idx]),
                   xytext=(data['Year'][worst_idx], data['Deaths'][worst_idx]+50),
                   arrowprops=dict(facecolor='red', shrink=0.05),
                   fontsize=10, color='red', fontweight='bold')

# --- Gradient Background (Bar Chart Only) ---
z = np.linspace(0, 1, 256).reshape(1, -1)
axs[0, 0].imshow(z, aspect='auto', cmap=LinearSegmentedColormap.from_list('winefade', ['#ffe5e0', '#8B0000']),
                 extent=[-0.5, len(years)-0.5, 0, max(data['Consumers'])+1000], alpha=0.2, zorder=1)

# --- Summary Stats ---
print("\nSummary Statistics:\n", data.describe())

# --- Rates ---
death_rate = (data['Deaths'] / data['Consumers']).mean()
print(f"\nHighest consumption year: {best_year}")
print(f"Highest death year: {worst_year}")
print(f"Average death rate: {death_rate:.2%}")

# --- Save and Show ---
plt.savefig('alcohol_dashboard.png', bbox_inches='tight')
plt.show()

# --- Prevent Instant Close ---
input("\nPress Enter to exit...")

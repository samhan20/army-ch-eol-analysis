import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for better visualizations
plt.style.use('seaborn-v0_8')  # Using a valid style name
sns.set_theme()  # This will set seaborn's default styling

# Read the CSV file
df = pd.read_csv('EOL post survey analysis.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Drop unnecessary columns
columns_to_drop = ['Respondent #', 'Are you a 56M or 56A', 'How many years have you been serving as a 56M/56A']
df = df.drop(columns=columns_to_drop)

# Create a function to save plots
def save_plot(fig, filename):
    # Adjust layout to prevent legend overlap
    plt.tight_layout()
    # Add extra space for the legend
    plt.subplots_adjust(right=0.85)
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

# Function to get response columns (excluding count columns)
def get_response_columns(df):
    # Get all numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Exclude columns that are likely to be counts or identifiers
    response_cols = [col for col in numeric_cols if not any(x in col.lower() for x in ['count', 'id', 'number'])]
    return response_cols

# Function to create a plot with proper legend placement
def create_plot(data, title, filename):
    plt.figure(figsize=(15, 8))  # Increased figure size
    ax = data.plot(kind='bar')
    plt.title(title, pad=20)  # Add padding to title
    plt.xticks(rotation=45, ha='right')  # Rotate and align x-axis labels
    
    # Move legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    # Adjust layout with more space for legend
    plt.subplots_adjust(right=0.85, bottom=0.2)  # Make room for legend and x-axis labels
    
    save_plot(plt.gcf(), filename)

# 1. Experience-based Analysis
def create_experience_analysis():
    # Get response columns
    response_cols = get_response_columns(df)
    
    # EOLC Experience
    eolc_means = df.groupby('Provided End of Life Care (EOLC)')[response_cols].mean()
    create_plot(eolc_means, 'Mean Responses by EOLC Experience', 'eolc_experience_analysis.png')
    
    # Combat Experience
    combat_means = df.groupby('Been in Combat Situations')[response_cols].mean()
    create_plot(combat_means, 'Mean Responses by Combat Experience', 'combat_experience_analysis.png')
    
    # Cadaver Experience
    cadaver_means = df.groupby('Worked with Cadavers')[response_cols].mean()
    create_plot(cadaver_means, 'Mean Responses by Cadaver Experience', 'cadaver_experience_analysis.png')

# 2. Preparedness Analysis
def create_preparedness_analysis():
    # Get response columns
    response_cols = get_response_columns(df)
    
    # EOLC Preparedness
    eolc_prep = df.groupby('Q1. Do you feel prepared to provide end of life care to this dying Soldier?')[response_cols].mean()
    create_plot(eolc_prep, 'Mean Responses by EOLC Preparedness', 'eolc_preparedness_analysis.png')
    
    # Multiple Cases Preparedness
    multi_prep = df.groupby('Q3. Do you feel prepared to handle more than 10 situations like Soldier each day over a sustained period?')[response_cols].mean()
    create_plot(multi_prep, 'Mean Responses by Multiple Cases Preparedness', 'multiple_cases_preparedness_analysis.png')

# 3. Faith and Comfort Analysis
def create_faith_comfort_analysis():
    # Get response columns
    response_cols = get_response_columns(df)
    
    # Faith Group Analysis
    faith_means = df.groupby('S1 Q4. Are you the same faith group as Soldier.')[response_cols].mean()
    create_plot(faith_means, 'Mean Responses by Faith Group Alignment', 'faith_group_analysis.png')
    
    # Comfort Level Analysis
    comfort1 = df.groupby('S1 Q5. If not, do you feel comfortable providing end-of-life care, such as offering prayer outside your faith or performing last rites?')[response_cols].mean()
    create_plot(comfort1, 'Mean Responses by Comfort Level with Different Faith Practices', 'comfort_level_analysis.png')

# 4. Scenario Response Analysis
def create_scenario_analysis():
    scenario_columns = [
        'S1 Q2. When SPC Smith asks you if he is going to die, will you tell him yes?',
        'S2 Q2. In his dying moments, SGT Tanner asks you if Jimmy, his team leader, is okay. Will you tell him that Jimmy is dead?',
        'S3 Q2. As the Soldier dies, the medic asks you to pray over the foreign Soldier. Will you pray for this foreign Soldier because the medic requested it?',
        'S4 Q2. As CPT Mohamed dies, he asks you to pray over him. Will you pray a Muslim prayer per his request?'
    ]
    
    # Get response columns
    response_cols = get_response_columns(df)
    
    for idx, col in enumerate(scenario_columns):
        scenario_means = df.groupby(col)[response_cols].mean()
        create_plot(scenario_means, f'Mean Responses by Scenario {idx+1} Response', f'scenario{idx+1}_analysis.png')

# 5. Summary Statistics
def create_summary_statistics():
    # Get response columns
    response_cols = get_response_columns(df)
    
    # Create summary for numeric columns
    summary_stats = df[response_cols].describe()
    
    # Add response counts for categorical columns
    categorical_cols = ['Provided End of Life Care (EOLC)', 'Been in Combat Situations', 'Worked with Cadavers']
    for col in categorical_cols:
        summary_stats[col] = df[col].value_counts()
    
    # Save to CSV
    summary_stats.to_csv('summary_statistics.csv')
    
    # Create a text file with key findings
    with open('key_findings.txt', 'w') as f:
        f.write("Key Findings from EOL Survey Analysis:\n\n")
        
        # Experience Summary
        f.write("Experience Summary:\n")
        f.write(f"Total Respondents: {len(df)}\n")
        f.write(f"EOLC Experience: {df['Provided End of Life Care (EOLC)'].value_counts().to_dict()}\n")
        f.write(f"Combat Experience: {df['Been in Combat Situations'].value_counts().to_dict()}\n")
        f.write(f"Cadaver Experience: {df['Worked with Cadavers'].value_counts().to_dict()}\n\n")
        
        # Preparedness Summary
        f.write("Preparedness Summary:\n")
        f.write(f"EOLC Preparedness: {df['Q1. Do you feel prepared to provide end of life care to this dying Soldier?'].value_counts().to_dict()}\n")
        f.write(f"Multiple Cases Preparedness: {df['Q3. Do you feel prepared to handle more than 10 situations like Soldier each day over a sustained period?'].value_counts().to_dict()}\n\n")
        
        # Faith and Comfort Summary
        f.write("Faith and Comfort Summary:\n")
        f.write(f"Same Faith Group as Soldier: {df['S1 Q4. Are you the same faith group as Soldier.'].value_counts().to_dict()}\n")
        f.write(f"Comfort with Different Faith Practices: {df['S1 Q5. If not, do you feel comfortable providing end-of-life care, such as offering prayer outside your faith or performing last rites?'].value_counts().to_dict()}\n")

# Execute all visualizations
def main():
    print("Creating visualizations...")
    create_experience_analysis()
    create_preparedness_analysis()
    create_faith_comfort_analysis()
    create_scenario_analysis()
    create_summary_statistics()
    print("Visualizations completed! Check the generated files.")

if __name__ == "__main__":
    main() 
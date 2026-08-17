import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_theme()

# Read both CSV files
pre_df = pd.read_csv('EOL pre survey analysis.csv')
post_df = pd.read_csv('EOL post survey analysis.csv')

# Clean column names
pre_df.columns = pre_df.columns.str.strip()
post_df.columns = post_df.columns.str.strip()

# Drop unnecessary columns
columns_to_drop = ['Respondent #', 'Are you a 56M or 56A', 'How many years have you been serving as a 56M/56A']
pre_df = pre_df.drop(columns=columns_to_drop, errors='ignore')
post_df = post_df.drop(columns=columns_to_drop, errors='ignore')

def create_comparison_plot(pre_data, post_data, title, filename):
    plt.figure(figsize=(15, 8))
    
    # Get all unique categories
    all_categories = sorted(set(pre_data.index) | set(post_data.index))
    
    # Reindex both series to include all categories
    pre_data = pre_data.reindex(all_categories, fill_value=0)
    post_data = post_data.reindex(all_categories, fill_value=0)
    
    # Create grouped bar chart
    x = np.arange(len(all_categories))
    width = 0.35
    
    plt.bar(x - width/2, pre_data, width, label='Pre-Survey')
    plt.bar(x + width/2, post_data, width, label='Post-Survey')
    
    plt.title(title, pad=20)
    plt.xticks(x, all_categories, rotation=45, ha='right')
    plt.legend()
    
    plt.subplots_adjust(bottom=0.2, right=0.95)
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

def analyze_experience():
    # Experience indicators
    experience_cols = ['Provided End of Life Care (EOLC)', 'Been in Combat Situations', 'Worked with Cadavers']
    
    for col in experience_cols:
        pre_counts = pre_df[col].value_counts()
        post_counts = post_df[col].value_counts()
        create_comparison_plot(pre_counts, post_counts, 
                             f'Comparison of {col} Experience', 
                             f'comparison_{col.lower().replace(" ", "_")}.png')

def analyze_preparedness():
    # Preparedness questions
    prep_cols = [
        'Q1. Do you feel prepared to provide end of life care to this dying Soldier?',
        'Q3. Do you feel prepared to handle more than 10 situations like Soldier each day over a sustained period?'
    ]
    
    for col in prep_cols:
        pre_counts = pre_df[col].value_counts()
        post_counts = post_df[col].value_counts()
        create_comparison_plot(pre_counts, post_counts,
                             f'Comparison of {col}', 
                             f'comparison_{col.split(".")[0].lower().replace(" ", "_")}.png')

def analyze_scenarios():
    # Scenario questions (use tuples for pre and post column names)
    scenario_cols = [
        ('S1 Q2. When SPC Smith asks you if he is going to die, will you tell him yes?',
         'S1 Q2. When SPC Smith asks you if he is going to die, will you tell him yes?'),
        ('S2 Q2. In his dying moments, SGT Tanner asks you if Jimmy, his team leader, is okay. Will you tell him that Jimmy is dead?',
         'S2 Q2. In his dying moments, SGT Tanner asks you if Jimmy, his team leader, is okay. Will you tell him that Jimmy is dead?'),
        ('S3 Q2. As the Soldier dies, the medic asks you to pray over the foreign Soldier. Will you pray for this foreign Soldier because the medic requested it?',
         'S3 Q2. As the Soldier dies, the medic asks you to pray over the foreign Soldier. Will you pray for this foreign Soldier because the medic requested it?'),
        ('S4 Q2. As CPT Mohamed dies, he asks you to pray over him. Will you pray for a Muslim Soldier per his request?',
         'S4 Q2. As CPT Mohamed dies, he asks you to pray over him. Will you pray a Muslim prayer per his request?')
    ]
    
    for pre_col, post_col in scenario_cols:
        pre_counts = pre_df[pre_col].value_counts()
        post_counts = post_df[post_col].value_counts()
        create_comparison_plot(pre_counts, post_counts,
                             f'Comparison of {pre_col}', 
                             f'comparison_scenario_{pre_col.split(".")[0].lower().replace(" ", "_")}.png')

def generate_summary():
    with open('survey_comparison_summary.txt', 'w') as f:
        f.write("Survey Comparison Summary\n")
        f.write("=======================\n\n")
        
        # Experience Summary
        f.write("1. Experience Comparison\n")
        f.write("----------------------\n")
        for col in ['Provided End of Life Care (EOLC)', 'Been in Combat Situations', 'Worked with Cadavers']:
            pre_yes = (pre_df[col] == 'Y').mean() * 100
            post_yes = (post_df[col] == 'Y').mean() * 100
            f.write(f"{col}:\n")
            f.write(f"  Pre-Survey: {pre_yes:.1f}% Yes\n")
            f.write(f"  Post-Survey: {post_yes:.1f}% Yes\n")
            f.write(f"  Change: {post_yes - pre_yes:+.1f}%\n\n")
        
        # Preparedness Summary
        f.write("\n2. Preparedness Comparison\n")
        f.write("------------------------\n")
        prep_cols = [
            'Q1. Do you feel prepared to provide end of life care to this dying Soldier?',
            'Q3. Do you feel prepared to handle more than 10 situations like Soldier each day over a sustained period?'
        ]
        for col in prep_cols:
            pre_mean = pre_df[col].mean()
            post_mean = post_df[col].mean()
            f.write(f"{col}:\n")
            f.write(f"  Pre-Survey Mean: {pre_mean:.2f}\n")
            f.write(f"  Post-Survey Mean: {post_mean:.2f}\n")
            f.write(f"  Change: {post_mean - pre_mean:+.2f}\n\n")
        
        # Scenario Response Summary
        f.write("\n3. Scenario Response Comparison\n")
        f.write("----------------------------\n")
        scenario_cols = [
            ('S1 Q2. When SPC Smith asks you if he is going to die, will you tell him yes?',
             'S1 Q2. When SPC Smith asks you if he is going to die, will you tell him yes?'),
            ('S2 Q2. In his dying moments, SGT Tanner asks you if Jimmy, his team leader, is okay. Will you tell him that Jimmy is dead?',
             'S2 Q2. In his dying moments, SGT Tanner asks you if Jimmy, his team leader, is okay. Will you tell him that Jimmy is dead?'),
            ('S3 Q2. As the Soldier dies, the medic asks you to pray over the foreign Soldier. Will you pray for this foreign Soldier because the medic requested it?',
             'S3 Q2. As the Soldier dies, the medic asks you to pray over the foreign Soldier. Will you pray for this foreign Soldier because the medic requested it?'),
            ('S4 Q2. As CPT Mohamed dies, he asks you to pray over him. Will you pray for a Muslim Soldier per his request?',
             'S4 Q2. As CPT Mohamed dies, he asks you to pray over him. Will you pray a Muslim prayer per his request?')
        ]
        for pre_col, post_col in scenario_cols:
            pre_mean = pre_df[pre_col].mean()
            post_mean = post_df[post_col].mean()
            f.write(f"{pre_col}:\n")
            f.write(f"  Pre-Survey Mean: {pre_mean:.2f}\n")
            f.write(f"  Post-Survey Mean: {post_mean:.2f}\n")
            f.write(f"  Change: {post_mean - pre_mean:+.2f}\n\n")

def main():
    print("Analyzing survey comparisons...")
    analyze_experience()
    analyze_preparedness()
    analyze_scenarios()
    generate_summary()
    print("Analysis complete! Check the generated files.")

if __name__ == "__main__":
    main() 
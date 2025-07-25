import pandas as pd

def create_funnel_table(df, platform):
    # Filter only by platform first
    df_filtered = df[df['Source'].str.lower() == platform.lower()].copy()
    
    # Initialize the Funnel column as None
    df_filtered['Funnel'] = None

    # Assign 'Product' if Comment contains 'Product'
    mask_product = df_filtered['Comment'].str.contains('Product', case=False, na=False)
    df_filtered.loc[mask_product, 'Funnel'] = 'Product'

    # Assign 'Paid' if Comment contains 'Paid' but NOT 'Product'
    mask_paid = (
        df_filtered['Comment'].str.contains('Paid', case=False, na=False) &
        ~df_filtered['Comment'].str.contains('Product', case=False, na=False)
    )
    df_filtered.loc[mask_paid, 'Funnel'] = 'Paid'

    # Assign 'Free' according to platform logic
    if platform.lower() == 'google':
        mask_free = ~df_filtered['Comment'].str.contains('Paid', case=False, na=False)
    elif platform.lower() == 'facebook':
        mask_free = (
            ~df_filtered['Comment'].str.contains('Paid', case=False, na=False) |
            (df_filtered['Comment'].isna())
        )
    else:
        # Default Free logic if platform is neither Google nor Facebook
        mask_free = ~df_filtered['Comment'].str.contains('Paid', case=False, na=False)
    
    # Only assign 'Free' where Funnel is still empty (i.e., not already Product or Paid)
    df_filtered.loc[mask_free & df_filtered['Funnel'].isna(), 'Funnel'] = 'Free'
    
    return df_filtered


def create_funnel_table2(df, platform):
    # Filter only by platform first
    df_filtered = df[df['Platform'].str.lower() == platform.lower()].copy()
    
    # Initialize the Funnel column as None
    df_filtered['Funnel'] = None

    # Assign 'Product' if Comment contains 'Product'
    mask_product = df_filtered['CampaignName'].str.contains('Product', case=False, na=False) | df_filtered['AdName'].str.contains('Product', case=False, na=False)
    df_filtered.loc[mask_product, 'Funnel'] = 'Product'

    # Assign 'Paid' if Comment contains 'Paid' but NOT 'Product'
    mask_paid = (
        df_filtered['CampaignName'].str.contains('Paid|conversion', case=False, na=False) &
       ~df_filtered['CampaignName'].str.contains('Product', case=False, na=False) & ~df_filtered['AdName'].str.contains('Product', case=False, na=False)
    )
    df_filtered.loc[mask_paid, 'Funnel'] = 'Paid'

    # Assign 'Free' according to platform logic
    if platform.lower() == 'google':
        mask_free = ~df_filtered['CampaignName'].str.contains('Paid', case=False, na=False)
    elif platform.lower() == 'facebook':
        mask_free = (
            ~df_filtered['CampaignName'].str.contains('Conversion', case=False, na=False) 
        )
    else:
        # Default Free logic if platform is neither Google nor Facebook
        mask_free = ~df_filtered['CampaignName'].str.contains('Paid', case=False, na=False)
    
    # Only assign 'Free' where Funnel is still empty (i.e., not already Product or Paid)
    df_filtered.loc[mask_free & df_filtered['Funnel'].isna(), 'Funnel'] = 'Free'
    
    return df_filtered



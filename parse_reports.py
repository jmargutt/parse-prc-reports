import pandas as pd
import click
import os

@click.command()
@click.option('--input', default='input', help='input directory with chapter reports')
@click.option('--output', default='output/output.xlsx', help='output (xlsx)')
def main(input, output):
    """ merge PRC chapter reports into one table and save it """

    # load chapter reports
    reports = os.listdir(input)
    dfc = pd.DataFrame()
    for report in reports:
        dfc_ = pd.read_excel(os.path.join(input, report), sheet_name='Chapter Relief', skiprows=8)
        dfc = dfc.append(dfc_, ignore_index=True)

    # fix typo in one column
    if 'fam' in dfc.columns:
        dfc = dfc.rename(columns={'fam': 'Emergency Cash'})

    # create a dictionary to map activities to sector
    sectors = {'Relief': ['2-3 days ration', '15 days Rations',
                          '30 days rations', 'Assorted', 'SK: Blankets ', 'SK: Mats',
                          'SK:Mosquito Nets', 'Hygiene Kit', 'Jerry Can', 'Jerry Can 20L',
                          'Kitchen Set', 'Tarpaulin', 'Tent', 'CGI', 'SHELTER KIT', 'Emergency Cash'],
               'Welfare': ['Welfare Desk', 'Hotmeals/ Biscuits', 'Psychosocial First Aid',
                           'Child Friendly Space Activities', 'Restoring Family Link/ I am Alive',
                           'Welfare Referral', 'Tracing'],
               'WASH': ['Water (Liters)', 'Family Received',
                        'Hygiene Promotion', 'Portalets'],
               'Health': ['Health Care (BHCU/AMP/EFH)',
                          'Medicine Dispence', 'Health Referral', 'First Aid Station',
                          'First Aid Management', 'Ambulance Transport', 'BP Taking',
                          'Basic Health Care (Consultation)', 'Health Promotion',
                          'Blood Sugar Testing', 'Blood (Units) - Augmented']}
    activities = [x for key, val in sectors.items() for x in val]

    # create a dictionary to map activities to unit
    units = {'families': ['Date of Activity', 'Location Notes/Place/Evacuation Center',
                          'Barangay', 'Municipality/ City', 'Province', 'Chapter',
                          'Relief  Donor', '2-3 days ration', '15 days Rations',
                          '30 days rations', 'Assorted', 'SK: Blankets ', 'SK: Mats',
                          'SK:Mosquito Nets', 'Hygiene Kit', 'Jerry Can', 'Jerry Can 20L',
                          'Kitchen Set', 'Tarpaulin', 'Tent', 'CGI', 'SHELTER KIT',
                          'Emergency Cash', 'Family Received'],
             'individuals': ['Hotmeals/ Biscuits',
                             'Psychosocial First Aid', 'Child Friendly Space Activities',
                             'Restoring Family Link/ I am Alive', 'Welfare Referral', 'Tracing',
                             'Hygiene Promotion', 'Portalets',
                             'Health Care (BHCU/AMP/EFH)', 'Medicine Dispence', 'Health Referral',
                             'First Aid Management', 'Ambulance Transport',
                             'BP Taking', 'Basic Health Care (Consultation)', 'Health Promotion',
                             'Blood Sugar Testing'],
             'units': ['Welfare Desk', 'Blood (Units) - Augmented'],
             'stations': ['First Aid Station']}

    # initialize empty dataframe (output)
    dff = pd.DataFrame()

    # loop over chapter report rows and add to output
    for ix, row in dfc.iterrows():
        for activity in activities:
            if not pd.isna(row[activity]):

                for key, val in sectors.items():
                    if activity in val:
                        sector = key
                for key, val in units.items():
                    if activity in val:
                        unit = key
                served = 'families' if unit == 'families' else 'individuals'

                series_to_append = {'Organisation': 'Philippine Red Cross',
                                    'Implementing Partner/Supported by': 'PRC',
                                    'Phase': 'EMERGENCY',
                                    'Sector/Cluster': sector,
                                    'Sub Sector': sector,
                                    'Region': '',
                                    'Province': row['Province'],
                                    'Municipality/City': row['Municipality/ City'],
                                    'Barangay': row['Barangay'],
                                    'Place Name': '',
                                    'Activity': activity,
                                    'Materials/Service Provided': activity,
                                    'Quantity': row[activity],
                                    'Unit': unit,
                                    'Primary Beneficiary Served': served,
                                    '# of Beneficiaries Served': row[activity],
                                    'Status': 'Finished',
                                    'Start Date': row['Date of Activity'],
                                    'End Date': row['Date of Activity'],
                                    'SOURCE': 'Chapter DSR',
                                    'Signature': '',
                                    'Weather System': '',
                                    'Remarks': ''}
                dff = dff.append(pd.Series(series_to_append), ignore_index=True)
    # re-order columns
    dff = dff['Organisation', 'Implementing Partner/Supported by', 'Phase',
           'Sector/Cluster', 'Sub Sector', 'Region', 'Province',
           'Municipality/City', 'Barangay', 'Place Name', 'Activity',
           'Materials/Service Provided', 'Quantity', 'Unit',
           'Primary Beneficiary Served', '# of Beneficiaries Served', 'Status',
           'Start Date', 'End Date', 'SOURCE', 'Signature', 'Weather System',
           'Remarks']

    # save output
    dff.to_excel(output, index=False)

if __name__ == "__main__":
    main()
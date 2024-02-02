from datetime import datetime, timedelta

import pandas as pd
import seaborn as sns

def calc_home_cost(base_rent, mortgage_per_month, offer_accept_date, 
                   start_calc_date, end_lease_date, stop_calc_date, month2month_rent):
    
    print(f"------ Offer accept date: {offer_accept_date} ---------")
    
    # time from offer accepted to move
    time_to_move=timedelta(days=60)

    rent_per_day = base_rent*12/365
    month_to_month_rate = month2month_rent*12/365
    mortgage_per_day = mortgage_per_month*12/365
    # convert to datetime
    start_calc_datetime = datetime.strptime(start_calc_date, '%m-%d-%Y')
    stop_calc_datetime = datetime.strptime(stop_calc_date, '%m-%d-%Y')
    end_lease_datetime = datetime.strptime(end_lease_date, '%m-%d-%Y')
    offer_accept_datetime = datetime.strptime(offer_accept_date, '%m-%d-%Y')

    # calculate move date
    move_datetime = offer_accept_datetime + time_to_move
    print(f"Move date: {move_datetime}")

    rent_paid = paid_in_rent(start_calc_datetime, end_lease_datetime, move_datetime, month_to_month_rate, rent_per_day)
    
    # calculate amount paid in mortgage
    mortgage_days = (stop_calc_datetime - move_datetime).days
    print(f"days at home: {mortgage_days}")
    
    mortgage_days -= 30 # skip mortgage payment on the first 30 days
    mortgage_paid = mortgage_per_day*(stop_calc_datetime - move_datetime).days

    total_paid = rent_paid + mortgage_paid

    cost_per_month = total_paid/((stop_calc_datetime - start_calc_datetime).days/30)
    
    cost_dict = {
        'Offer accept date':offer_accept_date,
        'Cost per month':cost_per_month,
        # 'Overlap spent': overlap,
        'rent paid': rent_paid,
        'mortgage paid': mortgage_paid,
        'total paid': total_paid,
    }
    
    return cost_dict
    
def paid_in_rent(start_calc_datetime, end_lease_datetime, move_datetime, month_to_month_rate, rent_per_day):
    # calculate amount paid in rent
    days_month_to_month = (move_datetime - end_lease_datetime).days
    days_month_to_month = 0 if days_month_to_month < 0 else days_month_to_month

    rent_month_to_month = days_month_to_month * month_to_month_rate
    
    print(f"days month to month: {days_month_to_month}")
    
    days_at_apartment=(end_lease_datetime-start_calc_datetime).days
    
    print(f"days at apartment: {days_at_apartment}")
    
    rent_paid = (rent_per_day*days_at_apartment) + rent_month_to_month
    
    return rent_paid

def sample_monthly_example():
    base_rent=1951
    mortgage_per_month=2500

    table_out = []
    for months in range(0,8):
        offer_accept_date = datetime.strptime('02-01-2024', '%m-%d-%Y') + timedelta(days=months*30)
        offer_accept_date_str = offer_accept_date.strftime('%m-%d-%Y')
        
        cost_dict = calc_home_cost(
            base_rent = base_rent,
            mortgage_per_month = mortgage_per_month,
            offer_accept_date = offer_accept_date_str,
            start_calc_date = '01-01-2024',
            end_lease_date = '05-27-2024',
            stop_calc_date = '11-30-2024',
            month2month_rent = 3000
        )
        
        table_out.append(cost_dict)

    df = pd.DataFrame(table_out)

    sns.lineplot(data=df,x='Offer accept date', y='Cost per month')
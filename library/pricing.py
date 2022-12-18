import numpy as np
import pandas as pd

def bond_cash_flow_calc(bond_len, coupon_per, par_val, len_time='annual', details=True):
    """ Calculate Cash-flows for a Bond
    
    Given args are converted into numpy arrrays. 
    They are then used to calculate what the payout is for a bond during its life into maturity.
    
    Args:
        bond_len (int): Number of bond periods before maturity.
        coupon_per (float): Current interest rate return on a bond per specified period.
        par_val (float): Value of bond at par.
        len_time (str): Period length designation.
        details (bool): Determines whether to print calculation results.
        
    Returns:
        np.float: The 1st return value. Number of payments per period.
        np.float: The 2nd return value. Return of par value at maturity.
        np.float: The 3rd return value. Number of periods of return.
        
    """
    
    # convert to numpy arrays
    bond_len = np.array(bond_len)
    coupon_per = np.array(coupon_per)
    par_val = np.array(par_val)
    
    # fail safe
    if (bond_len.size != coupon_per.size) | (coupon_per.size != par_val.size):
        return 'Incorrect argument dimensions'
    if len_time.lower() not in ('semiannual', 'annual'):
        return 'Incorrect period length description'

    # adjust fields based on length of bond period
    period = np.where(len_time.lower()=='semiannual', 2, 1)
    bond_len = np.multiply(bond_len, period)
    coupon_per = np.divide(coupon_per, period)
    
    # adjust for given coupon rate format
    coupon_per = np.where(coupon_per > 1, np.divide(coupon_per, 100), coupon_per)
    
    # calculate cash-flow
    coupon_per = np.multiply(par_val, coupon_per)
    
    if details:
        if bond_len.size == 1:
            print(len_time.capitalize() + ' Coupon Rate - ${:.2f} for {} periods'.format(coupon_per, bond_len))
            print('Maturity Value - ${:.2f}'.format(par_val))
        else:
            np.set_printoptions(precision=2)
            print(len_time.capitalize() + ' Coupon Rate - ${} for {} periods'.format(coupon_per, bond_len))
            print('Maturity Value - ${}'.format(par_val))
        
    return coupon_per, par_val, bond_len

def bond_price_calc(bond_len, coupon_per, par_val, req_yield_per, call_val=0, len_time='annual', details=True):
    """ Calculate Pricing for a Bond
    
    Given args are converted into numpy arrrays. 
    They are then used to calculate what the payout is for a bond during its life into maturity.
    
    Args:
        bond_len (int): Number of bond periods before maturity.
        coupon_per (float): Current interest rate return on a bond per specified period.
        par_val (float): Value of bona at par.
        req_yield_per (float): Expected yearly return on bond.
        call_val (float): Value of bond at first callable event.        
        len_time (str): Period length designation.
        details (bool): Determines whether to print calculation results.
        
    Returns:
        np.float: The 1st return value. The price of the coupon payment.
        np.float: The 2nd return value. The value at maturity.
        np.float: The 3rd return value. The current price of the bond.
        
    """
    # convert to numpy arrays
    bond_len = np.array(bond_len)
    coupon_per = np.array(coupon_per)
    par_val = np.array(par_val)
    req_yield_per = np.array(req_yield_per)
    
    # fail safe
    if (bond_len.size != coupon_per.size) | (coupon_per.size != par_val.size):
        return 'Incorrect argument dimensions'
    if len_time.lower() not in ('semiannual', 'annual'):
        return 'Incorrect period length description'
    
    # adjust fields based on length of bond period
    p1 = np.where(len_time.lower()=='semiannual', np.divide(12.0, 6.0), 0.0)
    p2 = np.where(len_time.lower()=='annual', np.divide(12.0, 12.0), 0.0)
    period = np.add(p1, p2)
    bond_len = np.multiply(bond_len, period)
    coupon_per = np.divide(coupon_per, period)
    req_yield_per = np.divide(req_yield_per, period)
    
    # adjust for given coupon rate format
    coupon_per = np.where(coupon_per > 1, np.divide(coupon_per, 100), coupon_per)
    req_yield_per = np.where(req_yield_per > 1, np.divide(req_yield_per, 100), req_yield_per)
    
    # calculate cash-flow
    coupon_pay, par_val = bond_cash_flow_calc(bond_len, coupon_per, par_val, len_time='annual', details=details)[0:2]
    par_val = np.where(call_val>0, call_val, par_val)
    
    # calculate price
    coupon_pay_price = np.round(np.multiply(coupon_pay, np.divide(np.subtract(1, np.divide(1, np.power(np.add(1, req_yield_per), bond_len))), req_yield_per)), decimals=2)
    par_val_price = np.round(np.multiply(par_val, np.divide(1, np.power(np.add(1, req_yield_per), bond_len))), decimals=2)
    bond_price = np.round(np.add(coupon_pay_price, par_val_price), decimals=2)
    
    if details:
        if (bond_len.size == 1) & (req_yield_per.size == 1):
            print('Present Value of Coupon Payment - ${:.2f}'.format(coupon_pay_price))
            print('Present Value of Par/Maturity Value - ${:.2f}'.format(par_val_price))
            print('Present Value of Bond - ${:.2f}'.format(bond_price))
        else:
            np.set_printoptions(precision=2)
            print('Present Value of Coupon Payment - ${}'.format(coupon_pay_price))
            print('Present Value of Par/Maturity Value - ${}'.format(par_val_price))
            print('Present Value of Bond - ${}'.format(bond_price))
        
    return coupon_pay_price, par_val_price, bond_price

def actual_time_ratio_calc(nd1, sd2, period):
    """ Calculate Ratio of Days Between Two Dates to Days in a Year
     
    They are then used to calculate days between settlement date and maturity date based on days in a year.
    Based on the fllowing option:
       - Actual: Direct count of days between dates
    Used to calculate time ratio for a given count of days in a year.
    
    Args:
        nd1 (date): Date of next payout for a bond.
        sd2 (date): Date of settlement for a bond, or official purchase date.
        period (int): number of bond payouts until maturity.
        
    Returns:
        np.float: The time ratio for number of days between maturity and settlement dates and total number of days in a year.
        np.float: The time ratio for number of days between settlement date and next coupon date and total number of days in a year.
        
    """
    numer = (nd1 - sd2) / np.timedelta64(1, 'D')
    denom = (nd1 - np.datetime64(np.datetime64(nd1, 'M') - np.timedelta64(6, 'M'), 'D')) / np.timedelta64(1, 'D')
    return np.divide(numer, denom), np.divide(np.subtract(denom, numer), denom)

def thirtysixty_time_ratio_calc(sd1, dr2, td3, period):
    """ Calculate Ratio of Days Between Two Dates to Days in a Year
     
    They are then used to calculate days between settlement date and maturity date based on days in a year.
    Based on the following option:
       - 30/60: Every month is treated for 30 days
    Used to calculate time ratio for a given count of days in a year.
    
    Args:
        sd1 (date): Date of settlement for a bond, or official purchase date.
        dr2 (int): Number of days remaining to next bond payout.
        td3 (int): Number of days from maturity to settlement date.
        period (int): number of bond payouts until maturity.
        
    Returns:
        np.float: The time ratio for number of days between maturity and settlement dates and total number of days in a year.
        np.float: The time ratio for number of days between settlement date and next coupon date and total number of days in a year.
        
    """    
    days_passed = (sd1 - (np.datetime64(sd1, 'M') - np.timedelta64(1, 'D'))) / np.timedelta64(1, 'D')
    days_remaining = np.where(np.add(dr2, days_passed) > 30, np.subtract(30, days_passed), dr2)
    numer = np.add(np.add(np.multiply(np.subtract(td3, 1), 30), days_remaining), 1)
    denom = np.multiply(30, period)
    return np.divide(numer, denom), np.divide(np.subtract(denom, numer), denom)
    
def next_pay_date_calc(sd1, md2, period):
    """ Calculate the Date of the Next Payout Period
     
    Finds the exact date for the next payout period.
    
    Args:
        sd1 (date): Date of settlement for a bond, or official purchase date.
        md2 (date): Date of maturity for a bond.
        period (int): number of bond payouts until maturity.
        
    Returns:
        np.datetime64: Date of next payout period for a bond.
        
    """
    days_remaining = (np.datetime64(sd1, 'M') + np.timedelta64(1, 'M') - np.timedelta64(1, 'D') - sd1) / np.timedelta64(1, 'D')
    time_diff = np.mod((md2 - sd1).astype('timedelta64[M]') / np.timedelta64(1, 'M'), period)
    time_diff = np.where(days_remaining > 0, np.add(time_diff, 1), time_diff)
    return np.datetime64(np.datetime64(sd1,'M') + time_diff.astype('timedelta64[M]'), 'D'), days_remaining, time_diff

def time_ratio_calc(mat_date, sett_date, period, date_calc='3060', len_time='semiannual'):   
    """ Calculate Ratio of Days Between Two Dates to Days in a Year
    
    Given args are converted into numpy arrrays. 
    They are then used to calculate days between settlement date and maturity date based on days in a year.
    Two options available:
       - Actual: Direct count of days between dates
       - 30/60: Every month is treated for 30 days
    Used to calculate time ratio for a given count of days in a year.
    
    Accrued interest calculated as well based on days between settlement date and next coupon date.
    
    Args:
        mat_date (date): Date of maturity for a bond.
        sett_date (date): Date of settlement for a bond, or official purchase date.
        date_calc (str): whether to calculate time difference (in days) based on actual or 30 days a month (360 days a year).
        len_time (str): Period length designation.
        
    Returns:
        np.float: The time ratio for number of days between maturity and settlement dates and total number of days in a year.
        
    """
    # fail safe
    if mat_date <= sett_date:
        return 'Settlement cannot come after maturity of bond!'
    if date_calc.lower() not in ('3060', 'actual'):
        return 'Incorrect description for timing calculation'   
    
    # calculate next pay date for coupon
    next_pay_date, days_remaining, time_diff = next_pay_date_calc(sett_date, mat_date, np.divide(12.0, period))
    
    # find time ratio based on specified time counting calculation
    time_ratio_3060 = np.where(date_calc=='3060', thirtysixty_time_ratio_calc(sett_date, days_remaining, time_diff, np.divide(12.0, period))[0], 0.0)
    ai_ratio_3060 = np.where(date_calc=='3060', thirtysixty_time_ratio_calc(sett_date, days_remaining, time_diff, np.divide(12.0, period))[1], 0.0)
    
    time_ratio_actual = np.where(date_calc=='actual', actual_time_ratio_calc(next_pay_date, sett_date, np.divide(12.0, period))[0], 0.0)
    ai_ratio_actual = np.where(date_calc=='actual', actual_time_ratio_calc(next_pay_date, sett_date, np.divide(12.0, period))[1], 0.0)
    
    time_ratio = np.add(time_ratio_3060, time_ratio_actual)
    ai_ratio = np.add(ai_ratio_3060, ai_ratio_actual)

    # caclulate the bond price
    np.zeros(12)
    
    # secondary fail safe
    if time_ratio == 0.0:
        return 'Incorrect timing calculated'
    
    return time_ratio, ai_ratio

def bond_price_calc_sett(bond_len, coupon_per, par_val, req_yield_per, price='clean', date_calc='3060', len_time='semiannual', details=True):
    """ Calculate Pricing for a Bond
    
    Given args are converted into numpy arrrays. 
    They are then used to calculate what the payout is for a bond during its life from a different 
    settlement date into maturity.
    
    Args:
        bond_len (array): Periods of time between maturity and bond purchase, respectively.
        coupon_per (float): Current interest rate return on a bond per specified period.
        par_val (float): Value of bona at par.
        req_yield_per (float): Expected yearly return on bond.
        date_calc (str): whether to calculate time difference (in days) based on actual or 30 days a month (360 days a year).
        len_time (str): Period length designation.
        details (bool): Determines whether to print calculation results.
        
    Returns:
        np.float: The price of the coupon payment.
        
    """
    # convert to numpy arrays
    coupon_per = np.array(coupon_per)
    par_val = np.array(par_val)
    req_yield_per = np.array(req_yield_per)
    mat_date = np.datetime64(bond_len[0])
    sett_date = np.datetime64(bond_len[1])    
    
    # fail safe
    if len_time.lower() not in ('semiannual', 'annual'):
        return('Incorrect period length description') 
    if price.lower() not in ('clean', 'dirty'):
        return('Incorrect price description') 
    
    # adjust fields based on length of bond period
    p1 = np.where(len_time.lower()=='semiannual', np.divide(12.0, 6.0), 0.0)
    p2 = np.where(len_time.lower()=='annual', np.divide(12.0, 12.0), 0.0)
    period = np.add(p1, p2)   
    bond_len = np.ceil(np.divide((mat_date - sett_date).astype('timedelta64[M]') / np.timedelta64(1, 'M'), np.divide(12.0, period)))
    coupon_per = np.divide(coupon_per, period)
    req_yield_per = np.divide(req_yield_per, period)
    
    # adjust for given coupon rate format
    coupon_per = np.where(coupon_per > 1, np.divide(coupon_per, 100), coupon_per)
    req_yield_per = np.where(req_yield_per > 1, np.divide(req_yield_per, 100), req_yield_per)
    
    # calculate time ratio and accrued interest ratio
    time_ratio = time_ratio_calc(mat_date=mat_date, sett_date=sett_date, period=period, date_calc=date_calc, len_time=len_time)[0]
    ai_ratio = time_ratio_calc(mat_date=mat_date, sett_date=sett_date, period=period, date_calc=date_calc, len_time=len_time)[1]
    if isinstance(time_ratio, str):
        return time_ratio
    
    # calculate cash-flow
    coupon_pay = bond_cash_flow_calc(bond_len, coupon_per, par_val, len_time='annual', details=details)[0]
    
    # calculate price
    bond_len = np.where(time_ratio.is_integer(), np.add(bond_len, 1), bond_len)
    periods = np.add(np.arange(bond_len.astype(int)), time_ratio)
    coupon_pay = np.full(bond_len.astype(int), coupon_pay)
    ai_price = np.multiply(coupon_pay[0], ai_ratio)
    coupon_pay[-1] = np.add(coupon_pay[-1], par_val)
    bond_price = np.divide(coupon_pay, np.power(np.add(1, req_yield_per), periods))
    bond_price[0] = np.where(price.lower() == 'clean', bond_price[0] - ai_price, bond_price[0])
    
    if details:
        print('Accrued Interest - ${:.2f}'.format(ai_price))
        if (bond_len.size == 1) & (req_yield_per.size == 1):
            comb_array = np.array([periods, coupon_pay, bond_price])
            comb_data = pd.DataFrame(data=comb_array.T, columns=['Period', 'Coupon Payment Scheduled', 'Bond Price'])
            print(comb_data)
            if price.lower() == 'clean':
                print('Present Clean Value of Bond - ${:.2f}'.format(np.sum(bond_price)))
            if price.lower() == 'dirty':
                print('Present Dirty Value of Bond - ${:.2f}'.format(np.sum(bond_price)))
        else:
            np.set_printoptions(precision=2)
            print('Present Value of Bond - ${}'.format(bond_price))
    return np.sum(bond_price)
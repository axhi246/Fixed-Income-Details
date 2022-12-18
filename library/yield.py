import numpy as np
import pandas as pd
import pricing as price

def bond_current_yield_calc(bond_len, coupon_per, bond_price, par_val, len_time='annual', details=True):
    """ Calculate Current Yield for a Bond
    
    Given args are converted into numpy arrrays. 
    They are then used to calculate what the current yield for a bond based on annualized coupon payments.
    
    Args:
        bond_len (int): Number of bond periods before maturity.
        coupon_per (float): Current interest rate return on a bond per specified period.
        par_val (float): Value of bond at par.
        bond_price(float): Price of bond given.
        len_time (str): Period length designation.
        details (bool): Determines whether to print calculation results.
        
    Returns:
        np.float: Required yield based on current yield percentage.
        
    """
    # convert to numpy arrays
    bond_len = np.array(bond_len)
    coupon_per = np.array(coupon_per)
    bond_price = np.array(bond_price)
    par_val = np.array(par_val)
    
    # fail safe
    if (bond_len.size != coupon_per.size) | (coupon_per.size != par_val.size):
        return 'Incorrect argument dimensions'
    if len_time.lower() not in ('semiannual', 'annual'):
        return 'Incorrect period length description'
    
    # adjust fields based on length of bond period
<<<<<<< Updated upstream
    period = np.where(len_time.lower()=='semiannual', 2, 1)
=======
    p1 = np.where(len_time.lower()=='semiannual', np.divide(12.0, 6.0), 0.0)
    p2 = np.where(len_time.lower()=='annual', np.divide(12.0, 12.0), 0.0)
    period = np.add(p1, p2)
>>>>>>> Stashed changes
    coupon_per = np.multiply(coupon_per, period)
    
    # adjust for given coupon rate format
    coupon_per = np.where(coupon_per > 1, np.divide(coupon_per, 100), coupon_per)
    
    # calculate current yield
    coupon_per = np.multiply(par_val, coupon_per)
    req_yield_per = np.divide(coupon_per, bond_price)
    
    if details:
        if bond_len.size == 1:
            'Annual Coupon Rate - ${:.2f}'.format(coupon_per)
            print(len_time.capitalize() + ' Coupon Rate - ${:.2f}'.format(coupon_per))
            print('Required Yield - {:.2%}'.format(req_yield_per))
        else:
            np.set_printoptions(precision=2)
            print(len_time.capitalize() + ' Coupon Rate - ${}'.format(coupon_per))
            print('Required Yield - {}'.format(req_yield_per))
        
    return req_yield_per

def bond_yield_maturity_calc(bond_len, coupon_per, bond_price, par_val, call_val=0, len_time='annual', details=True):    
    """ Calculate Yield-to-Maturity for a Bond
    
    Given args are converted into numpy arrrays. 
    They are then used to calculate what the payout is for a bond during its life into maturity.
    
    Args:
        bond_len (int): Number of bond periods before maturity.
        coupon_per (float): Current interest rate return on a bond per specified period.
        bond_price (float): Price of bond given.        
        par_val (float): Value of bond at par.
        call_val (float): Value of bond at first callable event.
        len_time (str): Period length designation.
        details (bool): Determines whether to print calculation results.
        
    Returns:
        np.float: Required interest optimized for given bond value.
        
    """    
    # calculate pricing
    req_yield_pers = np.arange(.01, 100, .01)
    bond_prices = price.bond_price_calc(bond_len=bond_len, coupon_per=coupon_per, par_val=par_val, call_val=call_val, req_yield_per=req_yield_pers, len_time=len_time, details=False)[2]
    
    # calculate yield
    try:
        bond_index = np.where(np.round(bond_prices, 2) == np.round(bond_price, 2))[0]
        bond_index.shape[1]
    except:
        ordered_bond_prices = bond_prices.copy()
        ordered_bond_prices.sort() 
        bond_index = np.searchsorted(np.round(ordered_bond_prices, 2), np.array(np.round(bond_price, 2)))
        bond_index = np.where(bond_prices == ordered_bond_prices[bond_index])
     
    if details:
            print('Yield-to-Maturity Lookup - {:.2%}'.format(np.divide(req_yield_pers[bond_index][0], 100)))

    return req_yield_pers[bond_index][0]
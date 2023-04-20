def calc_pnl(dfAllTnx: pd.DataFrame, wallet_address) -> pd.DataFrame: #api: MagicEdenAPI):

    dfAllTnx['datetime'] = pd.to_datetimedfAllTnx['blockTime']*1000, unit='ms')
    """Calculate the pnl of our wallet"""

    # Isolate the buy/sales
    dfAct = dfAllTnx[dfAllTnx['type'] == 'buyNow']
    # Get a list of each unique nft traded
    oids = dfAct['tokenMint'].unique().tolist()
    # Define a new column of net pnl
    dfAct['pnl'] = np.NaN
    dfAct['return'] = np.NaN
    # For each unique oid traded process the trade and record net round-trip pnl as a new column entry
    dfAct.sort_values(by='blockTime', inplace=True, ignore_index=True)
    for oid in oids:
        df = dfAct[dfAct['tokenMint'] == oid]
        df.reset_index(drop=False, names='idx', inplace=True)

        # Skip tnx if not fully executed
        if len(df) < 2:
            continue

        # Iterate over the rows of tnx for the oid and
        #   calculate the pnl on each row where prior
        #   tnx was a buy and current tnx is a sale

        i = 1
        while i < len(df):
            last_tnx_is_buy = (df.at[i-1, 'buyer'] == wallet_address)
            i_tnx_is_sell = (df.at[i, 'seller'] == wallet_address)
            if last_tnx_is_buy and i_tnx_is_sell:
                df.at[i-1, 'side'] = 'buy'
                df.at[i, 'side'] = 'sell'
                # calc the net pnl
                NET_PROFIT = df.at[i, 'price'] - df.at[i-1, 'price']
                HOLDING_PERIOD = (df.at[i, 'blockTime'] - df.at[i-1, 'blockTime'])

                PCNT_PROFIT = NET_PROFIT / df.at[i-1, 'price']
                # save net pnl to original dataframe
                idx = df.at[i, 'idx']
                dfAct.at[idx, 'pnl'] = NET_PROFIT
                #dfAct.at[idx, 'network_fee'] = NETWORK_FEE
                dfAct.at[idx, 'return'] = PCNT_PROFIT
                dfAct.at[idx, 'holding_period [s]'] = HOLDING_PERIOD
            i += 2 # skip the middle tnx
    # save original dataframe
    dfAct['datetime'] = pd.to_datetime(dfAct['blockTime']*1000, unit='ms')
    # Calculate the network fees inbetween snapshots after sorting by blocktime
    dfAct.sort_values(by="blockTime", inplace=True)
    dfAct['network_fee'] = dfAct.index.to_series().apply(
        lambda i: 0.000005 * np.sum(np.where(
                    (dfAllTnx['blockTime'] > dfAct.at[max(0, i-1), 'blockTime']) &
                    (dfAllTnx['blockTime'] <= dfAct.at[i, 'blockTime']), 1, 0
                ))
    )
    stamp = int(datetime.datetime.utcnow().timestamp() * 1000)
    return dfAct
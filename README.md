"# TradingTest" 

1. Install python v3.11
2. First task
   - Run LogMetrics.py for getting log Metrics (TradingPrice, BestBid, BestOffer, Volitality V1, V6, V24)
   - Run createCandleStick to generate csv file with our provided csv (Code Test Part 1.csv)
   - Run strategy.py for my own algorithm which is using Bollinger Bands.

3. Second Task
   - After reviewing the codebase of task2 it's great and learn so many things from there.

   - Key
      1. Code Efficiency: it's great : well designed and also optimized on defining and using varaiables
         but I think
         
         NET_PROFIT = df.at[i, 'price'] - df.at[i-1, 'price']
         HOLDING_PERIOD = (df.at[i, 'blockTime'] - df.at[i-1, 'blockTime'])

         PCNT_PROFIT = NET_PROFIT / df.at[i-1, 'price']
         # save net pnl to original dataframe
         idx = df.at[i, 'idx']
         dfAct.at[idx, 'pnl'] = NET_PROFIT
         dfAct.at[idx, 'return'] = PCNT_PROFIT
         dfAct.at[idx, 'holding_period [s]'] = HOLDING_PERIOD


         I think it would be great if we change the above code base as

         idx = df.at[i, 'idx']
         dfAct.at[idx, 'pnl'] = df.at[i, 'price'] - df.at[i-1, 'price']
         dfAct.at[idx, 'return'] =  dfAct.at[idx, 'pnl'] / df.at[i-1, 'price']
         dfAct.at[idx, 'holding_period [s]'] = (df.at[i, 'blockTime'] - df.at[i-1, 'blockTime'])

         No need to declare that kind of variables.


      2. Readability: Little bit not : Every instruction has comment but not structured well I think. it would be great if we could define functions for small instructions


      3. Redundancies: It's great I think
      4. Error handling: Yes I think there is no error_handling.

         - on while. if we only have 1 trx
         - etc

As you can see from my codebase, I am not that expertise but really eager to learn from you and join as your team member.

Best Regards
Justin


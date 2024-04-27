To make a market on the number of bikes at a time in the future we must come up with a range or confidence interval. We process the citibike historical data by dividing into 15 minute time buckets for a given day of the week. So, an example bucket is Tuesday 11:30-11:45 and another example is Friday 15:45-16:00. We then assume that the number of bikes coming in and going out in any 15 minute time interval is distributed independently Poisson. For instance, suppose we want to speculate on the total number of bikes 45 minutes from now. Let $X_1$, $X_2$, $X_3$ be random variables for the number of bikes in and $Y_1$, $Y_2$, $Y_3$ are r.v.s for bikes out. Then, the net change in the number of bikes 45 minutes from now is given by $$X_{1}+X_{2}+X_{3}-(Y_1+Y_2+Y_3)$$ 
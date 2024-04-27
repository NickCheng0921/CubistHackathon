# Market Making on Number of Citibikes
For the Cubist Hackathon groups were given a set of NYC-based datasets to work with. Inspired by the work at Cubist and interest in options pricing we decided to market make on the number of Citibikes thorughout NYC

Suite of endpoints to simulate a brokerage on number of citibikes in NYC.

A user places a bet predicting an amount of citibikes to be present at specific dock at a future time. If this bet is higher than our markets predicted output, they will profit if the citibikes at the endtime are equal to or greater than the amount they predicted. The opposite occurs if they guess under our markets predicted price. Depending on the difference in predictions, the user gets a multiplier on the money they placed onto the bet.



## Computing Confidence Intervals

In order to predict the number of bikes at a given station we create two distinct models whose combined value is the number of bikes in a station. The first model uses a Poisson distribution to calculate the given probability. However, this model may not accurately reflect short-term behaviors that may impact the current number of bikes present (i.e sporting events, emergencies, etc). To combat this we've created a model that creates an exponential moving average(ema) over the last x timesteps. The ema value and Poisson value are joined through a linear combination to construct our final prediction. 

To make a market on the number of bikes at a time in the future we must come up with a range or confidence interval. We process the citibike historical data by dividing into 15 minute time buckets for a given day of the week. So, an example bucket is Tuesday 11:30-11:45 and another example is Friday 15:45-16:00. We then assume that the number of bikes coming in and going out in any 15 minute time interval is distributed independently Poisson. This is a good simple way to model the distribution because we can view bikes arriving and leaving as occurences in a Poisson process since bike has a small probability of being moved and there are many bikes. Furthermore the bike movements are largely independent. For instance, suppose we want to speculate on the total number of bikes 45 minutes from now. Let $X_1$, $X_2$, $X_3$ be random variables for the number of bikes entering the station and $Y_1$, $Y_2$, $Y_3$ are r.v.s for bikes leaving in the three adjacent 15 minute intervals. Then $$X_1\sim \text{Pois}(\lambda_{in}^{(1)})$$ $$X_2\sim \text{Pois}(\lambda_{in}^{(2)})$$ $$X_3\sim \text{Pois}(\lambda_{in}^{(3)})$$ $$Y_1\sim \text{Pois}(\lambda_{out}^{(1)})$$ $$Y_2\sim \text{Pois}(\lambda_{out}^{(2)})$$ $$Y_3\sim \text{Pois}(\lambda_{out}^{(3)})$$ We can get the mean values $\lambda_{in}^{(1)}$, $\lambda_{in}^{(2)}$, $\lambda_{in}^{(3)}$, $\lambda_{out}^{(1)}$, $\lambda_{out}^{(2)}$, $\lambda_{out}^{(3)}$ using historical data from 2022 onwards. Then, the total number of bikes entering 45 minutes from now is $X=X_1+X_2+X_3$ and the total number of bikes leaving is $Y=Y_1+Y_2+Y_3$. Since the sum of Poisson random variables is also Poisson with the parameter lambda being the sum of individual lambdas, we have that $$X\sim \text{Pois}(\lambda_{in}^{(1)}+\lambda_{in}^{(2)}+\lambda_{in}^{(3)})$$ $$X\sim \text{Pois}(\lambda_{out}^{(1)}+\lambda_{out}^{(2)}+\lambda_{out}^{(3)})$$ The net change in the number of bikes is $$\Delta_{bike} = X-Y$$ The difference of two independent Poisson variables is the Skellam distribution so we get that $$\Delta_{bike} \sim \text{Skellam}(\lambda_{in}, \lambda_{out})$$ where $\lambda_{in}=\sum_{i} \lambda_{in}^{(i)}$ and $\lambda_{out}=\sum_{i}\lambda_{out}^{(i)}$. Now that we have an approximation for the distribution of net change in bike count, we can compute confidence intervals around the mean. Using scipy's scipy.stats.skellam object we use the interval function to get the confidence intervals for a given probability level.

Since the Skellam distribution only uses historical data, we adjust the $\lambda_{in}$ and $\lambda_{out}$ parameters using intraday real-time streamed data. If a station is gaining momentum by having more bikes coming in or out in the past few hours, we incorporate that in by multiplying the lambdas by a factor such as 1.3 or 0.7, depending on whether it is gaining or losing momentum. The data streaming is done using csp for clean execution.

In order to calculate payout factors we simply use the expected value of the contract and set it so that it is slightly positive EV for us and slightly negative for the users using our confidence intervals. For instance if the user predicts $x$ bikes 1.5 hours from now and we calculate that the actual number of bike will be less than that with probability 0.9, since the user has probability 0.1 of winning we would make the payout $0.9\cdot(\frac{1}{0.1})=9$ to make sure we have a slight edge. If the user had a bigger probability of winning like 0.25 the payout would be $0.9\cdot(\frac{1}{0.25})=3.6$.

# Client facing endpoints

## Add User

HTTP method: POST, URL: /adduser

Request

money: accountMoney
firstName: firstName
lastName: lastName

Response

201 on success

## Add User

HTTP method: GET, URL: /adduser

Request

[]

Response

200 on success and json user list

## User balance

HTTP method: GET, URL: /usermoney

Request

userId: userId

Response

200 on success + account balance

## Orders

HTTP method: GET, URL: /orders

Request

[]

Response

200 on success and json list of orders

## Place contract

HTTP method: POST, URL: /addcontract

Request

userId: userId
userBet: userBet
orderId: orderId

Response

201 on success

## View live contracts

HTTP method: POST, URL: /livecontracts

Request

earliestTime: earliestTime (datetime str format)
latestTime: latestTime	   (datetime str format)

Response

200 on success and json list of live contracts

# Internal endpoints

## View placed contracts

HTTP method: POST, URL: /contracts

Request

[]

Response

200 on success and json list of placed orders

## Add order

HTTP method: POST, URL: /addorders

Request

stationId: stationId
startTime: startTime
endTime: endTime
startBikes: startBikes
endBikes: endBikes
multiplier: multiplier
isBuy: isBuy

Response

201 on success


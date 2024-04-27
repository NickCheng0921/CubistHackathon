# Market Making on Number of Citibikes

Suite of endpoints to simulate a brokerage on number of citibikes in NYC.

## Computing Confidence Intervals
To make a market on the number of bikes at a time in the future we must come up with a range or confidence interval. We process the citibike historical data by dividing into 15 minute time buckets for a given day of the week. So, an example bucket is Tuesday 11:30-11:45 and another example is Friday 15:45-16:00. We then assume that the number of bikes coming in and going out in any 15 minute time interval is distributed independently Poisson. This is a good simple way to model the distribution because we can view bikes arriving and leaving as occurences in a Poisson process since bike has a small probability of being moved and there are many bikes. Furthermore the bike movements are largely independent. For instance, suppose we want to speculate on the total number of bikes 45 minutes from now. Let $X_1$, $X_2$, $X_3$ be random variables for the number of bikes entering the station and $Y_1$, $Y_2$, $Y_3$ are r.v.s for bikes leaving in the three adjacent 15 minute intervals. Then $$X_1\sim \text{Pois}(\lambda_{in}^{(1)})$$ $$X_2\sim \text{Pois}(\lambda_{in}^{(2)})$$ $$X_3\sim \text{Pois}(\lambda_{in}^{(3)})$$ $$Y_1\sim \text{Pois}(\lambda_{out}^{(1)})$$ $$Y_2\sim \text{Pois}(\lambda_{out}^{(2)})$$ $$Y_3\sim \text{Pois}(\lambda_{out}^{(3)})$$ We can get the mean values $\lambda_{in}^{(1)}$, $\lambda_{in}^{(2)}$, $\lambda_{in}^{(3)}$, $\lambda_{out}^{(1)}$, $\lambda_{out}^{(2)}$, $\lambda_{out}^{(3)}$ using historical data from 2022 onwards. Then, the total number of bikes entering 45 minutes from now is $X=X_1+X_2+X_3$ and the total number of bikes leaving is $Y=Y_1+Y_2+Y_3$. Since the sum of Poisson random variables is also Poisson with the parameter lambda being the sum of individual lambdas, we have that $$X\sim \text{Pois}(\lambda_{in}^{(1)}+\lambda_{in}^{(2)}+\lambda_{in}^{(3)})$$ $$X\sim \text{Pois}(\lambda_{out}^{(1)}+\lambda_{out}^{(2)}+\lambda_{out}^{(3)})$$ The net change in the number of bikes is $$\Delta_{bike} = X-Y$$ The difference of two independent Poisson variables is the Skellam distribution so we get that $$\Delta_{bike} \sim \text{Skellam}(\lambda_{in}^{(1)}+\lambda_{in}^{(2)}+\lambda_{in}^{(3)}, \lambda_{out}^{(1)}+\lambda_{out}^{(2)}+\lambda_{out}^{(3)})$$ Now that we have an approximation for the distribution of net change in bike count, we can compute confidence intervals around the mean. Using scipy's scipy.stats.skellam object we use the interval function to get the confidence intervals for a given probability level.


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

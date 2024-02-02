# Health and Climate Change: A Comparative Study Between the EU and China

## Introduction and Project Overview 

The research project has the following aims: to take a broad overview of climate change over the last 3 to 4 decades 
(depending on availability of data for certain variables) in China and the EU, to show trends in climate change mitigation
measures taken by China and the EU, and to find correspondence (if any) in climate change trends and health expenditure 
trends in both China and the EU. We use both statistics and recent policy documents to have a view of the trajectory 
so far and to anticipate the direction of climate change and health management policies of both states as they state in
their policy documents. The policy documents analyzed are the EU 2008 Climate Policy and the China Climate Strategy 2035.

Our logic for selecting EU and China for comparison is to have one developed region which is at the forefront of climate 
change mitigation policy and is (potentially) reducing its emissions year on year, and one developing region which is 
(potentially) still increasing emissions every year and to compare their policy directions, as well as their 
focus (if any) on controlling health risks associated with climate change, which is usually an underreported aspect of 
climate change. Our statistics are sourced from *Berkeley Earth Data, the IMF Climate Change dashboard and the 
OECD statistics web database*. Since we were not able to find consolidated estimates for the EU for all variables,
we consolidated data from the 5 biggest EU member states (Germany, France, Italy, Spain and Poland) and use the result
as a proxy for the EU in our analysis. For variables like climate disaster frequency, we summed the values for individual
countries to get the value for EU, and for % of GDP expenditure values, such as health expenditure, we took the mean of 
all the individual countries to get the value for the EU. 


## [Data Wrangling](datawrangling.py) 

From the abovementioned data sources, we extracted the following variables:

a. Mean Land Surface Temperature in China in degrees Celsius (1841-2020)

b. Mean Land Surface Temperature in Europe (the continent) in degrees Celsius (1750-2020)

c. Frequency of Climate Related Disasters for China and EU (1980-2022)

d. CO2 emissions in Millions of Metrics tons of CO2 for China and EU (1995-2018)

e. Environmental Protection Expenditures as % of GDP for China and EU (1995-2022)

f. Environmental Taxes as % of GDP for China and EU (1995-2021)

g. Healthcare Expenditures as % of GDP for China and EU (2015-2022)

For the following variables, only data for the EU was found:

h. Mortality due to Respiratory Illness in deaths per 100,000 population (standardised rates) 

i. Incidence of Communicable Diseases per 100,000 population (AIDS, Pertussis, Hepatitis B, Measles)

j. Air pollution in total emissions per capita (for SO, NO, Particulates, CO, NMVOC)


## [Text Analysis of Health Objectives in China Climate Strategy 2035 and EU Climate Policy](textprocessing.py)

The text processing pipeline analyzes climate policy documents from both China and the EU. Its main objective is to 
uncover if these documents address health-related risks, and which health related risks and entities are their main focus, 
within their respective climate change initiatives. The initial step involves document processing using the docx library. 
Python is used to load and preprocess the policy documents, filtering out titles, footnotes, and irrelevant text based on 
specific conditions. The code ensures that only meaningful content is retained for further analysis. The next stage employs 
keyword-based sentence extraction techniques. First, we identify health-related sentences by checking for the presence of 
predefined health-related keywords within the processed paragraphs. This step allows the pipeline to pinpoint sentences 
that are directly relevant to health concerns in climate policy. One sentence before and after the health policy is 
mentioned are also retained to keep context in mind. Text summarization is a crucial part of the pipeline, accomplished 
with Python's spaCy library. For each health-related sentence, spaCy tokenizes the text, calculates word frequencies, 
and ranks sentences accordingly. This process helps generate concise summaries that capture the essence of each 
paragraph's health-related content. To visually represent the key concepts and themes, word clouds are generated using 
libraries  wordcloud and matplotlib. By combining the selected summaries into a single string, the code creates word clouds 
that highlight the most prominent terms within the policy documents. Finally, the pipeline utilizes spaCy once more to 
extract entities related to health, such as diseases, treatments, and health organizations. These entities are presented 
in a separate word cloud, providing insights into the specific health concerns addressed in the documents and which 
entities are of the utmost concern to policymakers.


## Plotting 

*[Interactive Comparative Plots on Shiny](fin_app/app.py)* 

In Shiny, we plotted the frequency of climate disasters in both China and the EU against time (from 1980 to 2022). Visually, 
there is a slight upward trajectory in the graphs both for China and the EU. For most of this period, the frequency of
climate disasters in China remains higher. We also plotted emissions (in millions of metric tons of CO2) against
time (1995 to 2018) for both China and the EU. EU emissions remain largely static below 2000 units and even appear to
have declined. For China however, C02 emissions were at close to 3000 units in 1995, and due to a sharp upward trajectory,
in 2018 they are above 9000 units. 

In Matplotlib, we plotted the trend in Environmental Taxes as % of GDP over time (from 1995 to 2021) for both the EU
and China. Environmental taxes remain relatively static in the EU from 1995 to 2014, after which there is an small
increase. This may be attributed to the implementation of the 20/20/20 EU Climate Policy. China's environmental 
taxation is 0% of its GDP in 1995, but it steadily increases from there to a peak of almost 3% in 2011. In 2020
this figure is just above 1%. Finally we plotted the total emissions per capita (labeled as Pollution level) for 
the following greenhouse gases: Carbon Monoxide, Nitrogen Oxides, Non methane Volatile Organic Compounds, Particulates 
(PM10 AND PM2.5) and Sulphur Oxides from 1990 to 2020 in the EU only. All GHGs see a decline, and the sharpest decline is
in CO emissions falling from close to 140 units to only 40. 


## [Time Series (EU) and Regression (China) Analysis](analysis.py)

*Forecasting Levels of Particulates (PM2.5) in EU*

We performed a time series analysis of Particulate emissions per capita in the EU by creating a 5 year moving average
in order to clearly visualize the long term trends. To calculate the model parameters, we created autocorrelation 
function and partial autocorrelation function plots and used differencing. After fitting the model to the data, we
forecast future PM2.5 levels in the EU which continue to decline as seen in the available data for 1990 to 2020. 

Next, we regressed health expenditures on CO2 emissions for China from 2015 to 2018 only due to the limited period 
for which health expenditure data is available. 

=======
*Forecasting Levels of in Particulates (PM2.5) in EU*

The time series analysis pipeline begins with loading the data from a specified file, focusing on PM2.5 levels for the European Union
(EU). After selecting the relevant data, we plot the time series to visually inspect the trends and patterns. This plot includes a 5-
year moving average to smooth out short-term fluctuations, enhancing the visibility of long-term trends. To prepare for ARIMA modeling,
we conduct an Augmented Dickey-Fuller (ADF) test to check the stationarity of the series. Since most time series forecasting models
require stationary data, if the series is not stationary, we apply transformations like differencing. For the ARIMA model, parameters
(p, d, q) are crucial; 'p' and 'q' are determined based on the Autocorrelation Function (ACF) and Partial Autocorrelation Function
(PACF) plots, while 'd' is set based on the differencing applied to achieve stationarity. After fitting the ARIMA model to the data, we
use it to forecast future PM2.5 levels, providing insights into potential future air quality trends.


## Findings and Limitations

From the word cloud we see that China’s main focus was on health risks emerging from extreme weather related events and 
calamities, and their policy objectives were to focus on prevention of extremities. There was less of a focus on pollution. 
From the entity word cloud, we see that the most prominent entities include water bodies, and therefore, it seems 
indicative of their concern for preserving rivers, their ecosystems and biodiversity. For the European Union, their 
policy document was framed quite differently and was from 2008. There were much fewer mentions of health related risks 
and policy objectives and no specific entities mentioned. However, the main concern was related to carbon emissions 
and air pollution. 

The two policies while both climate related, however, are from different time periods which might affect their policy 
objectives based on the time’s context. Additionally, the EU’s policy was more general than a strategic plan from China 
which might have also been the reason we saw fewer climate policies recognising health risks and specific entities in the 
EU policy document. 

From our plots, we see a slight but definite upward trajectory in the frequency of climate disasters in both China and 
the EU, and while CO2 emissions in EU are slightly declining, in China they have increased sharply in the period under
study. It is possible that the emissions trajectory for other greenhouse gases like Nitrous Oxides and particulates
in China is also increasing, but we do not have the data to confirm this in our analysis. GHG emissions per capita
in the EU are on a definite declining trend as shown in our plot as well as the time series analysis. 
Environmental taxes increase in both the EU and China on slightly different schedules- the increase in taxation in the 
EU coincides with the years immediately following the adoption of the 2008 EU Climate Policy, while in China there is 
both a steady increase from 1995 onward and a slight decline to the end of the study period. Finally, for China only,
we regressed health expenditures on CO2 emissions from 2015 and 2018 and found a slope of -0.000045, indicating 
a very slight inverse relationship between the two variables. Importantly however, the R squared value of 0.073, which
means that only about 7% of the variation in health expenditures is explained by CO2 emissions. Therefore the correlation
between health expeditures and CO2 emissions, which we intended as a proxy for a health-focused response to climate change,
seems to be insignificant. 



Now, coming to our time series analysis for the EU - given their policy concern for air pollution, we use an ARIMA model to estimate
future pollutant levels to understand air quality. The ARIMA(1, 1, 1) model, selected based on the time series characteristics and
ACF/PACF plots, provides a statistical framework to forecast future PM2.5 levels. The forecasted values indicate a continuing trend
observed in the historical data. The model's summary, including coefficients and statistical tests, offers confidence in its
reliability. However, it is important to acknowledge that these forecasts are contingent on the assumption that past patterns will
persist and do not account for unforeseen future events or policy changes that might impact air quality. The analysis reveals a gradual
decrease in PM2.5 levels over the forecasted periods, suggesting an improving air quality trend in the EU. This trend aligns with
ongoing environmental policies and air quality control measures in the region. Nonetheless, the forecast should be interpreted with
caution, considering external factors and the inherent uncertainties in any predictive modeling.

## Conclusion and Future Work 

In this research we looked at a very broad range of variables to get a general idea of climate change trends,
climate mitigation trends and the relationship between climate and health for China and the EU. We extracted data for
both China and the EU for several variables, but health related data on China was scarce compared with the EU, so we
focused on health expenditure. Based on our findings, climate change events seem to be becoming more frequent, and
although mitigation is increasing in both China and the EU, there is a large difference in mitigation levels and 
trajectories between them, with EU being a clear frontrunner, and predicted to remain on a positive trajectory. We
were unable to find a relationship between increasing expenditure on health and CO2 emisssions (proxy for climate
change) for China. In China's 2035 policy, concerns for the effects of climate change on health stem from the outfall of 
extreme weather events as opposed to respiratory or communicable diseases. The EU policy document was more focused on 
the need to reduce Carbon emissions in relation to their focus on health risks. The EU focus on reducing carbon emissions
in the 2008 policy is followed through on as there is a decline in all GHGs in the EU over the studied period, and the
forecast suggests this trend will persist. 

We are aware that for several variables we did not have comparable statistics for China and the EU. Also, substituting
the 5 biggest member states for the entire EU introduces inaccuracy in our analysis. In the future we hope to extend 
our analysis by comparing the EU and China over all selected variables for a more comprehensive analysis, as well as
by finding data for the entire EU. 

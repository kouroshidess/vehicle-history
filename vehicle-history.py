''' 
## TODO
* plots for vehicle owners, mot-tests, services and/or costs(categorised)
* scrape? https://www.check-mot.service.gov.uk https://vehicleenquiry.service.gov.uk/
* lambda, mapreduce(pseudo)
* forcast future mileage?
* some form of deviation highlighting
* histogram and calc bins
'''

def vehicle_data(csv, reg):

       import pandas as pd
       import datetime as dt

       # Read csv as dataframe
       miles_df = pd.read_csv(csv)

       # Update dataframe with entry for 1st regisatrion date and 0 mileage and
       # final entry with today's date and no mileage (not known)
       miles_df = miles_df.append([
              {"date": reg, "miles": 0},
              {"date": dt.datetime.today().strftime('%Y-%m'), "miles": None}], 
              ignore_index=True)
       
       # Reformat date column values to actual datetime 
       miles_df['date'] = pd.to_datetime(miles_df['date'])

       # Now reorder date column
       # TODO need to fix/reorder index too!
       miles_df = miles_df.sort_values(by=['date'])

       return miles_df


def vehicle_plot(miles_df, car_dict):

       import matplotlib.pyplot as plt
       import matplotlib.dates as mdates
       import matplotlib as mpl

       # Create figure and plot space
       fig, ax = plt.subplots(figsize=(8, 8))

       # Add x-axis and y-axis
       # TODO fix to line plot even though using plot_date()
       ax.plot_date(miles_df["date"], miles_df["miles"], color='purple')

       # Set title and labels for axes. title should be concat of items in car_dict{}
       ax.set(xlabel="Date",
              ylabel="Miles",
              title=" ".join(["Vehicle History"] + 
                     [car_dict[key] for key in ['brand','name','year']]),
              # TODO need to fix/reorder index [0,-1[] not [7,8]
              xlim=[miles_df["date"][7], miles_df["date"][8]])

       # Define the date and number format for plot labels
       from matplotlib.dates import DateFormatter
       date_form = DateFormatter("%Y")
       ax.xaxis.set_major_formatter(date_form)
       ax.xaxis.set_major_locator(mdates.YearLocator())
       ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # TODO simplify format here

       plt.show()

# User prompts for data or simply [enter] implies defaults 
car = input("Enter brand & name [default:Ford Fiesta]:") or "Ford Fiesta"
reg = input("Enter reg year & month [default:2014-08]:") or "2014-08"
csv = input("Enter date & miles CSV file [default:miles.csv]:") or "miles.csv"


vehicle_plot(
       vehicle_data(csv, reg), 
       {
              "brand": car.split(" ")[0], 
              "name": car.split(" ")[1], 
              "year": reg.split("-")[0]
              })

###############################################################################
#   Computer Project #8
#
#   Algorithm
#       prompt for a file containing hurricane information
#           form a dictionary using the names, years, and data of the hurricane
#               update the dictionary for every name & year found
#           organize the hurricane information to be added in a table,graph
#               Add the information in a table
#               Graph the trajectory of the hurricanes
#               Plot the information in a graph according to wind speed
#           Call all the functions in a main function
#       Return the requested information
###############################################################################


import pylab as py
from operator import itemgetter

def open_file():
    '''
    Opens a file input by the user.
    Reprompts if the entered file name is invalid
    Returns the entered file name for reading (fp)
    '''
    while True:
        try:
            #try to open an input file for reading
            filename = input("Input a file name: ")
            fp = open(filename,"r")
            return fp
        except:
            #if the file isn't found, print an error message and reprompt
            print("Unable to open file. Please try again.")

def tryfloat(x):
    '''
    Converts values to floats if they're a number, otherwise the value is 0.
    x: value being converted
    returns the converted value (a)
    '''
    try:
        #convert it to a float
        a = float(x)
        #if the variable doesn't have digits in it
    except:
        #the variable is 0
        a = 0
    return a

def update_dictionary(dictionary, year, hurricane, data):
    '''
    Updates all the hurricane information contained in a dictionary.
    dictionary: dictionary where the years are stored.
    year: A key in the dictionary
    hurricane: a second key for the dictionary
    data: The hurricane data which is a value for the hurricanes
    '''
    hurricane_dict = {}
    #check if year is in the dictionary
    if year not in dictionary:
        #if not, create an empty dictionary for the year
        dictionary[year] = hurricane_dict
        #check if hurricane is in dictionary[year]
    if hurricane not in dictionary[year]:
        #if not, create an empty list for that hurricane & year
        dictionary[year][hurricane] = []
    #append the data to the list inside the dictionary[year][hurricane]
    dictionary[year][hurricane].append(data)
        
        
def create_dictionary(fp):
    '''
    Takes the data provided by the file being read then adds it to a tuple.
    fp: file pointer being read
    Returns a dictionary with all the hurricane information(dictionary)
    '''
    #create an empty dictionary
    dictionary = {}
    #read the file
    for line in fp:
        line = line.split()
        year = line[0]
        hurricane = line[1]
        lat = float(line[3])
        lon = float(line[4])
        date = line[5]
        wind = tryfloat(line[6])
        pressure = tryfloat(line[7])
        data = (lat,lon,date,wind,pressure)
        update_dictionary(dictionary,year,hurricane,data)
    return dictionary


def display_table(dictionary, year):
    '''
    Displays an alphabetical list of hurricane names.
    dictionary: the dictionary of hurricanes being iterated through
    year: The keys of the dictionary
    '''
    #create a list of the sorted hurricane names
    print("{:^70s}".format("Peak Wind Speed for the Hurricanes in " + year))
    print("{:15s}{:>15s}{:>20s}{:>15s}".format("Name","Coordinates",\
          "Wind Speed (knots)","Date"))
    hurricane_names = sorted(dictionary[year].keys())
    #iterate through the list of hurricanes
    for hurricane in hurricane_names:
        #get a sorted list of points in descending order
        list_to_sort = dictionary[year][hurricane]
        points = sorted(list_to_sort, key = itemgetter(3,0,1),reverse = True)
        max_points = points[0]
        print("{:15s}({:6.2f},{:6.2f}){:>20.2f}{:>15s}".format\
              (hurricane,max_points[0],max_points[1],max_points[3],max_points[2]))

def get_years(dictionary):
    '''
    Finds the oldest and most recent years in a dictioanry
    dictioanry: the dictionary with the hurricane names & corresponding years
    returns a tuple with the oldest year & the most recent year(tup)
    '''
    #sort the dictionary in chronological order
    years_list = sorted(dictionary)
    min_year = years_list[0]
    max_year = years_list[-1]
    #add the lowest and highest years to a tuple
    tup = (min_year, max_year)
    return tup   
        
def prepare_plot(dictionary, year):
    '''
    Makes a graph of hurricanes according to their maximum wind speeds
    dictionary: the dictionary containing the hurricane data
    year: the year the hurricane occured.
    returns a tuple of hurricane names,coordinates, and maximum wind speeds.
    '''
    #get the list of sorted hurricane names
    hurricane_names = sorted(dictionary[year].keys())
    
    #create empty lists of coordinates and max_speeds
    coordinates = []
    max_wind_speed = []
    
    #iterate through the list of hurricane names
    for hurricane in hurricane_names:
        data_list_tuples = dictionary[year][hurricane]
        #create empty lists of coordinates and wind speeds
        cord = []
        wind_speed = []
        #iterate through the list of tuples(dictionary values)
        for tup in data_list_tuples:
            #add the lattitude and longitude to the temporary coordinates list
            cord.append((tup[0],tup[1]))
            #add the wind speed to the wind_speed list
            wind_speed.append(tup[3])
            #sort the wind_speeds in ascending order
        wind_sorted = sorted(wind_speed)
        #add the cordinates to the coordinates list
        coordinates.append(cord)
        #add the maximum wind speed to the max_wind_speed list
        max_wind_speed.append(wind_sorted[-1])
        #return the hurricane names, coordinates, and maximum wind speed.
    return(hurricane_names,coordinates,max_wind_speed)

    
def plot_map(year, size, names, coordinates):
    '''
    Receives the year,category,hurricane names, and coordinates.
    Plots them on a graph.
    year: Year the hurricane occured
    size: Category of the hurricane
    names: names of the hurricane
    coordinates: longitude and lattitude of the coordinates
    '''
    
    # The the RGB list of the background image
    img = py.imread("world-map.jpg")

    # Set the max values for the latitude and longitude of the map
    max_longitude, max_latitude = 180, 90
    
    # Set the background image on the plot
    py.imshow(img,extent=[-max_longitude,max_longitude,\
                          -max_latitude,max_latitude])
    
    # Set the corners of the map to cover the Atlantic Region
    xshift = (50,190) 
    yshift = (90,30)
    
    # Show the atlantic ocean region
    py.xlim((-max_longitude+xshift[0],max_longitude-xshift[1]))
    py.ylim((-max_latitude+yshift[0],max_latitude-yshift[1]))
	
    # Generate the colormap and select the colors for each hurricane
    cmap = py.get_cmap('gnuplot')
    colors = [cmap(i/size) for i in range(size)]
    
    
    # plot each hurricane's trajectory
    for i,key in enumerate(names):
        lat = [ lat for lat,lon in coordinates[i] ]
        lon = [ lon for lat,lon in coordinates[i] ]
        py.plot(lon,lat,color=colors[i],label=key)
    

     # Set the legend at the bottom of the plot
    py.legend(bbox_to_anchor=(0.,-0.5,1.,0.102),loc=0, ncol=3,mode='expand',\
              borderaxespad=0., fontsize=10)
    
    # Set the labels and titles of the plot
    py.xlabel("Longitude (degrees)")
    py.ylabel("Latitude (degrees)")
    py.title("Hurricane Trayectories for {}".format(year))
    py.show() # show the full map


def plot_wind_chart(year,size,names,max_speed):
    '''
    Gets the year,size,name,and maximum speed of the hurricanes.
    Plots their Routes.
    year: Year the hurricane occured.
    size: Category of the hurricane.
    names: Name of the hurricane.
    max_speed: maximum speed of the hurricane
    '''
    
    # Set the value of the category
    cat_limit = [ [v for i in range(size)] for v in [64,83,96,113,137] ]
    
    
    # Colors for the category plots
    COLORS = ["g","b","y","m","r"]
    
    # Plot the Wind Speed of Hurricane
    for i in range(5):
        py.plot(range(size),cat_limit[i],COLORS[i],label="category-{:d}".format(i+1))
        
    # Set the legend for the categories
    py.legend(bbox_to_anchor=(1.05, 1.),loc=2,\
              borderaxespad=0., fontsize=10)
    
    py.xticks(range(size),names,rotation='vertical') # Set the x-axis to be the names
    py.ylim(0,180) # Set the limit of the wind speed
    
    # Set the axis labels and title
    py.ylabel("Wind Speed (knots)")
    py.xlabel("Hurricane Name")
    py.title("Max Hurricane Wind Speed for {}".format(year))
    py.plot(range(size),max_speed) # plot the wind speed plot
    py.show() # Show the plot
    

def main():
    '''
    Prints information for a specific hurricane by calling all the functions.
    '''
    #open the file for reading
    fp = open_file()
   
    #create a dictionary by iterating through the file pointer
    dictionary = create_dictionary(fp)
   
    #find the range of years
    (min_year,max_year) = get_years(dictionary)
    print("Hurricane Record Software")
    print("Records from {:4s} to {:4s}".format(min_year, max_year))
   
    #prompt the user for a year that the hurricane occured
    hurricane_year = input("Enter the year to show hurricane data or 'quit': ")
    hurricane_year = hurricane_year.lower()
   
    while hurricane_year !="quit":
        #if the year entered is a number from 2007-2017, display the table.
        if hurricane_year.isdigit() == True and \
        int(max_year)>= int(hurricane_year) >= int(min_year):
            display_table(dictionary,hurricane_year)
           
            #ask the user if they want to plot
            plot = input("\nDo you want to plot? ")
            
            if plot.lower() == "yes":
                #organize the names, coordinates, and speeds of the hurricanes
                names, coordinates, max_speed = prepare_plot(dictionary,hurricane_year)
                size = len(max_speed)
                #make a diagram of hurricane trajectories
                plot_map(hurricane_year, size, names, coordinates)
                #make a graph of wind_speeds
                plot_wind_chart(hurricane_year, size, names, max_speed)
       
        else:
            #if the year isn't an integer between 2007-2017, reprompt.
            print("Error with the year key! Try another year")
        hurricane_year = input("Enter the year to show hurricane data or 'quit': ")
        hurricane_year = hurricane_year.lower()
        
if __name__ == "__main__":
    main()
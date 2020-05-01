import time
import pandas as pd
import numpy as np

#Define dictionary of data files
CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv','washington': 'washington.csv' }

#Define lists required in several functions
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def welcome():
    print('Hello!\nThis interface will provide statistics on bikes usage provided by US Bikeshare.\n')

def filter_input(statement, list_to_accept, wrong_input = '\nWrong input!\n' ):
    """Makes sure the input is one of the given choices in the statement by comparing
    it with list_to_accept. If the input is not in list_to_accept, wrong_input is printed"""

    while True:
        a = input(statement)
        a = a.lower()        # to avoid any erros due to upper_cased letters
        if a in list_to_accept:
            return a
            break
        else:
            print(wrong_input)


def get_filters():
    """returns the filters (city, month, day) requested by the user"""

    #defining required lists
    cities = ['chicago', 'new york city', 'washington']
    time_filters = ['month', 'day', 'both', 'none']

    #initial values for month and day
    month='all'
    day='all'

    #Get city filter
    city = filter_input('Please select a city: Chicago, New York City, Washington\n', cities )

    #Get type of time_filter: single, both, or none
    time_filter = filter_input('Would you like to filter by month, day, both or none?\n', time_filters)

    #Get month filter
    if time_filter == 'both' or time_filter == 'month':
        month = filter_input('Please select a month: January, February, March, April, May, June or All\n', months)

    #Get day filter
    if time_filter == 'both' or time_filter == 'day':
        day = filter_input('Please select a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All\n', days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #Load data of the selectd city
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])


    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all' :
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def popular(df,column_names):
        """Finds the most common value"""
        return df[column_names].mode()[0]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    if month == 'all':
        popular_month = popular(df,'month')
        print('\nThe most common month is:\n{}'.format(months[popular_month-1].title()))


    #Display the most common day of week
    if day == 'all':
        popular_day_of_week= popular(df,'day_of_week')
        print('\nThe most common day is:\n{}'.format(popular_day_of_week))


    #Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = popular(df,'hour')

    print('\nThe most common hour is:\n{}'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_st = popular(df,'Start Station')
    print('The most common start station:\n{}'.format(popular_start_st))

    #Display most commonly used end station
    popular_end_st = popular(df,'End Station')
    print('\nThe most common end station:\n{}'.format(popular_end_st))

    # Display most frequent combination of start station and end station trip
    df['comb_st'] = df['Start Station'] + ' AND ' + df['End Station'] #create a new column of start-end stations combined
    popular_comb_st = popular(df,'comb_st')
    print('\nMost popular combination of stations is:\n{}'.format(popular_comb_st))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print('The total travel time is:\n{}'.format(total_travel_time))

    # Display mean travel time
    mean_travel_time = (df['End Time'] - df['Start Time']).mean()
    print('\nThe mean travel time is:\n{}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types_count = df['User Type'].value_counts()[0:2]
    print('User types counts:\n{}'.format(user_types_count))


    #Display counts of gender
    if city != 'washington':
        gender_counts = df['Gender'].value_counts()[0:2]
        print('\nGender counts:\n {}'.format(gender_counts))

    #Display earliest, most recent, and most common year of birth
        min_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year:\n{}'.format(min_birth_year))

        max_birth_year = df['Birth Year'].max()
        print('\nMost recent birth year:\n{}'.format(max_birth_year))

        common_birth_year = popular(df, 'Birth Year')
        print('\nMost common birth year:\n{}'.format(common_birth_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
        row=0 #initial value for row number
        df = df.drop(columns = ['hour','day_of_week','month','comb_st']) #to drop the extra columns created
        response = filter_input('Would you like to see some raw data? yes/no\n', ['yes','no'])

        #Loop to ask the use if the user requires any additional raw data
        try:
            while True:
                if response == 'yes':
                    print(df[:][row:row+5])
                if response == 'no':
                    break
                row += 5
                response = filter_input('Would you like to see more data? yes/no\n', ['yes','no'])

        #To account for the error arising from reaching the end of df
        except:
            print('You reached the end of the data')


#Main function
def main():
    while True:
        global city, month, day
        welcome()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = filter_input('Would you like to restart? Enter yes or no.\n', ['yes','no'])
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

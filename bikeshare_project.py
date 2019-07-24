import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    print('Would you like to see data for chicago, new york city, or washington?')

    city_list = ['chicago', 'new york city', 'washington']
    x = input().lower()
    if x in city_list:
        print("Great, let's look at {}!".format(x))
    else:
        print("No data available for that city. Try again.")
        x = input().lower()


    # get user input for month (all, january, february, ... , june)
    print('Would you like to see data for january, february, march, april, may, june or all months?')
    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    y = input().lower()
    if y in months_list:
        print("Great, let's look at {}!".format(y))
    else:
        print("No data available for that month. Try again.")
        y = input().lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Would you like to see data for Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or all days?')
    day_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    z = input().lower()
    if z in day_list:
        print("Great, let's look at {}!".format(z))
    else:
        print("No data available for that day. Try again.")
        z = input().lower()

    city = x
    month = y
    day = z

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    # extract hour from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)
    print('Most Popular Month:', popular_month)
    print('Most Popular Day:', popular_day)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'].str.cat(df['End Station'])
    popular_route = df['Route'].mode()[0]

    print('Most Popular Start Station:', popular_start_station)
    print('Most Popular End Station:', popular_end_station)
    print('Most Popular Route:', popular_route)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()

    # display mean travel time
    average_trip_length = df['Trip Duration'].mean()

    print('Total Travel Time:', total_travel)
    print('Average Travel Time:', average_trip_length)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()


    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('Gender Count:', gender_counts)
    except:
        print('No gender in this dataframe')

    # Display earliest, most recent, and most common year of birth
    # excepts for data frames with no birthday
    try:
        oldest = df['Birth Year'].min()
        print('Earliest Bday:', oldest)
    except:
        print('No birthdays in this dataframe')
    try:
        youngest = df['Birth Year'].max()
        print('Most Recent Bday', youngest)
    except:
        print('No birthdays in this dataframe')
    try:
        common = df['Birth Year'].mode()[0]
        print('Most Common Bday', common)
    except:
        print('No birthdays in this dataframe')


    print('User Types:', user_types)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_stats(df):
    """displays 10 rows at a time of selected city dataframe"""

    x = input('\nWould you like to see individual trip data?\nPlease enter yes or no\n').lower()

    if x in ('yes'):
        i = 0
        while True:
            print(df.iloc[i:i+10])
            i += 10
            more_data = input('Would you like to see more data? Please enter yes or no ').lower()
            if more_data not in ('yes'):
                print('Cool. I guess we\'re done!')
                break
    if x not in ('yes'):
        print('Cool. I guess we\'re done!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

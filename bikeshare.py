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
    city = ''
    cities = ['chicago', 'new york city', 'washington']
    while city not in cities:
        city = input('Enter city name, e.g. chicago, new york city or washington City: ').lower()
        #print(city)
        if city in cities:
            print('Your city selection is: ', city)            
            break
        else:
            print('Please try again. \n')

    # get user input for month (all, january, february, ... , june)
    month = ''
    months = ['all', 'january','february', 'march', 'april', 'may', 'june', \
              'july', 'august', 'september', 'october', 'november', 'december']
    while month not in months:
        month = input('Enter month e.g. all or january: ').lower()
        if month in months:
            print('Your month selection is: ', month)
            break
        else:
            print('Please try again \n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in days:
        day = input('Enter day e.g. all or wednesday: ').lower()
        if day in days:
            print('Your day selection is: ', day)
            break
        else:
            print('Please try again \n')

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

    # extract month, day of week and hour from Start Time to create new columns
    months = ['all', 'january','february', 'march', 'april', 'may', 'june', \
              'july', 'august', 'september', 'october', 'november', 'december']    
    month_name = df['Start Time'].dt.month.apply(lambda x: months[x])
    #print("month from list = ", months[month_num][:3])
    df['month'] = month_name
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    #print(df.head())
    #print("Month is : ", month)
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    #print(df.head())
    #valid_ans = ['yes', 'no']
    while True:
        ans1 = input('Would you like to see the top 5 data records (yes/no) : ')
        cnt = 0
        if ans1.lower() == 'yes':
            print(df.head(5))
            cnt += 5
            while True:
                ans2 = input('Would you like to see 5 more data records (yes/no) : ')
                if ans2.lower() == 'yes':
                    print(df[cnt:cnt+5])
                    cnt += 5
                elif ans2.lower() == 'no':
                    break
                else:
                    print('Please try again.') 
            break
        elif ans1.lower() == 'no':
            break
        else:
            print('Please try again.')
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    top_month = df.month.mode().iloc[0]

    # display the most common day of week
    top_day = df.day_of_week.mode().iloc[0]

    # display the most common start hour
    top_hr = df.hour.mode().iloc[0]
    
    print("Most common month is :", top_month)
    print("Most common day is : ", top_day)
    print("Most common hour is : ", top_hr)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #print(df.head())
    # display most commonly used start station
    top_start_station = df['Start Station'].mode().iloc[0]

    # display most commonly used end station
    top_end_station = df['End Station'].mode().iloc[0]

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' <--> ' + df['End Station']
    top_trip = df.trip.mode().iloc[0]

    print("Most common start station is :", top_start_station)
    print("Most common end station is : ", top_end_station)
    print("Most common trip combination is : ", top_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # display mean travel time
    print('Total traffic time = ', df.travel_time.sum())
    print('Mean travel time = ', df.travel_time.mean())
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #print(df.head())
    # Display counts of user types
    print('Breakdown of User Types : \n', df['User Type'].value_counts())
    print('\n')
    # Display counts of gender
    print('Breakdown of Gender : \n', df['Gender'].value_counts())
    print('\n')
    # Display earliest, most recent, and most common year of birth
    print('Earliest Year of Birth :', df['Birth Year'].min())
    print('Most recent Year of Birth : ', df['Birth Year'].max())
    print('Most common Year of Birth : ', df['Birth Year'].mode().iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

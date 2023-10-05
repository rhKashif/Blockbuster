'''OOP implementation of a Blockbuster Video Rental Store'''
import datetime
import string


class Time:
    '''class to implement static methods for calculating dates'''
    @staticmethod
    def current_year() -> int:
        '''Returns the current year in yyyy format'''
        return datetime.date.today().year

    @staticmethod
    def time_now() -> str:
        '''Returns the current date in dd/mm/yyyy format'''
        return datetime.date.today().strftime('%d/%m/%Y')

    @staticmethod
    def time_day_delta(delta: int) -> str:
        '''Returns the date in two weeks in dd/mm/yyyy format'''
        todays_date = datetime.date.today()
        date_delta = datetime.timedelta(days=delta)
        time = todays_date + date_delta

        return time.strftime('%d/%m/%Y')

CURRENT_YEAR = Time.current_year()
RENTAL_CHECKOUT_DATE = Time.time_now()
ON_TIME_RETURN_DATE = Time.time_day_delta(14)
LATE_RETURN_DATE = Time.time_day_delta(15)
EARLIER_THAN_RETURN_DATE = Time.time_day_delta(-1)
MAX_FINE = 5000


class Video:
    '''
    Object to hold all information regarding a video:
    title, year of release, runtime, price
    '''
    def __init__(self, title: str, year: int, runtime: int):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.price = self.rental_price()
        self.is_rewound = True

        if not isinstance(year, int):
            raise TypeError("Release year must be in integer")
        if year < 1900 or year > CURRENT_YEAR:
            raise ValueError(f"Video must be released between 1990 and {CURRENT_YEAR}")
        if not isinstance(runtime, int):
            raise TypeError("Video runtime must be a number")
        if runtime > 1440:
            raise ValueError("Maximum runtime limit (24 hours) exceeded")
        if runtime <= 5:
            raise ValueError("Video must be >5 min")
        if title == '':
            raise ValueError("Video must have a title")
        if len(title) > 1000:
            raise ValueError("Title characters exceeded 1000 character limit")

        alphanumerics = list(string.ascii_letters + string.digits)
        title_no_space = self.format_title_space()
        for character in title_no_space:
            if character in alphanumerics:
                break
            raise ValueError('Title must contain some alphanumerical characters')

    def rental_price(self) -> int:
        '''Calculates rental price based on video year of release and runtime'''
        double_runtime = 240

        if self.year == CURRENT_YEAR:
            price = 1000
        else:
            price = 500

        if self.runtime > double_runtime:
            price += price

        return price

    def display_title(self) -> str:
        '''Returns the title and year of release for the video'''
        return f'{self.title} ({self.year})'

    def display_price(self) -> str:
        '''Returns the price of the video to two decimal places'''
        return f"£{self.price/100:.2f}"

    def format_title_space(self) -> list[str|int]:
        '''Returns a list of all letters in the title with spaces ' ' removed'''
        title_no_space = []
        for character in self.title:
            if not character == ' ':
                title_no_space.append(character)
        return title_no_space

    def watch(self) -> None:
        '''
        Returns False is video is rewound
        raises exception if video is not rewound
        '''
        if self.is_rewound is True:
            self.is_rewound = False
        else:
            raise AssertionError('Video has not been rewound') 

    def rewind(self) -> None:
        '''
        Returns True is video is watched
        raises exception if video is not watched
        '''
        if self.is_rewound is False:
            self.is_rewound = True
        else:
            raise AssertionError('Video has already been rewound') 


class Customer:
    '''
    Object to hold all information related to a customer:
    name, date of birth, age, outstanding fines.
    If certain age and name requirements not met, exceptions raised
    '''
    def __init__(self, firstname: str, surname: str, date_of_birth: str):
        self._name = firstname + ' ' + surname
        self._date_of_birth = date_of_birth
        self._age = self.age
        self._outstanding_fine = 0

        if int(self._age) < 13:
            raise ValueError('You must be 13 or above.')
        if int(self._age) > 125:
            raise ValueError('Maximum age (125 years old) exceeded')

        for character in (firstname + surname):
            if character not in string.ascii_letters:
                raise ValueError('Name must contain only alphabetical characters')

    @property
    def name(self) -> str:
        '''Getter function to return the name of the customer'''
        return self._name

    @property
    def age(self) -> str:
        '''
        Calculates the age of the customer based of date of birth and current date.
        Returns age as a string
        '''
        date_of_birth = self._date_of_birth.split('/')
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day
        year_diff = current_year - int(date_of_birth[2])
        month_diff = current_month - int(date_of_birth[1])
        day_diff = current_day - int(date_of_birth[0])

        if day_diff < 0:
            month_diff -= 1
        if month_diff < 0:
            year_diff -= 1

        return str(year_diff)

    @property
    def outstanding_fine(self) -> int:
        '''Getter to return outstanding fine'''
        return self._outstanding_fine

    def pay_off_fine(self, payment: int) -> int:
        '''
        Takes in an integer and adds it to _outstanding_fine
        if argument passed in is not an in
        raises a Type error
        '''
        if not isinstance(payment, int) or payment < 0:
            raise TypeError('Please pay a positive integer i.e. 5 or 10')
        return self._outstanding_fine + payment*100

    @property
    def get_outstanding_fine(self) -> str:
        '''Getter for _outstanding_fine in format £0.00'''
        return f"£{self._outstanding_fine/100:.2f}"


class VideoStore:
    '''
    Object to represent a video store.
    Holds methods to process videos into a database.
    Allow videos to be added, rented and returned.
    '''
    def __init__(self, videos: list[Video]):
        self._videos = videos
        self._rent_status = self.rent_status_database()
        
        if not isinstance(videos, list):
            raise TypeError('Please input a list of movies')
        if len(self._videos) == 0:
            raise ValueError('Video Store cannot contain 0 videos')
        if len(self._videos) > 10:
            raise ValueError('Video Store maximum capacity is 10 videos')

    @property
    def rent_status(self) -> dict:
        '''Getter function for rent_status'''
        return self._rent_status

    @property
    def display_all_titles(self):
        '''
        returns a string of all titles in the store
        irrespective of rental status
        '''
        return ', '.join([video.display_title() for video in self._videos])

    def find_video_by_title(self, title: str) -> str:
        '''
        Takes in a title string.
        Returns a title and year of release if video held in database
        '''
        for video in self._videos:
            if title == video.title:
                return video.display_title

    def is_available(self, title: str) -> bool:
        '''
        Takes in a title string.
        Checks video database for whether the video is available to rent.
        Returns a boolean
        If title is not in the database, exception raised
        '''
        for video in self._rent_status:
            if title == video.title() and self._rent_status[title] is True:
                return True
            if title == video.title() and self._rent_status[title] is False:
                return False

        if title not in self._rent_status.keys():
            raise ValueError('Title not in stock')

    def rent_video(self, title: str, customer: object) -> object:
        '''
        Takes in a video title string and Customer object.
        If video is available for rent,
        returns Rental object with information about video and customer.
        Otherwise raises and exception
        '''
        if not isinstance(customer, Customer):
            raise TypeError('Invalid Customer')

        for video in self._videos:
            if title == video.title:
                video_object = video
        if title not in self._rent_status.keys():
            raise TypeError('Title not in stock at store')

        rented_video = Rental(video_object, customer)

        if customer.outstanding_fine < MAX_FINE:
            for video in self._rent_status:
                if title == video.title() and self.is_available(title):
                    self._rent_status[title] = False
                    return rented_video
                if title == video.title() and not self.is_available(title):
                    raise ValueError('Title unavailable')
        raise RuntimeError(f"You have an outstanding fine of {customer.outstanding_fine}")

    def rent_status_database(self) -> dict:
        '''
        Builds and returns a dictionary for video rental status
        All keys are set as video titles
        All values are set as true
        '''
        rent_status = {}
        for video in self._videos:
            rent_status[video.title] = True

        return rent_status

    def return_video(self, rented_video: object, return_date: str) -> None:
        '''
        Takes in the rented_video object and a return date string
        Updates the video database to show the video is once again available
        Checks if the video was returned within the due date
        Issues a fine if video was returned late
        '''
        if isinstance(rented_video, Rental) and isinstance(return_date, str):
            if rented_video.video.is_rewound is True:
                self.rent_status[rented_video.video.title] = True
                if self.check_date_one_bigger_than_two(rented_video.rented_date, return_date):
                    raise ValueError('Return date cannot be before date of rental')

                if self.check_date_one_bigger_than_two(return_date, rented_video.due_date):
                    if rented_video.video.year == CURRENT_YEAR:
                        rented_video.customer._outstanding_fine += 1500
                    else:
                        rented_video.customer._outstanding_fine += 1000
            else:
                raise AssertionError('Please rewind the video before returning')
        else:
            raise TypeError('Check return date or rented video ')

    def check_date_one_bigger_than_two(self, date_one: str, date_two: str) -> bool:
        '''
        Takes in two date arguments
        Returns True is first date argument is greater
        Returns False if not
        '''
        date_one = date_one.split('/')
        date_two = date_two.split('/')

        date_one = datetime.date(int(date_one[2]), int(date_one[1]), int(date_one[0]))
        date_two = datetime.date(int(date_two[2]), int(date_two[1]), int(date_two[0]))

        if date_one > date_two:
            return True
        return False


class Rental:
    '''
    Object to hold information regarding the Rented video:
    due date, rented date, video and customer
    '''
    def __init__(self, video: object, customer: object):
        self.due_date = Time.time_day_delta(14)
        self.rented_date = Time.time_now()
        self._video = video
        self._customer = customer

    @property
    def video(self) -> str:
        '''returns the video object of the rented video'''
        return self._video

    @property
    def customer(self) -> str:
        '''returns the customer object of the rented video'''
        return self._customer

    @property
    def video_title(self) -> str:
        '''returns the title of the rented video'''
        return self._video.title


class DVD(Video):
    '''
    Object which holds all information regarding DVDs
    Inherits from Video super class
    '''
    def rental_price(self) -> int:
        '''Returns a flat int value for dvd price'''
        return 1200

    def watch(self) -> None:
        return None


class VendingMachine(VideoStore):
    '''
    Object which hold all information regarding Vending Machines
    Inherits from VideoStore super class
    '''
    def __init__(self, videos):
        super().__init__(videos)

        if len(self._videos) == 0:
            raise ValueError('Video Store cannot contain 0 videos')
        if len(self._videos) > 5:
            raise ValueError('Vending Machine maximum capacity is 5 videos')


    def return_video(self, rented_video: object, return_date: str) -> None:
        return super().return_video(rented_video, rented_video.due_date)


if __name__ == "__main__":
    john = Customer('John', 'Smith', '24/01/1980')
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')

    vhs = Video('The Matrix', 1999, 150)
    dvd = DVD('The Matrix', 1999, 150)
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    creed = Video('Creed', 2023, 160)
    movie_list = [matrix, terminator, creed]
    
    store = VideoStore(movie_list)
    vendingmachine = VendingMachine(movie_list)

    rented_hassan = store.rent_video('The Matrix', hassan)
    rented_hassan.video.watch()
    rented_hassan.video.rewind()
    store.return_video(rented_hassan, ON_TIME_RETURN_DATE)

    
  


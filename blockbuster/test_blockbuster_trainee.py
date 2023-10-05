# pylint: skip-file

from blockbuster_oop import Video, Customer, VideoStore, Rental, Time, VendingMachine, DVD
import datetime
import pytest



RENTAL_CHECKOUT_DATE = Time.time_now()
ON_TIME_RETURN_DATE = Time.time_day_delta(14)
LATE_RETURN_DATE = Time.time_day_delta(15)
EARLIER_THAN_RETURN_DATE = Time.time_day_delta(-1)


def test_video_year_release_after_1900_and_before_now():
    with pytest.raises(ValueError):
        Video('The Dreyfus Affair', 1899, 13)


def test_video_year_currently_released():
    with pytest.raises(ValueError):
        Video('The Matrix Collapse', 2024, 90)


def test_video_year_is_int():
    with pytest.raises(TypeError):
        Video('The Matrix Collapse', '2023', 90)


def test_video_runtime_is_int_not_str():
    with pytest.raises(TypeError):
        Video('The Matrix Collapse', 2020, '200')


def test_video_runtime_is_int_not_float():
    with pytest.raises(TypeError):
        Video('The Matrix Collapse', 2020, 157.4)


def test_video_runtime_upper_limit():
    with pytest.raises(ValueError):
        Video('The Matrix Collapse', 2023, 1441)


def test_video_runtime_lower_limit():
    with pytest.raises(ValueError):
        Video('The Matrix Collapse', 2023, -5)


def test_video_title_given():
    with pytest.raises(ValueError):
        Video('', 2023, 90)


def test_video_title_max_characters():
    with pytest.raises(ValueError):
        Video('a' * 1001, 2023, 90)


def test_video_title_alphanumerical_characters():
    with pytest.raises(ValueError):
        Video('!', 2023, 90)


def test_customer_name():
    john = Customer('John', 'Smith', '24/01/1980')
    assert john._name == 'John Smith'


def test_customer_date_of_birth():
    john = Customer('John', 'Smith', '24/01/1980')
    assert john._date_of_birth == '24/01/1980'


def test_customer_name_getter():
    john = Customer('John', 'Smith', '24/01/1980')
    assert john.name == 'John Smith'


def test_customer_age():
    john = Customer('John', 'Smith', '24/01/1980')
    assert john.age == '43'


def test_customer_age_above_13():
    with pytest.raises(ValueError):
        Customer('Zoom', 'Smith', '24/01/2020')


def test_customer_age_below_125():
    with pytest.raises(ValueError):
        Customer('Zoom', 'Smith', '24/01/1897')


def test_customer_valid_name():
    with pytest.raises(ValueError):
        Customer('200m', 'Sm1th', '24/01/1999')


def test_videostore_empty():
    with pytest.raises(ValueError):
        VideoStore([])
        

def test_videostore_full():
    with pytest.raises(ValueError):
        VideoStore([Video('The Dreyfus Affair', 1950, 13) for i in range(11)])


def test_videostore_title_search():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    assert store.find_video_by_title('The Matrix') == matrix.display_title


def test_videostore_is_available_available():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    assert store.is_available('The Matrix') == True


def test_videostore_is_available_unavailable():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    store.rent_video('The Matrix', hassan)
    assert store.is_available('The Matrix') == False

def test_videostore_rent_video_removes_video_availability():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    assert store.is_available('The Terminator') == True
    store.rent_video('The Terminator', hassan)
    assert store.is_available('The Terminator') == False

def test_videostore_rent_video_non_existent_title():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    creed = Video('Creed', 2023, 160)
    store = VideoStore([matrix, terminator])
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    with pytest.raises(TypeError):
        store.rent_video(creed.title, hassan) 

def test_videostore_rent_video_non_object_argument():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    with pytest.raises(TypeError):
        store.rent_video('The Matrix', []) 

def test_videostore_rent_status_database_builds():
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    assert store._rent_status == {'The Matrix': True, 'The Terminator': True}

def test_videostore_rent_video_updates_database():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    assert store._rent_status == {'The Matrix': True, 'The Terminator': True}
    hassan_rental = store.rent_video('The Terminator', hassan)
    assert store._rent_status == {'The Matrix': True, 'The Terminator': False}

def test_videostore_return_video_updates_database():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    assert store._rent_status == {'The Matrix': True, 'The Terminator': True}
    hassan_rental = store.rent_video('The Terminator', hassan)
    assert store._rent_status == {'The Matrix': True, 'The Terminator': False}
    store.return_video(hassan_rental, ON_TIME_RETURN_DATE)
    assert store._rent_status == {'The Matrix': True, 'The Terminator': True}

def test_videostore_return_video_late_issues_fine():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    store.return_video(hassan_rental, LATE_RETURN_DATE)
    assert hassan._outstanding_fine == 1000

def test_videostore_return_video_earlier_than_issued():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    with pytest.raises(ValueError):
        store.return_video(hassan_rental, EARLIER_THAN_RETURN_DATE)
    
def test_videostore_return_video_incorrect_argument_type_object():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    with pytest.raises(TypeError):
        store.return_video([], EARLIER_THAN_RETURN_DATE)

def test_videostore_return_video_incorrect_argument_type_str():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    with pytest.raises(TypeError):
        store.return_video(hassan_rental, 10/10/2010)

def test_video_watch_updates_is_rewound():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    assert hassan_rental.video.is_rewound == True
    hassan_rental.video.watch()
    assert hassan_rental.video.is_rewound == False

def test_video_watch_raises_exception_if_not_rewound():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    hassan_rental.video.watch()
    with pytest.raises(AssertionError):
        hassan_rental.video.watch()

def test_video_rewind_updates_is_rewound():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    hassan_rental.video.watch()
    assert hassan_rental.video.is_rewound == False
    hassan_rental.video.rewind()
    assert hassan_rental.video.is_rewound == True

def test_video_rewind_raises_exception_if_already_rewound():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    with pytest.raises(AssertionError):
        hassan_rental.video.rewind()

def test_video_return_video_if_is_rewind_false():
    hassan = Customer('Hassan', 'Kashif', '09/03/1999')
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    store = VideoStore([matrix, terminator])
    hassan_rental = store.rent_video('The Terminator', hassan)
    hassan_rental.video.watch()
    with pytest.raises(AssertionError):
        store.return_video(hassan_rental, ON_TIME_RETURN_DATE)

def test_DVD_rental_price():
    dvd = DVD('The Matrix', 1999, 150)
    assert dvd.rental_price() == 1200

def test_VendingMachine_max_capacity():
    vhs = Video('The Matrix', 1999, 150)
    dvd = DVD('The Matrix', 1999, 150)
    matrix = Video('The Matrix', 1999, 150)
    terminator = Video('The Terminator', 1985, 108)
    creed = Video('Creed', 2023, 160)
    house = Video('House', 2021, 132)
    movie_list = [vhs, dvd, matrix, terminator, creed, house]
    with pytest.raises(ValueError):
        VendingMachine(movie_list)

def test_VendingMachine_non_list_argument():
    with pytest.raises(TypeError):
        VendingMachine('')
# pylint: skip-file

from blockbuster_oop import Video, Customer, VideoStore, VendingMachine, DVD
import pytest


@pytest.fixture
def the_matrix():
    return Video('The Matrix', 1999, 150)


def test_video_display_price(the_matrix):
    assert the_matrix.display_price() == '£5.00'


def test_video_title(the_matrix):
    assert the_matrix.display_title() == 'The Matrix (1999)'


def test_video_release_after_1900():
    with pytest.raises(Exception):
        Video('The Dreyfus Affair', 1899, 13)


def test_video_price_regular():
    video = Video('Mission Impossible 8', 2023, 90)
    assert video.rental_price() == 1000


def test_video_price_previous_years():
    video = Video('The Mummy', 1999, 124)
    assert video.rental_price() == 500


def test_video_price_extra_long():
    video = Video("Zack Snyder's Justice League",  2023, 242)
    assert video.rental_price() == 2000


def test_video_extra_long_previous_year():
    video = Video('Fellowship of the Ring: Extended Edition', 2001, 250)
    assert video.rental_price() == 1000


def test_video_has_title():
    with pytest.raises(Exception):
        Video(None, 2010, 90)

import doctest
suite = doctest.DocFileSuite('test_sliding_window.py')

if __name__ == '__main__':
    doctest.testfile("test_sliding_window.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.utils.sliding_window import SlidingWindow

>>> # basic test
>>> things = [chr(x) for x in range(ord('a'), ord('z'))]
>>> window = SlidingWindow(things)
>>> prev, next, window, i_from = window.view('k')
>>> print prev, next, window, i_from
j l ['d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y'] 3

>>> # test window size
>>> window = SlidingWindow(things, window_left=3, window_right=2)
>>> prev, next, window, i_from = window.view('k')
>>> print prev, next, window, i_from
j l ['h', 'i', 'j', 'k', 'l', 'm'] 7

>>> window = SlidingWindow(things, window_left=1, window_right=1)
>>> prev, next, window, i_from = window.view('k')
>>> print prev, next, window, i_from
j l ['j', 'k', 'l'] 9

>>> # an exmpale of a window onto page numbers
>>> pages = range(0, 100)
>>> window = SlidingWindow(pages, window_left=2, window_right=5)
>>> prev_page, next_page, page_window, i_from = window.view(10)
>>> print "prev_page:", prev_page
prev_page: 9

>>> print "next_page:", next_page
next_page: 11

>>> print "page_window:", page_window
page_window: [8, 9, 10, 11, 12, 13, 14, 15]

>>> print "i_from:", i_from
i_from: 8

>>> # test at limits
>>> print window.view(0)
(99, 1, [0, 1, 2, 3, 4, 5], 0)

>>> print window.view(1)
(0, 2, [0, 1, 2, 3, 4, 5, 6], 0)

>>> print window.view(2)
(1, 3, [0, 1, 2, 3, 4, 5, 6, 7], 0)

>>> print window.view(98)
(97, 99, [96, 97, 98, 99], 96)

>>> print window.view(100)
(99, 0, [98, 99], 98)

>>> print window.view(999)
(99, 0, [98, 99], 98)

'''

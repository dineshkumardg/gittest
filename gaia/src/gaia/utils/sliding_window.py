
class SlidingWindow:
    ''' A SlidingWindow presents a limited view across a set of objects.

        The shape and size of the window can be configured by window_left and window_right,
        by default, you'll see 7 before and 14 thiogs after the selected object.

        Note: One use of this class is to present a limited view of a
        set of pages in a UI (mostly replacing the django Paginator class).
    '''

    def __init__(self, things, window_left=7, window_right=14):
        self.things = things
        self.window_left  = window_left
        self.window_right = window_right

    def view(self, chosen_thing):
        ''' get a windowed view, focussing on a chosen_thing

            returns:
                prev: the thing before this one
                next: the thing after this one
                things_in_window: the limited set of things visible in the window
                i_from: the _index_ of this thing wihtin the full list of things
        '''
        things = self.things

        i = 0
        i_last = len(things) - 1

        for thing in things:
            if thing == chosen_thing:
                break
            i += 1

        if i < i_last:
            next = things[i + 1]
        else:
            next = things[0]

        if i == 0:
            prev = things[i_last]
        else:
            prev = things[i - 1]

        if i - self.window_left < 0:   # Querysets don't support negative indexing unfortunately :(
            i_from = 0
        else:
            i_from = i - self.window_left

        if i + self.window_right > i_last:
            i_to = i_last
        else:
            i_to = i + self.window_right

        things_in_window = things[i_from:i_to+1]  # limit the window of viewable things
        return prev, next, things_in_window, i_from

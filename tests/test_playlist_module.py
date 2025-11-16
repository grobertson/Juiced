import pytest

from juiced.lib.playlist import Playlist, PlaylistItem


def make_item_data(uid, title='t', seconds=10, queueby='u'):
    return {
        'uid': uid,
        'temp': False,
        'queueby': queueby,
        'media': {'type': 'yt', 'id': f'id{uid}', 'title': title, 'seconds': seconds}
    }


def test_playlist_item_and_eq_and_str():
    data = make_item_data(1, 'Title')
    it = PlaylistItem(data)
    assert str(it).startswith('<playlist item #1')
    assert it == 1
    it2 = PlaylistItem(make_item_data(1))
    assert it == it2


def test_playlist_add_get_remove_move_clear():
    pl = Playlist()
    pl.add(None, make_item_data(1))
    pl.add(None, make_item_data(2))
    assert len(pl.queue) == 2

    pl.current = 1
    # setting current by id should resolve to a PlaylistItem
    assert pl.current is not None
    assert pl.current.uid == 1

    pl.move(1, 2)
    # after move, still two items
    assert len(pl.queue) == 2

    pl.remove(1)
    assert len(pl.queue) == 1

    pl.clear()
    assert pl.queue == []

import pytest

from juiced.lib.media_link import MediaLink


def test_from_url_youtube_and_short():
    ml = MediaLink.from_url("https://youtube.com/watch?v=abc123")
    assert ml.type == "yt" and ml.id == "abc123"
    assert "youtube" in ml.url

    ml2 = MediaLink.from_url("https://youtu.be/xyz")
    assert ml2.type == "yt" and ml2.id == "xyz"


def test_from_url_file_and_rtmp_and_http_errors():
    # https file extension -> fi
    ml = MediaLink.from_url("https://example.com/video.mp4")
    assert ml.type == "fi"

    # rtmp scheme
    ml2 = MediaLink.from_url("rtmp://stream.example.com/live")
    assert ml2.type == "rt"

    # http (non-https) file should raise
    with pytest.raises(ValueError):
        MediaLink.from_url("http://example.com/video.mp4")


def test_unknown_type_url_property_fallback(caplog):
    m = MediaLink("zz", "id")
    url = m.url
    assert url == "zz:id"
    assert "unknown media type" in caplog.text.lower()

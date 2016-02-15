from __future__ import print_function
import pycurl

def perform(target, write_function=None):
    """
    Perform an HTTP request against a given target gathering some basic
    timing and content size values.
    """

    fnc = write_function or (lambda x: None)
    assert target

    connection = pycurl.Curl()
    connection.setopt(pycurl.URL, target)
    connection.setopt(pycurl.FOLLOWLOCATION, True)
    connection.setopt(pycurl.WRITEFUNCTION, fnc)
    connection.perform()

    result = {
        'response': connection.getinfo(pycurl.RESPONSE_CODE),
        'rtt': round(connection.getinfo(pycurl.CONNECT_TIME), 5),
        'response_time': round(connection.getinfo(pycurl.TOTAL_TIME), 5),
        'content_size': (
            int(connection.getinfo(pycurl.SIZE_DOWNLOAD)) + int(connection.getinfo(pycurl.HEADER_SIZE))
        ) * 8
    }

    try:
        result['bps'] = round(
            result['content_size'] / result['response_time'],
            5
        )
    except ZeroDivisionError:
        result['bps'] = 0
    return result

if __name__ == '__main__':
    import sys
    target = sys.argv[1]
    iterations = int(sys.argv[2])

    for i in range(iterations):
        print(perform(target))
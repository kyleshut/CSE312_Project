def getByteLength(file):
    f = open(file, "rb")
    length = 0
    for line in f:
        for char in line:
            length = length + 1
    f.close()
    return length


def ok(type, length, message):
    output = "HTTP/1.1 200 OK\r\nContent-Type: ".encode() + type.encode() +";\r\nContent-Length: ".encode() + str(length).encode() + "\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + message.encode()
    return output


def notFound(type, length, message):
    output = "HTTP/1.1 404 Not Found\r\nContent-Type: ".encode() + type.encode() +";\r\nContent-Length: ".encode() + str(length).encode() + "\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + message.encode()
    return output


def parse_get(data):
    parsed = data.split()

    if(parsed[1] == '/'.encode("utf-8")):
        print("Parsed index properly\n")
        return 'index'
    elif(parsed[1] == '/button'.encode("utf-8")):
        print("Parsed button properly\n")
        return 'button'
    else:
        print("Did not find anything\n")
        return '404'
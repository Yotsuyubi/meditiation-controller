# from progress.spinner import Spinner


def log(type, msg):
    print('\033[34m'+"[{}]: {}".format(type, msg)+'\033[0m')


def error(type, msg):
    print('\033[31m'+"[{}]! {}".format(type, msg)+'\033[0m')


def lerp(a, b, t):
    return a + (b - a) * t


def slide(array, x):
    array.append(x)
    return array[1:]

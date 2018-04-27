# coding:utf-8


def _ori_iter():
    n = 1
    while True:
        n += 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def prime():
    it = _ori_iter()
    while True:
        n = next(it)
        yield n
        # it = filter(lambda x: x % n > 0, it)
        it = filter(_not_divisible(n), it)


if __name__ == '__main__':
    for i in prime():
        if i < 50:
            print(i)
        else:
            break

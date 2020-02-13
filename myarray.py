# coding:utf-8
# 数组: 一种线性表数据结构。它由一组 连续 的内存空间，来存储一组具有 相同类型的 数据。
# 插入 删除 随机访问

class MyArray:

    def __init__(self, capacity: int):
        self._data = []
        self._capacity = capacity

    def __getitem__(self, position: int) -> object:
        return self._data[position]

    def __setitem__(self, index: int, value: object):
        self._data[index] = value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        for item in self._data:
            yield item

    def find(self, index: int) -> object:
        try:
            return self._data[index]
        except IndexError:
            return None

    def delete(self, index: int) -> bool:
        try:
            self._data.pop(index)
            return True
        except IndexError:
            return False

    def insert(self, index: int, value: int) -> bool:
        if len(self) >= self._capacity:
            return False
        return self._data.insert(index, value)

    def print_all(self):
        for item in self:
            print(item)


def test():
    array = MyArray(5)
    array.insert(0, 'a')
    array.insert(1, 'b')
    array.insert(2, 'c')
    array.insert(3, 'd')
    array.insert(4, 'e')
    assert array.insert(3, 'f') is False
    assert len(array) == 5
    assert array.find(1) == 'b'
    assert array.delete(4) is True
    array.print_all()


if __name__ == "__main__":
    test()

# 素数算法

看到廖雪峰网站上用python的[实现](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431821084171d2e0f22e7cc24305ae03aa0214d0ef29000), 看起来很简单, 但是最终还是自己实现一遍比较好, ==[代码点我跳转](https://github.com/CabbyWang/practice/blob/master/code/prime_numbers.py).==

- 素数算法 ([埃拉托色尼筛选法](https://baike.baidu.com/item/%E5%9F%83%E6%8B%89%E6%89%98%E8%89%B2%E5%B0%BC%E7%AD%9B%E9%80%89%E6%B3%95))

原理很简单, 在数学界`1`既不是质数也不是合数, 所以不用管`1`, 从`2`开始

	输出最小的质数`2`, 然后将`2`的倍数都删除
	输出剩下的第一个数为`3`, 然后将`3`的倍数都删除
	输出剩下的第一个数为`5`, 然后将`5`的倍数都删除
	输出剩下的第一个数为`7`, 然后将`7`的倍数都删除
	...

这样不断循环下去, 直到所有的数都被删除或者输出, 输出的数即为`质数`.

- 实现

```python
def _ori_iter():
    n = 1
    while True:
        n += 2
        yield n
```
这里先定义一个`ori_iter`方法, 返回的是一个`生成器`(从`3`开始的奇数, 如 3, 5, 7...)

```python
def _not_divisible(n):
    return lambda x: x % n > 0
```
这里定义了一个`_not_divisible`方法, 这可以理解成一种规则, `x`能整除`n`返回`false`, 不能整除则返回`true`, 后面`filter`中有用到

```python
def prime():
    it = _ori_iter()
    while True:
        n = next(it)
        yield n
        # it = filter(lambda x: x % n > 0, it)
        it = filter(_not_divisible(n), it)
```
这里定义的`prime`返回的则是全体素数. 第一行的`it = _ori_iter()`, 这时it是一个会返回从`3`开始的所有奇数(也就是不能被2整除)的生成器==(3, 5, 7, 9, 11...)==, `while True`表示将会无限循环下去,直到天荒地老, 下面是循环过程
1. 取出的第一个`n`是`it`的第一个元素`3`, `yield n`将`3`作为`prime`生成器的第一个元素. 之后经过`it = filter(_not_divisible(n), it)`, 这里的`it`经过筛选, 将`3`的倍数全部丢弃==(3, 5, 7, ~~9~~, 11...)==
2. 取出被筛选过的`it`的第二个元素, 也就是`5`, 作为`prime`生成器的第二个元素. 之后在经过`it = filter(_not_divisible(n), it)`筛选, 将`5`的倍数全部丢弃(3, 5, 7, 11, 13, ~~15~~...)
3. 取出被筛选过的`it`的第三个元素, 也就是`7`, 作为`prime`生成器的第三个元素. 之后在经过`it = filter(_not_divisible(n), it)`筛选, 将`7`的倍数全部丢弃(3, 5, 7, 11, 13...~~21~~...)
4. ...

这是一个无限循环, 所以`prime`返回的是一个的生成器, 里面包含无穷多个`质数`


- 总结
算法很容易理解, 实现起来也并不难, 下面是在实现的过程中遇到的一个问题

```python
def _not_divisible(n):
    return lambda x: x % n > 0

def prime():
    it = _ori_iter()
    while True:
        n = next(it)
        yield n
        # it = filter(lambda x: x % n > 0, it)
        it = filter(_not_divisible(n), it)
```

最后两句分为注释部分`it = filter(lambda x: x % n > 0, it)`和未注释部分`it = filter(_not_divisible(n), it)`咋一看并没有什么区别, 但是输出的结果却大有不同, 这就有意思了, 思前想后, 请教同事, 最后总算是有点理解, 这里大致描述一下为什么会出现输出不同的情况...

**生成器(Iterator)是一种惰性计算的序列(他很懒, 你催他一下, 他才会给你下一个数据- -), 只有当你使用`next`取值时, 才会去执行, 然后返回给你正确的值**
- 这里如果使用未注释部分, `it = filter(lambda x: x % n > 0, it)`这里的`n`值确实是上一句正确返回的`n`值, 但是由于`filter`也是惰性的, `filter`只会去执行一次筛选, 然后到下次循环时, `n`的值就变了成下次返回的`n`, 这样每次`filter`都只会筛选一次, 真正需要筛选出去的值并没有被筛选, 最后的执行结果显然不会正确了...
- 然而使用未注释部分代码, `n`的值是通过`_not_divisible`函数的参数传进去的, 不会去改变, 传进去第一个`3`, 他就会一直筛选下去, 然后传进第二个`5`的时候, 同理也会筛选下去, 所以可以得出正确的质数序列

**归根结底, 这里应该是`filter`和`lambda`内部处理的问题, 可能研究一下源码会更加明了, 这里就先不倒腾了/哭笑...**


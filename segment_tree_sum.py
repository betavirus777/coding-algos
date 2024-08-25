class SegmentTree:

    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        self.data = data

    def build(self):
        for i in range(self.n):
            self.tree[i+self.n] = self.data[i]
        
        for i in range(self.n-1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]


    def update(self, pos, value):
        pos += self.n
        self.tree[pos] = value
        while pos > 1:
            pos = pos//2

            self.tree[pos] = self.tree[2*pos] + self.tree[2*pos+1]

    def print_tree(self):
        print(self.tree)

    def query(self, l, r):
        l += self.n
        r += self.n
        _sum = 0
        while l < r:
            if l % 2:
                _sum += self.tree[l]
                l = l + 1
            if r % 2:
                r = r-1
                _sum += self.tree[r]

            l = l //2
            r = r //2
        print(_sum)
        return _sum


seg = SegmentTree([1,2,3,3,4,5,6])

seg.build()

seg.print_tree()
seg.query(1, 3)
seg.update(2,9)

seg.print_tree()

seg.query(1,3)


        
        
class UnionFind:
    
    def __init__(self, n):
        self.parent = {}
        self.rank = {}
        self.islands = 0
        
    def find(self, n):
        
        if n not in self.parent:
            self.parent[n] = n
            self.rank[n] = 0
            self.islands += 1  
        else:
            if self.parent[n] == n:
                return n
            self.parent[n] = self.find(self.parent[n])
        return self.parent[n]
        
    def union(self, n1, n2):
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            return
        self.islands -= 1
        
        if(self.rank[n1] > self.rank[n2]):
            self.parent[n2] = n1
        elif(self.rank[n2] > self.rank[n1]):
            self.parent[n1] = n2
        else:
            self.parent[n2] = n1
            self.rank[n1] += 1
            
class Solution:
    def __init__(self):
        self.graph = set()
        
    def addLand(self,x,y):
        self.graph.add((x,y))
        
    def numIslands2(self):
        uf = UnionFind(1000)
        n = 1000
        res = []
        for r, c in self.graph:
            
            uf.find(r * n + c)
            self.graph.add((r, c))
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if (nr, nc) in self.graph:
                    uf.union(r * n + c, nr * n + nc)
            
        return uf.islands
        
g = Solution()

g.addLand(1,1)
print(g.numIslands2())
g.addLand(1,2)
print(g.numIslands2())
g.addLand(2,4)
print(g.numIslands2())

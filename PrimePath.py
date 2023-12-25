import sys
import codecs as cs

def readGraphFromFile(src):
    with cs.open(src, 'r', 'utf-8') as graphFile:
        # Read nodes set of graph
        graphFile.readline()
        nodes = [int(n) for n in graphFile.readline().split()]
        # Read initial nodes set of graph
        graphFile.readline()
        initNodes = [int(n) for n in graphFile.readline().split()]
        # Read end nodes set of graph
        graphFile.readline()
        endNodes = [int(n) for n in graphFile.readline().split()]
        # Read edges set of graph
        graphFile.readline()
        edges = {}
        for i in nodes:
            s = graphFile.readline().strip().split()
            if len(s) >= 1:
                edges[i] = [int(n) for n in s if n != '-1']
            else:
                edges[i] = []
        graph = {'nodes': nodes, 'init': initNodes,
                 'end': endNodes, 'edges': edges}
        return graph

def isPrimePath(path, graph):
    if len(path) >= 2 and path[0] == path[-1]:
        return True
    elif reachHead(path, graph) and reachEnd(path, graph):
        return True
    else:
        return False


def reachHead(path, graph):
    former_nodes = filter(lambda n: path[0] in graph['edges'][n], graph['nodes'])
    for n in former_nodes:
        if n not in path or n == path[-1]:
            return False
    return True


def reachEnd(path, graph):
    later_nodes = graph['edges'][path[-1]]
    for n in later_nodes:
        if n not in path or n == path[0]:
            return False
    return True


def extendable(path, graph):
    if isPrimePath(path, graph) or reachEnd(path, graph):
        return False
    else:
        return True


def findSimplePath(graph, exPaths, paths=[]):
    paths.extend(filter(lambda p: isPrimePath(p, graph), exPaths))
    exPaths = filter(lambda p: extendable(p, graph), exPaths)
    newExPaths = []
    for p in exPaths:
        for nx in graph['edges'][p[-1]]:
            if nx not in p or nx == p[0]:
                newExPaths.append(p + (nx, ))
    if len(newExPaths) > 0:
        findSimplePath(graph, newExPaths, paths)

def GetTestPaths(graph: dict, primes: list) -> None:
    testpaths = []
    sideTracks = []
    starts = graph['init']
    ends = graph['end']
    for path in primes:
        first = path[0]
        second = path[-1]
        if (first in starts and second in ends):
            testpaths.append(list(path))
        elif (first not in starts and second not in ends):
            sideTracks.append(list(path))
             
    sidepaths = []
    for path in testpaths:
        for sideTrack in sideTracks:
            for index, i in enumerate(path):
                for Ind, j in enumerate(sideTrack):
                    if Ind == 0 and i == j:
                        temp = list(path)
                        temp.remove(i)
                        for h in sideTrack:
                            temp.insert(index, h)
                        sidepaths.append(temp)

    if sidepaths:
        testpaths.extend(sidepaths)                 
    return testpaths

def findPrimePaths(graph):
    exPaths = [(n, ) for n in graph['nodes']]
    simplePaths = []
    findSimplePath(graph, exPaths, simplePaths)
    primePaths = sorted(simplePaths, key=lambda a: (len(a), a))
    print("Prime paths: ")
    for p in primePaths:
        print (list(p))
    tps = GetTestPaths(graph, primePaths)
    print('Test Paths: ')
    for tp in tps:
        print(tp)

if __name__ == "__main__":
    graphFile = sys.argv[1]
    graph = readGraphFromFile(graphFile)
    findPrimePaths(graph)
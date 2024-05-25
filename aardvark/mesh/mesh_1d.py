import aardvark.internal_api as adv

class Mesh1D(adv.Mesh):
    def setup(self, nodes: adv.np.ndarray = None):
        self.nodes = adv.np.ndarray(nodes)
        self.cells = adv.np.ndarray([0.5*nodes[i+1] + 0.5*nodes[i] for i in range(len(nodes)-1)])
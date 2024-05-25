import aardvark.internal_api as adv

from abc import ABC, abstractmethod
from itertools import count

class Variable(ABC):

    _id = count(0)
    
    @property
    def value(self) -> adv.np.ndarray:
        return self._value
    
    @value.setter
    def value(self, new_value: adv.np.ndarray):
        self.prev_value = self._value

        if(new_value is None):
            self._value = None

        else:
            self._value = adv.np.array(new_value)

    @property
    def initial(self) -> adv.np.ndarray:
        return self._initial
    
    @initial.setter
    def initial(self, new_initial):
        if(new_initial is None):
            self._initial = None

        else:
            self._initial = adv.np.array(new_initial)

    def __init__(self, name: str, initial: adv.np.ndarray = None):
        self.name = name

        self.initial: adv.np.ndarray = initial
        self._value = None
        self.prev_value = None

        self.is_initialized = False

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def r2(self) -> float:
        pass

class FloatVar(Variable):
    def initialize(self):
        if(not self.is_initialized):
            self.value = self.initial

            self.is_initialized = True

    def r2(self) -> float:
        return (self.value - self.prev_value)**2

class Mesh1DVar(Variable):
    def initialize(self, x: adv.np.ndarray):
        if(not self.is_initialized):
            self.x = x

            if(self.initial.size == 1):
                self.value = adv.np.array(len(x)*[self.initial])

            else:
                self.value = self.initial

            self.is_initialized = True

    def r2(self) -> float:
        return adv.np.sum((self.value - self.prev_value)**2)
    
    def plot(self):
        adv.plt.xlabel("Node X (m)")
        adv.plt.ylabel(self.name)
        adv.plt.grid(True)
        adv.plt.tight_layout()

        adv.plt.plot(self.x, self.value, 'o')
        adv.plt.show()

class FlowStateVar(Variable):

    # T0 
    @property
    def T0_value(self) -> adv.np.ndarray:
        return self._T0_value
    
    @T0_value.setter
    def value(self, new_value: adv.np.ndarray):
        self.T0_prev_value = self._T0_value

        if(new_value is None):
            self._T0_value = None

        else:
            self._T0_value = adv.np.array(new_value)

    @property
    def T0_initial(self) -> adv.np.ndarray:
        return self._T0_initial
    
    @T0_initial.setter
    def T0_initial(self, new_initial):
        if(new_initial is None):
            self._T0_initial = None

        else:
            self._T0_initial = adv.np.array(new_initial)

    # P0 
    @property
    def P0_value(self) -> adv.np.ndarray:
        return self._P0_value
    
    @P0_value.setter
    def value(self, new_value: adv.np.ndarray):
        self.P0_prev_value = self._P0_value

        if(new_value is None):
            self._P0_value = None

        else:
            self._P0_value = adv.np.array(new_value)

    @property
    def P0_initial(self) -> adv.np.ndarray:
        return self._P0_initial
    
    @P0_initial.setter
    def P0_initial(self, new_initial):
        if(new_initial is None):
            self._P0_initial = None

        else:
            self._P0_initial = adv.np.array(new_initial)

    # m_dot 
    @property
    def m_dot_value(self) -> adv.np.ndarray:
        return self._m_dot_value
    
    @m_dot_value.setter
    def value(self, new_value: adv.np.ndarray):
        self.m_dot_prev_value = self._m_dot_value

        if(new_value is None):
            self._m_dot_value = None

        else:
            self._m_dot_value = adv.np.array(new_value)

    @property
    def m_dot_initial(self) -> adv.np.ndarray:
        return self._m_dot_initial
    
    @m_dot_initial.setter
    def m_dot_initial(self, new_initial):
        if(new_initial is None):
            self._m_dot_initial = None

        else:
            self._m_dot_initial = adv.np.array(new_initial)

    def __init__(self, name: str, T0_initial: adv.np.ndarray = None, 
                 P0_initial: adv.np.ndarray = None, m_dot_initial: adv.np.ndarray = None):
        self.name = name

        self.T0_initial: adv.np.ndarray = T0_initial
        self.P0_initial: adv.np.ndarray = P0_initial
        self.m_dot_initial: adv.np.ndarray = m_dot_initial

        self._T0_value = None
        self._P0_value = None
        self._m_dot_value = None

        self.T0_prev_value = None
        self.P0_prev_value = None
        self.m_dot_prev_value = None
        
        self.is_initialized = False

    def set_initial(self, T0_initial: adv.np.ndarray = None, 
                 P0_initial: adv.np.ndarray = None, m_dot_initial: adv.np.ndarray = None):
        
        self.T0_initial = T0_initial
        self.P0_initial = P0_initial
        self.m_dot_initial = m_dot_initial
        
    def initialize(self):
        if(not self.is_initialized):
            self.T0 = self.T0_initial
            self.P0 = self.P0_initial
            self.m_dot = self.m_dot_initial

            self.is_initialized = True

    def r2(self) -> float:
        return adv.np.sum((self.value - self.prev_value)**2)
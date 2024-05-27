import aardvark.internal_api as adv

from abc import ABC, abstractmethod


class Component(ABC):
    component_name = "Component"

    def register(self, name: str):
        self._name = name + " (" + self.component_name + ")"

        for component in adv.components:
            if(component._name == name):
                adv.Log.error("Tried to create a component named \"" + name + "\" but a component with that name already exists.")

        self._name = name
        adv.components.append(self)

    def log_message(self, message: str):
        adv.Log.message(self._name +" :: " + message)

    def log_error(self, message: str):
        adv.Log.error(self._name +" :: " + message)

    def check_inputs(self):
        inputs: dict = vars(self.inputs)

        variable: adv.Variable
        for variable in inputs.values():
            if(variable.initial is None):
                
                self.log_error("Input variable \"" + variable.name + "\" initial value is None.")

    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def solve_steady_state(self):
        """TODO
        """
        pass

    def residual(self) -> float:
        r2 = 0

        outputs: dict = vars(self.outputs)

        variable: adv.Variable
        for variable in outputs.values():
            r2 += variable.r2()

        return adv.np.sqrt(r2)

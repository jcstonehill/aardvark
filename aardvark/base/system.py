import aardvark.internal_api as adv

import os
from itertools import count


class System:


    components: list[adv.Component] = []
    variables: list[adv.Variable] = []
    variable_types: list[type] = []

    var_id: count = count(0)

    @classmethod
    def define_variable(cls, var_type: type):
        id = next(cls.var_id)

        cls.variable_types.append(var_type)

        return id

    @classmethod
    def modify_case_name(cls, orig_case_name: str) -> str:
        i = 0

        new_case_name = orig_case_name

        while(os.path.isdir("output/" + new_case_name)):
            i += 1
            new_case_name = orig_case_name + "-" + str(i)

        return new_case_name

    @classmethod
    def create_outputs_dir(cls, desired_case_name: str):
        outputs_dir_exists = os.path.isdir("output")

        if(not outputs_dir_exists):
            os.mkdir("output")

        case_exists = os.path.isdir("output/" + desired_case_name)

        if(case_exists):
            case_name = cls.modify_case_name(desired_case_name)

        else:
            case_name = desired_case_name

        os.mkdir("output/" + case_name)
        
        adv.Log.create(case_name)

        if(not outputs_dir_exists):
            adv.Log.message("Output folder not found. Created new outputs folder.")

        if(case_exists):
            adv.Log.message("A case named \"" + desired_case_name + "\" already exists. Modifying case name to \"" + case_name + "\".")
            
        adv.Log.message("Created case named \"" + str(case_name) + "\".")
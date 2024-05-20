#import aardvark.internal_api as adv


start_message = """
                                                #######                               
                                         #####################                        
                                      #######             #######                     
                                   ######                      #####                  
    ##               ####       ######                            ####                
      ##            ##   #     ####                                  ###              
    ## ###         #     #  ####                                      ####            
     ##  ###       #      ####                                          ###           
      ##   ###     #      ##                                              ##          
       ##   ###   #       #                                                ##         
        ##    ### #   #  #                                                  ##        
         ###   ####  #                                                       ##       
           ##         #                                                      ##       
            ##   ###                                                          ##      
           ##  ##                                                             ##      
          ##                                                              #    ##     
        ###     ###                                                     ###### ##     
        ##      #                         ###                          ##    # ##     
       ##                                   ##          ###           ##        #     
      ##           ######  ###               # ##    ####  ###        ## ##     ##    
   ####          ####    ##  ####            ## ##  #      # ##      ##   ##    ##    
 ####          ##         ##    ##  #       ##   ###       ## ##    ##     ##    ##   
 ##         ###           ##      # #       ##     ##      ## ##    ##      ##    #   
 ##      ###               ##    ## ##      ##      ##    ### ##    ##       ##   ##  
  #### ###                  ##   ##  ##    ##      ##    ###  ##    ##        ##   ## 
   ######                   ##   ##  ###   ##    ###    ##    ##    ###        ###  # 
                            ##    #   ##  ##   ####    ###   ###     ##          ## # 
                        #####  ###   ####    #      ####    #       ##           ###  
                        ##   ####  ##   ###    #########     #########              # 

                        
"""

class Log:
    case_name = ""

    @classmethod
    def create(cls, case_name: str):
        cls.case_name = case_name

        cls._create_log_file()

    @classmethod
    def message(cls, message: str):
        message = "AARDVARK :: " + message

        print(message)

        message = message + "\n"
        cls._add_to_log_file(message)

    @classmethod
    def line_break(cls):
        print("\n")

        cls._add_to_log_file("\n")

    @classmethod
    def error(cls, message: str):
        message = "AARDVARK :: ERROR :: " + message

        print(message)
        
        message = message + "\n"
        cls._add_to_log_file(message)
        
        raise Exception(message)

    @classmethod
    def hanging_message(cls, message: str):
        message = "AARDVARK :: " + message

        print(message, end="")

        cls._add_to_log_file(message)

    @classmethod
    def end_of_hanging_message(cls, message: str):
        print(message)

        cls._add_to_log_file(message)
    
    @classmethod
    def _create_log_file(cls):
        with open("output/" + cls.case_name + "/aardvark.log", "w") as file:
            file.write(start_message)

    @classmethod
    def _add_to_log_file(cls, message: str):
        with open("output/" + cls.case_name + "/aardvark.log", "a") as file:
            file.write(message)
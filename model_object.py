class model_object:
    def __init__(self,model_no,Nparam,model_desc,param_desc):
        self.model_no = model_no
        self.Nparam = Nparam
        self.param_desc = param_desc
        self.param_value = []
        for i in range(0,self.Nparam):
            self.param_value.append(0)
    def display_window(self):
        # Here put instructions on how to display the window depending on which model it is.
        # if (self.model_no == 0):
        #    do it one way
        # elif self.model_no == 1):
        #    do it another way
        # Values can be stored in the self.param_value list
        pass


harmonic_oscillator = model_object(0,2,"harmonic oscillator",["mu","k"])
morse_oscillator = model_object(1,3,"morse oscillator",["mu","D","a"])

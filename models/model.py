"""
Some models such as 
A model with high precision
"""

class Model_Regression():

    def __init__(self):

        self.name = 'a_good_model'

    def predict(self,x):
        
        y  = x*2

        return y 

        


if __name__ == '__main__':
    model = Model_Regression()

    print(model.predict(1))
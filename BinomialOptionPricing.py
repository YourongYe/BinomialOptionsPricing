#https://en.wikipedia.org/wiki/Binomial_options_pricing_model
#https://www.investopedia.com/articles/investing/021215/examples-understand-binomial-option-pricing-model.asp
import math

class BinomialOptionPricing:
    def __init__(self, T, rf, n, sigma, stock_price, strike_price):
        self.T = T
        self.rf = rf #risk free rate
        self.n = n
        self.sigma = sigma #volatility
        self.stock_price = stock_price
        self.strike_price = strike_price
        t = T/n
        
        self.up_rate = math.e**(sigma*math.sqrt(T/n))
        print("up rate",self.up_rate)
        self.down_rate = 1/self.up_rate
        print("down rate", self.down_rate)
        
        self.discount_factor = math.e**(-rf*t)
        print("discount factor",self.discount_factor)

        self.up_probability = (math.e**(rf*T/n) - self.down_rate)/(self.up_rate-self.down_rate)
        self.down_probability = 1 - self.up_probability
        print("up probability",self.up_probability)
        print("down probability",self.down_probability)
        
    def __get_intrinsic_value_final_layer(self):
        zero_layer = [1]
        change_rate_final_layer = zero_layer
        for level in range(1,self.n):
            #print("generating level:"+str(level))
            last_elem = change_rate_final_layer[-1]*self.down_rate

            change_rate_final_layer = [i*self.up_rate for i in change_rate_final_layer]

            change_rate_final_layer.append(last_elem)
            #print(change_rate_final_layer)

        self.intrinsic_value_final_layer = [max(self.stock_price*rate-self.strike_price,0) for rate in change_rate_final_layer]

        #print("final layer",self.intrinsic_value_final_layer)
        
    def __get_init_intrinsic_value(self):
        current_intrinsic_values = self.intrinsic_value_final_layer
        while len(current_intrinsic_values)>1:
            earlier_intrinsic_values = []
            #print(current_intrinsic_values)
            for i in range(1,len(current_intrinsic_values)):
                up_intrinsic = current_intrinsic_values[i-1]
                down_intrinsic = current_intrinsic_values[i]
                expected_intrinsic_value = up_intrinsic*self.up_probability + down_intrinsic*self.down_probability
                expected_intrinsic_value *= self.discount_factor
                earlier_intrinsic_values.append(expected_intrinsic_value) 
            current_intrinsic_values = earlier_intrinsic_values

        self.init_intrinsic_value = current_intrinsic_values[0]
        
    def get_price(self):
        self.__get_intrinsic_value_final_layer()
        self.__get_init_intrinsic_value()
        return self.init_intrinsic_value
    
#__init__(self, T, rf, n, sigma, stock_price, strike_price):
model = BinomialOptionPricing(T=1/3, rf=0.02, n=40,sigma=0.1, stock_price=221.2, strike_price=222.5)
print("option price", model.get_price())

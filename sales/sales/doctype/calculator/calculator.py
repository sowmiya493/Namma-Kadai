import frappe
from frappe.model.document import Document
from frappe import _
from sympy import sympify


class calculator(Document):
    def validate(self):
        self.get_answer()

    @frappe.whitelist()
    def get_answer(self):
        formula=self.formula
        formula = self.formula.replace('2ab','2*a*b')  
        #formula = self.formula.replace('ab','a*b')
        formula = formula.replace('a',str(self.field_a))
        formula = formula.replace('b',str(self.field_b))
        self.ans = str(sympify(formula))
        return self.ans


     
        


        
                                             
        # self.cal_addition(self.addition)
        # self.cal_subtraction(self.subtraction)
        # self.cal_multiplication(self.multiplication)
        # self.cal_division(self.division)
        
    # def cal_addition(self,addition):
    #     self.addition = self.field_a + self.field_b
    #     # frappe.db.set_value('calculator', self.name, 'add', self.add)
    # def cal_subtraction(self,subtraction):
    #     self.subtraction = self.field_a - self.field_b
    #     # frappe.db.set_value('calculator', self.name, 'sub', self.sub)
    # def cal_multiplication(self,multiplication):
    #     self.multiplication = self.field_a * self.field_b
    #     # frappe.db.set_value('calculator', self.name, 'mul', self.mul)
    # def cal_division(self,division):
    #     if self.field_b ==0:
    #         frappe.throw("This calculation is not valid")
    #     else:
    #         self.division =self.field_a / self.field_b
        
   

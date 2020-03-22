import pandas as pd
import openpyxl
import matplotlib.pyplot as plt 


def validation (t1,t2,t3,t5,t8,t11):
    
    quality_list = []

    for instance in range(0,3000):
        quality_list.append(t1*fixed_acidity[instance] + t2*volatile_acidity[instance] + t3*citric_acid[instance] +  t5*chlorides[instance] + t8*density[instance] + t11*alcohol[instance])  

    return quality_list

def test(t1,t2,t3,t5,t8,t11):
    
    quality_list_test = []

    for instance in range(3000,4800):
        quality_list_test.append(t1*fixed_acidity[instance] + t2*volatile_acidity[instance] + t3*citric_acid[instance] +  t5*chlorides[instance] + t8*density[instance] + t11*alcohol[instance])  

    return quality_list_test


def calculate_error(prediction): 
    sum = 0
    MSE = 0
    for i in range(0,3000):
        error = pow(quality [i] - prediction [i],2)
        sum = sum + error
    MSE = sum/3000
    #print(MSE)
    return MSE

def validate_model(prediction,a,b): 
    sum_a = 0
    accuracy = 0
    for i in range(a,b):
        if (quality[i] < prediction[i]):
            accuracy_instance = quality[i]/prediction[i]
            sum_a = sum_a + accuracy_instance
        else:
            accuracy_instance = prediction[i]/quality[i]
            sum_a = sum_a + accuracy_instance
    accuracy = sum_a/(b-a)
    print("Validation Accuracy")
    print(accuracy)

def test_model(prediction,a,b): 
    sum_a = 0
    accuracy = 0
    for i in range(a,b):
        if (quality[i] < prediction[i-3000]):
            accuracy_instance = quality[i]/prediction[i-3000]
            sum_a = sum_a + accuracy_instance
        else:
            accuracy_instance = prediction[i-3000]/quality[i]
            sum_a = sum_a + accuracy_instance
    accuracy = sum_a/(b-a)
    print("Test Accuracy")
    print(accuracy)
        

def show_error(x,y):

    plt.plot(x, y) 
    plt.xlabel('iterations') 
    plt.ylabel('error') 
    plt.title('Error evolution') 
    plt.show() 


#Lists obtained of each parameter

archive = pd.read_excel('winequality-white.xlsx')
fixed_acidity = archive['fixed acidity'].tolist()
volatile_acidity = archive['volatile acidity'].tolist()
citric_acid = archive['citric acid'].tolist()
residual_sugar= archive['residual sugar'].tolist()
chlorides = archive['chlorides'].tolist()
free_sulfur_dioxide = archive['free sulfur dioxide'].tolist()
total_sulfur_dioxide = archive['total sulfur dioxide'].tolist()
density= archive['density'].tolist()
pH = archive['pH'].tolist()
sulphates = archive['sulphates'].tolist()
alcohol = archive['alcohol'].tolist()
quality = archive['quality'].tolist()



tetha1 = 0.0001
tetha2 = 0.0001
tetha3 = 0.0001
tetha5 = 0.0001
tetha8 = 0.0001
tetha11 = 0.0001

alpha = 0.0001

sum1 = 0
sum2 = 0
sum3 = 0
sum5 = 0
sum8 = 0
sum11 = 0


items= 3000
epochs_list= []
errors_list = []
epochs = 0
e = 5

a = "S"

while e > 0.65:

    for instance in range(0, items):
        #print(sum1)
        sum1 = sum1 + (tetha1*fixed_acidity[instance] + tetha2*volatile_acidity[instance] + tetha3*citric_acid[instance] + tetha5*chlorides[instance] + tetha8*density[instance] + tetha11*alcohol[instance]- quality[instance])*fixed_acidity[instance]
        sum2 = sum2 + (tetha1*fixed_acidity[instance] + tetha2*volatile_acidity[instance] + tetha3*citric_acid[instance] + tetha5*chlorides[instance] +  tetha8*density[instance] + tetha11*alcohol[instance]- quality[instance])*volatile_acidity[instance]
        sum3 = sum3 + (tetha1*fixed_acidity[instance] + tetha2*volatile_acidity[instance] + tetha3*citric_acid[instance] + tetha5*chlorides[instance] + tetha8*density[instance] + tetha11*alcohol[instance]- quality[instance])*citric_acid[instance]
        sum5 = sum5 + (tetha1*fixed_acidity[instance] + tetha2*volatile_acidity[instance] + tetha3*citric_acid[instance] + tetha5*chlorides[instance] + tetha8*density[instance] + tetha11*alcohol[instance]- quality[instance])*chlorides[instance]
        sum8 = sum8 + (tetha1*fixed_acidity[instance] + tetha2*volatile_acidity[instance] + tetha3*citric_acid[instance] + tetha5*chlorides[instance] + tetha8*density[instance] + tetha11*alcohol[instance]- quality[instance])*density[instance]
        sum11= sum11 +(tetha1*fixed_acidity[instance] + tetha2*volatile_acidity[instance] + tetha3*citric_acid[instance] + tetha5*chlorides[instance] + tetha8*density[instance] + tetha11*alcohol[instance]- quality[instance])*alcohol[instance]
        
    
    
    tetha1 = tetha1 - (alpha/(2*items))*sum1
    tetha2 = tetha2 - (alpha/(2*items))*sum2
    tetha3 = tetha3 - (alpha/(2*items))*sum3
    tetha5 = tetha5 - (alpha/(2*items))*sum5
    tetha8 = tetha8 - (alpha/(2*items))*sum8
    tetha11 = tetha11 - (alpha/(2*items))*sum11

    predictions = validation(tetha1,tetha2, tetha3, tetha5, tetha8, tetha11)
    tests = test(tetha1,tetha2, tetha3, tetha5, tetha8, tetha11)
    e = calculate_error(predictions)

    epochs = epochs + 1

    epochs_list.append(epochs)
    errors_list.append(e)
    
    if e < 0.65:
        validate_model(predictions, 0, 3000)
        test_model(tests,3000, 4800)
        show_error(epochs_list, errors_list)

equation = str(tetha1) + "*x1 +" + str(tetha2) + "*x2 +" + str(tetha3) + "*x3 +" + str(tetha5) + "*x4 +" + str(tetha8) + "*x5 +" + str(tetha11)
print("Resulting equation:")
print(equation)

while (a != "No"):
    
    x1 = input("Enter Fixed acidity value: ")
    x2 = input("Enter volatile acidity value: ")
    x3 = input("Enter citric acidity value: ")
    x4 = input("Enter chlorides value: ")
    x5 = input("Enter density value:")
    x6 = input("Enter alcohol value:")
    predict =  float(x1)*tetha1 + float(x2)*tetha2 + float(x3)*tetha3 + float(x4)*tetha5 + float(x5)*tetha8 + float(x6)*tetha11
    print("The quality is:", predict )
    a = input("Do you want to predict the quality of another wine? Yes/No")






    





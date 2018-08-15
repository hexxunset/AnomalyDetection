import numpy as np
import pandas as pd

if __name__ == '__main__':
    #Change MasterFlag to run desired part of code
    MasterFlag = {
        -1: 'AnomDet1994',
        0: 'Testspace',
        1: 'Make fake dataset',

    }[-1]
    if MasterFlag == 'AnomDet1994':
        print('welcome to AnomDet1994') 
        
        import anomDet as AT


    elif MasterFlag == 'Testspace':
        import dataset as DS
        import functions as F
        yearToFit=[2018]
        yearToCheck=[2016]
        print('Welcome to testspace')
        
        df = pd.DataFrame({'Year': [2016, 2016,2018,2018,2018,2018], 'Month': [1, 3,3,4,5,5], 'Day': [1, 2,1,2,3,2], 'from': ['a', 'b','a','a','c','b'], 'x': [1, 0,4,-5,3,2], 'y': [-2, 1,7,4,2,8]})
        df.set_index(['Year','Month'], inplace=True)
        print(df)

    elif MasterFlag=='Make fake dataset':
        import dataset as DS
        LENGTH=100
        city_strings=['Oslo','Trondheim','Bergen','Stavanger']
        name_strings=['Frode','Arne','Ine','Håkon','August','Karoline','Vilde','Christine','Morten','Aleksander','Harald',
               'Ole','Ida','Mari','Kristin','Alexandra','Bruno','Henning','Henrik','Oskar','Elisabeth','Camilla',
               'Emma','Nora','Sofie','Erlend','Vårin','Rasmus','Sara','Ella','Emilie','Olivia','Ingrid','Emil','Erik',
               'Elias','Vetle','Lukas','Isak','Kyrre','Amund','Julie','Siri','Kevin','Terje','Erling','Patrik',
               'Eivind','Henrik','Cecilie','Mads']
        answerDate_strings=['2018-01','2018-02','2018-03','2018-04','2018-05','2018-06','2018-07']
        ages=np.random.randint(18,26,LENGTH)
        answerDate=np.random.choice(answerDate_strings, LENGTH)
        social_sec=np.random.choice(np.arange(235412,236487), LENGTH, replace=False)
        cities=np.random.choice(city_strings, LENGTH)
        names=np.random.choice(name_strings,LENGTH)
        cityId=np.where(cities=='Oslo',1,2)
        cityId[np.where(cities=='Bergen')]=3
        cityId[np.where(cities == 'Stavanger')] = 4

        print(len(np.arange(1,101)))
        df=pd.DataFrame({'Name':names,'Age':ages,'SocialSecurity':social_sec,'City':cities,'CityID':cityId,'DateAnswered':answerDate})
        DS.writeToFile_excel(df, False, 'newSheet2.xlsx')
        print(df)

from sqlalchemy import *
import sqlalchemy
import pandas

class InsertAggregatesDataToDB():
    
    def execute():
        df = pandas.read_csv("C:/Users/CYTech Student/AppData/Local/Programs/Python/Python39/Scripts/aggregatesInformation.csv", encoding="ISO-8859-1")
        df = df.dropna()
        """ print(df.head())
        print("#####################################################")
        print(df.loc[0,'id'])
        print("#####################################################")
        print(len(df.count()))

        for i in range(0,len(df.count()),2):
            df = df.drop(i)
        df.reset_index()
        print(df.head())
        print("#####################################################")

        counter = -1
        print(len(df.count()))
        for i in range(0,len(df.count())):
            counter +=1
            df.loc[i,'id'] = counter+1
        """
        print(df.head())
        print("#####################################################")
        df = df.drop(columns = "id")
        print(df.head())
        print("#####################################################")
        print (df.isnull().sum())
        df = df.dropna()
        #Droping the empty rows
        """ df = df.reset_index()
        df = df.rename(columns={"index":"id"})
        df['id'] = df.index + 0 """
        print(df.head())
        print(df.tail())
        print("#####################################################")

        engine = create_engine('mysql+mysqldb://root:adrien@127.0.0.1/stockcompaniesdb')
        mysql_connection = engine.connect()
        df.to_sql("compagny_aggregates", mysql_connection, if_exists='append', index=false)

def main():
   insertAggregatesDataToDB = InsertAggregatesDataToDB()
   insertAggregatesDataToDB.execute()

if __name__ == "__main__":
     main()
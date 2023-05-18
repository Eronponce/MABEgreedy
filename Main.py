import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from EGreedyMAB import EgreedyMAB
from Arm import Arm
import statistics
import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


#mostra a tabela com as escolha dos braços
def mostraTabela(arm_quantity):
  coluna1= []
  coluna2 = []
  coluna3 = []
  contador = 0
  for i in arm_quantity:
    contador += 1
    coluna1.append(str(f"braço {contador}°")) 
    coluna2.append(i[0])
    coluna3.append(i[1])
  pd.set_option('display.max_colwidth', None)
  st.write(pd.DataFrame({
    'Braço referente': coluna1,
    'Valor minimo': coluna2,
    'Valor maximo': coluna3,
  }).set_index(['Braço referente']))

def pieChart(choices):
  st.write("### Gráfico de pizza de porcentagem de escolha")
  df = pd.DataFrame(choices).T
  df.columns = [f"Braço {i+1}" for i in range(len(choices))]
  df.index.name = "Execução"

  # Define a custom function to format the value labels
  def format_autopct(value):
      if value == 0:
          return ''
      else:
          return '%1.1f%%' % value
  # Get the non-zero choices and their corresponding labels
  non_zero_choices = [choice for choice in choices if choice != 0]
  non_zero_labels = [label for choice, label in zip(choices, df.columns) if choice != 0]
  # Create the pie chart
  fig1, ax1 = plt.subplots(facecolor='none')
  
  colours1 = ['#26C6DA','#6699fc','#f0a1a2','#fd266f','#7defa1','#ffd16a','#C0CA33','orange','purple']
  
  ax1.pie(non_zero_choices, labels=non_zero_labels, autopct=format_autopct, textprops={'color': 'white'}, colors=colours1,wedgeprops={"edgecolor":"k",'linewidth': 1,'linestyle': '-'})
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

  st.pyplot(fig1)
  return (non_zero_choices )

# mostrar individual por drop   
def frequency(all_rewards):
  st.write("### Frequência de recompensas")
  df = pd.DataFrame(all_rewards).T
  df.columns = [f"Braço {i+1}" for i in range(len(all_rewards))]
  df.index.name = "Execução"
  st.line_chart(df)
  

def averages(rewards,all_rewards,regret,execution_times):
 # transforma em int para encontrar moda media e mediana
  all_rewards = [[int(val) for val in sublist] for sublist in all_rewards]
  mode = []
  for j in range(len(all_rewards)):
      if all_rewards[j]:
          mode.append(statistics.mode(all_rewards[j]))
      else:
          mode.append(None)
  median = [statistics.median(lst) if len(lst) > 0 else None for lst in all_rewards]
  std_devs = []
  for j in range(len(all_rewards)):
      if len(all_rewards[j]) >= 2:
          std_devs.append(statistics.stdev(all_rewards[j]))
      else:
          std_devs.append(None)
  
  st.write("### média, mediana, moda, desvio padrão, vezes de execuções e arrependimento das recompensas ")
  df = pd.DataFrame(rewards).T
  df.columns = [f"Braço {i+1}" for i in range(len(rewards))]
  df.index.name = "Braços"
  df = df.rename(index={0: "Média"})
  df.loc["Mediana"] = median
  df.loc["Moda"] = mode
  df.loc["Desvio Padrão"] = std_devs
  df.loc["Vezes de execução"] = execution_times
  sum_regret =[]
  for values in regret:
    sum_regret.append(sum(values))
  df.loc["Arrependimento"] = sum_regret
  st.dataframe(np.transpose(df))
  return (std_devs,median,mode,execution_times,sum_regret)

connection = create_db_connection("localhost", "root", "root", "teste2")
cursor= connection.cursor()
cursor.execute("SELECT Name FROM Execution")


options =  [row[0] for row in cursor.fetchall()]

options.append("Novo")

st.sidebar.title("Configurar MAB")
instance = st.sidebar.selectbox("Selecione a instância",options)
send = False
replace = False
delete = False
if instance == 'Novo':
  #input para colocar o nomes da nova instancia
  executions_times_value = 1
  epsilon_value = 0.1
  arm_quantity_value = 1
  intance_name = st.sidebar.text_input("Escreva o nome da nova instância")
  author_name = st.sidebar.text_input("Escreva o nome do autor")
  send = st.sidebar.button("Guardar Instância")
else:
  # carrega os parametros na tabela
  cursor.execute("Select * from Execution where Name = %s" ,([instance]))
  parameters = cursor.fetchone()
  st.write(parameters)
  executions_times_value = parameters[4]
  epsilon_value = parameters[5]
  arm_quantity_value = parameters[6]
  delete = st.sidebar.button("Deletar Instância")
  replace = st.sidebar.button("Atualizar instância")



epsilon =  st.sidebar.slider("Epsilon",0.01,1.0,value=epsilon_value)
st.title("MAB em funcionamento")
executions = st.sidebar.number_input("numeros de execuções",value=executions_times_value, min_value= 1, max_value =10000, step=1)
arm_quantity = st.sidebar.number_input("Quantidade de braços",value = arm_quantity_value,min_value= 1,max_value =50 ,step=1)




if st.sidebar.button("Executar mab com braços com ranges aleatórios"):
  st.write(instance)
  Arms = Arm(arm_quantity)  
  fake_rewards = Arm.CreateArms(Arms)   
  mab_class = EgreedyMAB(Arms,arm_quantity,executions,epsilon)
  rewards,choices_arms,all_rewards,regret,execution_times = EgreedyMAB.execute(mab_class)
  mostraTabela(fake_rewards)
  std_devs,median,mode,execution_times,sum_regret = averages(rewards,all_rewards,regret,execution_times)
  frequency(all_rewards)
  times_choosen = pieChart(choices_arms)
  
if send:

  insert_query = """
    INSERT INTO `execution` (`Name`, `Author`, `MabName`, `IterationTimes`, `Epsilon`,`ArmQuantity`)
    VALUES (%s, %s, %s, %s, %s, %s)
  """

  # Define the data to be inserted
  execution_data = (
    intance_name,  
    author_name, 
    "Epsilon Greedy",  
    executions,  
    epsilon,  
    arm_quantity
  )

  cursor.execute(insert_query,execution_data)
  connection.commit()
  st.experimental_rerun()

if replace:
  insert_query = """
  UPDATE `teste2`.`execution`
  SET `IterationTimes` = %s,
  `Epsilon` = %s,
  `ArmQuantity` = %s
  WHERE `Name` = %s;
  """ 

  # Define the data to be inserted
  execution_data = (
    executions,  
    epsilon,  
    arm_quantity,
    instance
  )

  cursor.execute(insert_query,execution_data)
  connection.commit()
  st.experimental_rerun()

if delete:
  insert_query = """DELETE FROM  `teste2`.`execution`
  WHERE `Name` = %s;
  """
  # Define the data to be inserted
  execution_data = [instance]
  cursor.execute(insert_query,execution_data)
  connection.commit()
  st.experimental_rerun()
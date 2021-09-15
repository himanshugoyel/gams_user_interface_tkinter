from gams import *
from tkinter import *

def get_model_text():
    return '''
  Sets
       i   Generators
       j   Loads

  Parameters
       a(i)   capacity of Generator i in cases
       b(j)   demand at load j in cases
       d(i)   Cost of generation

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load i j a b d
$gdxin

  Scalar Pbase 'Base MW rating' / 100/

  Variables
       x(i)    Generators
       z       Total Gen cost ;

  Positive Variable x ;

  Equations
       cost        define objective function
       supply(i)   observe supply limit at plant i
       demand      satisfy demand at market j ;

  cost..      z =e= sum(i, d(i)*x(i)*Pbase);

  supply(i).. x(i) =l= a(i);

  demand.. sum(i, x(i)) - sum(j, b(j)) =e= 0;

  Model transport /all/ ;

  Solve transport using lp minimizing z ; '''

def update():
	global nbus
	nbus=n_bus
	print(nbus)

def destroy():
	for i in range(0, int(nbus)):
	  	buses[i].destroy()
	  	Pgen[i].destroy()
	  	Pload[i].destroy()
	  	Pcost[i].destroy()
	  	Gen_name[i].destroy()
	  	Load_name[i].destroy()
	enter2.destroy()
	calculate.destroy()
	for i in range(0, datlen):
		labl[i].destroy()

root = Tk()
col=1
n_bus=-1
def value1():
  global n_bus
  update()
  print(n_bus)
  print(nbus)
  if (int(nbus) > 0):
  	destroy()

  n_bus=n.get()
  bus = Label(root, text = n_bus)
  bus.grid(row=0, column=3)
  label_bus_no = Label(root, text = "Bus No.")
  label_bus_no.grid(row=col+1, column=0)
  label_bus_no = Label(root, text = "|Generation Pg|")
  label_bus_no.grid(row=col+1, column=1)
  label_bus_no = Label(root, text = "|Load Pl|")
  label_bus_no.grid(row=col+1, column=2)
  label_bus_no = Label(root, text = "|Generation cost|")
  label_bus_no.grid(row=col+1, column=3)
  label_bus_no = Label(root, text = "|Generator Name|")
  label_bus_no.grid(row=col+1, column=4)
  label_bus_no = Label(root, text = "|Load Name|")
  label_bus_no.grid(row=col+1, column=5)

  global Pgen, Pload, Pcost, Gen_name, Load_name, buses, enter2
  buses = []
  Pgen = []
  Pload = []
  Pcost = []
  Gen_name=[]
  Load_name = []
  for i in range (0, int(n_bus)):
    buses.append("bus"+ str(i+1))
    Pgen.append("Pgen"+ str(i+1))
    Pload.append("Pload"+ str(i+1))
    Pcost.append("Pcost"+ str(i+1))
    Gen_name.append("Gen"+ str(i+1))
    Load_name.append("Load"+ str(i+1))

  for i in range(0,int(n_bus)):
    buses[i] = Label(root, text = i+1)
    buses[i].grid(row=col+2+i, column=0)
    Pgen[i] = Entry(root, width=5)
    Pgen[i].grid(row=col+2+i, column=1)
    if i == 0:
      Pgen[0].insert(0, "6")
    if i == 1:
      Pgen[1].insert(0, "2")

    Pload[i] = Entry(root, width=5)
    Pload[i].grid(row=col+2+i, column=2)
    if i == 0:
      Pload[0].insert(0, "1.8")
    if i == 1:
      Pload[1].insert(0, "1.5")
    Pcost[i] = Entry(root, width=5)
    Pcost[i].grid(row=col+2+i, column=3)
    if i == 0:
      Pcost[0].insert(0, "10")
    if i == 1:
      Pcost[1].insert(0, "20")
    g=Gen_name[i]
    Gen_name[i] = Entry(root, width=5)
    Gen_name[i].grid(row=col+2+i, column=4)
    Gen_name[i].insert(0, g)
    L=Load_name[i]
    Load_name[i] = Entry(root, width=5)
    Load_name[i].grid(row=col+2+i, column=5)
    Load_name[i].insert(0, L)

    global col1
    col1 = col+2+i
 
  enter2 = Button(root, text = "Press After adding the data", command=lambda: get_data(n_bus))
  enter2.grid(row=col1+1, column=2)
 
def get_data(n_bus):
  Pgen_data = []
  Pload_data = []
  Pcost_data = []
  Pgen_name = []
  Pload_name = []
  P=Pgen[1].get()
  for i in range(0,int(n_bus)):
    k=Pgen[i].get()
    Pgen_data.append(k)
  for i in range(0,int(n_bus)):
    k=Pload[i].get()
    Pload_data.append(k)
  for i in range(0,int(n_bus)):
    k=Pcost[i].get()
    Pcost_data.append(k)
  for i in range(0,int(n_bus)):
    k=Gen_name[i].get()
    Pgen_name.append(k)
  for i in range(0,int(n_bus)):
    k=Load_name[i].get()
    Pload_name.append(k)
  
  Pgen_data = list(map(float, Pgen_data))
  Pload_data = list(map(float, Pload_data))
  Pcost_data = list(map(float, Pcost_data))
    
  global plants, markets, capacity, demand, Gen_cost
  plants   = []
  markets  = []
  capacity = {} 
  demand   = {}
  Gen_cost = {}

  plants = Pgen_name
  markets = Pload_name
  capacity = {Pgen_name[i]: Pgen_data[i] for i in range(0, int(n_bus))}
  Gen_cost = {Pgen_name[i]: Pcost_data[i] for i in range(0, int(n_bus))}
  demand = {Pload_name[i]: Pload_data[i] for i in range(0, int(n_bus))}

  global calculate
  calculate = Button(root, text ="Calculate", command = gams_code)
  calculate.grid(row=col1+2, column=2)
     
def gams_code():

  ws = GamsWorkspace(working_directory=".")
  db = ws.add_database()

  i = db.add_set("i", 1, "Generators")
  for p in plants:
      i.add_record(p)
    
  j = db.add_set("j", 1, "Loads")
  for m in markets:
      j.add_record(m)

  a = db.add_parameter_dc("a", [i], "capacity of plant i in cases")
  for p in plants:
      a.add_record(p).value = capacity[p]

  b = db.add_parameter_dc("b", [j], "demand at market j in cases")
  for m in markets:
      b.add_record(m).value = demand[m]

  d = db.add_parameter_dc("d", [i], "Cost in Rupees/MW")
  for p in plants:
      d.add_record(p).value = Gen_cost[p]
     
  t4 = ws.add_job_from_string(get_model_text())
  opt = ws.add_options()
    
  opt.defines["gdxincname"] = db.name
  opt.all_model_types = "xpress"
  dat = []
  t4.run(opt, databases = db)
  for rec in t4.out_db["x"]:
    dat.append(str(rec))
    print(str(rec))

  it = 0
  global labl, datlen
  labl=[]
  datlen = len(dat)
  print(datlen)
  for i in range(0,datlen):
    labl.append("bus"+ str(i+1))
  print(labl)
  for i in range(0,datlen):
    it=it+1
    labl[int(i)] = Label(root, text = dat[i])
    labl[int(i)].grid(row=it+col1+3, column=2)
    global col2
    col2 = it+col1+3

label2 = Label(root, text= "Number of buses: ")
n = Entry(root, width=5)
label2.grid(row=0, column=0)
n.grid(row=0, column=1)
n.insert(0, "2")

enter1 = Button(root, text = "Enter", command= lambda: value1())
enter1.grid(row=0, column=2)

root.mainloop()
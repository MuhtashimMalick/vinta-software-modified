import pyodbc
 
conn = pyodbc.connect(
    r"DRIVER={SQL Server Native Client 10.0};"
    r"SERVER=.\SQLEXPRESSRICG;"
    r"DATABASE=MYOBPremierMirrorDB_test;"
    r"UID=sa;"
    r"PWD=pwd$123;"
)
print("connected")
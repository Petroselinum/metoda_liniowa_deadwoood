from sqlmodel import create_engine
import urllib

def connection(driver='{ODBC Driver 18 for SQL Server}', 
               server='BudniakP', 
               database='WISL_baza_zbiorcza_IV_cykl', 
               trusted_connection='yes'):
    
    '''Funkcja zwraca obiekt silnika SQLAlchemy do połączenia z lokalną bazą danych WISL'''

    if any (param == '' for param in [driver, server, database, trusted_connection]):
        raise ValueError("Wszystkie parametry muszą być podane i nie mogą być puste.")

    params = urllib.parse.quote_plus(f'''
                                     DRIVER={driver};
                                     SERVER={server};
                                     DATABASE={database};
                                     Trusted_Connection={trusted_connection};
                                     TrustServerCertificate=yes;
                                     Encrypt=no;
                                     LoginTimeout=10;
                                     QueryTimeout=10;''')
    
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params,
                           pool_pre_ping=True,
                            pool_timeout=10,
                            connect_args={"timeout": 10})
    return engine


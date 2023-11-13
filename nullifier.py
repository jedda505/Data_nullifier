import pandas as pd
import sqlalchemy as sa
from sqlalchemy import exc
from tkinter import messagebox
from possible_datacols import data_cols

class Querying:
    # Class contains querying functionality
    def __init__(self, URN=None):
        # URN(s)
        if URN != None:
            self.URN, self.URN_list = handle_multiple_entries(URN)
        # Initialise SQL_Runner class
        self.SQLR = SQL_Runner()
        # Get query data tables from data schema
        self.table_names = self.SQLR.query(Config.table_names_SQL)

    def show_tables(self):
        # View data tables that contain URN(s)
        tables_to_null = []
        for tblname in self.table_names['name']:
            for i in Config.URN_cols:
                try:
                    results = self.SQLR.query(Config.by_URN_SQL.format(tblname, i, self.URN))
                    if len(results) == 0:
                        #print(tblname, "\n", "0 ROWS\n")
                        break
                    if results.columns.str.upper().isin(data_cols).any():
                        tables_to_null.append(tblname)
                        print(tblname, "\n", results, "\n"*3)
                    else:
                        print(tblname, "\n", ", ".join(results.columns), "\n NO data COLUMNS DETECTED", "\n"*3)

                        
                except exc.SQLAlchemyError:
                    if i in Config.URN_cols[:-1]:
                        continue
                    else:
                        #print(tblname, "No URN column in this dataset...\n\n")
                        pass              
        print(f"\n"*2, f"Tables to nullyify: \n {tables_to_null}", "\n"*2, "No of tables:" ,len(tables_to_null), "\n"*2, "=== END ===", "\n"*3)
                

    def run_nullifier(self):
        # nullify data tables by nullifying data columns where the inputted URN(s) exists. 
        with self.SQLR.connection as con:
            for tblname in self.table_names['name']:
                
                col_names = self.SQLR.query(Config.col_name_SQL.format(tblname, data_cols, self.URN))

                data_col_names = col_names['COLUMN_NAME'][col_names['COLUMN_NAME'].isin(data_cols)]

                print("\n", tblname, "\n=============="*2)

                for data_col in data_col_names:
                    print(data_col)
                    for icol in Config.URN_cols:
                        try:
                            # print(Config.null_SQL.format(tblname, data_col, icol, self.URN))
                            con.execute(sa.text(Config.null_SQL.format(tblname, data_col, icol, self.URN)))
                        except exc.SQLAlchemyError:
                            continue

            # Ask if you want to commit changes
            commit_changes = messagebox.askyesno(title="Commit Changes", message="Do you wish to commit to this nullification?")
            
            if commit_changes:
                con.commit()
                print("=== nullification has been completed. ===", "\n"*3)
                

        
    def logit(self, FRM, log_gui):
        FRMs = [x.strip() for x in FRM.split(",")]
        with self.SQLR.connection as con:
            for i in range(len(FRMs)):
                con.execute(sa.text(Config.logging_SQL.format(self.URN_list[i], FRMs[i])))
                con.commit()
        print("nullification(s) logged at [Schema].[Table].\nDONE.")
        log_gui.destroy()
        

class SQL_Runner:

    def __init__(self):
        # Initialise SQL Server engine
        engine = sa.create_engine("mssql+pyodbc://*************/**************")
        self.connection = engine.connect()


    def query(self, SQL):
        # This queries the database, taking SQL string as arg 1 and arg 2.

        df = pd.read_sql(sa.text(SQL), self.connection)

        return df

class Config:
    # Config class acts as a container for SQL blocks, column names and other metadata
    col_name_SQL = r'''SELECT UPPER(COLUMN_NAME) AS COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = N'{}'
    '''

    table_names_SQL = r'''

            SELECT
                    t.name
            FROM
                    sys.tables t
            WHERE
                    t.schema_id = 85

    '''

    by_URN_SQL = '''

    SELECT
        *
    FROM
        Schema.{}
    WHERE
        [{}] IN ('{}')

    '''

    null_SQL = r'''
        UPDATE [Schema].{}
        SET [{}] = NULL
        WHERE [{}] IN ('{}')
    ''' #tblname, data_col, icol, self.URN


    logging_SQL = r'''
    INSERT INTO [Schema].[Table] ([URN2], [Jira_Ticket], [Insert_Date])
    VALUES ('{}','{}',GETDATE())
    '''


    URN_cols = ['URN2',
     'URN']
    


def handle_multiple_entries(entry_string):
    # A function to handle multiple entries. Delimits the input string by commas.
    entries_list = [x.strip() for x in entry_string.split(',')]
    multiple_entries = "','".join(entries_list)
    print("\n", multiple_entries)
    return multiple_entries, entries_list

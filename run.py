from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from database.tables import Base

from generators.generate_static_data import generate_random_users, generate_random_transaction

from PyQt6.QtWidgets import QMainWindow, QApplication
from ui.db_helper_ui import Ui_db_helper

import sys


class MainWindow(QMainWindow, Ui_db_helper):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setConnection_pushButton.clicked.connect(self.set_connection)

        self.createTables_pushButton.clicked.connect(self.create_db)
        self.dropDatabase_pushButton.clicked.connect(self.drop_db)

        self.users_createEntries_pushButton.clicked.connect(self.create_entries_users)
        self.transactions_createEntries_pushButton.clicked.connect(self.create_entries_transactions)


    def set_connection(self):
        login = self.login_lineEdit.text()
        password = self.password_lineEdit.text()
        link = self.link_lineEdit.text()
        name = self.dbName_lineEdit.text()
        
        url = f"postgresql+psycopg2://{login}:{password}@{link}/{name}"

        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def drop_db(self):
        Base.metadata.drop_all(self.engine)

    def create_entries_users(self):
        entry_amount = int(self.users_entryAmount_lineEdit.text())
        upper_limit = int(self.users_upperBalanceLimit_lineEdit.text())
        lower_limit = int(self.users_lowerBalanceLimit_lineEdit.text())

        generate_random_users(entry_amount, lower_limit, upper_limit, session=self.Session)

    def create_entries_transactions(self):
        entry_amount = int(self.transactions_entryAmount_lineEdit.text())
        upper_limit = int(self.transactions_upperTransactedLimit_lineEdit.text())
        lower_limit = int(self.transactions_lowerTransactedLimit_lineEdit.text())

        generate_random_transaction(entry_amount, lower_limit, upper_limit, session=self.Session)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

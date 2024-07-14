import sys
from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.tables import Base
from database.ui_orm_query import (
    save_to_json_together,
    save_to_yaml_together,
    save_to_json_separately,
    save_to_yaml_separately,
    all_transactions,
    all_users,
    counts_of_users,
    counts_of_transactions,
    show_user_with_transactions,
    show_details_of_transaction
)
from generators.ui_generate_static_data import (
    generate_random_users,
    generate_random_transaction
)
from ui.db_helper_ui import Ui_db_helper


class MainWindow(QMainWindow, Ui_db_helper):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.engine = None
        self.Session = None

        self.login_lineEdit.setFocus()

        self.setConnection_pushButton.clicked.connect(self.set_connection)

        self.createTables_pushButton.clicked.connect(self.create_db)
        self.dropDatabase_pushButton.clicked.connect(self.drop_db)

        self.oneFile_Json_pushButton.clicked.connect(self.save_one_json)
        self.SeparatedFiles_Json_pushButton.clicked.connect(self.save_separated_json)
        self.oneFile_Yaml_pushButton.clicked.connect(self.save_one_yaml)
        self.SeparatedFiles_Yaml_pushButton.clicked.connect(self.save_separated_yaml)

        self.users_createEntries_pushButton.clicked.connect(self.create_entries_users)
        self.transactions_createEntries_pushButton.clicked.connect(self.create_entries_transactions)

        self.showAll_users_pushButton.clicked.connect(self.show_all_users)
        self.showAll_transactions_pushButton.clicked.connect(self.show_all_transactions)
        self.ShowEverything_pushButton.clicked.connect(self.show_one_user_with_transactions)
        self.ShowDetailesOfTransaction_pushButton.clicked.connect(self.show_detailed_transaction)
        self.CountOfEverything_pushButton.clicked.connect(self.count_of_everything)

        self.log("App start SUCCESS")

    def set_connection(self):
        login = self.login_lineEdit.text() if self.login_lineEdit.text() != '' else 'postgres'
        password = self.password_lineEdit.text()
        link = self.link_lineEdit.text() if self.link_lineEdit.text() != '' else 'localhost'
        name = self.dbName_lineEdit.text()

        url = f"postgresql+psycopg2://{login}:{password}@{link}/{name}"

        try:
            self.engine = create_engine(url)
            connection = self.engine.connect()
            connection.close()
            self.Session = sessionmaker(bind=self.engine)
            self.stackedWidget.setCurrentIndex(1)
            self.log("Successful connection")
        except Exception as e:
            self.log(f"Lost connection\n Smth went wrong: \n{e}")

    def create_db(self):
        try:
            Base.metadata.create_all(self.engine)
            self.log("Successfully created new db")
        except Exception as e:
            self.log(f"Smth went wrong during creating db: \n{e}")

    def drop_db(self):
        Base.metadata.drop_all(self.engine)
        try:
            Base.metadata.create_all(self.engine)
            self.log("Successfully dropped db")
        except Exception as e:
            self.log(f"Smth went wrong during dropping db: \n{e}")

    def show_all_users(self):
        try:
            all_data = all_users(Session=self.Session)
            self.listWidget.clear()
            for data in all_data:
                self.listWidget.addItem(data)
        except Exception as e:
            self.log(e)

    def show_all_transactions(self):
        try:
            self.listWidget.clear()
            all_data = all_transactions(Session=self.Session)
            for data in all_data:
                self.listWidget.addItem(data)
        except Exception as e:
            self.log(e)

    @staticmethod
    def _is_number(s):
        try:
            float(s)
            return True
        except Exception:
            return False

    def show_one_user_with_transactions(self):
        user_id = int(
            self.user_id_toShowing_lineEdit.text()) if self._is_number(
            self.user_id_toShowing_lineEdit.text()) else ''
        user_ipn = int(
            self.user_ipn_toShowing_lineEdit.text()) if self._is_number(
            self.user_ipn_toShowing_lineEdit.text()) else ''
        try:
            self.listWidget.clear()
            all_data = show_user_with_transactions(Session=self.Session, user_id=user_id, user_ipn=user_ipn)
            for data in all_data:
                self.listWidget.addItem(data)
        except Exception as e:
            self.log(e)

    def show_detailed_transaction(self):
        try:
            transaction_id = int(
                self.transcation_id_toShowing_lineEdit.text()) if self._is_number(
                self.transcation_id_toShowing_lineEdit.text()) else ''
            self.listWidget.clear()
            all_data = show_details_of_transaction(Session=self.Session, transaction_id=transaction_id)
            for data in all_data:
                self.listWidget.addItem(data)
        except Exception as e:
            self.log(e)

    def count_of_everything(self):
        try:
            self.listWidget.clear()
            counts_users = counts_of_users(Session=self.Session)
            counts_transactions = counts_of_transactions(Session=self.Session)
            data = f'There are {counts_users} USERS'
            self.listWidget.addItem(data)
            data = f'There are {counts_transactions} TRANSACTIONS'
            self.listWidget.addItem(data)
        except Exception as e:
            self.log(e)

    def create_entries_users(self):
        try:
            entry_amount = int(self.users_entryAmount_lineEdit.text()) if self._is_number(
                self.users_entryAmount_lineEdit.text()) else 0
            lower_limit = int(self.users_lowerBalanceLimit_lineEdit.text()) if self._is_number(
                self.users_lowerBalanceLimit_lineEdit.text()) else 1_000
            upper_limit = int(self.users_upperBalanceLimit_lineEdit.text()) if self._is_number(
                self.users_upperBalanceLimit_lineEdit.text()) else 50_000
            if entry_amount != 0:
                generate_random_users(self.Session, entry_amount, lower_limit, upper_limit, )
                self.log('Generation of users DONE')
            else:
                self.log('Sorry, you need to write how much to create')
        except Exception as e:
            self.log(f'Maybe you missed some arguments: \n{e}')

    def create_entries_transactions(self):
        try:
            dt_start = self.transactions_timeWindowStart_dateTimeEdit.dateTime().toString(self.transactions_timeWindowStart_dateTimeEdit.displayFormat())
            dt_start_formatted = datetime.strptime(dt_start, '%d.%m.%Y, %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%f')
            dt_end = self.transactions_timeWindowEnd_dateTimeEdit.dateTime().toString(self.transactions_timeWindowEnd_dateTimeEdit.displayFormat())
            dt_end_formatted = datetime.strptime(dt_end, '%d.%m.%Y, %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%f') 

            entry_amount = int(self.transactions_entryAmount_lineEdit.text()) if self._is_number(
                self.transactions_entryAmount_lineEdit.text()) else 0
            user_id = int(self.user_id_toGeneration_lineEdit.text()) if self._is_number(
                self.user_id_toGeneration_lineEdit.text()) else ''
            user_ipn = int(self.user_ipn_toGeneration_lineEdit.text()) if self._is_number(
                self.user_ipn_toGeneration_lineEdit.text()) else ''
            if entry_amount == 0:
                self.log('Sorry, you need to write how much to create')
            elif user_ipn != '':
                generate_random_transaction(self.Session, entry_amount, user_ipn=int(user_ipn), from_date=dt_start_formatted, to_date=dt_end_formatted)
                self.log('Generation of transaction DONE')
            elif user_id != '':
                generate_random_transaction(self.Session, entry_amount, user=int(user_id), from_date=dt_start_formatted, to_date=dt_end_formatted)
                self.log('Generation of transaction DONE')
            else:
                generate_random_transaction(self.Session, entry_amount, from_date=dt_start_formatted, to_date=dt_end_formatted)
                self.log('Generation of transaction DONE')
        except Exception as e:
            self.log(f'Smth went wrong: \n{e}')

    def save_one_json(self):
        save_to_json_together(Session=self.Session)

    def save_separated_json(self):
        save_to_json_separately(Session=self.Session)

    def save_one_yaml(self):
        save_to_yaml_together(Session=self.Session)

    def save_separated_yaml(self):
        save_to_yaml_separately(Session=self.Session)

    def log(self, text):
        current_time = datetime.now().strftime('%d.%m.%Y, %H:%M:%S')
        self.logs_textBrowser.append(f"[{current_time}] {text}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

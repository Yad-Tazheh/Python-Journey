# handles the main flow of the program
import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv" # it's a class var
    COLUMNS = ["Date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls): # have access to the class itself but not the instances
        try:
             pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            # DataFrame is a pandas Obj, allows us to access diff rows and columns within a csv file
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        # open the csv file, take a dictionary and write it into a csv file
        with open(cls.CSV_FILE, "a", newline="") as csvfile:   # this is a context manager
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("entry added successfully")
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # df["Date"] is accessing all the values in the date column
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT) # changing the vals in date column and format it
        start_date = datetime.strptime(start_date, CSV.FORMAT) # start_date is a string so needed to be formated
        end_date = datetime.strptime(end_date, CSV.FORMAT) # same for this
        # check if the data in the current row in the column date has the relative properties <=/ >=
        # mask is sth that we apply to the diff rows in a dataframe to see if we should select that row or not
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date) # & is bitwise
        filtered_df = df.loc[mask] # filtered df only contains the rows where above statement is True
        if filtered_df.empty:
            print('No transactions found in the given date range')
        else:
            print(f'Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:')
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            # we put column name as key and the function that you wanna apply to each element inside the column if -
            # - we wanna format it differently, lamda is "one line anonymous function"
            total_income = filtered_df[filtered_df["category"] == "Income"]['amount'].sum()
            # kinda similar to mask , we are getting all the rows where the category is income, get all the values in the amount column
            total_expense = filtered_df[filtered_df["category"] == "Expense"]['amount'].sum()
            print("\nSummary:")
            print(f'Total Income: ${total_income:.2f}')
            print(f'Total Expense: ${total_expense:.2f}')
            print(f'Net Savings: ${(total_income - total_expense):.2f}')
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    # Make a copy so the original DataFrame isn't modified
    df = df.copy()

    # Set Date as the index
    df.set_index("Date", inplace=True)

    # Create a complete daily date range
    all_dates = pd.date_range(df.index.min(), df.index.max(), freq="D")

    # Daily income
    income_df = (
        df[df["category"] == "Income"]["amount"]
        .resample("D")
        .sum()
        .reindex(all_dates, fill_value=0)
    )

    # Daily expenses
    expense_df = (
        df[df["category"] == "Expense"]["amount"]
        .resample("D")
        .sum()
        .reindex(all_dates, fill_value=0)
    )

    plt.figure(figsize=(12, 8))
    plt.plot(income_df.index, income_df, label="Income", color="green")
    plt.plot(expense_df.index, expense_df, label="Expense", color="red")

    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense")
    plt.legend()
    plt.grid(True)
    plt.show()



def main():
    while True:
        print('\n1. Add new transaction')
        print('2. Get transactions')
        print('3. Exit')
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date("enter the start date(dd-mm-yyyy): ")
            end_date = get_date("enter the end date(dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input('Do you want to see a plot? (y/n): ').lower() == 'y':
                plot_transactions(df)
        elif choice == '3':
            print('Exiting...')
            break
        else:
            print('Invalid choice, please enter again')

# protecting the code so if we import it somewhere we dont run main() , only runs when we run the code from itself
if __name__ == '__main__':
    main()




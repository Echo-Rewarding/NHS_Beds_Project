import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from google.colab import files
import os
import shutil


def modify_column(df):
    """
    Modifies the DataFrame by subtracting the values of the third column 
    from the second column, for the purposes of generating a stacked chart.
    """
    col2_idx = 1  # Index of the second column (Column2)
    col3_idx = 2  # Index of the third column (Column3)

    # Subtract the values of Column3 from Column2
    df.iloc[:, col3_idx] -= df.iloc[:, col2_idx]

    return df

def bar_chart(df, title, pdf_pages):
    """
    Generates a stacked bar chart based on the given DataFrame and 
    saves it to a PDF file.
    """
    df = pd.DataFrame(df)

    # Set the 'Date' column as the index using column index 0
    df = df.set_index(df.columns[0])

    # Create a stacked bar chart
    df.plot(kind='bar', stacked=True, figsize=(20, 10.5))

    # Set the x-axis label with increased font size
    plt.xlabel('Year and Quarter', fontsize=12)

    # Set the y-axis label with increased font size
    plt.ylabel('Number of Beds', fontsize=12)

    # Set the chart title with increased font size
    plt.title('Total Number of ' + title + ' NHS Beds in England', fontsize=14)

    # Set the x-axis tick label font size
    plt.xticks(fontsize=10)

    # Set the y-axis tick label font size
    plt.yticks(fontsize=10)

    pdf_pages.savefig()

def column_title(df):
    """
    Sets the column titles of the DataFrame.
    """
    df.columns = ['Y+Q', 'Occupied', 'Unoccupied']
    return df

def download_data(url, file_path):
    """
    Downloads data from the given URL and saves it to the specified file path.
    """
    response = requests.get(url)

    with open(file_path, 'wb') as file:
        file.write(response.content)

def process_data(file_path):
    """
    Processes the data from the Excel file and generates bar charts.
    """
    df = pd.read_excel(file_path)
    
    # Remove parts of .xls file not part of data table
    df = df.iloc[13:, 1:] # header
    df = df.dropna(axis=0, how='all')  # empty rows
    df = df.drop(df.index[-1])  # footer
    
    # Collate the Year and Quarter Entries
    df['Combined'] = df.apply(lambda row: str(row[0]) + ' ' + str(row[1]), axis=1)

    # Create Sub Types of NHS Beds
    Total = df.iloc[:, [-1, 9, 3]]
    Gen_acute = df.iloc[:, [-1, 10, 4]]
    LD = df.iloc[:, [-1, 11, 5]]
    Maternity = df.iloc[:, [-1, 12, 6]]
    Mental_Illness = df.iloc[:, [-1, 13, 7]]

    # Label Columns
    Total = column_title(Total)
    Gen_acute = column_title(Gen_acute)
    LD = column_title(LD)
    Maternity = column_title(Maternity)
    Mental_Illness = column_title(Mental_Illness)

    # Modify the columns for a stacked bar chart 
    # Accounts for occupied beds being part of the total number
    Total = modify_column(Total)
    Gen_acute = modify_column(Gen_acute)
    LD = modify_column(LD)
    Maternity = modify_column(Maternity)
    Mental_Illness = modify_column(Mental_Illness)

    # Return the five data frames
    return Total, Gen_acute, LD, Maternity, Mental_Illness

def output_data(Total, Gen_acute, LD, Maternity, Mental_Illness):
    """
    Process the data frames and perform any necessary output operations.
    """

    # Create a PDF file
    pdf_filename = 'plots.pdf'
    pdf_pages = PdfPages(pdf_filename)

    bar_chart(Total, "all", pdf_pages)
    bar_chart(Gen_acute, "General & Acute", pdf_pages)
    bar_chart(LD, "Learning Disabilities", pdf_pages)
    bar_chart(Maternity, "Maternity", pdf_pages)
    bar_chart(Mental_Illness, "Mental Illness", pdf_pages)

    # Close the PDF file
    pdf_pages.close()

    # Get the full path of the PDF file
    full_path = os.path.abspath(pdf_filename)

    return full_path

def data_pipeline(url, file_path):
    """
    Runs the data pipeline to download the data, process it, 
    and generate the charts.
    """
    # Download data
    download_data(url, file_path)

    # Process data and get the five data frames
    Total, Gen_acute, LD, Maternity, Mental_Illness = process_data(file_path)

    # Pass data frames to generate the charts and PDF
    pdf_filename = output_data(Total, Gen_acute, LD, Maternity, Mental_Illness)

    return pdf_filename

def download_pdf(pdf_filename):
    # Specify a different directory and filename for a copied PDF file
    copied_filename = '/content/NHS_Beds_Output.pdf'

    # Copy the PDF file to the specified directory with a different filename
    shutil.copy(pdf_filename, copied_filename)

    # Download the copied PDF file
    files.download(copied_filename)

# Set the URL and file path
url = 'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/05/Beds-Timeseries-2010-11-onwards-Q4-2022-23-ADJ-for-missings-YQWSA.xls'
file_path = 'data.xls'

# Execute the data pipeline
pdf_filename = data_pipeline(url, file_path)

# Download a PDF file of the output
download_pdf(pdf_filename)


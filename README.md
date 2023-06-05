# NHS Beds Data Pipeline Documentation

Owner: C Grant

Created: 04/06/2023

## Purpose: 
A data pipeline that takes publically availible data on NHS Beds in England, in particular number of beds and degree to which they are occupied, and produces a series of stacked bar charts visualising the information.

This data pipeline fetches data from a remote URL from NHS England, preprocesses it, generates plots, and saves the plots in a PDF file. The pipeline is designed to run in a Google Colab environment.

## Requirements
The code is writtent for the Google Colab environment.

Ensure that the required libraries (pandas, requests, matplotlib, os, shutil) are installed in your Colab environment.
  
## Pipeline Steps

### 1. Download the Data
The download_data(url, file_path) function downloads data from a given URL and saves it to the specified file path. It uses the requests library to make HTTP requests and save the response content to a file.

### 2. Process the Data
The process_data(file_path) function processes the downloaded data from the Excel file. It performs data cleaning and transformation operations, including removing empty rows, selecting specific columns, modifying column values, and creating new columns. 

### 3. Generate the Plots
The processed data is then used to generate bar charts for different categories. The bar_chart(df, title, pdf_pages) function generates a stacked bar chart based on a given DataFrame. It uses the matplotlib library to create the chart, set labels and titles, and save it to a PDF file using the PdfPages class.

## Input preprocessing: 
The URL for the data is taken from:

https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/05/Beds-Timeseries-2010-11-onwards-Q4-2022-23-ADJ-for-missings-YQWSA.xls

## Model training: 
Nil utilised in this instance.

## Model evaluation: 
Nil utilised in this instance.







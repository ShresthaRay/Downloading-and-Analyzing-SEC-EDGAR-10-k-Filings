# Downloading-and-Analyzing-SEC-EDGAR-10-k-Filings

### <ins>Assignment:</ins> 

Download and analyze Sec-edgar 10-k filings of public firms. Construct and deploy simple app for the same.


### <ins>Introduction:</ins> 

Analyzing SEC-EDGAR 10-K filings is crucial for understanding a company's financial health and performance. The analysis also holds immense significance for various stakeholders, as follows:
  1. _Investors:_ Investors rely on these filings to make informed decisions about buying, holding, or selling securities. 10-K   filings provide comprehensive insights into a company's financial performance, risks, and future outlook.
  2. _Analysts:_ Financial analysts use SEC-EDGAR filings to conduct thorough research on companies, assessing their strengths,  weaknesses, and competitive positioning. This analysis helps in generating investment recommendations and forecasts.
  3. _Regulators and Authorities:_ Regulatory bodies and government agencies use SEC-EDGAR filings to ensure compliance with     financial reporting standards and regulations. These filings aid in monitoring market integrity and safeguarding investor interests.
  4. _Academic and Research Purposes:_ Researchers and academics leverage SEC-EDGAR filings for studying various aspects of       corporate finance, governance, and market dynamics. These filings provide valuable data for empirical research and case studies.

The assignment is done using Python. Python is chosen as the preferred tech stack for several reasons:
1. _Ease of Use:_ Python's simple and readable syntax makes it accessible for both beginners and experienced developers. It allows for rapid development and prototyping, which is advantageous in research and analysis projects.
2. _Rich Ecosystem:_ Python boasts a vast ecosystem of libraries and tools tailored for data analysis, web scraping, and finance. Libraries like BeautifulSoup, pandas, and requests simplify tasks such as downloading filings, parsing HTML content, and analyzing financial data.
3. _Web Scraping Capabilities:_ Python excels in web scraping tasks, making it well-suited for extracting data from SEC-EDGAR's website. With libraries like BeautifulSoup and Scrapy, developers can efficiently navigate web pages, extract relevant information, and automate data collection processes.
4. _Data Analysis and Visualization:_ Python's data analysis libraries, such as pandas and NumPy, facilitate the manipulation and analysis of financial data extracted from SEC-EDGAR filings. Additionally, libraries like Matplotlib and Seaborn enable visualization of key insights, aiding in the interpretation and presentation of results.

Overall, Python's versatility, robustness, and extensive ecosystem make it an ideal choice for analyzing SEC-EDGAR filings, offering a balance of power, simplicity, and efficiency.


### <ins>Task 1.1</ins>:

The first part of the task was to download some SEC 10-K filings of public firms, which would be used in the next tasks. The task was to write a script or program to do this automatically.
The python script written downloads 10-K filings for a list of specified companies from the SEC-EDGAR database using the sec_edgar_downloader library, and stores the data in a file named sec-edgar-filings.

__Approach:__

The program is sub-divided into two modules :  

1. _Function download_10k_filings:_
   1. This function takes three arguments: ticker (stock ticker symbol of the company), output_folder (folder to save the downloaded filings), and email_address (user's email address, which might be required by the library).
   2. It initializes a Downloader object from the sec_edgar_downloader library using the provided output_folder and email_address.
   3. It iterates over the years from 1995 to 2023 and attempts to download 10-K filings for the specified ticker within each year.
   4. If filings are available for a specific year, it prints a success message; otherwise, it prints a message indicating no filings are available.
   5. It catches any exceptions that occur during the downloading process and prints an error message.

2. _Main Section (__main__):_
   1. Defines a list of companies (companies) for which 10-K filings will be downloaded.
   2. Specifies the output folder (output_folder) where the downloaded filings will be saved.
   3. Provides an email address (your_email_address) that might be required by the library.
   4. Iterates over each company in the companies list and calls the download_10k_filings function.
   5. Prints a message indicating the download process is complete after downloading filings for all specified companies.


### <ins>Task 1.2</ins>:

The main task for this part was to conduct text analysis using LLM API available for free. 

__Approach__:

This problem was also broken down into two parts:
1. Text generation
2. Graph Generation

__Code Analysis:__
1. __Text Generation__:
   1. _Import Statements_:
      1. <ins>import openai</ins>: Imports the OpenAI Python library, which provides access to OpenAI's language models and APIs.
      2. <ins>from sec_api import ExtractorApi</ins>: Imports the ExtractorApi class from the sec_api module, which is a module used for extracting text from SEC filings.

   2. _API Key Initialization:_
      1. <ins>openai.api_key</ins>: Sets the API key for the OpenAI library. This key is used to authenticate API requests to the OpenAI service.
      2. <ins>extractorApi</ins> = ExtractorApi("Api_Key_To_Be_Inserted"): Initializes an instance of the ExtractorApi class with the same API key. This suggests that both the OpenAI and SEC API services use the same API key for authentication.

   3. _Filing URL and Section Extraction:_
      1. <ins>filing_url</ins> = "https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm": Specifies the URL of an SEC filing. This URL points to a specific filing on the SEC EDGAR database.
      2. <ins>section_text</ins> = extractorApi.get_section(filing_url, "1A", "text"): Calls the get_section method of the ExtractorApi instance to extract text from section "1A" of the filing specified by the filing_url. The extracted text is stored in the section_text variable.
      3. <ins>prompt</ins> = f"Summarize the following text in 25 sentences:\n{section_text}": Constructs a prompt string for summarizing the extracted text. This prompt is used as input for the summarization model.
   4. _Text Summarization with OpenAI API:_
      1. <ins>response</ins> = openai.Completion.create(engine="text-davinci-003", prompt=prompt): Calls the Completion.create method of the OpenAI library to generate a text completion (i.e., summary) based on the provided prompt. The text-davinci-003 engine is specified for the completion, which refers to a specific language model offered by OpenAI.
      2. <ins>print(response["choices"][0]["text"])</ins>: Prints the generated text completion, which represents the summary of the input text. The summary is extracted from the response object returned by the OpenAI API.

   5. _Repeat for Another Section:_
      The process is repeated for another section of the filing. The section text is extracted using a different section identifier ("8"), and a summary is generated using the same procedure described above.


2. __Graph Generation__
   1. _Import Statements:_
   Imports the XbrlApi class from the sec_api module and the pandas library, which is commonly used for data manipulation and analysis.

   2. _API Key Initialization:_
   Initializes an instance of the XbrlApi class with the provided API key.

   3. _Retrieve XBRL Data from SEC Filing:_
   Specifies the URL of 10-K filing and retrieves the XBRL data in JSON format using the xbrl_to_json method of the XbrlApi instance.

   4. _Convert XBRL-JSON to DataFrame (Income Statement):_
   Defines a function get_income_statement to convert XBRL JSON data into a pandas DataFrame representing the income statement. Calls this function to extract income statement from the retrieved XBRL JSON data.

   5. _Retrieve and Process XBRL Data for Multiple Years:_
   Specifies URLs of 10-K filings for the last five years and retrieves XBRL data for each filing. Processes the XBRL data into income statements for each year.

   6. _Data Cleaning and Transformation:_
   Performs data cleaning and transformation operations on income statements, such as fixing naming inconsistencies and filtering data based on duration.

   7. _Data Visualization:_
   Generates bar charts to visualize revenue by region and product using matplotlib.

   8. _Plotting and Customization:_
   Customizes the appearance and layout of the generated bar charts, including titles, labels, legends, and formatting.

   9. _Displaying Visualizations:_
    Displays the generated bar charts to visualize revenue by region and product.

This code essentially retrieves XBRL data from SEC filings, processes it into meaningful representations (such as income statements), and visualizes the financial data using bar charts. It combines data retrieval, manipulation, visualization, and presentation into a single script.

The factors chosen for analysis are as follows:
1. Risk factors.
2. Financial statements.
3. Revenue by product and revenue by region.
   
__Reasons for choosing the above factors for analysis__:

<ins>_Risk Factor_:</ins> 

Analyzing risk factors in SEC EDGAR filings is essential for:

1. __Risk Assessment__    :   Helps investors evaluate potential risks before investing.
2. __Transparency__       :   Provides clear insights into a company's risks and challenges.
3. __Compliance__         :   Ensures companies meet regulatory requirements for disclosure.
4. __Risk Management__    :   Assists companies in identifying and addressing key risks.
5. __Investor Protection__:   Empowers investors to make informed investment decisions.
6. __Market Analysis__    :   Offers valuable insights into industry-wide risks and trends.
7. __Legal and Financial Due Diligence__:   Facilitates evaluation of risks in transactions and investments.

<ins>_Financial Statement_:</ins>

Analyzing financial statements in SEC EDGAR filings is crucial because it:

1. __Assesses Financial Health:__ Provides insights into a company's financial status and performance.
2. __Guides Investment Decisions:__ Helps investors evaluate growth potential and risk.
3. __Enables Comparative Analysis:__ Facilitates benchmarking and trend identification.
4. __Aids Risk Management:__ Highlights potential financial risks and vulnerabilities.
5. __Ensures Regulatory Compliance:__ Meets disclosure obligations and transparency requirements.
6. __Enhances Stakeholder Communication:__ Communicates financial information clearly to stakeholders.
7. __Supports Performance Evaluation:__ Evaluates management performance and strategic effectiveness.
8. __Facilitates Due Diligence:__ Provides critical information for mergers, acquisitions, and investments.

<ins>_Revenue by product and revenue by region_:</ins>

Providing a graphical representation of revenue by region and product in SEC EDGAR filings is crucial because it:

1. __Enhances Clarity:__ Offers clear visualization of revenue distribution across regions and among products.
2. __Identifies Key Markets:__ Helps quickly pinpoint regions and products contributing the most to revenue.
3. __Analyzes Trends:__ Reveals patterns and changes in product and regional performance over time.
4. __Facilitates Comparison:__ Enables easy comparison of revenue among different regions and product lines.
5. __Assesses Risks:__ Helps evaluate geographical risks and market dependencies.
6. __Aids Communication:__ Simplifies complex financial data for stakeholders.
7. __Guides Strategy:__ Informs decisions on market expansion and resource allocation and highlights revenue concentration risks for mitigation strategies.
8. __Monitors Performance:__ Demonstrates transparency and accountability to investors and provides ongoing tracking of product revenue.


### <ins>Task 2</ins>:

The main task of this part was to create a simple app that takes the company ticker as input and displays some visualization. 

__Approach__:

The code for this task generates graphical representation for:
1. EBITDA v/s Time
2. Total Revenue v/s Time

__Graph Generation__:

1. Import Statements:

   1. _import datetime:_ Imports the datetime module to work with dates and times.
   2. _import yfinance as yf:_ Imports the yfinance library for fetching financial data.
   3. _import dash, import dash_core_components as dcc, import dash_html_components as html:_ Imports necessary components from the Dash library for creating the web application.
   4. _from dash.dependencies import Input, Output:_ Imports the Input and Output classes from the dash.dependencies module for defining callback functions.

2. Dash Application Setup:

   1. _app = dash.Dash():_ Initializes a Dash application.
   2. _app.title_ = "Financial Statements Visualization": Sets the title of the Dash application.
   3. _app.layout:_ Defines the layout of the Dash application using HTML components.

3. Layout Definition:

   1. _html.Div:_ Defines a division in the layout.
   2. _html.H1:_ Defines a level-one heading.
   3. _html.H4:_ Defines a level-four heading.
   4. _dcc.Input:_ Defines an input field for entering a stock ticker symbol.
   5. _html.Div:_ Defines a division where the graph will be displayed.

4. Callback Function:

   1. _@app.callback:_ Decorator that defines a callback function to update the graph based on user input.
   2. _def update_graph(input_data):_ Defines the callback function with an input parameter input_data representing the stock ticker symbol entered by the user.
   3. _Inside the function:_
      1. _start and end:_ Define start and end dates for fetching financial data (from 1995 to the current date).
      2. _try block:_
         1. _For EBITDA v/s Time:_
            1.  _financials = yf.Ticker(input_data).financials:_ Fetches financial statements data using the yfinance library.
            2.   _normalized_ebitda:_ Extracts the Normalized EBITDA data from the fetched financials data.
            3.    _x_axis_labels:_ Creates a list of years from 1995 to 2023.
            4. _graph:_ Defines a Dash graph component (dcc.Graph) with data and layout properties to display the normalized EBITDA trend.
               
         2. _For Total Revenue v/s Time:_
            1. _financials = yf.Ticker(input_data).financials.T:_ Fetches financial statements data using the yfinance library and transposes the DataFrame for easier manipulation.
            2. _if 'Total Revenue' in financials.columns:_ Checks if the 'Total Revenue' column is available in the financials DataFrame.
            3. _revenue:_ Extracts the 'Total Revenue' data from the financials DataFrame.
            4. _x_axis_labels:_ Creates a list of years from the index of the revenue DataFrame.
            5. _graph:_ Defines a Dash graph component (dcc.Graph) with data and layout properties to display the total revenue trend.

      3. _except block:_
         1. _error_message:_ Generates an error message if there's an exception while fetching financial data.
         2. _graph:_ Displays the error message in a html.Div component.
   4. _return graph:_ Returns the graph component to be displayed on the web page.

5. Main Function:

   1. _if __name__ == '__main__':_ Checks if the script is being run directly.
   2. app.run_server(): Runs the Dash application server.

The code for the deployed application runs on port 8050 automatically, when executed. 
1. EBITDA v/s Time: https://legendary-pancake-9pppjjgrq4g3pqqj-8050.app.github.dev/
2. Total Revenue v/s Time: https://potential-space-memory-rjjjpp5q64v2p97g-8050.app.github.dev/

__Reasons for choosing the above factors for analysis:__

<ins>_EBITDA v/s Time Analysis:_</ins>

EBITDA provides insights into operating profitability, cash flow, financial health, comparative analysis, investment decisions, debt servicing capacity, and valuation, making it a valuable metric for assessing a company's overall performance. It further helps in:

1. Performance Tracking: Graphs track EBITDA trends over time.
2. Financial Health: Assess operational efficiency and profitability.
3. Investment Insight: Aid investors in evaluating opportunities.
4. Comparative Analysis: Compare EBITDA across companies.
5. Strategic Planning: Inform optimization strategies.
6. Communication: Enhance understanding for stakeholders.



<ins>_Total Revenue v/s Time Analysis:_</ins>

Total revenue provides insights into revenue growth, market demand, product performance, competitive positioning, financial health, investor confidence, and strategic decision making, making it a critical metric for evaluating a company's overall performance and prospects. It further helps in:

1. Performance Tracking: Graphical plots track total revenue trends over time.
2. Business Growth: Visual representation highlights revenue growth or decline.
3. Market Insights: Helps understand market demand and economic trends.
4. Strategic Decision Making: Guides resource allocation and business strategies.
5. Investor Confidence: Demonstrates business stability and growth potential.
6. Comparative Analysis: Facilitates comparison with competitors and industry benchmarks.
7. Communication: Simplifies complex financial data for stakeholders.


### <ins>Limitations and Improvements</ins>:

Analyzing the limitations and scope of improvement for each code snippet:

1. __Code for downloading and analyzing SEC EDGAR 10-K filings using Python:__

   1. Limitations:
      1. Limited Data Coverage: The code does not cover all companies or retrieve filings for certain periods, limiting the scope of analysis.
      2. Dependency on External Libraries: Reliance on the sec_edgar_downloader library might restrict customization or additional functionalities.
      3. Error Handling: Error handling could be improved by stating which kind of error is handled by the except block. This could help in narrowing down the possible errors, leading to faster debugging.

   2. Improvements:
      1. Extended Filings Coverage: Enhance the code to cover a broader range of filings, allowing users to specify the type of filings they want to download and analyze.
      2. Data Validation: Improve data validation mechanisms to ensure the accuracy and completeness of retrieved filings, verifying document integrity and consistency.
      3. Parallel Processing: Implement parallel processing techniques to speed up the download and analysis process, especially for large datasets or multiple companies.
      4. Interactive Interface: Developing a user-friendly interface or command-line interface (CLI) that would guide users through the process of selecting companies, specifying parameters, and analyzing the retrieved filings. This would enhance usability and accessibility for users with varying levels of technical expertise.
      5. Documentation and Logging: Providing comprehensive documentation and logging functionalities to help users understand how to use the code effectively and troubleshoot any issues that may arise during the download and analysis process.


2. __Code for summarizing text sections from SEC EDGAR filings using OpenAI's API:__

   1. Limitations:
      1. Limited to summarizing specific sections ("1A" and "8" in this case) from SEC EDGAR filings.
      2. Relies heavily on OpenAI's API for text summarization, which may have limitations in accessing and/or summarizing complex financial documents accurately.
      3. Currently only provides analysis for one company. This can be improved by optimizing the code to reduce the number of query requests sent to the server.

   2. Improvements:
      1. Increase flexibility to summarize arbitrary sections based on user input, to improve the analysis by taking into account more factors
      2. Implement custom summarization algorithms tailored specifically for financial documents, potentially improving accuracy and relevance of summaries.
      3. Increase user flexibility to allow for text analysis for more than one company at a time.


3. __Code for retrieving financial data from SEC EDGAR filings and visualizing it using Python:__

   1. Limitations:
      1. Relies on the sec_api and xbrlApi libraries for retrieving XBRL data, which may have limitations or dependencies on third-party services.
      2. Limited to specific financial metrics and visualizations, such as income statements and revenue breakdowns.
      3. Currently only provides analysis for one company. This can be improved by optimizing the code to reduce the number of query requests sent to the server.

   2. Improvements:
       1. Expand data retrieval capabilities to include a broader range of financial metrics and statements, such as balance sheets, cash flow statements, etc.
       2. Enhance visualization options to cover a wider range of financial insights and provide more interactive visualizations for better analysis.
       3. Increase user flexibility to allow for text analysis for more than one company at a time.


4. __Code for visualizing normalized EBITDA trend using yfinance and Dash:__

   1. Limitations:
      1. Cannot display EBITDA trends for more than one company at a time.
      2. Needs fine-tuning for error handling in cases where financial data retrieval fails or when certain data fields are missing. In such cases, currently, the point is left blank.

   2. Improvements:
      1. Extend functionality to support multiple stock ticker symbols for comparative analysis in a single graph.
      2. Implement error handling to gracefully handle cases of missing or incomplete financial data, providing informative messages to the user.
      3. To allow for comparative analysis between multiple companies, we would also have to include color coding schemes to differentiate between the multiple companies.


5. __Code for visualizing revenue trends by region and product using yfinance and Dash:__

   1. Limitations:
      1.  Cannot display Total revenue trends for more than one company at a time.
      2.  Potential issues with data consistency and completeness, especially if certain segments or dimensions are missing from the financial data. In such cases, currently, the point is left blank.

   2. Improvements:
      1. Expantion in functionality to support multiple stock ticker symbols and enable comparative analysis across different companies.
      2. Improvement in data preprocessing and validation to ensure consistency and completeness of the financial data, handling missing or inconsistent segments gracefully, and provide necessary user message.
      3.  To allow for comparative analysis between multiple companies, we would also have to include color coding schemes to differentiate between the multiple companies.


### <ins>Sources</ins>:
1. https://sec-edgar-downloader.readthedocs.io/en/latest/
2. https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm
3. https://www.geeksforgeeks.org/python-stock-data-visualisation/
4. https://fishtail.ai/blog-2-accessing-company-financials-using-the-sec-edgar-api
5. https://realpython.com/python-dash/
6. https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/\
7. https://www.learndatasci.com/tutorials/python-finance-part-yahoo-finance-api-pandas-matplotlib/
8. https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/
9. https://pypi.org/project/yahoofinancials/
10. https://www.geeksforgeeks.org/python-bokeh-visualizing-stock-data/
11. https://sec-api.io/resources/extract-financial-statements-from-sec-filings-and-xbrl-data-with-python#Extract-and-Merge-Financial-Statements-from-Multiple-10-K-Filings
12. https://medium.com/@jan_5421/summarize-sec-filings-with-openai-gtp3-a363282d8d8

from sec_edgar_downloader import Downloader

def download_10k_filings(ticker, output_folder, email_address):
    """This function downloads 10-K filings for a company ticker from 1995 to 2023.

    Args:
        ticker: The stock ticker symbol of the company.
        output_folder: The folder where the downloaded filings will be saved.
        email_address: The user's email address (might be required by the library).
    """
    downloader = Downloader(output_folder, email_address)
    for year in range(1995, 2024):
        try:
            response = downloader.get("10-K", ticker, after=str(year)+"-01-01", before=str(year)+"-12-31", download_details=True)
            if response == 1:
                downloader.get("10-K", ticker, after=str(year)+"-01-01", before=str(year)+"-12-31")
                print(f"Downloaded 10-K filings for {ticker} in {year}")
            else:
                print(f"No filings available for {ticker} in {year}")
        except Exception as e:
            print(f"Error downloading filings for {ticker} in {year}: {e}")

if __name__ == "__main__":
    # Replace these with any chosen tickers
    companies = ["AAPL", "GOOG", "TSLA"]
    output_folder = "sec_filings"  # Change this to the desired output folder
    your_email_address = "your_email@example.com"  # Replace with an actual email address

    for company in companies:
        download_10k_filings(company, output_folder, your_email_address)

    print("Download complete!")
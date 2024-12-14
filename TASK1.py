from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import requests

headers = {"User-Agent": "Mozilla/5.0"}
data = {
    "Stock Name": [],
    "PE": [],
    "EPS": [],
    "52W High": [],
    "52W Low": [],
    # "Upper Circuit": [],
    # "Lower Circuit": [],
    "LTP": [],
    "Market Cap": [],
    "Volume": [],
    "% Change": [],
    "6M Return": [],
    "1Y Return": [],
    "5Y Return": [],
}


with open("STOCKS.txt", "r") as file:
    for line in file:
        words = line.split()
        SYMBOL0 = words[0]
        SYMBOL = f"{SYMBOL0}.NS"
        # SYMBOL = "RELIANCE.NS"  # Make sure you're using the correct ticker symbol
        # SYMBOL0 = "RELIANCE"  # Make sure you're using the correct ticker symbol
        url = f"https://www.screener.in/company/{SYMBOL0}/"
        url2 = f"https://www.nseindia.com/get-quotes/equity?symbol={SYMBOL0}"
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        response2 = requests.get(url2, headers=headers, timeout=15)
        soup2 = BeautifulSoup(response2.content, "html.parser")
        stock = yf.Ticker(SYMBOL)

        # PE
        stock_pe_span = soup.find(
            "span", class_="name", string=lambda text: "Stock P/E" in text
        )
        PE = (
            stock_pe_span.find_next("span", class_="number").text.strip()
            if stock_pe_span
            else "NaN"
        )
        # print(f"PE is {PE}")

        # EPS
        EPS = stock.info.get(
            "regularMarketEPS", "NaN"
        )  # Using .get() to avoid KeyError
        # print(f"EPS is {EPS}")

        # 52W HIGH LOW
        stock_high_span = soup.find(
            "span", class_="name", string=lambda text: "High / Low" in text
        )
        if stock_high_span:
            HIGH = stock_high_span.find_next("span", class_="number").text.strip()
            LOW = (
                stock_high_span.find_next("span", class_="number")
                .find_next("span", class_="number")
                .text.strip()
            )
        else:
            HIGH, LOW = "NaN", "NaN"

        # print(f"HL is {HIGH} {LOW}")

        # UPPER CIRCUIT and LOWER CIRCUIT
        stock_UC_span = soup2.find("span", id="upperbandVal")
        UC = stock_UC_span if stock_UC_span else "NaN"
        stock_LC_span = soup2.find("span", id="lowerbandVal")
        LC = stock_LC_span if stock_LC_span else "NaN"
        # print(f"UCLC is {UC} {LC}")

        # LTP
        stock_pe_span = soup.find(
            "span", class_="name", string=lambda text: "Current Price" in text
        )
        LTP = (
            stock_pe_span.find_next("span", class_="number").text.strip()
            if stock_pe_span
            else "NaN"
        )

        # print(f"LTP is {LTP}")

        # MARKET CAP
        stock_pe_span = soup.find(
            "span", class_="name", string=lambda text: "Market Cap" in text
        )
        CAP = (
            stock_pe_span.find_next("span", class_="number").text.strip()
            if stock_pe_span
            else "NaN"
        )

        # print(f"Cap is {CAP}")

        # VOLUME
        hist = stock.history("1d")
        VOL = hist["Volume"].iloc[-1].item() if not hist["Volume"].empty else "NaN"
        # print(f"Vol is {VOL}")

        # % Change
        hist = stock.history(period="5d")
        if not hist.empty:
            previous = hist["Close"].iloc[-2]
            current = hist["Close"].iloc[-1]
            CHANGE = ((current - previous) / previous) * 100
        else:
            CHANGE = "NaN"

        # print(f"Change is {CHANGE}")

        # 6M Return
        hist = stock.history(period="6mo")
        if not hist.empty:
            current = hist["Close"].iloc[-1]
            old = hist["Close"].iloc[0]
            RETURN6 = ((current - old) / old) * 100
        else:
            RETURN6 = "NaN"

        # print(f"6m is {RETURN6}")

        # 1Y Return
        hist = stock.history(period="1y")
        if not hist.empty:
            current = hist["Close"].iloc[-1]
            old = hist["Close"].iloc[0]
            RETURN1 = ((current - old) / old) * 100
        else:
            RETURN1 = "NaN"

        # print(f"1y is {RETURN1}")

        # 5Y Return
        hist = stock.history(period="5y")
        if not hist.empty:
            current = hist["Close"].iloc[-1]
            old = hist["Close"].iloc[0]
            RETURN5 = ((current - old) / old) * 100
        else:
            RETURN5 = "NaN"
        # print(f"5y is {RETURN5}")

        # Append data to the dictionary
        data["Stock Name"].append(SYMBOL)
        data["PE"].append(PE)
        data["EPS"].append(EPS)
        data["52W High"].append(HIGH)
        data["52W Low"].append(LOW)
        data["LTP"].append(LTP)
        data["Market Cap"].append(CAP)
        data["Volume"].append(VOL)
        data["% Change"].append(CHANGE)
        data["6M Return"].append(RETURN6)
        data["1Y Return"].append(RETURN1)
        data["5Y Return"].append(RETURN5)

        # Print DataFrame

# Convert to DataFrame
df = pd.DataFrame(data)
print(pd.DataFrame(data))
# Save as CSV
# df.to_csv("output.csv", index=False)

# Save as Excel
# df.to_excel("output.xlsx", index=False)
# with open("DATA.txt", "w") as file:
#     for key, value in data.items():
#         file.write(f"{key}: {value}\n")

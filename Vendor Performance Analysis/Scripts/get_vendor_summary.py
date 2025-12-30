import pandas as pd
import os
import logging
from sqlalchemy import create_engine
from ingestion_db import ingest_db

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
    force=True   
)

def create_vendor_summary(engine):
    """
    This function merges different tables to get the overall vendor summary
    """
    
    vendor_sales_summary = pd.read_sql_query("""
    WITH FreightSummary AS (
        SELECT 
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY 
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),

    SalesSummary AS (
        SELECT 
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """, engine)

    return vendor_sales_summary

def clean_data(df):
    """
    This function cleans the vendor summary data
    """

    # Change datatype
    df['Volume'] = df['Volume'].astype(float)

    # Fill missing values
    df.fillna(0, inplace=True)

    # Remove extra spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Create new calculated columns
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (
        df['GrossProfit'] / df['TotalSalesDollars']
    ) * 100

    df['StockTurnover'] = (
        df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    )

    df['SalesToPurchaseRatio'] = (
        df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    )

    return df

if __name__ == "__main__":

    # Create SQLAlchemy engine
    engine = create_engine("sqlite:///inventory.db")

    logging.info("Creating Vendor Summary Table.....")
    vendor_sales_summary = create_vendor_summary(engine)
    logging.info(vendor_sales_summary.head())

    logging.info("Cleaning Data.....")
    clean_df = clean_data(vendor_sales_summary)
    logging.info(clean_df.head())

    logging.info("Ingesting data.....")
    ingest_db(clean_df, "vendor_sales_summary", engine)

    logging.info("Completed")

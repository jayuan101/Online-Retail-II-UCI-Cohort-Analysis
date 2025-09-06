WITH FirstPurchase AS (
    SELECT CustomerID, MIN(InvoiceDate) AS FirstPurchaseDate
    FROM sales
    GROUP BY CustomerID
),
CohortData AS (
    SELECT
        s.CustomerID,
        DATE_TRUNC('month', f.FirstPurchaseDate) AS CohortMonth,
        DATE_TRUNC('month', s.InvoiceDate) AS InvoiceMonth,
        COUNT(DISTINCT s.InvoiceNo) AS InvoiceCount,
        SUM(s.UnitPrice * s.Quantity) AS Revenue
    FROM sales s
    JOIN FirstPurchase f ON s.CustomerID = f.CustomerID
    GROUP BY s.CustomerID, f.FirstPurchaseDate, s.InvoiceDate
)
SELECT
    CohortMonth,
    EXTRACT(MONTH FROM AGE(InvoiceMonth, CohortMonth)) AS CohortIndex,
    COUNT(DISTINCT CustomerID) AS ActiveCustomers,
    SUM(Revenue) AS Revenue
FROM CohortData
GROUP BY CohortMonth, CohortIndex
ORDER BY CohortMonth, CohortIndex;

class SalesHistoryService:
    @staticmethod
    def process_sales_history(distributed_dates: dict, sales_records: dict):
        result_sales = distributed_dates.copy()
        for key in result_sales.keys():
            result_sales[key] = sales_records.get(key, 0)
        return result_sales

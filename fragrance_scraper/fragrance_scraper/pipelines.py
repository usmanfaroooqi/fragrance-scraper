import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ExcelExportPipeline:
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        if not self.items:
            spider.logger.info("No items scraped.")
            return
        df = pd.DataFrame(self.items)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        csv_path = f"fragrance_data_{ts}.csv"
        excel_path = f"fragrance_data_{ts}.xlsx"
        df.to_csv(csv_path, index=False)
        try:
            df.to_excel(excel_path, index=False)
        except Exception as e:
            spider.logger.warning("Failed to write Excel file: %s", e)
            excel_path = None
        spider.logger.info("Saved CSV: %s, Excel: %s", csv_path, excel_path)

        # Optional: Google Sheets upload
        if spider.settings.getbool("ENABLE_GSHEETS", False):
            creds_file = spider.settings.get("GSHEETS_CREDENTIALS_JSON")
            sheet_name = spider.settings.get("GSHEETS_SHEET_NAME", f"fragrance_data_{ts}")
            if not creds_file:
                spider.logger.warning("GSHEETS_CREDENTIALS_JSON not configured.")
                return
            try:
                import gspread
                gc = gspread.service_account(filename=creds_file)
                sh = gc.create(sheet_name)
                worksheet = sh.get_worksheet(0)
                worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                spider.logger.info("Uploaded to Google Sheets: %s", sh.url)
            except Exception as e:
                spider.logger.error("Failed to upload to Google Sheets: %s", e)

    def process_item(self, item, spider):
        d = dict(item)
        for f in ("discounted_price", "original_price", "discount_percentage"):
            if f in d and isinstance(d[f], str):
                d[f] = d[f].strip()
        d['scraped_at'] = datetime.utcnow().isoformat()
        self.items.append(d)
        return item

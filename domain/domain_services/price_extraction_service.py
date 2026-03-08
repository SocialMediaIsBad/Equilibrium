import easyocr
import re
import cv2

from rapidfuzz import fuzz
from typing import List, Optional
from collections import Counter

class PriceExtractionService:
    num_like = re.compile(r"[0-9OIlS,.]+")

    def read(self, picture):
        reader = easyocr.Reader(['de'])
        return reader.readtext(picture)

    def overlap_satisfied(self, a, b):
        height_a = a[0][3][1] - a[0][0][1]
        height_b = b[0][3][1] - b[0][0][1]
        overlap = a[0][3][1] - b[0][0][1]

        if overlap > height_a / 2 or overlap > height_b / 2:
            return True
        else:
            return False

    def get_all_lines(self, result):
        lines = []
        current_line = "" + result[0][1]

        for i in range(len(result)):
            if i + 1 == len(result):
                current_line = current_line + " " + result[i][1]
                lines.append(current_line)
                break

            if self.overlap_satisfied(result[i], result[i + 1]):
                current_line = current_line + " " + result[i][1]
            else:
                current_line = current_line + " " + result[i][1]
                lines.append(current_line)
                current_line = ""

        return lines

    def get_relevant_lines(self, lines_of_document):
        keywords = ["summe", "gesamt", "total", "betrag", "zu zahlen"]
        relevant_lines = []

        for line in lines_of_document:
            for kw in keywords:
                ratio = fuzz.partial_ratio(kw.casefold(), line.casefold())
                if fuzz.partial_ratio(kw.casefold(), line.casefold()) > 75:
                    relevant_lines.append(line)

        return relevant_lines

    def extract_obvious_prices(self, line):
        candidates = self.num_like.findall(line)
        prices = []

        for c in candidates:
            norm = self.normalize_number_token(c)
            if re.fullmatch(r"\d{1,4}\.\d{2}", norm):
                prices.append(float(norm))

        return prices

    def normalize_number_token(self, token: str) -> str:
        token = (token
                 .replace("O", "0")
                 .replace("o", "0")
                 .replace("I", "1")
                 .replace("l", "1")
                 .replace("S", "5")
                 .replace(",", ".")
                 )

        token = re.sub(r"(\d)\s\.\s(\d)", r"\1.\2", token)
        token = re.sub(r"(\d)\.\s(\d)", r"\1.\2", token)
        token = re.sub(r"(\d)\s\.(\d)", r"\1.\2", token)

        token = re.sub(r"(?<=\d)\s+(?=\d)", ".", token)

        return token

    def extract_not_so_obvious_prices(self, line):
        candidates = self.num_like.findall(line)

        for c in candidates:
            norm = normalize_number_token(c)
            if re.fullmatch(r"\d{1,4}\.\d{2}", norm):
                line = re.sub(c, "", line)

        line = normalize_number_token(line)
        return extract_obvious_prices(line)

    def extract_price_from_list(strings: List[str]) -> Optional[str]:
        if not strings:
            return None

        counter = Counter(strings)
        return counter.most_common(1)[0][0]

    def preprocess(picture_data):
        img = cv2.imread(picture_data)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 10)

        return thresh

    def extract_price_from_picture(picture):
        possible_payments = []

        text_matrix = read(picture)
        lines_of_document = get_all_lines(text_matrix)
        relevant_lines = get_relevant_lines(lines_of_document)
        for line in relevant_lines:
            possible_payments = possible_payments + extract_obvious_prices(line)
            possible_payments = possible_payments + extract_not_so_obvious_prices(line)
        price = extract_price_from_list(possible_payments)

        return price

    def extract_price(self, picture) -> float:
        picture = bytes(picture)
        price = extract_price_from_picture(picture)
        if price is None:
            picture_processed = preprocess(picture)
            price = extract_price_from_picture(picture_processed)

        return float(price)
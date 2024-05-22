import csv
from collections import defaultdict, Counter
import os


def read_sales_data(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            sales_data = [row for row in reader]
        return sales_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []


def calculate_total_revenue(sales_data):
    total_revenue = sum(float(item['Общая стоимость']) for item in sales_data)
    return total_revenue


def find_most_sold_product(sales_data):
    product_sales = Counter()
    for item in sales_data:
        product_sales[item['Название товара']] += int(item['Количество продаж'])
    most_sold_product = product_sales.most_common(1)[0]
    return most_sold_product


def find_highest_revenue_product(sales_data):
    product_revenue = defaultdict(float)
    for item in sales_data:
        product_revenue[item['Название товара']] += float(item['Общая стоимость'])
    highest_revenue_product = max(product_revenue.items(), key=lambda x: x[1])
    return highest_revenue_product


def generate_report(sales_data):
    total_revenue = calculate_total_revenue(sales_data)
    most_sold_product, most_sold_quantity = find_most_sold_product(sales_data)
    highest_revenue_product, highest_revenue = find_highest_revenue_product(sales_data)

    product_sales = Counter()
    product_revenue = defaultdict(float)

    for item in sales_data:
        product_sales[item['Название товара']] += int(item['Количество продаж'])
        product_revenue[item['Название товара']] += float(item['Общая стоимость'])

    report = {
        'total_revenue': total_revenue,
        'most_sold_product': most_sold_product,
        'most_sold_quantity': most_sold_quantity,
        'highest_revenue_product': highest_revenue_product,
        'highest_revenue': highest_revenue,
        'product_sales': product_sales,
        'product_revenue': product_revenue
    }

    return report


def print_report(report):
    print(f"Общая выручка магазина: {report['total_revenue']:.2f}")
    print(
        f"Товар, который был продан наибольшее количество раз: {report['most_sold_product']} ({report['most_sold_quantity']} шт.)")
    print(
        f"Товар, который принес наибольшую выручку: {report['highest_revenue_product']} ({report['highest_revenue']:.2f} руб.)")

    print("\nОтчет по каждому товару:")
    print(f"{'Название товара':<30} {'Количество продаж':<20} {'Доля в общей выручке':<20}")
    for product, sales in report['product_sales'].items():
        revenue_share = (report['product_revenue'][product] / report['total_revenue']) * 100
        print(f"{product:<30} {sales:<20} {revenue_share:.2f}%")


if __name__ == "__main__":
    file_path = 'sales_data.csv'
    sales_data = read_sales_data(file_path)

    if sales_data:
        report = generate_report(sales_data)
        print_report(report)
from db.recommender_dao import RecommenderDAO


class RecommenderService:
    @staticmethod
    def process_cart_products(cart_id: int):
        cart_products = list(RecommenderDAO.get_cart_products_id(cart_id))
        products_price_history = RecommenderDAO.get_price_history(cart_products)
        products_sales_history = RecommenderDAO.get_sales_history(cart_products)
        print('Cart is:')
        print(cart_products)
        print('\nPrice history:')
        print(products_price_history)
        print('\nSales history:')
        print(products_sales_history)

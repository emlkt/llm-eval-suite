"""Статусы заказов для модели. Берет только статус, без персональных данных (имя/телефон остаются в fixtures/fake_orders.py, модель их не видит)"""

from fixtures.fake_orders import FAKE_ORDERS

ORDER_STATUSES = {order_id: data["status"] for order_id, data in FAKE_ORDERS.items()}

statuses_text = "\n".join(f"- {order_id}: {status}" for order_id, status in ORDER_STATUSES.items())

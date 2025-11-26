# from django.db import models

# # --------------------------
# # User Table
# # --------------------------
# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=128)
#     email = models.EmailField(unique=True)


# # --------------------------
# # Product Table
# # --------------------------
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.IntegerField()


# # --------------------------
# # Order Table
# # --------------------------
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     order_date = models.DateTimeField(auto_now_add=True)


# # --------------------------
# # Order_Product Table (Join Table)
# # --------------------------
# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')
#     quantity = models.PositiveIntegerField()

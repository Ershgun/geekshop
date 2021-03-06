from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet): # Вариант 1
#
#     def delete(self):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()  # Вариант 1

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product,verbose_name="продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def _get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    product_cost = property(_get_product_cost)

    def get_total_quantity(self):
        _items = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity
    # total_quantity = property(_get_total_quantity)


    def get_total_cost(self):
        _items = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost
    # total_cost = property(_get_total_cost)











    # def _get_total_quantity(self):
    #     "return total quantity for user"
    #     _items = Basket.objects.filter(user=self.user)
    #     _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
    #     return _totalquantity
    #
    # total_quantity = property(_get_total_quantity)
    #
    #
    # def _get_total_cost(self):
    #     "return total cost for user"
    #     _items = Basket.objects.filter(user=self.user)
    #     _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
    #     return _totalcost
    #
    # total_cost = property(_get_total_cost)



    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category').select_related()

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)    \

    @staticmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]
        return basket_items_dic



    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()




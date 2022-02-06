from django.db.models import OuterRef, Subquery, Q

from apps.store.models import Product, ProductPrice, ProductImage


class ProductRetrieveService():
    def get_products_list(self, include_price=True, include_image=True):
        # actual_price = ProductPrice.objects.filter(product=OuterRef('pk')).order_by('-date_actual')
        # product_image = ProductImage.objects.filter(Q(product=OuterRef('pk')) & Q(is_main=True))
        # products = Product.objects.select_related('vendor', 'category') \
        #     .annotate(price=Subquery(actual_price.values('price')[:1])) \
        #     .annotate(image=Subquery(product_image.values('image')[:1]))
        # return products
        products = Product.objects.select_related('vendor', 'category')
        if include_price:
            actual_price = ProductPrice.objects.filter(product=OuterRef('pk')).order_by('-date_actual')
            products = products.annotate(price=Subquery(actual_price.values('price')[:1]))
        if include_image:
            product_image = ProductImage.objects.filter(Q(product=OuterRef('pk')) & Q(is_main=True))
            products = products.annotate(image=Subquery(product_image.values('image')[:1]))
        return products


class ProductCreateService():
    def save_product_price(self, product, price):
        ProductPrice(product=product, price=price).save()

    # bug images doesn't delete
    # idea: images with blank image but given id on delete should cause ''.delete()
    def process_product_images(self, product, image_list):
        is_main_image = True
        for image_form in image_list:
            if image_form.cleaned_data:
                product_image = image_form.save(commit=False)
                print(product_image)
                # if delete_image or not product_image:
                #     image_form = None
                #     ProductImage.objects.get(pk=product_image_id).delete()
                # else:
                #     product_image = image_form.save(commit=False)
                #     product_image.product = product
                #     product_image.is_main = is_main_image
                #     product_image.save()
                #     is_main_image = False
        if False:
            ProductImage(product=product, is_main=True).save()



class ProductDestroyService():
    def delete_product(self, product):
        product.delete()

from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, CategoryForm, AddToCartForm, DeleteFromCartForm
from .models import Product, Category
from cart.views import get_cartid


def user_is_staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        return True
    return False


class CreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = ProductForm()

            cart = get_cartid(request)

            return render(request, 'product/create.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()

                messages.success(request, 'محصول با موفقیت ایجاد شد ')
                return redirect('/product/allforadmin/')

            cart = get_cartid(request)

            return render(request, 'product/create.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def get_product_or_404(id):
    product = get_object_or_404(Product, pk=id)
    return product


class EditView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            product = get_product_or_404(id)
            form = ProductForm(instance=product)

            cart = get_cartid(request)

            return render(request, 'product/edit.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            product = get_product_or_404(id)
            form = ProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()
                messages.success(request, 'محصول با موفقیت ویرایش شد')
                return redirect('/product/' + str(id) + '/')

            cart = get_cartid(request)

            return render(request, 'product/edit.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class ListView(TemplateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        from cart.views import get_cartid
        cart = get_cartid(request)
        return render(request, 'product/list.html', {'products': products, 'cartid': cart.id})

    def post(self, request, *args, **kwargs):
        search_string = request.POST['search']
        return redirect('/product/' + search_string + '/search/')


class ListForAdminView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            products = Product.objects.all()
            from cart.views import get_cartid
            cart = get_cartid(request)
            return render(request, 'product/list2.html', {'products': products, 'cartid': cart.id})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class DetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        from cart.views import get_cartid
        from cart.views import product_is_already_in_cart

        product = get_product_or_404(id)
        cart = get_cartid(request)

        forms = [AddToCartForm(initial={'pid': id, 'count': 1})]
        submits = ['اضافه به سبد']
        actions = ['/cart/' + str(cart.id) + '/add/' + str(id) + '/']
        methods = ['POST']
        if product_is_already_in_cart(cart, product, 0):
            forms.append(DeleteFromCartForm())
            submits.append('حذف از سبد')
            actions.append('/cart/' + str(cart.id) + '/delete/' + str(id) + '/')
            methods.append('GET')

        return render(request, 'product/detail.html', {'product': product, 'forms': forms, 'submits': submits,
                                                       'actions': actions, 'methods': methods, 'cartid': cart.id})

    def add_to_cart_return_message(self, request, form, id):
        count = form.cleaned_data['count']
        from cart.views import get_cartid, AddToCart
        cart = get_cartid(request)
        message = AddToCart.get(AddToCart, request, cart.id, id, count).content
        return message

    def post(self, request, id, *args, **kwargs):
        messages.success(request, 'این صفحه از درخواست POST پشتیبانی نمیکند.')
        return redirect('/product/' + str(id) + '/')


class DeleteView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            product = get_product_or_404(id)
            product.delete()

            messages.success(request, 'محصول با موفقیت حذف شد.')
            return redirect('/product/allforadmin/')

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class CategoryCreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CategoryForm()

            cart = get_cartid(request)

            return render(request, 'category/create.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, 'دسته با موفقیت اضافه شد.')

                return redirect('/product/category/all/')

            cart = get_cartid(request)

            return render(request, 'category/edit.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def get_category_or_404(id):
    category = get_object_or_404(Category, pk=id)
    return category


class CategoryEditView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            category = get_category_or_404(id)
            form = CategoryForm(instance=category)

            cart = get_cartid(request)

            return render(request, 'category/edit.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            category = get_category_or_404(id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()

                messages.success(request, 'دسته با موفقیت ویرایش شد')
                return redirect('/product/category/' + str(id) + '/')

            cart = get_cartid(request)

            return render(request, 'category/edit.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class CategoryListView(TemplateView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        cart = get_cartid(request)

        return render(request, 'category/list.html', {'categories': categories, 'cartid': cart.id})


class CategoryDetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        category = get_category_or_404(id)

        cart = get_cartid(request)

        return render(request, 'category/detail.html', {'category': category, 'cartid': cart.id})


class CategoryDeleteView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            category = get_category_or_404(id)
            category.delete()

            messages.success(request, 'دسته با موفقیت حذف شد')
            return redirect('/product/category/all/')

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class CategoryProductsView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        products = Product.objects.all().filter(category=id)
        from cart.views import get_cartid
        cart = get_cartid(request)
        return render(request, 'product/list.html', {'products': products, 'cartid': cart.id})


class SearchView(TemplateView):

    def get(self, request, search_string, *args, **kwargs):
        products = Product.objects.all().filter(name__contains=search_string)
        from cart.views import get_cartid
        cart = get_cartid(request)
        return render(request, 'product/list.html',
                      {'products': products, 'cartid': cart.id, 'search_string': search_string})

    def post(self, request, *args, **kwargs):
        search_string = request.POST['search']
        return redirect('/product/' + search_string + '/search/')


class SearchInCategory(TemplateView):

    def get(self, request, id, search_string, *args, **kwargs):
        products = Product.objects.all().filter(category=id, name__contains=search_string)
        from cart.views import get_cartid
        cart = get_cartid(request)
        return render(request, 'product/list.html',
                      {'products': products, 'cartid': cart.id, 'search_string': search_string})

    def post(self, request, *args, **kwargs):
        search_string = request.POST['search']
        return redirect('/product/' + search_string + '/search/')
# donations/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.urls import reverse
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DonationForm, ItemForm, DonorForm, ItemAdminForm
from .models import CustomUser, Donation, Item, Donor
from .models import News, Activity
from .forms import NewsForm, ActivityForm
from django.db.models import Sum, Count


def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Verificar se já existe um Donor associado ao usuário
            if not Donor.objects.filter(user=user).exists():
                Donor.objects.create(user=user)
            messages.success(request, 'Usuário e doador registrados com sucesso!')
            return redirect("admin_dashboard")
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, "donations/admin_register.html", {"form": form})
    
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect("home")
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, "donations/register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "donations/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

def home(request):
    # Verifica se o parâmetro visit_site está na URL
    visit_site = request.GET.get('visit_site', None)

    if request.user.is_superuser and not visit_site:
        # Redireciona para a dashboard de admin se o usuário for administrador e não tiver o parâmetro visit_site
        return redirect(reverse('admin_dashboard'))
    else:
        # Renderiza a home page para usuários não administradores ou se o parâmetro visit_site estiver presente
        context = {
            'username': request.user.username,
            'is_admin': request.user.is_superuser,  # Check if the user is an admin
        }
        return render(request, "donations/home.html", context)

@login_required
def donate(request):
    try:
        donor = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        messages.error(request, 'Usuário doador não encontrado.')
        return redirect('not-donor')
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = donor
            donation.save()
            messages.success(request, 'Obrigado pela sua doação!')
            return redirect('thank-you')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
            print(form.errors)  # Adiciona print para depurar erros no formulário
    else:
        form = DonationForm()

    context = {
        'form': form,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,  # Check if the user is an admin
    }
    return render(request, 'donations/donate.html', context)

@login_required
def items_for_sale(request):
    # Filtrar apenas itens em análise e aprovados
    items_for_sale = Item.objects.filter(estado__in=['analise', 'aprovado'])

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        if item.estado == 'aprovado':  # Somente itens aprovados podem ser comprados
            item.estado = 'comprado'
            item.comprado_por = request.user
            item.save()
            messages.success(request, f'Você comprou o item {item.name} com sucesso.')
        else:
            messages.error(request, f'O item {item.name} não está disponível para compra.')

        return redirect('items_for_sale')

    context = {
        'items': items_for_sale,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,  # Check if the user is an admin
    }
    return render(request, 'donations/items_for_sale.html', context)

def thank_you(request):
    context = {
        'username': request.user.username,
        'is_admin': request.user.is_superuser,  # Check if the user is an admin
    }
    return render(request, 'donations/thank_you.html', context)

def not_donor(request):
    return render(request, 'donations/not_donor.html', {"username": request.user.username})


@login_required
def item_donation_view(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = ItemAdminForm(request.POST)
        else:
            form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_superuser:
                try:
                    donor = Donor.objects.get(user=request.user)
                    item.donated_by = donor  # Define o doador automaticamente
                    item.estado = 'analise'  # Define o estado como 'Em Análise' para usuários comuns
                except Donor.DoesNotExist:
                    messages.error(request, 'Usuário doador não encontrado.')
                    return redirect('not-donor')
            item.save()
            messages.success(request, 'Item registrado com sucesso.')
            return redirect('thank-you')

        # Processar as ações de aprovação e rejeição
        elif 'approve' in request.POST or 'reject' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(Item, id=item_id)

            if 'approve' in request.POST:
                item.estado = 'aprovado'
                item.save()
                messages.success(request, f'O item {item.name} foi aprovado.')
            elif 'reject' in request.POST:
                item.estado = 'rejeitado'
                item.save()
                messages.success(request, f'O item {item.name} foi rejeitado.')

            return redirect('register_item')

    else:
        if request.user.is_superuser:
            form = ItemAdminForm()
        else:
            form = ItemForm()

    # Filtrar itens com base no tipo de usuário
    if request.user.is_superuser:
        items_in_analysis = Item.objects.filter(estado='analise')  # Apenas itens em análise
    else:
        items_in_analysis = Item.objects.filter(donated_by__user=request.user, estado='analise')

    context = {
        'form': form,
        'items': items_in_analysis,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,  # Verificar se o usuário é um administrador
    }
    return render(request, 'donations/register_item.html', context)

@login_required
def validate_item(request, item_id):
    if request.user.is_superuser:
        item = get_object_or_404(Item, id=item_id)
        item.estado = 'aprovado'  # Define o estado como 'Aprovado'
        item.save()
        messages.success(request, 'Item aprovado com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
    return redirect('register_item')  # Redirecionar de volta para a página de doação de itens

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.estado = 'rejeitado'
    item.save()
    messages.success(request, f'O item {item.name} foi rejeitado.')
    return redirect('register_item')


def item_admin_edit_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = ItemAdminForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ItemAdminForm(instance=item)
    
    return render(request, 'item_admin_edit_form.html', {'form': form, 'item': item})

def item_admin_list(request):
    # Query para obter todos os itens em análise
    items = Item.objects.filter(status='analise')

    context = {
        'form': form,
        'items': items,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,  # Check if the user is an admin
    }
    return render(request, 'item_admin_list.html', context)


@login_required
def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            try:
                donor = form.save(commit=False)
                if Donor.objects.filter(email=donor.email).exists():
                    messages.error(request, 'Este email já está registrado.')
                else:
                    donor.user = request.user
                    donor.save()
                    messages.success(request, 'Registro realizado com sucesso!')
                    return redirect('some-success-page')
            except Exception as e:
                messages.error(request, f'Erro ao registrar: {e}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = DonorForm()

    context = {
        'form': form,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,  # Check if the user is an admin
    }
    return render(request, 'donations/register_donor.html', context)


@login_required
def user_profile_view(request):
    donor = get_object_or_404(Donor, user=request.user)
    donations = Donation.objects.filter(donor=donor)
    donated_items = Item.objects.filter(donated_by=donor)
    
    total_donated = donations.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    context = {
        'user': request.user,
        'username': request.user.username,
        'donor': donor,
        'donations': donations,
        'donated_items': donated_items,
        'total_donated': total_donated,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'donations/user_profile.html', context)

@login_required
def edit_profile_view(request):
    donor = get_object_or_404(Donor, user=request.user)
    
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES, instance=donor, user_instance=request.user)
        if form.is_valid():
            form.save()
            # Atualizar o campo full_name no modelo User
            request.user.full_name = form.cleaned_data.get('full_name')
            request.user.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('user_profile')
    else:
        form = DonorForm(instance=donor, user_instance=request.user)

    context = {
        'form': form,
        'user': request.user,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,
    }

    return render(request, 'donations/edit_profile.html', context)

#admin dashboard views configure
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_user_list(request):
    users = CustomUser.objects.all()
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'users': users,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_user_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_donation_list(request):
    donations = Donation.objects.all()
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'donations': donations,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_donation_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_item_list(request):
    items = Item.objects.all()
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'items': items,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_item_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_items_in_analysis(request):
    # Filtrar itens com base no estado 'analise'
    items_in_analysis = Item.objects.filter(estado='analise')

    context = {
        'items': items_in_analysis,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'donations/admin_items_in_analysis.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_items_in_analysis(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        if 'approve' in request.POST:
            item.estado = 'aprovado'
            item.save()
            messages.success(request, f'O item {item.name} foi aprovado.')
        elif 'reject' in request.POST:
            item.estado = 'rejeitado'
            item.save()
            messages.success(request, f'O item {item.name} foi rejeitado.')

        return redirect('admin_items_in_analysis')

    # Filtrar itens com base no estado 'analise'
    items_in_analysis = Item.objects.filter(estado='analise')
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'items': items_in_analysis,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_items_in_analysis.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_items_sold(request):
    # Filtrar itens com base no estado 'vendido'
    items_sold = Item.objects.filter(estado='comprado')
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    total_sold_value = items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'items': items_sold,
        'total_sold_value': total_sold_value,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_items_sold.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_funds(request):
    # Calcular o total das doações
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    # Calcular o total geral
    total_general = total_donations + total_sold_value

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()


    context = {
        'total_donations': total_donations,
        'total_sold_value': total_sold_value,
        'total_general': total_general,
        'total_items': total_items,
        'total_users': total_users,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_funds.html', context)


# Views de notícias
@user_passes_test(lambda u: u.is_superuser)
def admin_news_list(request):
    news_list = News.objects.all()
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'news_list': news_list,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_news_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_news_create(request):
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Notícia criada com sucesso.')
            return redirect('admin_news_list')
    else:
        form = NewsForm()

    context = {
        'form': form,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }

    return render(request, 'donations/admin_news_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_news_edit(request, news_id):
    news = get_object_or_404(News, id=news_id)
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notícia atualizada com sucesso.')
            return redirect('admin_news_list')
    else:
        form = NewsForm(instance=news)


    context = {
        'form': form,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }

    return render(request, 'donations/admin_news_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_news_delete(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    messages.success(request, 'Notícia excluída com sucesso.')
    return redirect('admin_news_list')

# Views de atividades
@user_passes_test(lambda u: u.is_superuser)
def admin_activity_list(request):
    activities = Activity.objects.all()
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    context = {
        'activities': activities,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }
    return render(request, 'donations/admin_activity_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_activity_create(request):
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.organizer = request.user
            activity.save()
            messages.success(request, 'Atividade criada com sucesso.')
            return redirect('admin_activity_list')
    else:
        form = ActivityForm()


    context = {
        'form': form,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }

    return render(request, 'donations/admin_activity_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_activity_edit(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_items = Item.objects.count()
    total_users = CustomUser.objects.count()

    # Calcular o total dos valores dos itens vendidos
    total_items_sold = Item.objects.filter(estado='comprado')
    total_sold_value = total_items_sold.aggregate(total=Sum('price'))['total'] or 0

    total_acao = total_donations + total_sold_value

    total_news = News.objects.count()
    total_activities = Activity.objects.count()

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada com sucesso.')
            return redirect('admin_activity_list')
    else:
        form = ActivityForm(instance=activity)


    context = {
        'form': form,
        'total_donations': total_donations,
        'total_items': total_items,
        'total_users': total_users,
        'total_sold_value': total_sold_value,
        'total_acao': total_acao,
        'total_news': total_news,
        'total_activities': total_activities,
    }

    return render(request, 'donations/admin_activity_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.delete()
    messages.success(request, 'Atividade excluída com sucesso.')
    return redirect('admin_activity_list')


# Views de atividade e noticias para o usuário
def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    context = {
        'news_list': news_list,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'donations/news_list.html', context)

def activity_list(request):
    activity_list = Activity.objects.all().order_by('-created_at')
    context = {
        'activity_list': activity_list,
        'username': request.user.username,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'donations/activity_list.html', context)

def custom_500_view(request):
    return render(request, 'donations/custom_500.html', status=500)

def custom_404_view(request, exception):
    return render(request, 'donations/custom_404.html', status=404)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def get_current_user(request):
    if request.user.is_authenticated:
        try:
            return Users.objects.get(username=request.user.username)
        except Users.DoesNotExist:
            return None
    return None

@login_required
def gender_list(request):
    try:
        search_query = request.GET.get('search', '')
        genders = Genders.objects.all()
        
        if search_query:
            genders = genders.filter(
                gender__icontains=search_query
            )
            
        paginator = Paginator(genders, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        data = {
            'genders': page_obj,
            'page_obj': page_obj,
            'search_query': search_query,
            'current_user': get_current_user(request)
        }
        
        return render(request, 'gender/GenderList.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html', {'current_user': get_current_user(request)})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            gender = request.POST.get('gender')
            genderObj.gender = gender
            genderObj.save()
            messages.success(request, 'Gender updated successfully!')
            return redirect('/gender/list')
        else:
            genderObj = Genders.objects.get(pk=genderId)
            data = {
                'gender': genderObj,
                'current_user': get_current_user(request)
            }
            return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()
            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list')
        else:
            genderObj = Genders.objects.get(pk=genderId)
            data = {
                'gender': genderObj,
                'current_user': get_current_user(request)
            }
            return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def user_list(request):
    try:
        search_query = request.GET.get('search', '')
        user_list = Users.objects.select_related('gender').all()
        
        if search_query:
            user_list = user_list.filter(
                full_name__icontains=search_query
            ) | user_list.filter(
                username__icontains=search_query
            ) | user_list.filter(
                email__icontains=search_query
            )
            
        paginator = Paginator(user_list, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        data = {
            'users': page_obj,
            'page_obj': page_obj,
            'search_query': search_query,
            'current_user': get_current_user(request)
        }
        
        return render(request, 'user/UserList.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def add_user(request):
    try:
        if request.method == 'POST':
            fullname = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPass = request.POST.get('confirm_password')
            
            if password != confirmPass:
                messages.error(request, 'Password and Confirm Password doesnt match!')
                data = {
                    'genders': Genders.objects.all(),
                    'form_data': {
                        'full_name': fullname,
                        'gender': gender,
                        'birth_date': birthdate,
                        'address': address,
                        'contact_number': contactNumber,
                        'email': email,
                        'username': username
                    },
                    'current_user': get_current_user(request)
                }
                return render(request, 'user/AddUser.html', data)
            
            Users.objects.create(
                full_name = fullname,
                gender = Genders.objects.get(pk=gender),
                birth_date = birthdate,
                address = address,
                contact_number = contactNumber,
                email = email,
                username = username,
                password = make_password(password)
            ).save()
            
            messages.success(request, 'User added successfully!')
            return redirect('/user/list')
        
        else: 
            genderObj = Genders.objects.all()
            data = {
                'genders': genderObj,
                'current_user': get_current_user(request)
            }
            return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def edit_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            fullname = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            
            if not gender: 
                messages.error(request, 'Please select a gender')
                return redirect(f'/user/edit/{userId}')
            if Users.objects.filter(username=username).exclude(user_id=userId).exists():
                messages.error(request, 'Username already exists')
                return redirect(f'/user/edit/{userId}')
            if password and confirmPassword:
                if password != confirmPassword:
                    messages.error(request, 'Password and confirm password dont match')
                    return redirect(f'/user/edit/{userId}')
                userObj.password = make_password(password)
                
            try:
                genderObj = Genders.objects.get(pk=gender)
                userObj.gender = genderObj
            except Genders.DoesNotExist:
                messages.error(request, 'Invalid gender selected')
                return redirect(f'/user/edit/{userId}')
            
            userObj.full_name = fullname
            userObj.birth_date = birthdate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email
            userObj.username = username
            userObj.save()
            
            messages.success(request, 'User updated successfully!')
            return redirect('/user/list')
        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()
            data = {
                'user': userObj,
                'gender': genderObj,
                'current_user': get_current_user(request)
            }
            return render(request, 'user/EditUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def change_pass(request, userId):
    try:
        if request.method == 'POST':
            user = Users.objects.get(pk=userId)
            current_pass = request.POST.get('current_password')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            
            if not check_password(current_pass, user.password):
                messages.error(request, 'Current password is incorrect')
                return redirect(f'/user/changepass/{userId}')
            if not password or not confirmPassword:
                messages.error(request, 'Please fill out both password fields')
                return redirect(f'/user/changepass/{userId}')
            if password != confirmPassword:
                messages.error(request, 'New password and confirm password dont match')
                return redirect(f'/user/changepass/{userId}')
            
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('/user/list')
        else:
            user = Users.objects.get(pk=userId)
            return render(request, 'user/ChangePass.html', {
                'user': user,
                'current_user': get_current_user(request)
            })
    except Users.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('/user/list')
    except Exception as e:
        return HttpResponse(f'Error: {e}')

@login_required
def delete_user(request, userId):
    try:
        if request.method == 'POST':
            user = Users.objects.get(pk=userId)
            user.delete()
            messages.success(request, f'User {user.username} has been deleted')
            return redirect('/user/list')
        else:
            user = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()
            data = {
                'user': user,
                'gender': genderObj,
                'current_user': get_current_user(request)
            }
            return render(request, 'user/DeleteUser.html', data)
    except Users.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('/user/list')
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                # Get or create Django user
                django_user, created = User.objects.get_or_create(
                    username=user.username,
                    defaults={'password': make_password(password)}
                )
                if created:
                    django_user.set_password(password)
                    django_user.save()
                
                login(request, django_user)
                messages.success(request, 'Login successful!')
                return redirect('/gender/list')
            else:
                messages.error(request, 'Invalid username or password.')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')
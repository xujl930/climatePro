from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, DevForm
from .models import Profile, Terminal
from .serializers import TerminalSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


# Create your views here.
def check_code(request):
    import io
    from backend import check_code as CheckCode

    stream = io.BytesIO()
    # img图片对象,code在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

    # 代码：生成一张图片，在图片中写文件
    # request.session['CheckCode'] =  图片上的内容

    # 自动生成图片，并且将图片中的文字保存在session中
    # 将图片内容返回给用户

@cache_page(60*15)
def user_login(request):
    print(request.POST)
    if request.method == 'POST':
        form =  LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                request.session['CheckCode']
            except KeyError:
                return HttpResponse('checkcode-expired', status=400)#, 'error': '验证码已失效，请重新输入!'

            print(request.session['CheckCode'].upper())

            if cd['checkcode'].upper() != request.session['CheckCode'].upper():
                # messages.error(request, '验证码不匹配!')
                return HttpResponse('checkcode', status=400)
                # return render(request, 'account/login.html',  {'form':form, 'error': '验证码不匹配'},status=400)
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return HttpResponse('admin')

                if user.is_active:
                    login(request, user)
                    username = request.user.username
                    terminals = Terminal.objects.filter(username=username).order_by('deviceEui')
                    serializer = TerminalSerializer(terminals, many=True)
                    dev_dic = {}
                    for i in serializer.data:
                        dev_dic[i.get('deviceEui')]=i.get('terminalId')# append(i.get('deviceEui'))
                    print(dev_dic)
                    request.session['dev_dic'] = dev_dic
                    #return redirect('/accounts/', {'section':'dashboard'})
                    return HttpResponse('')
            else:
                # return render(request, 'account/login.html', {'form':form, 'error':'用户名或密码错误'}, status=400)
                return HttpResponse('password', status=400)
                # else:
                #     return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        logout(request)
        return render(request, 'account/login.html', {'form': LoginForm()})
    dev_dic = request.session['dev_dic']
    return render(request, 'account/dashboard.html', {'section':'dashboard', 'dev_dic': dev_dic})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                    user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                    'account/register_done.html',
                    {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                       data=request.POST,
                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            cd = profile_form.cleaned_data
            print(cd['photo'])
            # user_form.save()
            # profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
        instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                  'profile_form': profile_form})

@login_required
def addDev(request):
    if request.method == 'POST':
        dev_form = DevForm(instance=request.user,data=request.POST)

        if dev_form.is_valid():
            cd = dev_form.cleaned_data
            cd.update({'deviceAddr':cd['deviceAddr'].cityName})

            t = TerminalSerializer(data=cd)
            if t.is_valid():
                t.save()
                messages.success(request, 'device add successfully')
                print(t.data)
            else:
                messages.error(request, t.errors)
            # print(t)
            # print(cd)
            # print(cd.get('deviceAddr').cityName)
            #dev_form.save()

        else:
            messages.error(request, 'Error adding your device')
    else:
        dev_form = DevForm(instance=request.user)

    return render(request,
                  'account/dev_add.html',
                  {'dev_form': dev_form})
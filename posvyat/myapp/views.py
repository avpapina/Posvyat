from django.shortcuts import render, redirect

def main_page(request):
    return render(request, 'main_page.html')

def start_page(request):
    return redirect('main_page')

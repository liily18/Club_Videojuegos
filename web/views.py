from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from datetime import timedelta, date
from datetime import date, timedelta
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import *


@login_required 
def index(request):
    form = PlataformaFilterForm(request.GET)  
    
    if form.is_valid():
        plataforma = form.cleaned_data.get('plataforma')  
        if plataforma:
            juegos = Juego.objects.filter(plataforma=plataforma, disponible=True)
        else:
            juegos = Juego.objects.filter(disponible=True)  
    else:
        juegos = Juego.objects.filter(disponible=True)

    return render(request, 'index.html', {'juegos': juegos, 'form': form})




class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect(reverse('register'))  

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        user = authenticate(username=email, password=password1)
        if user is not None:
            login(request, user)

        messages.success(request, 'Usuario creado exitosamente')
        return redirect('index')


class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Sesión iniciada exitosamente"
    template_name = 'registration/login.html'  
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.WARNING, "Sesión cerrada exitosamente")
        return response
    


@login_required
def arrendar(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        fecha_seleccionada = timezone.datetime.strptime(fecha, "%Y-%m-%d").date()
        fecha_hoy = timezone.now().date()
        
        if fecha_seleccionada < fecha_hoy:
            messages.error(request, "La fecha seleccionada debe ser hoy o una fecha futura.")
            return render(request, 'arrendar.html', {
                'juego': juego,
                'plataforma': juego.plataforma,
                'fecha': fecha, 
            })


        nuevo_arriendo = Arriendo.objects.create(
            fecha_arriendo=fecha_seleccionada,
            user=request.user,
            juego=juego
        )
 
        juego.disponible = False  
        juego.save()

        messages.success(request, "Videojuego arrendado exitosamente.")
        return redirect('index')  

    return render(request, 'arrendar.html', {
        'juego': juego,
        'plataforma': juego.plataforma,
    })



@login_required
def misArriendos(request):
    arriendos = Arriendo.objects.filter(user=request.user).select_related('juego')

    juegos_data = []

    for arriendo in arriendos:
        juego = arriendo.juego
        fecha_arriendo = arriendo.fecha_arriendo 
        dias_arriendo = juego.plataforma.dias_arriendo if juego.plataforma else 0
        fecha_devolucion = fecha_arriendo + timedelta(days=dias_arriendo) if fecha_arriendo else None

        # para calcular lamulta si la fecha de devolucion ya pasó
        multa = 0
        if fecha_devolucion and date.today() > fecha_devolucion:
            dias_atraso = (date.today() - fecha_devolucion).days
            multa = dias_atraso * juego.plataforma.precio_dias_atraso if juego.plataforma else 0


        juegos_data.append({  
            'id': juego.id,
            'nombre': juego.titulo,
            'genero': juego.genero,
            'plataforma': juego.plataforma,
            'fecha_arriendo': fecha_arriendo,
            'fecha_devolucion': fecha_devolucion,
            'multa': multa,
        })

    return render(request, 'mis_arriendos.html', {'juegos_data': juegos_data})




@login_required
def devolver(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    arriendo = get_object_or_404(Arriendo, juego=juego, user=request.user)
    
    if request.method == 'POST':
       
        fecha_retorno = request.POST.get('fecha_retorno')
        
        fecha_retorno = date.fromisoformat(fecha_retorno) if fecha_retorno else date.today()
        
       
        dias_arriendo = juego.plataforma.dias_arriendo if juego.plataforma else 0
        fecha_devolucion_esperada = arriendo.fecha_arriendo + timedelta(days=dias_arriendo)
        dias_atraso = (fecha_retorno - fecha_devolucion_esperada).days
        multa = 0

        if dias_atraso > 0:
            multa = dias_atraso * juego.plataforma.precio_dias_atraso if juego.plataforma else 0
            messages.warning(
                request,
                f"El VideoJuego '{juego.titulo}' ha sido retornado con {dias_atraso} días de atraso, generando una multa de ${multa}."
            )
        else:
            messages.success(request, f"El Videojuego '{juego.titulo}' fue devuelto sin problemas. ¡GRACIAS POR PREFERIRNOS!")

        
        juego.disponible = True
        juego.save()
        arriendo.delete() 

        return redirect('misarriendos')
    
  
    return render(request, 'devolver_juego.html', {'juego': juego})


@login_required
@permission_required('web.agregar_juegos', raise_exception=True)
def lista_arriendos(request):
    arriendos = Arriendo.objects.select_related('juego', 'user').all()
    
    # Lista para almacenar las multas 
    multas = []

    for arriendo in arriendos:
        juego = arriendo.juego
        dias_arriendo = juego.plataforma.dias_arriendo if juego.plataforma else 0
        fecha_devolucion_esperada = arriendo.fecha_arriendo + timedelta(days=dias_arriendo)

       
        multa = 0
        
        
        if date.today() > fecha_devolucion_esperada:
           dias_atraso = (date.today() - fecha_devolucion_esperada).days
           multa = dias_atraso * juego.plataforma.precio_dias_atraso if juego.plataforma else 0
            
        multas.append({
            'juego': juego.titulo,
            'fecha_devolucion_esperada': fecha_devolucion_esperada,
            'monto': multa,
        })

    return render(request, 'reporte_arriendos.html', {'arriendos': arriendos, 'multas': multas})

@login_required
@permission_required('web.agregar_juegos', raise_exception=True)
def agregar_observacion(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)

    if request.method == 'POST':
        observacion = request.POST.get('observacion')
        arriendo.observacion = observacion
        arriendo.save()
        return redirect('lista_arriendos')

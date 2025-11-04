from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import Usrs, Productos
from .backends import UsrsBackend

def login_view(request):
    """
    Vista para manejar el login de usuarios - Redirige a consulta después del login
    """
    # Si el usuario ya está autenticado, redirigir a consulta
    if request.user.is_authenticated:
        return redirect('consulta_productos')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validar que se hayan ingresado ambos campos
        if not username or not password:
            messages.error(request, 'Por favor, ingrese usuario y contraseña')
            return render(request, 'login.html')
        
        # Usar nuestro backend personalizado
        backend = UsrsBackend()
        user = backend.authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.Status:  # Verificar si el usuario está activo
                auth_login(request, user, backend='InventarioWeb.backends.UsrsBackend')
                # Mensaje de bienvenida personalizado
                return redirect('consulta_productos')  # Redirigir a consulta de productos
            else:
                messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # Renderizar el template con el diseño original
    return render(request, 'login.html')

@login_required
def logout_view(request):
    """
    Vista para cerrar sesión
    """
    auth_logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

@login_required
def home(request):
    """
    Vista principal del dashboard/home (ahora redirige a consulta)
    """
    return redirect('consulta_productos')

@login_required
def consulta_productos(request):
    """
    Vista para consultar productos con filtros y búsqueda
    - Solo muestra resultados cuando hay búsquedas activas
    - Al inicio muestra mensaje de bienvenida
    """
    productos = Productos.objects.none()  # QuerySet vacío por defecto
    busqueda_realizada = False
    
    # Obtener parámetros de búsqueda
    codigo = request.GET.get('codigo', '').strip()
    articulo = request.GET.get('articulo', '').strip()
    marca = request.GET.get('marca', '').strip()
    estatus = request.GET.get('estatus', '')
    stock_minimo = request.GET.get('stock_minimo', '').strip()
    
    # Verificar si hay algún criterio de búsqueda activo
    tiene_filtros = any([codigo, articulo, marca, estatus, stock_minimo])
    
    if tiene_filtros:
        busqueda_realizada = True
        productos = Productos.objects.all()
        
        # Aplicar filtros
        if codigo:
            productos = productos.filter(CODIGO__icontains=codigo)
        if articulo:
            productos = productos.filter(ARTICULO__icontains=articulo)
        if marca:
            productos = productos.filter(MARCA__icontains=marca)
        if estatus:
            productos = productos.filter(Estatus=estatus)
        if stock_minimo:
            try:
                stock_min = int(stock_minimo)
                # Productos con stock bajo en cualquier departamento
                productos = productos.filter(
                    Q(DISPVEST__lt=stock_min) |
                    Q(DISPMAQ__lt=stock_min) |
                    Q(DISPLAV__lt=stock_min) |
                    Q(DISPALM__lt=stock_min)
                )
            except ValueError:
                pass
        
        # Ordenar por código
        productos = productos.order_by('CODIGO')
    
    context = {
        'productos': productos,
        'codigo_busqueda': codigo,
        'articulo_busqueda': articulo,
        'marca_busqueda': marca,
        'estatus_busqueda': estatus,
        'stock_minimo': stock_minimo,
        'busqueda_realizada': busqueda_realizada,
        'tiene_filtros': tiene_filtros,
    }
    
    return render(request, 'productos/consulta.html', context)
@login_required
def lista_productos(request):
    """
    Vista para listar todos los productos (alternativa)
    """
    productos = Productos.objects.all()
    
    # Filtrar por búsqueda si se proporciona
    query = request.GET.get('q')
    if query:
        productos = productos.filter(
            Q(CODIGO__icontains=query) | 
            Q(ARTICULO__icontains=query) |
            Q(DESCRIP__icontains=query) |
            Q(MARCA__icontains=query)
        )
    
    # Filtrar por estatus si se proporciona
    estatus = request.GET.get('estatus')
    if estatus:
        productos = productos.filter(Estatus=estatus)
    
    context = {
        'productos': productos,
        'query': query,
        'estatus_filter': estatus
    }
    return render(request, 'productos/lista.html', context)

@login_required
def detalle_producto(request, id):
    """
    Vista para ver los detalles de un producto específico
    """
    producto = get_object_or_404(Productos, ID=id)
    return render(request, 'productos/detalle.html', {'producto': producto})

@login_required
def buscar_productos(request):
    """
    Vista para búsqueda avanzada de productos
    """
    productos = Productos.objects.all()
    
    if request.method == 'GET':
        codigo = request.GET.get('codigo', '')
        articulo = request.GET.get('articulo', '')
        marca = request.GET.get('marca', '')
        estatus = request.GET.get('estatus', '')
        
        if codigo:
            productos = productos.filter(CODIGO__icontains=codigo)
        if articulo:
            productos = productos.filter(ARTICULO__icontains=articulo)
        if marca:
            productos = productos.filter(MARCA__icontains=marca)
        if estatus:
            productos = productos.filter(Estatus=estatus)
    
    context = {
        'productos': productos,
        'codigo_busqueda': codigo,
        'articulo_busqueda': articulo,
        'marca_busqueda': marca,
        'estatus_busqueda': estatus
    }
    return render(request, 'productos/buscar.html', context)

@login_required
def actualizar_stock(request, id):
    """
    Vista para actualizar el stock de un producto (AJAX)
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        producto = get_object_or_404(Productos, ID=id)
        
        try:
            dispvest = request.POST.get('dispvest')
            dispmaq = request.POST.get('dispmaq')
            displav = request.POST.get('displav')
            dispalm = request.POST.get('dispalm')
            
            if dispvest is not None:
                producto.DISPVEST = int(dispvest)
            if dispmaq is not None:
                producto.DISPMAQ = int(dispmaq)
            if displav is not None:
                producto.DISPLAV = int(displav)
            if dispalm is not None:
                producto.DISPALM = int(dispalm)
            
            producto.save()
            return JsonResponse({'success': True, 'message': 'Stock actualizado correctamente'})
        
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Valores inválidos'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def dashboard_estadisticas(request):
    """
    Vista para obtener estadísticas del dashboard (JSON)
    """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        total_productos = Productos.objects.count()
        productos_activos = Productos.objects.filter(Estatus=1).count()
        productos_inactivos = Productos.objects.filter(Estatus=0).count()
        
        # Productos con stock bajo
        stock_bajo_vest = Productos.objects.filter(DISPVEST__lt=5, Estatus=1).count()
        stock_bajo_maq = Productos.objects.filter(DISPMAQ__lt=5, Estatus=1).count()
        stock_bajo_lav = Productos.objects.filter(DISPLAV__lt=5, Estatus=1).count()
        stock_bajo_alm = Productos.objects.filter(DISPALM__lt=5, Estatus=1).count()
        
        # Productos disponibles vs no disponibles
        productos_disponibles = Productos.objects.filter(CANT__gt=0).count()
        productos_no_disponibles = Productos.objects.filter(CANT=0).count()
        
        data = {
            'total_productos': total_productos,
            'productos_activos': productos_activos,
            'productos_inactivos': productos_inactivos,
            'stock_bajo_vest': stock_bajo_vest,
            'stock_bajo_maq': stock_bajo_maq,
            'stock_bajo_lav': stock_bajo_lav,
            'stock_bajo_alm': stock_bajo_alm,
            'productos_disponibles': productos_disponibles,
            'productos_no_disponibles': productos_no_disponibles
        }
        
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Solicitud no válida'})

# Vistas para manejo de errores
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

# Vista adicional para estadísticas del dashboard
@login_required
def dashboard_view(request):
    """
    Vista del dashboard con estadísticas generales
    """
    total_productos = Productos.objects.count()
    productos_activos = Productos.objects.filter(Estatus=1).count()
    productos_disponibles = Productos.objects.filter(CANT__gt=0).count()
    
    # Productos con stock crítico (<3 unidades)
    stock_critico = Productos.objects.filter(
        Q(DISPVEST__lt=3) | Q(DISPMAQ__lt=3) | Q(DISPLAV__lt=3) | Q(DISPALM__lt=3),
        Estatus=1
    ).count()
    
    context = {
        'total_productos': total_productos,
        'productos_activos': productos_activos,
        'productos_disponibles': productos_disponibles,
        'stock_critico': stock_critico,
        'usuario': request.user
    }
    
    return render(request, 'dashboard.html', context)
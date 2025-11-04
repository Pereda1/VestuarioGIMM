from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from .models import Usrs

class UsrsBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usrs.objects.get(IdLogin=username)
            
            # DEBUG - Información detallada
            print(f"=== DEBUG AUTENTICACIÓN ===")
            print(f"Usuario: {user.IdLogin}")
            print(f"Contraseña en DB: '{user.Secreto}'")
            print(f"Contraseña ingresada: '{password}'")
            print(f"Longitud DB: {len(user.Secreto)}")
            print(f"Longitud ingresada: {len(password)}")
            
            # Primero intentar con el sistema de hashing de Django
            if user.check_password(password):
                print("✓ Contraseña correcta (hash)")
                user.last_login = timezone.now()
                user.save()
                return user
            
            # Si falla, verificar si es texto plano
            elif user.Secreto == password:
                print("✓ Contraseña correcta (texto plano) - Actualizando a hash")
                # Actualizar a contraseña hasheada
                user.set_password(password)
                user.last_login = timezone.now()
                user.save()
                return user
            
            else:
                print("✗ Contraseña incorrecta")
                print(f"Comparación: '{user.Secreto}' vs '{password}'")
                return None
                
        except Usrs.DoesNotExist:
            print(f"✗ Usuario no encontrado: {username}")
            return None
        except Exception as e:
            print(f"✗ Error en autenticación: {e}")
            return None
    
    def get_user(self, user_id):
        try:
            return Usrs.objects.get(pk=user_id)
        except Usrs.DoesNotExist:
            return None